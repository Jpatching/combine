// GTA IV native names/signatures: sannybuilder/library 34bedee0, API 0.108.
// F6 toggles; mode 1 is W push, A/D steer and mouse orbit; mode 0 retains controller 0.
const INPUT_MODE = 1;
let inputMode = INPUT_MODE;
const SCALE = 1; // GTA metres assumption: MUST verify against a surveyed real surface.
// Isolated runtime preparation supplies strict private data after floor qualification.
const SURFACES = [];
// Explicit coverage:"mesh" records qualify their complete triangle footprint;
// legacy records retain their evidence-bounded radius, even if their mesh extends farther.
// Mesh mode rejects legacy center/radius metadata; it requires whole-mesh qualification.
// Derived windows retain that original qualification and never qualify new ground.
const windowRegions = new WeakMap();
const LOCAL_RADIUS = 4 / SCALE;
let ride = null, preparing = null, announced=false, inputConfigured=false, inputRefused=false;
let selectedSurface = null, readinessAnnounced=false;
function surfaceHeight(surface, x, y) {
    const region=surface && windowRegions.get(surface);
    if(region && surfaceHeight(region,x,y)===null)return null;
    if (!surface || surface.qualified!==true || typeof surface.evidence!=="string" || !surface.evidence
        || !Number.isInteger(surface.layer) || surface.layer<=0 || surface.layer>0xffffffff
        || (surface.coverage!==undefined && surface.coverage!=="mesh")
        || (surface.coverage==="mesh" && (surface.center!==undefined || surface.radius!==undefined))
        || (surface.coverage!=="mesh" && (!Array.isArray(surface.center) || surface.center.length!==2
            || !surface.center.every(Number.isFinite) || !Number.isFinite(surface.radius) || surface.radius<=0
            || Math.hypot(x-surface.center[0],y-surface.center[1])>surface.radius))
        || !Array.isArray(surface.triangles) || !surface.triangles.length || surface.triangles.length>4096) return null;
    const heights=[];
    for (const triangle of surface.triangles) {
        if (!Array.isArray(triangle) || triangle.length!==3
            || triangle.some(v=>!Array.isArray(v)||v.length!==3||!v.every(Number.isFinite))) return null;
        const [a,b,c]=triangle;
        if(surface.coverage==="mesh") {
            // Explicit complete meshes receive the native coordinate and area bounds
            // before any local subset is selected, including distant obstacles.
            if(triangle.some(v=>v.some(component=>Math.abs(component)>1_000_000)))return null;
            const u=b.map((component,i)=>component-a[i]),v=c.map((component,i)=>component-a[i]);
            if(Math.hypot(u[1]*v[2]-u[2]*v[1],u[2]*v[0]-u[0]*v[2],u[0]*v[1]-u[1]*v[0])
                *SCALE*SCALE<0.000001)return null;
        }
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
// Coverage window: sampled surface around the rider, or the coverage gap that refuses it.
// It makes no native calls; probe(x,y,z) returns ground z (mount() wraps the ground native).
const WINDOW_SAMPLES = 5, WINDOW_SPACING = 2 / SCALE, WALL_THRESHOLD = 0.3;
function coverageWindow(probe, x, y, z) {
    const half=(WINDOW_SAMPLES-1)/2, grid=[];
    // Query from just above the rider so the floor underfoot is sampled, not a roof above it.
    for (let j=0;j<WINDOW_SAMPLES;j++) for (let i=0;i<WINDOW_SAMPLES;i++) {
        const px=x+(i-half)*WINDOW_SPACING, py=y+(j-half)*WINDOW_SPACING;
        const pz=probe(px,py,z+2);
        if(!Number.isFinite(pz))return {gap:"non-finite"};
        if(Math.abs(pz)<0.001)return {gap:"near-zero"};
        grid.push([px,py,pz]);
    }
    const at=(i,j)=>grid[j*WINDOW_SAMPLES+i];
    for (let j=0;j<WINDOW_SAMPLES;j++) for (let i=0;i<WINDOW_SAMPLES;i++) {
        for(const n of [i+1<WINDOW_SAMPLES&&at(i+1,j),j+1<WINDOW_SAMPLES&&at(i,j+1)]) {
            if(n && Math.abs(n[2]-at(i,j)[2])*SCALE>WALL_THRESHOLD)return {gap:"wall"};
        }
    }
    const triangles=[];
    for (let j=0;j+1<WINDOW_SAMPLES;j++) for (let i=0;i+1<WINDOW_SAMPLES;i++) {
        triangles.push([at(i,j),at(i+1,j),at(i+1,j+1)],[at(i,j),at(i+1,j+1),at(i,j+1)]);
    }
    // A complete mesh record: surfaceHeight() bounds it by its own footprint (the window edge).
    return {coverage:"mesh",sampled:true,layer:1,qualified:true,evidence:"sampled-surface",triangles};
}
function surfaceObservation(surface,x,y,ground) {
    const height=surfaceHeight(surface,x,y);
    return height!==null && Number.isFinite(ground) && Math.abs(height-ground)*SCALE<=0.05;
}
function sameFloor(a,b,x,y) {
    const first=surfaceHeight(a,x,y),second=surfaceHeight(b,x,y);
    return a.layer===b.layer && first!==null && second!==null && Math.abs(first-second)*SCALE<=0.001;
}
function surfaceContainsPose(surface,x,y,z) {
    const height=surfaceHeight(surface,x,y);
    return height!==null && Number.isFinite(z) && Math.abs(z-height)*SCALE<3;
}
function surfaceMargin(surface,x,y) {
    let margin;
    if(surface.coverage==="mesh") {
        // Bounds rank already validated mesh candidates; actual support is always
        // checked against triangles, so holes never become qualified ground.
        let minX=surface.triangles[0][0][0],maxX=minX,minY=surface.triangles[0][0][1],maxY=minY;
        for(const triangle of surface.triangles)for(const vertex of triangle) {
            minX=Math.min(minX,vertex[0]);maxX=Math.max(maxX,vertex[0]);
            minY=Math.min(minY,vertex[1]);maxY=Math.max(maxY,vertex[1]);
        }
        margin=Math.min(x-minX,maxX-x,y-minY,maxY-y);
    }else margin=surface.radius-Math.hypot(x-surface.center[0],y-surface.center[1]);
    // Original qualification is enforced by surfaceHeight, including radial
    // bounds, holes and edges. Rank local windows by their streaming margin;
    // proximity to an original boundary must not suppress valid refresh.
    return margin;
}
function localSurface(region,x,y) {
    if(region.coverage!=="mesh" && region.radius<=LOCAL_RADIUS)return region;
    // Full triangles whose XY bounds intersect the window square are retained.
    // This conservative selection keeps walls/curbs; it never clips or flattens them.
    const triangles=region.triangles.filter(triangle=>
        Math.min(...triangle.map(v=>v[0]))<=x+LOCAL_RADIUS
        && Math.max(...triangle.map(v=>v[0]))>=x-LOCAL_RADIUS
        && Math.min(...triangle.map(v=>v[1]))<=y+LOCAL_RADIUS
        && Math.max(...triangle.map(v=>v[1]))>=y-LOCAL_RADIUS);
    const window={...region,coverage:undefined,center:[x,y],radius:LOCAL_RADIUS,triangles};
    windowRegions.set(window,region);
    return window;
}
// A replacement must overlap the accepted pose on the same qualified floor.
// Keep presenting that pose while the asynchronous worker acknowledges it.
function refreshSurface(pos,ground) {
    const now=native("GET_GAME_TIMER");
    if(ride.coverage) {
        const pending=ride.coverage;
        const supported=(pose,height)=>sameFloor(pending.surface,selectedSurface,pose[0],pose[1])
            && surfaceObservation(pending.surface,pose[0],pose[1],height)
            && surfaceContainsPose(pending.surface,...pose);
        if(!supported(pos,ground))return 0;
        // Stay below the native 250 ms tick/freshness deadline, including upload time.
        if(((now-ride.lastTick)>>>0)>200)return 0;
        if(pending.submitted) {
            const state=native("COMBINE_SKATE_POLL");
            if(state===2)return 2;
            if(state!==1)return 0;
            const accepted=[0,1,2].map(i=>native("COMBINE_SKATE_VALUE",i));
            const support=native("GET_GROUND_Z_FOR_3D_COORD",accepted[0],accepted[1],accepted[2]+2);
            if(!supported(accepted,support))return 0;
            selectedSurface=pending.surface;ride.coverage=null;return 1;
        }
        // Bound native upload work per frame; never upload a whole large mesh at once.
        const end=Math.min(pending.vertex+96,pending.surface.triangles.length*3);
        while(pending.vertex<end) {
            const vertex=pending.surface.triangles[Math.floor(pending.vertex/3)][pending.vertex%3];
            if(!native("COMBINE_SKATE_SURFACE_VERTEX",...vertex))return 0;
            pending.vertex++;
        }
        if(pending.vertex<pending.surface.triangles.length*3)return 2;
        const result=native("COMBINE_SKATE_SURFACE_REPLACE",pos[0],pos[1],ground,pending.surface.layer,1);
        if(result===3) {
            // Poll without queuing another tick, then re-read pose/ground next frame.
            return native("COMBINE_SKATE_POLL")===0?0:2;
        }
        if(result===2){pending.submitted=true;return 2;}
        if(result!==1)return 0;
        selectedSurface=pending.surface;ride.coverage=null;return 1;
    }
    let next=selectedSurface;
    for(const region of SURFACES) {
        // Validate the complete region before selecting a subset; malformed distant
        // triangles must never disappear through local filtering.
        if(!surfaceObservation(region,pos[0],pos[1],ground))continue;
        const currentRegion=windowRegions.get(selectedSurface)||selectedSurface;
        if(region===currentRegion && (!windowRegions.has(selectedSurface)
            || surfaceMargin(selectedSurface,pos[0],pos[1])>LOCAL_RADIUS/2))continue;
        const surface=localSurface(region,pos[0],pos[1]);
        if(surface!==selectedSurface && sameFloor(surface,selectedSurface,pos[0],pos[1])
            && surfaceObservation(surface,pos[0],pos[1],ground)
            && surfaceContainsPose(surface,...pos)
            && surfaceMargin(surface,pos[0],pos[1])>surfaceMargin(next,pos[0],pos[1])+0.25)next=surface;
    }
    if(next===selectedSurface)return 1;
    if(!native("COMBINE_SKATE_SURFACE_BEGIN",next.layer,next.triangles.length))return 0;
    ride.coverage={surface:next,vertex:0,submitted:false};
    return refreshSurface(pos,ground);
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
function stopRide(reason) {
    const firstStop=ride && !ride.stopReason;
    if(ride && !ride.stopReason) {
        ride.stopReason=reason;
        record("ride-stopped:"+reason);
    }
    restore();
    if(firstStop) {
        const explanations={
            "dismount-toggle":"dismounted",
            "outside-qualified-surface":"outside supplied floor coverage",
            "outside-floor-height":"rider exceeded floor-relative height limit",
            "window-edge":"window edge",
            "surface-input-time-unavailable":"floor, input or timing check failed",
            "coverage-replacement-unavailable":"next floor coverage could not be loaded",
            "adapter-not-ready":"Skate adapter unavailable",
            "character-unavailable":"character no longer available on foot",
            "owner-changed":"player character changed",
            "camera-missing":"riding camera unavailable",
            "paused":"game paused",
            "cutscene":"cutscene started",
            "nonfinite-pose":"Skate returned an invalid position",
            "mouse-input-unavailable":"mouse input unavailable",
            "native-exception":"game operation failed"
        };
        notify("Skate: "+(explanations[reason] || reason)+" - "
            +(ride?"recovery pending":"GTA controls restored"));
    }
}
function mount(player, ped) {
    const blocked=!native("IS_CHAR_ON_FOOT",ped)?"character not on foot"
        :!native("IS_PLAYER_CONTROL_ON",player)?"GTA player control unavailable"
        :native("IS_PAUSE_MENU_ACTIVE")?"game paused"
        :native("HAS_CUTSCENE_LOADED") && !native("HAS_CUTSCENE_FINISHED")?"cutscene active":null;
    if(blocked) {notify("Skate: "+blocked+" - cannot mount");return;}
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
        const heights=matches.map(surface=>surfaceHeight(surface,pos.x,pos.y));
        if(!matches.length || matches.some(surface=>surface.layer!==matches[0].layer)
            || (Math.max(...heights)-Math.min(...heights))*SCALE>0.001) {
            notify("Skate: qualified floor unavailable - GTA retained");return;
        }
        // Overlapping patches on one agreeing floor are coverage, not separate floors.
        const region=matches.reduce((best,surface)=>
            surfaceMargin(surface,pos.x,pos.y)>surfaceMargin(best,pos.x,pos.y)?surface:best);
        selectedSurface=localSurface(region,pos.x,pos.y);
    } else {
        const samples=[];
        const coverage=coverageWindow((x,y,z)=>{
            const sample=native("GET_GROUND_Z_FOR_3D_COORD",x,y,z);samples.push([x,y,z,sample]);return sample;
        },pos.x,pos.y,pos.z);
        // Raw samples go to the private local log so runtime ground can be replayed as fixtures.
        record("coverage-samples:"+JSON.stringify(samples));
        if(coverage.gap) {
            const reasons={"non-finite":"ground not found","near-zero":"ground not loaded","wall":"wall-height step"};
            record("coverage-gap:"+coverage.gap);
            notify("Skate: coverage gap ("+reasons[coverage.gap]+") - GTA retained");return;
        }
        selectedSurface=coverage;
    }
    if(!native("COMBINE_SKATE_SURFACE_BEGIN",selectedSurface.layer,selectedSurface.triangles.length)) {restore();notify("Skate: floor setup failed - GTA retained");return;}
    for(const triangle of selectedSurface.triangles)for(const vertex of triangle) {
        if(!native("COMBINE_SKATE_SURFACE_VERTEX",...vertex)){restore();notify("Skate: floor upload failed - GTA retained");return;}
    }
    const heading=native("GET_CHAR_HEADING",ped);
    const result=native("COMBINE_SKATE_MOUNT_SURFACE",pos.x,pos.y,ground,heading,SCALE,selectedSurface.layer,1);
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
    ride={player,ped,camera,lastTick:native("GET_GAME_TIMER"),lift:pos.z-initial[2],yaw:0,pitch:Math.atan2(2.5,4)*180/Math.PI};
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
                const wasRiding=ride!==null;
                if(ride)stopRide("adapter-not-ready");else restore();
                if(pending)notify("Skate: preparation failed - GTA retained");
                else if(!wasRiding && !readinessAnnounced)notify("Skate: adapter not ready - F6 unavailable");
                readinessAnnounced=true;
                continue;
            }
            if(readinessAnnounced){readinessAnnounced=false;announced=false;}
            if(ride && ride.recovering){restore();continue;}
            if(!inputConfigured) {
                if(!native("COMBINE_SKATE_INPUT_MODE",INPUT_MODE)) {
                    if(!inputRefused){record("input-mode-refused");notify("Skate: input mode unavailable - F6 cannot mount");}
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
            if (!announced) {notify(SURFACES.length?"Skate adapter ready - F6 on a qualified floor":"Skate adapter ready - F6 on gentle ground");announced=true;}
            const player=native("CONVERT_INT_TO_PLAYERINDEX",native("GET_PLAYER_ID"));
            const ped=native("GET_PLAYER_CHAR",player);
            const valid=native("DOES_CHAR_EXIST",ped) && native("IS_PLAYER_PLAYING",player)
                && native("IS_CHAR_ON_FOOT",ped);
            const toggle=native("COMBINE_SKATE_TOGGLE");
            if(toggle)record("toggle-received:"+(ride?"riding":preparing?"preparing":"dismounted"));
            if (ride && (toggle || !valid || ped!==ride.ped || player!==ride.player
                || !native("DOES_CAM_EXIST",ride.camera))) {
                const reason=toggle?"dismount-toggle":!valid?"character-unavailable"
                    :ped!==ride.ped || player!==ride.player?"owner-changed":"camera-missing";
                stopRide(reason);continue;
            }
            const paused=native("IS_PAUSE_MENU_ACTIVE");
            const interrupted=paused
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
            if (!ride) {
                if(toggle) {
                    if(valid)mount(player,ped);
                    else notify("Skate: character unavailable on foot - cannot mount");
                }
                continue;
            }
            if(interrupted) {stopRide(paused?"paused":"cutscene");continue;}
            const prior=[0,1,2].map(i=>native("COMBINE_SKATE_VALUE",i));
            const ground=native("GET_GROUND_Z_FOR_3D_COORD",prior[0],prior[1],prior[2]+2);
            // The sampled window doesn't move yet: leaving it is a coverage gap.
            const sampled=selectedSurface.sampled===true;
            if(sampled && surfaceHeight(selectedSurface,prior[0],prior[1])===null) {stopRide("window-edge");continue;}
            if(!surfaceObservation(selectedSurface,prior[0],prior[1],ground)) {
                stopRide("surface-input-time-unavailable");continue;
            }
            // refreshSurface() only draws from authored SURFACES.
            if(!sampled) {
                const coverage=refreshSurface(prior,ground);
                if(!coverage){stopRide("coverage-replacement-unavailable");continue;}
                if(coverage===2)continue;
            }
            const timer=native("GET_GAME_TIMER");
            const tick=surfaceObservation(selectedSurface,prior[0],prior[1],ground)
                && native("COMBINE_SKATE_TICK_SURFACE",timer,prior[0],prior[1],ground,selectedSurface.layer,valid?1:0);
            if (!tick) {
                stopRide("surface-input-time-unavailable");continue;
            }
            ride.lastTick=timer;
            const [x,y,z,heading]=[0,1,2,3].map(i=>native("COMBINE_SKATE_VALUE",i));
            if (![x,y,z,heading].every(Number.isFinite)) {stopRide("nonfinite-pose");continue;}
            if(!surfaceContainsPose(selectedSurface,x,y,z)) {
                stopRide(surfaceHeight(selectedSurface,x,y)!==null?"outside-floor-height"
                    :sampled?"window-edge":"outside-qualified-surface");continue;
            }
            native("SET_CHAR_COORDINATES",ped,x,y,z+ride.lift);
            native("SET_CHAR_HEADING",ped,heading);
            if(inputMode===1) {
                const mouse=native("GET_MOUSE_INPUT");
                if(!mouse || !Number.isFinite(mouse.x) || !Number.isFinite(mouse.y)
                    || Math.abs(mouse.x)>1000 || Math.abs(mouse.y)>1000) {
                    stopRide("mouse-input-unavailable");record("mouse-input-unavailable");continue;
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
            record("native-exception");
            if(ride) {try {stopRide("native-exception");}catch (_) {}}
            else {restore();try {notify("Skate: native operation failed - GTA retained");}catch (_) {}}
        }
    }
} finally {restore();}
