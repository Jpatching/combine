// Owned, bounded, opt-in observer. No input, pose writes, reset or rescue calls.
// Private preparation replaces only TAG, MODE and qualified SURFACES data.
const TAG="readonly-template", MODE="lifecycle", SURFACES=[];
const LIFETIME_MS=120000;
const start=native("COMBINE_SKATE_EVAL_TIME");
let previous=null, selected=null, lastFlags=null;
function emit(event,flags={}) {log("COMBINE_READONLY "+TAG+" "+event+" "+JSON.stringify(flags));}
function height(surface,x,y) {
    if(!surface || surface.qualified!==true || !Number.isFinite(surface.radius)
        || surface.radius<=0 || !Array.isArray(surface.center) || surface.center.length!==2
        || !surface.center.every(Number.isFinite) || !Array.isArray(surface.triangles)
        || surface.triangles.length<1 || surface.triangles.length>4096
        || Math.hypot(x-surface.center[0],y-surface.center[1])>surface.radius)return null;
    const heights=[];
    for(const t of surface.triangles) {
        if(!Array.isArray(t)||t.length!==3||t.some(v=>!Array.isArray(v)||v.length!==3||!v.every(Number.isFinite)))return null;
        const [a,b,c]=t, d=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1]);
        if(Math.abs(d)<1e-9)continue;
        const u=((b[1]-c[1])*(x-c[0])+(c[0]-b[0])*(y-c[1]))/d;
        const v=((c[1]-a[1])*(x-c[0])+(a[0]-c[0])*(y-c[1]))/d;
        if(Math.min(u,v,1-u-v)>=-1e-6)heights.push(u*a[2]+v*b[2]+(1-u-v)*c[2]);
    }
    return heights.length && Math.max(...heights)-Math.min(...heights)<=0.001?heights[0]:null;
}
emit("started");
try {
    while(((native("COMBINE_SKATE_EVAL_TIME")-start)>>>0)<LIFETIME_MS) {
        wait(MODE==="lifecycle"?100:0);
        if(MODE==="lifecycle")continue;
        const owner=native("COMBINE_SKATE_EVAL_OWNER");
        if(owner.player<0) {
            if(previous) {
                emit("owner-ended",{last:lastFlags,normal_control:Boolean(native("IS_PLAYER_CONTROL_ON",previous.player)),
                    owned_camera_absent:!native("DOES_CAM_EXIST",previous.camera)});
                previous=null;selected=null;lastFlags=null;
            }
            continue;
        }
        const pose=[0,1,2,3].map(i=>native("COMBINE_SKATE_VALUE",i));
        const finite=pose.every(Number.isFinite);
        // VALUE is thread-bound and returns zero outside its captured context.
        // Owner coherence alone does not validate a pose getter. Compare against
        // host character XY (Z includes the GTA presentation lift). A mismatch
        // makes support observations unknown, never evidence of missing ground.
        const char=native("GET_CHAR_COORDINATES",owner.ped);
        const matchesChar=finite&&char&&Number.isFinite(char.x)&&Number.isFinite(char.y)
            &&Math.hypot(pose[0]-char.x,pose[1]-char.y)<=0.05;
        const allZero=pose.every(v=>v===0);
        const poseVerified=Boolean(matchesChar)&&!allZero;
        const paused=Boolean(native("IS_PAUSE_MENU_ACTIVE"));
        const cutscene=Boolean(native("HAS_CUTSCENE_LOADED")&&!native("HAS_CUTSCENE_FINISHED"));
        // Ground queries and cached pose reads are observers, not simulation ticks.
        const ground=poseVerified?native("GET_GROUND_Z_FOR_3D_COORD",pose[0],pose[1],pose[2]+2):null;
        const matches=poseVerified?SURFACES.filter(s=>{const h=height(s,pose[0],pose[1]);return h!==null&&Number.isFinite(ground)&&Math.abs(h-ground)<=0.05;}):[];
        if(!selected&&matches.length===1)selected=matches[0];
        const support=poseVerified&&selected?height(selected,pose[0],pose[1]):null;
        const flags={backend_ready:Boolean(native("COMBINE_SKATE_READY")),finite_pose:finite,pose_all_zero:allZero,
            pose_matches_char_xy:Boolean(matchesChar),pose_observation_verified:poseVerified,
            paused,cutscene,camera_exists:Boolean(native("DOES_CAM_EXIST",owner.camera)),
            same_owner:!previous||(owner.player===previous.player&&owner.ped===previous.ped&&owner.camera===previous.camera),
            unique_ground_match:poseVerified?matches.length===1:null,qualified_support_present:poseVerified?support!==null:null,
            height_within_support:poseVerified?support!==null&&Math.abs(pose[2]-support)<3:null};
        const after=native("COMBINE_SKATE_EVAL_OWNER");
        if(after.player!==owner.player||after.ped!==owner.ped||after.camera!==owner.camera) {
            emit("owner-raced-observation",{last:lastFlags});
            previous=owner;
            continue; // Do not mistake a reset during reads for a bad mounted pose.
        }
        const changed=JSON.stringify(flags)!==JSON.stringify(lastFlags);
        if(changed)emit(previous?"changed":"owner-started",flags);
        previous=owner;lastFlags=flags;
    }
    emit("expired");
}catch(_) {emit("observer-unavailable");}
