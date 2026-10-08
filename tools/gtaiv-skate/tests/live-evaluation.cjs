// CLEO/native boundary replay; never substitutes for real physics acceptance.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync(process.argv[2]||`${__dirname}/live-evaluation.js`,'utf8');
function replay(mode) {
    let real=0,profile=0,outer=0;
    const logs=[],stop={};
    const owner={player:1,ped:2,camera:3};
    const context={log:text=>logs.push(text),wait:ms=>{
        if(ms===100 && ++outer>1)throw stop;
        if(ms===0)real+=50;
        if(real>10000)throw new Error('observer exceeded host deadline');
    },native:(name,...args)=>{
        switch(name) {
        case 'COMBINE_SKATE_EVAL_OWNER': return mode==='walking'?{player:-1,ped:-1,camera:-1}:owner;
        case 'COMBINE_SKATE_EVAL_TIME': return real;
        case 'GET_GAME_TIMER': return mode==='frozen'?0:(0x7fffff00+real)|0;
        case 'COMBINE_SKATE_EVAL_INPUT': profile=args[0];return mode==='refused'?0:1;
        case 'IS_KEYBOARD_KEY_PRESSED': return args[0]===(mode==='walking'?120:119);
        case 'IS_PAUSE_MENU_ACTIVE': case 'HAS_CUTSCENE_LOADED': return false;
        case 'HAS_CUTSCENE_FINISHED': return true;
        case 'IS_PLAYER_CONTROL_ON': return mode==='walking';
        case 'DOES_CAM_EXIST': case 'IS_CAM_ACTIVE': case 'IS_CAM_PROPAGATING': return true;
        case 'GET_CHAR_COORDINATES': case 'GET_CAM_POS': return {x:real/1000,y:0,z:1};
        case 'GET_CHAR_HEADING': return profile===2?10:profile===3&&mode!=='broken-right'?350:0;
        case 'CONVERT_INT_TO_PLAYERINDEX': case 'GET_PLAYER_ID': return 1;
        case 'GET_PLAYER_CHAR': return 2;
        case 'IS_CHAR_ON_FOOT': return true;
        default: throw new Error(`Unexpected native ${name}`);
        }
    }};
    try {vm.runInNewContext(source,context,{timeout:1000});}catch(error){if(error!==stop)throw error;}
    return {logs,real};
}
const refused=replay('refused');
assert(refused.logs.some(line=>line.includes('REFUSED: evaluation input unavailable')));
console.log('PASS: explicit input refusal remains distinct from unavailable evidence');
const frozen=replay('frozen');
assert(frozen.real<=1500);
assert(frozen.logs.some(line=>line.includes('UNAVAILABLE: playback interrupted')));
console.log('PASS: stopped game clock cannot exceed independent observation deadline');
const rollover=replay('rollover');
assert(rollover.real<4000);
assert(rollover.logs.some(line=>line.includes('PASS: real-input')));
console.log('PASS: signed game-timer rollover retains bounded playback');
const walking=replay('walking');
assert(!walking.logs.some(line=>line.includes('PASS: ordinary walking')));
assert(walking.logs.some(line=>line.includes('UNAVAILABLE: ordinary walking prerequisites absent')));
console.log('PASS: ordinary walking cannot claim a restoration that never occurred');
const broken=replay('broken-right');
assert(broken.logs.some(line=>line.includes('FAIL: real-input')));
assert(!broken.logs.some(line=>line.includes('PASS: real-input')));
console.log('PASS: one responding steering direction cannot pass the playback check');
