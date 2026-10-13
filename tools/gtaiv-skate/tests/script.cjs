const assert=require('node:assert/strict');const fs=require('node:fs');const vm=require('node:vm');
function run(mode, surfaces = []) {
 let frame=0,mounted=false,restored=false,camera=false,vertices=0,poseWrites=0,queries=0,recoveryFailures=0,geometryTicks=0;
 const calls=[],transfers=[],logs=[];
 const native=(name,...args)=>{
  calls.push([name,...args]);
  switch(name){
   case 'COMBINE_SKATE_READY':return ['prepReadyLoss','rideReadyLoss'].includes(mode)&&frame>=2||mode==='escapeRecoveryLoss'&&frame>=3?0:1;
   case 'COMBINE_SKATE_INPUT_MODE':return mode==='modeRefused'?0:1;
   case 'COMBINE_SKATE_INPUT_TOGGLE':return mode==='controller'&&frame===1?0:-1;
   case 'GET_MOUSE_INPUT':return mode==='invalidMouse'?{x:NaN,y:0}:mode==='mouse'?{x:40,y:20}:{x:0,y:0};
   case 'COMBINE_SKATE_TOGGLE':if(mode==='geometryRemount')return [1,3,5].includes(frame);return frame===1||frame===4&&!['prepFail','prepPause','prepMove','gridNonfinite','gridZero','gridOver','vertexFail'].includes(mode);
   case 'GET_PLAYER_ID':case 'CONVERT_INT_TO_PLAYERINDEX':return 0;
   case 'GET_PLAYER_CHAR':return mode==='ownerChanged'&&frame>=2?8:7;
   case 'DOES_CHAR_EXIST':case 'IS_PLAYER_PLAYING':return true;
   case 'HAS_CUTSCENE_LOADED':return mode==='cutscene'||mode==='rideCutscene'&&frame>=2;
   case 'HAS_CUTSCENE_FINISHED':return mode!=='cutscene'&&!(mode==='rideCutscene'&&frame>=2);
   case 'IS_PAUSE_MENU_ACTIVE':return mode==='paused'||mode==='ridePaused'&&frame>=2||mode==='prepPause'&&frame>=2;
   case 'IS_PLAYER_CONTROL_ON':return mode!=='blocked' && !mounted;
   case 'IS_CHAR_ON_FOOT':return mode!=='vehicle'||frame<3;
   case 'GET_CHAR_COORDINATES':return {x:mode==='prepMove'&&frame>=2?101:100,y:200,z:mode==='noGround'?1:11};
   case 'GET_CHAR_HEADING':return 0;
   case 'GET_GROUND_Z_FOR_3D_COORD':queries++;return mode==='geometry'?10+(args[0]-100)*0.1:mode==='noGround'?0:queries>1&&mode==='gridNonfinite'?NaN:queries>1&&mode==='gridZero'?0:queries>1&&mode==='gridOver'?10.1:10;
   case 'GET_CHAR_HEIGHT_ABOVE_GROUND':return 1;
   case 'COMBINE_SKATE_VERTEX':vertices++;return mode==='vertexFail'?0:1;
   case 'COMBINE_SKATE_SURFACE_BEGIN':return 1;
   case 'COMBINE_SKATE_SURFACE_VERTEX':return mode==='geometryUploadFail'?0:1;
   case 'COMBINE_SKATE_MOUNT_SURFACE':return mode==='geometryMountFail'?0:mode==='geometryPreparing'?2:1;
   case 'COMBINE_SKATE_TICK_SURFACE':geometryTicks++;return mode==='geometryTickFail'||mode==='geometryRemount'&&geometryTicks===1?0:1;
   case 'COMBINE_SKATE_MOUNT':return mode==='initFail'?0:['preparing','prepCancel','prepFail','prepPause','prepMove','prepTimeout','prepReadyLoss','prepCameraFail'].includes(mode)?2:1;
   case 'COMBINE_SKATE_POLL':return mode==='prepFail'?0:['prepCancel','prepTimeout'].includes(mode)?2:frame<2?2:1;
   case 'COMBINE_SKATE_TICK':return mode==='inputFail'?0:1;
   case 'COMBINE_SKATE_STOP':if(mode==='stopThrow'&&frame>=4)throw Error('stop failure');return;
   case 'COMBINE_SKATE_RELEASE':if(mode==='releaseThrow')throw Error('release failure');return;
   case 'COMBINE_SKATE_VALUE':return mode==='invalidInitial'||mode==='invalidReturnedPose'&&frame>=2&&args[0]===3?NaN:['geometryEscape','escapeRecoveryLoss'].includes(mode)&&geometryTicks>=1||mode==='geometryInitialEscape'?[104,200,10.4,0][args[0]]:[100.1,200.2,11,0][args[0]];
   case 'GET_GAME_TIMER':return frame*(mode==='prepTimeout'?60001:16);
   case 'CREATE_CAM':camera=mode!=='prepCameraFail';return 99;
   case 'DOES_CAM_EXIST':return camera;
   case 'DESTROY_CAM':camera=false;return;
   case 'SET_PLAYER_CONTROL':if(args[1]&&['restoreOnce','escapeRecoveryLoss'].includes(mode)&&recoveryFailures++===0)throw Error('transient restoration failure');if(!args[1])transfers.push(frame);mounted=!args[1];if(args[1])restored=true;return;
   case 'SET_CHAR_COORDINATES':if(mode==='nativeThrow')throw Error('native failure');poseWrites++;return;
   default:return undefined;
  }
 };
 const context={native,log:event=>logs.push(event),wait:()=>{if(++frame>5)throw Error('END');},console,Math,Number};
 const source=fs.readFileSync('tools/gtaiv-skate/combine_skate.js','utf8').replace('const SURFACES = [];','const SURFACES = '+JSON.stringify(surfaces)+';');
 try {vm.runInNewContext(source,context);}catch(e){if(e.message!=='END')throw e;}
 return {calls,logs,transfers,mounted,restored,camera,vertices,poseWrites};
}
const slope=[{layer:1,qualified:true,evidence:'authored-two-floor-witness',center:[100,200],radius:3,
 triangles:[[[95,195,9.5],[105,195,10.5],[105,205,10.5]],[[95,195,9.5],[105,205,10.5],[95,205,9.5]]]}];
const geometry=run('geometry',slope);
assert.ok(geometry.calls.some(c=>c[0]==='COMBINE_SKATE_MOUNT_SURFACE'&&c[6]===1&&c[7]===1));
assert.ok(geometry.calls.some(c=>c[0]==='COMBINE_SKATE_TICK_SURFACE'&&c[2]===100.1&&c[3]===200.2&&c[5]===1&&c[6]===1));
assert.equal(geometry.vertices,0);assert.ok(geometry.poseWrites>0);assert.ok(geometry.restored);
console.log('PASS: qualified slope mounts and rides through the triangle route, then restores GTA');
for (const surfaces of [slope.map(s=>({...s,qualified:false})), slope.map(s=>({...s,center:[110,210]})),
 slope.map(s=>({...s,triangles:s.triangles.map(t=>t.map(v=>[v[0],v[1],v[2]+1]))})), [...slope,...slope.map(s=>({...s,layer:2}))]]) {
 const refused=run('geometry',surfaces);
 assert.equal(refused.transfers.length,0);assert.equal(refused.vertices,0);assert.equal(refused.poseWrites,0);
}
console.log('PASS: unqualified, uncovered, wrong-floor and ambiguous geometry cannot take GTA control');
const geometryPending=run('geometryPreparing',slope);
assert.equal(geometryPending.transfers[0],2);assert.ok(geometryPending.poseWrites>0);assert.ok(geometryPending.restored);
const geometryTickFailure=run('geometryTickFail',slope);
assert.ok(geometryTickFailure.restored);assert.equal(geometryTickFailure.mounted,false);assert.equal(geometryTickFailure.camera,false);
console.log('PASS: triangle preparation stays asynchronous and tick refusal restores normal GTA control');
for(const mode of ['geometryUploadFail','geometryMountFail','geometryInitialEscape']) {
 const failed=run(mode,slope);assert.equal(failed.transfers.length,0);assert.equal(failed.poseWrites,0);
}
const escaped=run('geometryEscape',slope);assert.ok(escaped.restored);assert.ok(escaped.transfers.length>0);
assert.ok(escaped.calls.some(c=>c[0]==='COMBINE_SKATE_TICK_SURFACE'));
assert.ok(!escaped.calls.some(c=>c[0]==='SET_CHAR_COORDINATES'&&c[2]===104));
assert.ok(escaped.logs.includes('COMBINE_SKATE ride-stopped:outside-qualified-surface'));
const invalidReturned=run('invalidReturnedPose');
assert.ok(invalidReturned.logs.includes('COMBINE_SKATE ride-stopped:nonfinite-pose'));
assert.ok(invalidReturned.restored);assert.equal(invalidReturned.poseWrites,0);
const escapeRecovery=run('escapeRecoveryLoss',slope);
assert.deepEqual(escapeRecovery.logs.filter(s=>s.startsWith('COMBINE_SKATE ride-stopped:')), ['COMBINE_SKATE ride-stopped:outside-qualified-surface']);
assert.ok(escapeRecovery.logs.indexOf('COMBINE_SKATE ride-stopped:outside-qualified-surface')<escapeRecovery.logs.indexOf('COMBINE_SKATE recovery-pending'));
assert.ok(escapeRecovery.restored);assert.equal(escapeRecovery.mounted,false);
const overlapping=slope.map(s=>({...s,triangles:[...s.triangles,s.triangles[0].map(v=>[v[0],v[1],v[2]+0.005])]}));
assert.equal(run('geometry',overlapping).transfers.length,0);
const remounted=run('geometryRemount',slope);assert.deepEqual(remounted.transfers,[1,3]);assert.ok(remounted.poseWrites>0);assert.ok(remounted.restored);
console.log('PASS: triangle failures recover and remount; initial and returned poses stay inside qualified coverage');

const successful=run('ok');assert.equal(successful.vertices,25);assert.ok(successful.poseWrites>0);
assert.ok(successful.calls.some(c=>c[0]==='COMBINE_SKATE_INPUT_MODE'&&c[1]===1));
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
const rescueCalls=[];let rescueFrame=0,rescueCamera=true,rescueControl=false;
try {vm.runInNewContext(fs.readFileSync('tools/gtaiv-skate/combine_skate_watchdog.js','utf8'),{
 wait:()=>{if(++rescueFrame>1)throw Error('END');},
 native:(name,...args)=>{rescueCalls.push([name,...args]);
  if(name==='COMBINE_SKATE_RESCUE')return {player:0,ped:7,camera:99};
  if(name==='DOES_CAM_EXIST')return rescueCamera;
  if(name==='DOES_CHAR_EXIST')return true;
  if(name==='DESTROY_CAM'){rescueCamera=false;return;}
  if(name==='SET_PLAYER_CONTROL'){rescueControl=args[1];return;}
  if(name==='IS_PLAYER_CONTROL_ON')return rescueControl;
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

for(const [mode,reason] of [['ridePaused','paused'],['rideCutscene','cutscene'],['rideReadyLoss','adapter-not-ready'],['ownerChanged','owner-changed'],['vehicle','character-unavailable']]) {
 const ended=run(mode);
 assert.ok(ended.transfers.length>0);assert.ok(ended.restored);assert.equal(ended.mounted,false);
 assert.ok(ended.logs.includes('COMBINE_SKATE ride-stopped:'+reason), reason+' must explain why an already mounted Session stopped');
}
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
const preparationTimeout=run('prepTimeout');
assert.equal(preparationTimeout.transfers.length,0);
assert.ok(preparationTimeout.logs.includes('COMBINE_SKATE Skate: preparation timed out - GTA retained'));
assert.ok(preparationTimeout.calls.some(c=>c[0]==='COMBINE_SKATE_STOP'));
console.log('PASS: pending preparation has a visible timeout without taking GTA control');
for(const [mode,message] of [['prepReadyLoss','preparation failed'],['prepCameraFail','camera unavailable']]) {
 const result=run(mode);assert.equal(result.transfers.length,0);assert.equal(result.poseWrites,0);
 assert.ok(result.logs.includes('COMBINE_SKATE Skate: '+message+' - GTA retained'));
}
console.log('PASS: lost readiness and unavailable camera report terminal preparation outcomes');
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
for(const [mode,reason] of [['inputFail','surface-input-time-unavailable'],['invalidMouse','mouse-input-unavailable'],['nativeThrow','native-exception'],['ok','dismount-toggle']]) {
 assert.ok(run(mode).logs.includes('COMBINE_SKATE ride-stopped:'+reason));
}
const mouse=run('mouse');
const mouseCamera=mouse.calls.filter(c=>c[0]==='SET_CAM_POS');
const ordinaryCamera=successful.calls.filter(c=>c[0]==='SET_CAM_POS');
assert.ok(mouseCamera.length>0);
assert.notDeepEqual(mouseCamera[0].slice(2),ordinaryCamera[0].slice(2));
assert.equal(mouse.mounted,false);assert.equal(mouse.camera,false);
const invalidMouse=run('invalidMouse');
assert.ok(invalidMouse.restored);assert.equal(invalidMouse.camera,false);
assert.equal(run('modeRefused').transfers.length,0);
console.log('PASS: keyboard/mouse mode orbits the owned camera and restores GTA on invalid mouse or input-mode refusal');
const controller=run('controller');assert.ok(controller.poseWrites>0);
assert.equal(controller.calls.some(c=>c[0]==='GET_MOUSE_INPUT'),false);
assert.ok(controller.restored);
console.log('PASS: dismounted input selection preserves controller riding and camera recovery');
const transient=run('restoreOnce');
assert.ok(transient.restored,'a transient control restoration failure must be retried');
assert.equal(transient.mounted,false);
const recoveryCalls=transient.calls.filter(c=>c[0]==='SET_PLAYER_CONTROL'&&c[2]===true);
assert.ok(recoveryCalls.length>=2);
const firstRelease=transient.calls.findIndex(c=>c[0]==='COMBINE_SKATE_RELEASE');
assert.ok(firstRelease>transient.calls.lastIndexOf(recoveryCalls[1]));
console.log('PASS: transient restoration keeps recovery ownership until GTA control is restored');
