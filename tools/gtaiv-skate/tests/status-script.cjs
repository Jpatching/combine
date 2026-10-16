const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
function observe(mode) {
 let snapshot,frame=0;
 const calls=[];
 try {vm.runInNewContext(fs.readFileSync('tools/gtaiv-skate/combine_game_status.js','utf8'),{
  wait(){if(++frame>1)throw Error('END');},
  native(name,...args){
   calls.push(name);
   switch(name){
    case 'COMBINE_SKATE_READY':return mode!=='notReady';
    case 'HAS_CUTSCENE_LOADED':return mode==='cutscene';
    case 'HAS_CUTSCENE_FINISHED':return mode!=='cutscene';
    case 'IS_PAUSE_MENU_ACTIVE':return mode==='paused';
    case 'GET_PLAYER_ID':case 'CONVERT_INT_TO_PLAYERINDEX':return 0;
    case 'GET_PLAYER_CHAR':return 7;
    case 'IS_PLAYER_PLAYING':if(mode==='queryFailure')throw Error('query failure');return mode!=='unavailable';
    case 'IS_PLAYER_CONTROL_ON':return mode==='gameplay';
    case 'IS_CHAR_ON_FOOT':case 'DOES_CHAR_EXIST':return true;
    case 'COMBINE_GAME_STATUS':snapshot=args;return;
    default:throw Error('Unexpected native '+name);
   }
  }
 });}catch(e){if(e.message!=='END')throw e;}
 assert.ok(calls.every(c=>!/^(SET_|FREEZE_|CREATE_|DESTROY_|ACTIVATE_|COMBINE_SKATE_(MOUNT|CLAIM))/.test(c)));
 return snapshot;
}
assert.deepEqual(observe('cutscene'),[2,0,1]);
assert.deepEqual(observe('gameplay'),[1,1,1]);
assert.deepEqual(observe('paused'),[3,0,1]);
assert.deepEqual(observe('unavailable'),[4,0,0]);
assert.deepEqual(observe('notReady'),[0,0,0]);
assert.deepEqual(observe('queryFailure'),[0,0,0]);
console.log('PASS: native status distinguishes cutscene/gameplay/pause and fails closed without game writes');
