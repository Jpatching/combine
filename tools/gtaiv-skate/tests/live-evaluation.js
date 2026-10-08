// Private, opt-in evaluation only. Stage with --evaluation definitions/plugin.
// F8 runs bounded real worker input; F9 observes ordinary walking after restore.
// Outputs fixed verdicts only. No positions, assets or controller identities.
let previous=null, held8=false, held9=false;
function report(text) {log("COMBINE_EVALUATION "+text);}
function finite(p) {return [p.x,p.y,p.z].every(Number.isFinite);}
function distance(a,b) {return Math.hypot(a.x-b.x,a.y-b.y,a.z-b.z);}
function snapshot(owner) {
    const current=native("COMBINE_SKATE_EVAL_OWNER");
    if(current.player!==owner.player || current.ped!==owner.ped || current.camera!==owner.camera
        || native("IS_PLAYER_CONTROL_ON",owner.player)
        || !native("DOES_CAM_EXIST",owner.camera)
        || !native("IS_CAM_ACTIVE",owner.camera)
        || !native("IS_CAM_PROPAGATING",owner.camera)) throw new Error("ride unavailable");
    const pos=native("GET_CHAR_COORDINATES",owner.ped);
    const camera=native("GET_CAM_POS",owner.camera);
    const heading=native("GET_CHAR_HEADING",owner.ped);
    if(!finite(pos) || !finite(camera) || !Number.isFinite(heading)) throw new Error("nonfinite observation");
    return {pos,camera,heading};
}
function phase(owner,profile,duration) {
    if(!native("COMBINE_SKATE_EVAL_INPUT",profile,duration)) throw new Error("input refused");
    const started=native("GET_GAME_TIMER");
    let latest=snapshot(owner);
    do {wait(0);latest=snapshot(owner);} while(native("GET_GAME_TIMER")-started<duration);
    return latest;
}
function playback(owner) {
    try {
        const start=snapshot(owner);
        phase(owner,0,250);
        const push=phase(owner,1,750);
        phase(owner,0,250);
        const left=phase(owner,2,400);
        phase(owner,0,250);
        const right=phase(owner,3,400);
        phase(owner,0,250);
        const angle=(a,b)=>Math.abs(((a-b+540)%360)-180);
        const moved=distance(start.pos,push.pos)>0.01;
        const steered=angle(push.heading,left.heading)>0.1 || angle(left.heading,right.heading)>0.1;
        const followed=distance(start.camera,right.camera)>0.01;
        report((moved&&steered&&followed?"PASS":"FAIL")+": real-input movement="+moved+", heading-change="+steered+", finite-active-camera-moved="+followed);
    } catch (_) {report("UNAVAILABLE: playback interrupted or native input/query refused");}
    finally {try {native("COMBINE_SKATE_EVAL_INPUT",-1,0);}catch (_) {}}
}
function walking() {
    const player=native("CONVERT_INT_TO_PLAYERINDEX",native("GET_PLAYER_ID"));
    const ped=native("GET_PLAYER_CHAR",player);
    if(!native("IS_PLAYER_CONTROL_ON",player) || !native("IS_CHAR_ON_FOOT",ped)) {
        report("UNAVAILABLE: ordinary walking prerequisites absent");return;
    }
    const start=native("GET_CHAR_COORDINATES",ped), timer=native("GET_GAME_TIMER");
    let end=start;
    do {
        wait(0);
        if(!native("IS_PLAYER_CONTROL_ON",player) || !native("IS_CHAR_ON_FOOT",ped)) {
            report("UNAVAILABLE: ordinary walking interrupted");return;
        }
        end=native("GET_CHAR_COORDINATES",ped);
    } while(native("GET_GAME_TIMER")-timer<2000);
    report((finite(start)&&finite(end)&&distance(start,end)>0.03?"PASS":"FAIL")+": ordinary walking displacement after restoration");
}
while(true) {
    wait(100);
    try {
        const owner=native("COMBINE_SKATE_EVAL_OWNER");
        if(owner.player>=0)previous=owner;
        else if(previous) {
            const restored=native("IS_PLAYER_CONTROL_ON",previous.player)
                && !native("DOES_CAM_EXIST",previous.camera);
            report((restored?"PASS":"FAIL")+": native GTA control and owned camera destruction after ride");
            previous=null;
        }
        const key8=Boolean(native("IS_KEYBOARD_KEY_PRESSED",119));
        const key9=Boolean(native("IS_KEYBOARD_KEY_PRESSED",120));
        if(key8&&!held8) {
            if(owner.player>=0)playback(owner);
            else report("UNAVAILABLE: mounted ride required for playback");
        }
        if(key9&&!held9 && owner.player<0)walking();
        held8=key8;held9=key9;
    } catch (_) {report("UNAVAILABLE: evaluation native query failed");wait(1000);}
}
