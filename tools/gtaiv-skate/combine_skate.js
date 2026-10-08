// GTA IV native names/signatures: sannybuilder/library 34bedee0, API 0.108.
// F6 toggles; Xbox controller 0 supplies raw Skate push/steering input.
const SCALE = 1; // GTA metres assumption: MUST verify against a surveyed real surface.
let ride = null, preparing = null, announced=false;
function record(event) {try {log("COMBINE_SKATE "+event);}catch (_) {}}
function notify(text) { record(text);native("PRINT_STRING_WITH_LITERAL_STRING_NOW", "STRING", text, 2500, 1); }
function restore() {
    const saved = ride;
    preparing = null;
    const attempt = action => { try { action(); } catch (_) {} };
    attempt(() => native("COMBINE_SKATE_STOP"));
    if (!saved) return;
    // Independent restoration attempts ensure a missing ped/camera cannot trap control.
    attempt(() => native("ACTIVATE_SCRIPTED_CAMS", false, false));
    attempt(() => { if (native("DOES_CAM_EXIST", saved.camera)) {
        native("SET_CAM_PROPAGATE", saved.camera, false);
        native("SET_CAM_ACTIVE", saved.camera, false);
        native("DESTROY_CAM", saved.camera);
    }});
    attempt(() => { if (native("DOES_CHAR_EXIST", saved.ped)) {
        native("FREEZE_CHAR_POSITION", saved.ped, false);
    }});
    attempt(() => native("SET_PLAYER_CONTROL", saved.player, true));
    attempt(() => native("COMBINE_SKATE_RELEASE"));
    ride = null;
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
    for (let y=0;y<5;y++) for (let x=0;x<5;x++) {
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
    const result=native("COMBINE_SKATE_MOUNT",pos.x,pos.y,ground,native("GET_CHAR_HEADING",ped),SCALE);
    if (!result) {
        notify("Skate: initialization/controller unavailable");return;
    }
    if (result===2) {
        preparing={player,ped,pos,ground,started:native("GET_GAME_TIMER")};
        notify("Skate: preparing - F6 cancels");return;
    }
    finishMount(player,ped,pos);
}
function finishMount(player,ped,pos) {
    const initial=[0,1,2,3].map(i=>native("COMBINE_SKATE_VALUE",i));
    if(!initial.every(Number.isFinite)) {restore();notify("Skate: invalid initial pose - GTA retained");return;}
    const camera=native("CREATE_CAM",14);
    ride={player,ped,camera,lift:pos.z-initial[2]};
    if (!native("DOES_CAM_EXIST",camera)) {restore();return;}
    native("COMBINE_SKATE_CLAIM",player,ped,camera);
    native("SET_PLAYER_CONTROL",player,false);
    native("FREEZE_CHAR_POSITION",ped,true);
    native("SET_CAM_ACTIVE",camera,true);native("SET_CAM_PROPAGATE",camera,true);
    native("ACTIVATE_SCRIPTED_CAMS",true,true);
    notify("Skate: mounted - A/X push, left stick steer, F6 dismount");
}
try {
    while (true) {
        wait(0);
        try {
            if (!native("COMBINE_SKATE_READY")) {restore();continue;}
            if (!announced) {notify("Skate adapter ready - F6 on a clear flat surface");announced=true;}
            const player=native("CONVERT_INT_TO_PLAYERINDEX",native("GET_PLAYER_ID"));
            const ped=native("GET_PLAYER_CHAR",player);
            const valid=native("DOES_CHAR_EXIST",ped) && native("IS_PLAYER_PLAYING",player)
                && native("IS_CHAR_ON_FOOT",ped);
            const toggle=native("COMBINE_SKATE_TOGGLE");
            if (ride && (toggle || !valid || ped!==ride.ped || player!==ride.player
                || !native("DOES_CAM_EXIST",ride.camera))) {
                restore();notify("Skate: GTA controls restored");continue;
            }
            const interrupted=native("IS_PAUSE_MENU_ACTIVE")
                || (native("HAS_CUTSCENE_LOADED") && !native("HAS_CUTSCENE_FINISHED"));
            if (preparing) {
                const p=preparing, current=native("GET_CHAR_COORDINATES",ped);
                const moved=![current.x,current.y,current.z].every(Number.isFinite)
                    || Math.hypot(current.x-p.pos.x,current.y-p.pos.y,current.z-p.pos.z)>0.2;
                if(toggle || !valid || interrupted || moved || ped!==p.ped || player!==p.player
                    || !native("IS_PLAYER_CONTROL_ON",player)
                    || ((native("GET_GAME_TIMER")-p.started)>>>0)>60000) {restore();continue;}
                const state=native("COMBINE_SKATE_POLL");
                if(!state) {restore();notify("Skate: preparation failed - GTA retained");continue;}
                if(state===1) {
                    const ground=native("GET_GROUND_Z_FOR_3D_COORD",current.x,current.y,current.z+2);
                    if(!Number.isFinite(ground) || Math.abs(ground-p.ground)*SCALE>0.05) {restore();continue;}
                    preparing=null;finishMount(player,ped,current);
                }
                continue;
            }
            if (!ride) {if(toggle && valid)mount(player,ped);continue;}
            if(interrupted) {restore();continue;}
            const prior=[0,1,2].map(i=>native("COMBINE_SKATE_VALUE",i));
            const ground=native("GET_GROUND_Z_FOR_3D_COORD",prior[0],prior[1],prior[2]+2);
            if (!native("COMBINE_SKATE_TICK",native("GET_GAME_TIMER"),ground,valid?1:0)) {
                restore();notify("Skate: surface/input/time unavailable - GTA restored");continue;
            }
            const [x,y,z,heading]=[0,1,2,3].map(i=>native("COMBINE_SKATE_VALUE",i));
            if (![x,y,z,heading].every(Number.isFinite)) {restore();continue;}
            native("SET_CHAR_COORDINATES",ped,x,y,z+ride.lift);
            native("SET_CHAR_HEADING",ped,heading);
            const angle=heading*Math.PI/180;
            native("SET_CAM_POS",ride.camera,x+Math.sin(angle)*4,y-Math.cos(angle)*4,z+2.5);
            native("POINT_CAM_AT_COORD",ride.camera,x,y,z+1);
        } catch (_) {record("native-exception");restore();}
    }
} finally {restore();}
