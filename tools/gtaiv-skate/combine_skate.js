// GTA IV native names/signatures: sannybuilder/library 34bedee0, API 0.108.
// F6 toggles; mode 1 is W push, A/D steer and mouse orbit; mode 0 retains controller 0.
const INPUT_MODE = 1;
let inputMode = INPUT_MODE;
const SCALE = 1; // GTA metres assumption: MUST verify against a surveyed real surface.
// Isolated runtime preparation supplies strict private data after floor qualification.
const SURFACES = [];
let ride = null, preparing = null, announced=false, inputConfigured=false, inputRefused=false;
let selectedSurface = null;
function surfaceHeight(surface, x, y) {
    if (!surface || surface.qualified!==true || typeof surface.evidence!=="string" || !surface.evidence
        || !Number.isInteger(surface.layer) || surface.layer<=0 || surface.layer>0xffffffff
        || !Array.isArray(surface.center) || surface.center.length!==2 || !surface.center.every(Number.isFinite)
        || !Number.isFinite(surface.radius) || surface.radius<=0
        || Math.hypot(x-surface.center[0],y-surface.center[1])>surface.radius
        || !Array.isArray(surface.triangles) || !surface.triangles.length || surface.triangles.length>4096) return null;
    const heights=[];
    for (const triangle of surface.triangles) {
        if (!Array.isArray(triangle) || triangle.length!==3
            || triangle.some(v=>!Array.isArray(v)||v.length!==3||!v.every(Number.isFinite))) return null;
        const [a,b,c]=triangle;
        const denominator=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1]);
        if(Math.abs(denominator)<1e-9)continue;
        const u=((b[1]-c[1])*(x-c[0])+(c[0]-b[0])*(y-c[1]))/denominator;
        const v=((c[1]-a[1])*(x-c[0])+(a[0]-c[0])*(y-c[1]))/denominator;
        const w=1-u-v;
        if(Math.min(u,v,w)>=-1e-6)heights.push(u*a[2]+v*b[2]+w*c[2]);
    }
    if(!heights.length || (Math.max(...heights)-Math.min(...heights))*SCALE>0.001)return null;
    return heights[0];
}
function surfaceObservation(surface,x,y,ground) {
    const height=surfaceHeight(surface,x,y);
    return height!==null && Number.isFinite(ground) && Math.abs(height-ground)*SCALE<=0.05;
}
function surfaceContainsPose(surface,x,y,z) {
    const height=surfaceHeight(surface,x,y);
    return height!==null && Number.isFinite(z) && Math.abs(z-height)*SCALE<3;
}
function record(event) {try {log("COMBINE_SKATE "+event);}catch (_) {}}
function notify(text) { record(text);native("PRINT_STRING_WITH_LITERAL_STRING_NOW", "STRING", text, 2500, 1); }
function restore() {
    const saved = ride;
    preparing = null;
    selectedSurface = null;
    const attempt = action => { try { action(); } catch (_) {} };
    attempt(() => native("COMBINE_SKATE_STOP"));
    if (!saved) return;
    saved.recovering=true;
    let recovered=true;
    const recover=action=>{try{action();}catch(_){recovered=false;}};
    // Independent restoration attempts ensure a missing ped/camera cannot trap control.
    recover(() => native("ACTIVATE_SCRIPTED_CAMS", false, false));
    recover(() => { if (native("DOES_CAM_EXIST", saved.camera)) {
        native("SET_CAM_PROPAGATE", saved.camera, false);
        native("SET_CAM_ACTIVE", saved.camera, false);
        native("DESTROY_CAM", saved.camera);
    }});
    recover(() => { if (native("DOES_CHAR_EXIST", saved.ped)) {
        native("FREEZE_CHAR_POSITION", saved.ped, false);
    }});
    recover(() => native("SET_PLAYER_CONTROL", saved.player, true));
    recover(() => {if(!native("IS_PLAYER_CONTROL_ON",saved.player) || native("DOES_CAM_EXIST",saved.camera))throw new Error("recovery-unverified");});
    if(recovered) {
        recover(() => native("COMBINE_SKATE_RELEASE"));
        if(recovered)ride=null;
    }
    if(ride && !saved.recoveryAnnounced){record("recovery-pending");saved.recoveryAnnounced=true;}
}
function mount(player, ped) {
    if (!native("IS_CHAR_ON_FOOT", ped) || !native("IS_PLAYER_CONTROL_ON", player)
        || native("IS_PAUSE_MENU_ACTIVE")
        || (native("HAS_CUTSCENE_LOADED") && !native("HAS_CUTSCENE_FINISHED"))) return;
    const pos = native("GET_CHAR_COORDINATES", ped);
    const ground = native("GET_GROUND_Z_FOR_3D_COORD", pos.x, pos.y, pos.z + 2);
    const height=native("GET_CHAR_HEIGHT_ABOVE_GROUND",ped);
    if (![pos.x,pos.y,pos.z,ground,height].every(Number.isFinite) || Math.abs(ground)<0.001
        || Math.abs(pos.z-ground)>2 || Math.abs(pos.z-ground-height)>0.2) {
        notify("Skate: ground unavailable/ambiguous - choose another clear surface");return;
    }
    native("COMBINE_SKATE_STOP");
    if(SURFACES.length) {
        const matches=SURFACES.filter(surface=>surfaceObservation(surface,pos.x,pos.y,ground));
        if(matches.length!==1){notify("Skate: qualified floor unavailable - GTA retained");return;}
        selectedSurface=matches[0];
        if(!native("COMBINE_SKATE_SURFACE_BEGIN",selectedSurface.layer,selectedSurface.triangles.length)) {restore();return;}
        for(const triangle of selectedSurface.triangles)for(const vertex of triangle) {
            if(!native("COMBINE_SKATE_SURFACE_VERTEX",...vertex)){restore();return;}
        }
    } else for (let y=0;y<5;y++) for (let x=0;x<5;x++) {
        const px=pos.x+(x-2)*2/SCALE, py=pos.y+(y-2)*2/SCALE;
        const z=native("GET_GROUND_Z_FOR_3D_COORD", px, py, pos.z+2);
        let reason=null;
        if(!Number.isFinite(z)) reason="non-finite";
        else if(Math.abs(z)<0.001) reason="near-zero";
        else if(Math.abs(z-ground)*SCALE>0.05) reason="over-0.05-metres";
        else if(!native("COMBINE_SKATE_VERTEX",px,py,z)) reason="vertex-rejection";
        if(reason) {
            record("surface-refused:"+reason);
            native("COMBINE_SKATE_STOP");notify("Skate: choose a clear, flat surface");return;
        }
    }
    const heading=native("GET_CHAR_HEADING",ped);
    const result=selectedSurface
        ?native("COMBINE_SKATE_MOUNT_SURFACE",pos.x,pos.y,ground,heading,SCALE,selectedSurface.layer,1)
        :native("COMBINE_SKATE_MOUNT",pos.x,pos.y,ground,heading,SCALE);
    if (!result) {
        restore();notify("Skate: initialization/controller unavailable");return;
    }
    if (result===2) {
        preparing={player,ped,pos,ground,started:native("GET_GAME_TIMER")};
        notify("Skate: preparing - F6 cancels");return;
    }
    finishMount(player,ped,pos);
}
function finishMount(player,ped,pos) {
    const initial=[0,1,2,3].map(i=>native("COMBINE_SKATE_VALUE",i));
    if(!initial.every(Number.isFinite) || (selectedSurface && !surfaceContainsPose(selectedSurface,initial[0],initial[1],initial[2]))) {restore();notify("Skate: invalid initial pose - GTA retained");return;}
    const camera=native("CREATE_CAM",14);
    ride={player,ped,camera,lift:pos.z-initial[2],yaw:0,pitch:Math.atan2(2.5,4)*180/Math.PI};
    if (!native("DOES_CAM_EXIST",camera)) {restore();notify("Skate: camera unavailable - GTA retained");return;}
    native("COMBINE_SKATE_CLAIM",player,ped,camera);
    native("SET_PLAYER_CONTROL",player,false);
    native("FREEZE_CHAR_POSITION",ped,true);
    native("SET_CAM_ACTIVE",camera,true);native("SET_CAM_PROPAGATE",camera,true);
    native("ACTIVATE_SCRIPTED_CAMS",true,true);
    if(inputMode===1)native("GET_MOUSE_INPUT"); // Discard pre-mount movement.
    notify(inputMode===1?"Skate: mounted - W push, A/D steer, mouse camera, F6 dismount"
        :"Skate: mounted - A/X push, left stick steer, F6 dismount");
}
try {
    while (true) {
        wait(0);
        try {
            if (!native("COMBINE_SKATE_READY")) {
                const pending=preparing!==null;
                restore();
                if(pending)notify("Skate: preparation failed - GTA retained");
                continue;
            }
            if(ride && ride.recovering){restore();continue;}
            if(!inputConfigured) {
                if(!native("COMBINE_SKATE_INPUT_MODE",INPUT_MODE)) {
                    if(!inputRefused)record("input-mode-refused");
                    inputRefused=true;continue;
                }
                inputConfigured=true;
            }
            const selected=native("COMBINE_SKATE_INPUT_TOGGLE");
            if(selected===0 || selected===1) {
                inputMode=selected;
                notify(inputMode===1?"Skate: keyboard/mouse selected - F5 switches while dismounted"
                    :"Skate: controller selected - F5 switches while dismounted");
            }
            if (!announced) {notify(SURFACES.length?"Skate adapter ready - F6 on a qualified floor":"Skate adapter ready - F6 on a clear flat surface");announced=true;}
            const player=native("CONVERT_INT_TO_PLAYERINDEX",native("GET_PLAYER_ID"));
            const ped=native("GET_PLAYER_CHAR",player);
            const valid=native("DOES_CHAR_EXIST",ped) && native("IS_PLAYER_PLAYING",player)
                && native("IS_CHAR_ON_FOOT",ped);
            const toggle=native("COMBINE_SKATE_TOGGLE");
            if (ride && (toggle || !valid || ped!==ride.ped || player!==ride.player
                || !native("DOES_CAM_EXIST",ride.camera))) {
                restore();notify(ride?"Skate: recovery pending - riding blocked":"Skate: GTA controls restored");continue;
            }
            const interrupted=native("IS_PAUSE_MENU_ACTIVE")
                || (native("HAS_CUTSCENE_LOADED") && !native("HAS_CUTSCENE_FINISHED"));
            if (preparing) {
                const p=preparing, current=native("GET_CHAR_COORDINATES",ped);
                const moved=![current.x,current.y,current.z].every(Number.isFinite)
                    || Math.hypot(current.x-p.pos.x,current.y-p.pos.y,current.z-p.pos.z)>0.2;
                const timedOut=((native("GET_GAME_TIMER")-p.started)>>>0)>60000;
                if(toggle || !valid || interrupted || moved || ped!==p.ped || player!==p.player
                    || !native("IS_PLAYER_CONTROL_ON",player) || timedOut) {
                    restore();
                    notify(timedOut?"Skate: preparation timed out - GTA retained"
                        :"Skate: preparation cancelled - GTA retained");
                    continue;
                }
                const state=native("COMBINE_SKATE_POLL");
                if(!state) {restore();notify("Skate: preparation failed - GTA retained");continue;}
                if(state===1) {
                    const ground=native("GET_GROUND_Z_FOR_3D_COORD",current.x,current.y,current.z+2);
                    if(!Number.isFinite(ground) || Math.abs(ground-p.ground)*SCALE>0.05
                        || (selectedSurface && !surfaceObservation(selectedSurface,current.x,current.y,ground))) {
                        restore();notify("Skate: preparation floor changed - GTA retained");continue;
                    }
                    preparing=null;finishMount(player,ped,current);
                }
                continue;
            }
            if (!ride) {if(toggle && valid)mount(player,ped);continue;}
            if(interrupted) {restore();continue;}
            const prior=[0,1,2].map(i=>native("COMBINE_SKATE_VALUE",i));
            const ground=native("GET_GROUND_Z_FOR_3D_COORD",prior[0],prior[1],prior[2]+2);
            const tick=selectedSurface
                ?surfaceObservation(selectedSurface,prior[0],prior[1],ground)
                    && native("COMBINE_SKATE_TICK_SURFACE",native("GET_GAME_TIMER"),prior[0],prior[1],ground,selectedSurface.layer,valid?1:0)
                :native("COMBINE_SKATE_TICK",native("GET_GAME_TIMER"),ground,valid?1:0);
            if (!tick) {
                restore();notify("Skate: surface/input/time unavailable - GTA restored");continue;
            }
            const [x,y,z,heading]=[0,1,2,3].map(i=>native("COMBINE_SKATE_VALUE",i));
            if (![x,y,z,heading].every(Number.isFinite)
                || (selectedSurface && !surfaceContainsPose(selectedSurface,x,y,z))) {restore();continue;}
            native("SET_CHAR_COORDINATES",ped,x,y,z+ride.lift);
            native("SET_CHAR_HEADING",ped,heading);
            if(inputMode===1) {
                const mouse=native("GET_MOUSE_INPUT");
                if(!mouse || !Number.isFinite(mouse.x) || !Number.isFinite(mouse.y)
                    || Math.abs(mouse.x)>1000 || Math.abs(mouse.y)>1000) {
                    restore();record("mouse-input-unavailable");continue;
                }
                ride.yaw=(ride.yaw+mouse.x*0.15)%360;
                ride.pitch=Math.max(-20,Math.min(60,ride.pitch-mouse.y*0.15));
            }
            const angle=(heading+ride.yaw)*Math.PI/180;
            const elevation=ride.pitch*Math.PI/180, distance=Math.hypot(4,2.5);
            native("SET_CAM_POS",ride.camera,x+Math.sin(angle)*Math.cos(elevation)*distance,
                y-Math.cos(angle)*Math.cos(elevation)*distance,z+Math.sin(elevation)*distance);
            native("POINT_CAM_AT_COORD",ride.camera,x,y,z+1);
        } catch (_) {
            record("native-exception");restore();
            try {notify(ride?"Skate: recovery pending - riding blocked":"Skate: native operation failed - GTA retained");}catch (_) {}
        }
    }
} finally {restore();}
