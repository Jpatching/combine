// Private, opt-in evaluation only. Stage with --evaluation definitions/plugin.
// F8 runs bounded real worker input; F9 observes ordinary walking after restore.
// Outputs fixed verdicts only. No positions, assets or controller identities.
let previous=null, restoredForWalk=null, held8=false, held9=false, attempt=0;
const PROFILE={neutral:0,push:1,left:2,right:3}, INPUT_REFUSED={};
function report(text) {log("COMBINE_EVALUATION "+text);}
function finite(p) {return [p.x,p.y,p.z].every(Number.isFinite);}
function distance(a,b) {return Math.hypot(a.x-b.x,a.y-b.y,a.z-b.z);}
function elapsed(command,start) {return (native(command)-start)>>>0;}
function interrupted() {
    return native("IS_PAUSE_MENU_ACTIVE")
        || (native("HAS_CUTSCENE_LOADED") && !native("HAS_CUTSCENE_FINISHED"));
}
function snapshot(owner) {
    const current=native("COMBINE_SKATE_EVAL_OWNER");
    if(interrupted()) throw new Error("game-interrupted");
    if(current.player!==owner.player || current.ped!==owner.ped || current.camera!==owner.camera)
        throw new Error("ride-ended");
    if(native("IS_PLAYER_CONTROL_ON",owner.player)) throw new Error("GTA-control-returned");
    if(!native("DOES_CAM_EXIST",owner.camera)) throw new Error("camera-missing");
    if(!native("IS_CAM_ACTIVE",owner.camera)) throw new Error("camera-inactive");
    if(!native("IS_CAM_PROPAGATING",owner.camera)) throw new Error("camera-not-propagating");
    const pos=native("GET_CHAR_COORDINATES",owner.ped);
    const camera=native("GET_CAM_POS",owner.camera);
    const heading=native("GET_CHAR_HEADING",owner.ped);
    if(!finite(pos) || !finite(camera) || !Number.isFinite(heading)) throw new Error("nonfinite-observation");
    return {pos,camera,heading};
}
function phase(owner,profile,duration) {
    if(!native("COMBINE_SKATE_EVAL_INPUT",profile,duration)) throw INPUT_REFUSED;
    const started=native("GET_GAME_TIMER"), realStarted=native("COMBINE_SKATE_EVAL_TIME");
    let latest=snapshot(owner);
    do {
        wait(0);latest=snapshot(owner);
        if(elapsed("COMBINE_SKATE_EVAL_TIME",realStarted)>duration+1000) throw new Error("observation-timeout");
    } while(elapsed("GET_GAME_TIMER",started)<duration);
    return latest;
}
function playback(owner) {
    try {
        report("attempt:"+(++attempt)+" started");
        const start=snapshot(owner);
        phase(owner,PROFILE.neutral,250);
        const push=phase(owner,PROFILE.push,750);
        const beforeLeft=phase(owner,PROFILE.neutral,250);
        const left=phase(owner,PROFILE.left,400);
        const beforeRight=phase(owner,PROFILE.neutral,250);
        const right=phase(owner,PROFILE.right,400);
        phase(owner,PROFILE.neutral,250);
        const angle=(a,b)=>((b-a+540)%360)-180;
        const moved=distance(start.pos,push.pos)>0.01;
        const leftDelta=angle(beforeLeft.heading,left.heading), rightDelta=angle(beforeRight.heading,right.heading);
        const leftMoved=Math.abs(leftDelta)>0.1, rightMoved=Math.abs(rightDelta)>0.1;
        const opposite=leftMoved&&rightMoved&&leftDelta*rightDelta<0;
        const followed=distance(start.camera,right.camera)>0.01;
        const sign=delta=>delta>0.1?"positive":delta< -0.1?"negative":"unchanged";
        report((moved&&opposite&&followed?"PASS":"FAIL")+": real-input movement="+moved+", left-heading="+sign(leftDelta)+", right-heading="+sign(rightDelta)+", finite-active-camera-moved="+followed+"; scale/orientation acceptance unverified");
    } catch (error) {
        const known=["game-interrupted","ride-ended","GTA-control-returned","camera-missing",
            "camera-inactive","camera-not-propagating","nonfinite-observation","observation-timeout"];
        const reason=known.includes(error.message)?error.message:"native-query-unavailable";
        report(error===INPUT_REFUSED?"REFUSED: evaluation input unavailable":
            "UNAVAILABLE: playback interrupted or native observation unavailable; prerequisite="+reason);
    }
    finally {try {native("COMBINE_SKATE_EVAL_INPUT",-1,0);}catch (_) {}}
}
function walking() {
    report("walking-attempt:"+(++attempt)+" started");
    const player=native("CONVERT_INT_TO_PLAYERINDEX",native("GET_PLAYER_ID"));
    const ped=native("GET_PLAYER_CHAR",player);
    if(!restoredForWalk || restoredForWalk.player!==player || restoredForWalk.ped!==ped
        || interrupted() || !native("IS_PLAYER_CONTROL_ON",player) || !native("IS_CHAR_ON_FOOT",ped)) {
        report("UNAVAILABLE: ordinary walking prerequisites absent");return;
    }
    const start=native("GET_CHAR_COORDINATES",ped), timer=native("GET_GAME_TIMER"), realTimer=native("COMBINE_SKATE_EVAL_TIME");
    let end=start;
    do {
        wait(0);
        if(interrupted() || elapsed("COMBINE_SKATE_EVAL_TIME",realTimer)>3000
            || !native("IS_PLAYER_CONTROL_ON",player) || !native("IS_CHAR_ON_FOOT",ped)) {
            report("UNAVAILABLE: ordinary walking interrupted");return;
        }
        end=native("GET_CHAR_COORDINATES",ped);
    } while(elapsed("GET_GAME_TIMER",timer)<2000);
    report((finite(start)&&finite(end)&&distance(start,end)>0.03?"PASS":"FAIL")+": ordinary walking displacement after restoration");
}
while(true) {
    wait(100);
    try {
        const owner=native("COMBINE_SKATE_EVAL_OWNER");
        if(owner.player>=0) {previous=owner;restoredForWalk=null;}
        else if(previous) {
            const restored=native("IS_PLAYER_CONTROL_ON",previous.player)
                && !native("DOES_CAM_EXIST",previous.camera);
            report((restored?"PASS":"FAIL")+": native GTA control and owned camera destruction after ride");
            restoredForWalk=restored?previous:null;
            previous=null;
        }
        const key8=Boolean(native("COMBINE_SKATE_EVAL_KEY",0));
        const key9=Boolean(native("COMBINE_SKATE_EVAL_KEY",1));
        if(key8&&!held8) {
            if(owner.player>=0)playback(owner);
            else report("UNAVAILABLE: mounted ride required for playback");
        }
        if(key9&&!held9 && owner.player<0)walking();
        held8=key8;held9=key9;
    } catch (_) {report("UNAVAILABLE: evaluation native query failed");wait(1000);}
}
