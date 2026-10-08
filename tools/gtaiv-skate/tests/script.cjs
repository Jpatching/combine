const assert=require('node:assert/strict');const fs=require('node:fs');const vm=require('node:vm');
function run(mode) {
 let frame=0,mounted=false,restored=false,camera=false,vertices=0,poseWrites=0,queries=0;
 const calls=[],transfers=[],logs=[];
 const native=(name,...args)=>{
  calls.push([name,...args]);
  switch(name){
   case 'COMBINE_SKATE_READY':return 1;
   case 'COMBINE_SKATE_TOGGLE':return frame===1||frame===4&&!['prepFail','prepPause','prepMove','gridNonfinite','gridZero','gridOver','vertexFail'].includes(mode);
   case 'GET_PLAYER_ID':case 'CONVERT_INT_TO_PLAYERINDEX':return 0;
   case 'GET_PLAYER_CHAR':return 7;
   case 'DOES_CHAR_EXIST':case 'IS_PLAYER_PLAYING':return true;
   case 'HAS_CUTSCENE_LOADED':return mode==='cutscene';
   case 'HAS_CUTSCENE_FINISHED':return mode!=='cutscene';
   case 'IS_PAUSE_MENU_ACTIVE':return mode==='paused'||mode==='prepPause'&&frame>=2;
   case 'IS_PLAYER_CONTROL_ON':return mode!=='blocked' && !mounted;
   case 'IS_CHAR_ON_FOOT':return mode!=='vehicle'||frame<3;
   case 'GET_CHAR_COORDINATES':return {x:mode==='prepMove'&&frame>=2?101:100,y:200,z:mode==='noGround'?1:11};
   case 'GET_CHAR_HEADING':return 0;
   case 'GET_GROUND_Z_FOR_3D_COORD':queries++;return mode==='noGround'?0:queries>1&&mode==='gridNonfinite'?NaN:queries>1&&mode==='gridZero'?0:queries>1&&mode==='gridOver'?10.1:10;
   case 'GET_CHAR_HEIGHT_ABOVE_GROUND':return 1;
   case 'COMBINE_SKATE_VERTEX':vertices++;return mode==='vertexFail'?0:1;
   case 'COMBINE_SKATE_MOUNT':return mode==='initFail'?0:['preparing','prepCancel','prepFail','prepPause','prepMove'].includes(mode)?2:1;
   case 'COMBINE_SKATE_POLL':return mode==='prepFail'?0:mode==='prepCancel'?2:frame<2?2:1;
   case 'COMBINE_SKATE_TICK':return mode==='inputFail'?0:1;
   case 'COMBINE_SKATE_STOP':if(mode==='stopThrow'&&frame>=4)throw Error('stop failure');return;
   case 'COMBINE_SKATE_RELEASE':if(mode==='releaseThrow')throw Error('release failure');return;
   case 'COMBINE_SKATE_VALUE':return mode==='invalidInitial'?NaN:[100.1,200.2,10,0][args[0]];
   case 'GET_GAME_TIMER':return frame*16;
   case 'CREATE_CAM':camera=true;return 99;
   case 'DOES_CAM_EXIST':return camera;
   case 'DESTROY_CAM':camera=false;return;
   case 'SET_PLAYER_CONTROL':if(!args[1])transfers.push(frame);mounted=!args[1];if(args[1])restored=true;return;
   case 'SET_CHAR_COORDINATES':if(mode==='nativeThrow')throw Error('native failure');poseWrites++;return;
   default:return undefined;
  }
 };
 const context={native,log:event=>logs.push(event),wait:()=>{if(++frame>5)throw Error('END');},console,Math,Number};
 try {vm.runInNewContext(fs.readFileSync('tools/gtaiv-skate/combine_skate.js','utf8'),context);}catch(e){if(e.message!=='END')throw e;}
 return {calls,logs,transfers,mounted,restored,camera,vertices,poseWrites};
}
const successful=run('ok');assert.equal(successful.vertices,25);assert.ok(successful.poseWrites>0);
assert.equal(successful.mounted,false);assert.equal(successful.camera,false);assert.ok(successful.restored);
console.log('PASS: mount presents Session pose and dismount restores GTA');
const stopFailure=run('stopThrow');
assert.equal(stopFailure.mounted,false);assert.equal(stopFailure.camera,false);assert.ok(stopFailure.restored);
assert.ok(stopFailure.calls.some(c=>c[0]==='COMBINE_SKATE_RELEASE'));
console.log('PASS: throwing Session stop still restores GTA ownership on dismount');
const releaseFailure=run('releaseThrow');
assert.equal(releaseFailure.mounted,false);assert.equal(releaseFailure.camera,false);assert.ok(releaseFailure.restored);
console.log('PASS: throwing ownership release cannot interrupt GTA restoration');
const failedInit=run('initFail');assert.equal(failedInit.poseWrites,0);assert.equal(failedInit.camera,false);
assert.equal(failedInit.calls.some(c=>c[0]==='SET_PLAYER_CONTROL'&&c[2]===false),false);
const lostInput=run('inputFail');assert.equal(lostInput.mounted,false);assert.equal(lostInput.camera,false);
assert.ok(lostInput.restored);
console.log('PASS: failed initialization retains GTA; lost input restores controls/camera');

for(const mode of ['vehicle','nativeThrow']) {
 const result=run(mode);assert.equal(result.mounted,false);assert.equal(result.camera,false);assert.ok(result.restored);
}
console.log('PASS: vehicle transition and throwing presentation restore GTA');
function runWatchdog(mode) {
const rescueCalls=[];let rescueFrame=0;
try {vm.runInNewContext(fs.readFileSync('tools/gtaiv-skate/combine_skate_watchdog.js','utf8'),{
 wait:()=>{if(++rescueFrame>1)throw Error('END');},
 native:(name,...args)=>{rescueCalls.push([name,...args]);
  if(name==='COMBINE_SKATE_RESCUE')return {player:0,ped:7,camera:99};
  if(name==='DOES_CAM_EXIST'||name==='DOES_CHAR_EXIST')return true;
  if(mode==='stopThrow'&&name==='COMBINE_SKATE_STOP')throw Error('stop failure');
  if(mode==='releaseThrow'&&name==='COMBINE_SKATE_RELEASE')throw Error('release failure');
 }
});}catch(e){if(e.message!=='END')throw e;}
return rescueCalls;
}
const rescueCalls=runWatchdog('ok');
assert.ok(rescueCalls.some(c=>c[0]==='SET_PLAYER_CONTROL'&&c[2]===true));
assert.ok(rescueCalls.some(c=>c[0]==='FREEZE_CHAR_POSITION'&&c[2]===false));
assert.ok(rescueCalls.some(c=>c[0]==='DESTROY_CAM'&&c[1]===99));
console.log('PASS: independent watchdog restores owned controls and camera');
const watchdogStopFailure=runWatchdog('stopThrow');
assert.ok(watchdogStopFailure.some(c=>c[0]==='COMBINE_SKATE_RELEASE'));
console.log('PASS: watchdog releases ownership and keeps running when Session stop throws');
assert.ok(runWatchdog('releaseThrow').some(c=>c[0]==='SET_PLAYER_CONTROL'&&c[2]===true));
console.log('PASS: watchdog keeps running when ownership release throws');

const noGround=run("noGround");assert.equal(noGround.poseWrites,0);assert.equal(noGround.calls.some(c=>c[0]==="SET_PLAYER_CONTROL"&&c[2]===false),false);
console.log("PASS: ambiguous no-ground zero probe retains GTA ownership");

for(const mode of ['cutscene','paused','blocked']) {
 const result=run(mode);
 assert.equal(result.vertices,0,`${mode} must not sample a mount surface`);
 assert.equal(result.calls.some(c=>c[0]==='SET_PLAYER_CONTROL'&&c[2]===false),false);
}
console.log('PASS: cutscenes, pause menus and disabled GTA control prevent mount');

const preparing=run('preparing');
assert.ok(preparing.calls.some(c=>c[0]==='COMBINE_SKATE_POLL'));
assert.ok(preparing.poseWrites>0);
assert.ok(preparing.restored);
console.log('PASS: asynchronous preparation leaves GTA responsive before mounting');
assert.equal(preparing.transfers[0],2);
for(const mode of ['prepCancel','prepFail','prepPause','prepMove']) {
 const result=run(mode);assert.equal(result.poseWrites,0);assert.equal(result.transfers.length,0);
 assert.equal(result.camera,false);assert.equal(result.mounted,false);
}
console.log('PASS: cancellation, preparation fault, pause and movement retain GTA controls');

for(const [mode,reason] of [['gridNonfinite','non-finite'],['gridZero','near-zero'],['gridOver','over-0.05-metres'],['vertexFail','vertex-rejection']]) {
 const result=run(mode);assert.ok(result.logs.includes('COMBINE_SKATE surface-refused:'+reason));
 assert.equal(result.transfers.length,0);assert.equal(result.poseWrites,0);
 if(mode!=='vertexFail')assert.equal(result.vertices,0);
}
console.log('PASS: surface refusal reports exact reason and preserves short-circuit vertex calls');
const invalidInitial=run('invalidInitial');assert.equal(invalidInitial.transfers.length,0);assert.equal(invalidInitial.camera,false);
console.log('PASS: nonfinite initial output cannot transfer GTA ownership');
