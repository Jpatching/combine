// Exercise the riding script across the GTA/Session native boundary.
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
function patch(center,layer=1,height=10) {
 return {layer,qualified:true,evidence:'authored-corridor',center:[center,0],radius:3,
  triangles:[[[center-3,-3,height],[center+3,-3,height],[center+3,3,height]],
             [[center-3,-3,height],[center+3,3,height],[center-3,3,height]]]};
}
function drive(options={}) {
 let frame=0,x=options.startX||0,camera=false,control=true,transfers=0,pending=0,replacements=0,maxPresented=0,uploads=[],upload=null;
 const logs=[];let unreadSnapshot=false,lastTick=0,dismountSent=false;
 const native=(name,...args)=>{
  switch(name){
   case 'COMBINE_SKATE_READY':case 'COMBINE_SKATE_INPUT_MODE':return 1;
   case 'COMBINE_SKATE_INPUT_TOGGLE':return -1;
   case 'COMBINE_SKATE_TOGGLE':if(frame===1)return true;if(x>=(options.endAt||4) && !dismountSent){dismountSent=true;return true;}return false;
   case 'GET_PLAYER_ID':case 'CONVERT_INT_TO_PLAYERINDEX':return 0;
   case 'GET_PLAYER_CHAR':return 7;
   case 'DOES_CHAR_EXIST':case 'IS_PLAYER_PLAYING':case 'IS_CHAR_ON_FOOT':return true;
   case 'IS_PAUSE_MENU_ACTIVE':case 'HAS_CUTSCENE_LOADED':return false;
   case 'IS_PLAYER_CONTROL_ON':return control;
   case 'GET_CHAR_COORDINATES':return {x:options.startX||0,y:0,z:11};
   case 'GET_GROUND_Z_FOR_3D_COORD':return 10;
   case 'GET_CHAR_HEIGHT_ABOVE_GROUND':return 1;
   case 'GET_CHAR_HEADING':return 0;
   case 'COMBINE_SKATE_SURFACE_BEGIN':upload={layer:args[0],count:args[1],vertices:[]};uploads.push(upload);return 1;
   case 'COMBINE_SKATE_SURFACE_VERTEX':upload.vertices.push(args);return 1;
   case 'COMBINE_SKATE_MOUNT_SURFACE':return 1;
   case 'COMBINE_SKATE_VALUE':return [x,0,10,0][args[0]];
   case 'COMBINE_SKATE_SURFACE_REPLACE':replacements++;if(options.refuse)return 0;if(options.retry && unreadSnapshot)return 3;pending=options.ackFrames||2;return 2;
   case 'COMBINE_SKATE_POLL':if(options.neverReady)return 2;if(pending>0 && --pending>0)return 2;if(options.retryShift && unreadSnapshot && pending===0)x+=0.25;unreadSnapshot=false;return 1;
   case 'COMBINE_SKATE_TICK_SURFACE':assert.equal(pending,0,'do not tick unacknowledged collision');if(lastTick && frame*16-lastTick>250)return 0;lastTick=frame*16;unreadSnapshot=true;x+=0.75;return 1;
   case 'GET_GAME_TIMER':return frame*16;
   case 'CREATE_CAM':camera=true;return 99;
   case 'DOES_CAM_EXIST':return camera;
   case 'DESTROY_CAM':camera=false;return;
   case 'SET_PLAYER_CONTROL':control=args[1];if(!control)transfers++;return;
   case 'SET_CHAR_COORDINATES':maxPresented=Math.max(maxPresented,args[1]);return;
   case 'GET_MOUSE_INPUT':return {x:0,y:0};
  }
 };
 const surfaces=options.surfaces||[patch(0),patch(4)];
 const script=fs.readFileSync('tools/gtaiv-skate/combine_skate.js','utf8').replace('const SURFACES = [];','const SURFACES = '+JSON.stringify(surfaces)+';');
 try {vm.runInNewContext(script,{native,log:s=>logs.push(s),wait:()=>{if(++frame>(options.frames||50))throw Error('END');},Math,Number});}
 catch(e){if(e.message!=='END')throw e;}
 return {maxPresented,transfers,control,camera,replacements,logs,uploads};
}
const crossed=drive();
assert.ok(crossed.maxPresented>=4,'rider crosses the original qualified boundary');
assert.equal(crossed.transfers,1,'crossing does not remount');
assert.equal(crossed.control,true);assert.equal(crossed.camera,false);
console.log('PASS: asynchronous same-floor coverage crossing preserves one ride and dismount recovery');

for(const surfaces of [[patch(0)], [patch(0),patch(4,2)], [patch(0),patch(4,1,20)], [patch(0),patch(4,1,10.02)],
 [patch(0),{...patch(4),qualified:false}], [patch(0),patch(7)]]) {
 const stopped=drive({surfaces});
 assert.ok(stopped.maxPresented<=3,'unavailable, wrong-floor or unqualified neighbors do not extend coverage');
 assert.equal(stopped.replacements,0);
 assert.equal(stopped.control,true);assert.equal(stopped.camera,false);
}
console.log('PASS: missing, disjoint, unqualified and wrong-floor neighbors restore ordinary GTA');
for(const options of [{refuse:true},{neverReady:true}]) {
 const stopped=drive(options);
 assert.ok(stopped.maxPresented<=3);
 assert.ok(stopped.logs.includes('COMBINE_SKATE ride-stopped:coverage-replacement-unavailable'));
 assert.equal(stopped.control,true);assert.equal(stopped.camera,false);
}
console.log('PASS: failed or timed-out replacement restores controls and camera');

const retried=drive({retry:true});
assert.ok(retried.maxPresented>=4,'a newer native snapshot can be consumed before retrying replacement');
assert.equal(retried.transfers,1);assert.equal(retried.control,true);assert.equal(retried.camera,false);
console.log('PASS: native snapshot race retries within the same ride');

const delayed=drive({ackFrames:20});
assert.ok(delayed.logs.includes('COMBINE_SKATE ride-stopped:coverage-replacement-unavailable'),
 'replacement expires before it could resume beyond the native clock budget');
assert.equal(delayed.control,true);assert.equal(delayed.camera,false);
const nearBudget=drive({ackFrames:10});
assert.ok(nearBudget.maxPresented>=4);assert.equal(nearBudget.control,true);
const many=patch(4);many.triangles=Array.from({length:20},()=>many.triangles).flat();
assert.ok(drive({surfaces:[patch(0),many]}).maxPresented>=4,'bounded uploads span frames and preserve the ride');
console.log('PASS: multi-frame uploads and delayed acknowledgement respect native timing limits');

const overlap=drive({startX:2});
assert.equal(overlap.transfers,1,'mount from an overlap on the same verified floor');
assert.ok(overlap.maxPresented>=4);assert.equal(overlap.control,true);assert.equal(overlap.camera,false);
const ambiguous=drive({startX:2,surfaces:[patch(0),patch(4,2)]});
assert.equal(ambiguous.transfers,0,'matching separate layers remain ambiguous');
const inconsistent=drive({startX:2,surfaces:[patch(0),patch(4,1,10.02)]});
assert.equal(inconsistent.transfers,0,'same-layer disagreement is not resolved by arbitrary choice');
console.log('PASS: overlapping same-floor mount works; conflicting heights or layers refuse');

const three=[patch(0,1,10),patch(2,1,10.0009),patch(4,1,10.0018)];
for(const order of [[1,0,2],[0,1,2],[2,0,1]]) {
 assert.equal(drive({startX:2,surfaces:order.map(i=>three[i])}).transfers,0,
  'overlap agreement is independent of catalogue order');
}
console.log('PASS: multi-patch height disagreement refuses in every catalogue order');

const diverging=patch(4);
diverging.triangles=diverging.triangles.map(t=>t.map(v=>[v[0],v[1],10+0.08*(v[0]-2.25)]));
const freshMismatch=drive({surfaces:[patch(0),diverging],retry:true,retryShift:true});
assert.equal(freshMismatch.replacements,1,'fresh retry pose must requalify the pending floor before resubmission');
assert.ok(freshMismatch.logs.includes('COMBINE_SKATE ride-stopped:coverage-replacement-unavailable'));
assert.equal(freshMismatch.control,true);assert.equal(freshMismatch.camera,false);
console.log('PASS: snapshot retry revalidates support at the new pose');

const corridor={layer:1,qualified:true,evidence:'authored-large-region',center:[0,0],radius:20,triangles:[]};
for(let x=-30;x<30;x+=2) {
 corridor.triangles.push([[x,-2,10],[x+2,-2,10],[x+2,2,10]],[[x,-2,10],[x+2,2,10],[x,2,10]]);
}
const wall=[[2,-1,10],[2,1,10],[2,1,12]];
corridor.triangles.push(wall);
const local=drive({surfaces:[corridor],endAt:30,frames:160});
assert.ok(local.uploads[0].count<corridor.triangles.length,'mount uploads local collision instead of the entire qualified region');
assert.ok(local.uploads[0].vertices.some(v=>v[0]===2 && v[2]===12),'nearby wall collision is retained');
assert.ok(!local.uploads[0].vertices.some(v=>v[0]>=14),'distant collision stays outside the initial window');
assert.ok(local.replacements>=2,'local collision refreshes while riding within one qualified region');
assert.ok(local.maxPresented>=18 && local.maxPresented<=20,'ride traverses local windows but does not escape original qualification');
assert.equal(local.transfers,1,'local window refresh never remounts');
assert.ok(local.logs.includes('COMBINE_SKATE ride-stopped:outside-qualified-surface'));
assert.equal(local.control,true);assert.equal(local.camera,false);
console.log('PASS: local windows retain nearby obstacles, refresh one ride and enforce original qualification');

const malformed={...corridor,triangles:[...corridor.triangles,[[100,100,10],[101,100,10],[101,101,NaN]]]};
assert.equal(drive({surfaces:[malformed]}).transfers,0,'malformed distant geometry refuses complete region before local filtering');
const small={...patch(0),triangles:[[[ -6,-6,10],[6,-6,10],[6,6,10]],[[-6,-6,10],[6,6,10],[-6,6,10]]]};
const bounded=drive({surfaces:[small],endAt:10});
assert.ok(bounded.maxPresented<=3,'existing 3m qualification is retained even when decoded triangles extend farther');
assert.equal(bounded.replacements,0,'small qualified patches are not enlarged into local windows');
assert.equal(bounded.control,true);assert.equal(bounded.camera,false);
const edge=drive({surfaces:[corridor],startX:19,endAt:30});
assert.ok(edge.maxPresented>=19 && edge.maxPresented<=20,'player-centered window near region edge cannot extend original qualification');
assert.ok(edge.logs.includes('COMBINE_SKATE ride-stopped:outside-qualified-surface'));
assert.equal(edge.control,true);assert.equal(edge.camera,false);
console.log('PASS: malformed distant triangles refuse; small and edge-centered windows retain original region bounds');

const mesh={coverage:'mesh',layer:1,qualified:true,evidence:'authored-complete-mesh',triangles:corridor.triangles};
const meshRide=drive({surfaces:[mesh],endAt:40,frames:240});
assert.ok(meshRide.maxPresented>=27 && meshRide.maxPresented<=30,'explicit complete mesh follows geometric extent without region radius metadata');
assert.ok(meshRide.replacements>=4,'local streaming windows refresh without becoming outer ride boundary');
assert.equal(meshRide.transfers,1);assert.equal(meshRide.control,true);assert.equal(meshRide.camera,false);
assert.ok(meshRide.logs.includes('COMBINE_SKATE ride-stopped:outside-qualified-surface'));
console.log('PASS: explicitly qualified complete mesh rides beyond 3m until its actual geometric edge');

const meshWithOldRadius=drive({surfaces:[{...mesh,center:[0,0],radius:3}],endAt:10});
assert.equal(meshWithOldRadius.transfers,0,'mesh mode refuses ambiguous mixed full-mesh and legacy radius qualification');
assert.equal(meshWithOldRadius.control,true);assert.equal(meshWithOldRadius.camera,false);
const holeMesh={...mesh,triangles:mesh.triangles.filter(t=>t.every(v=>v[0]<=6)||t.every(v=>v[0]>=8))};
const holeRide=drive({surfaces:[holeMesh],endAt:12});
assert.ok(holeRide.maxPresented>=5 && holeRide.maxPresented<=6,'mesh bounding box cannot qualify an actual missing-floor hole');
assert.ok(holeRide.logs.includes('COMBINE_SKATE ride-stopped:outside-qualified-surface'));
assert.equal(holeRide.control,true);assert.equal(holeRide.camera,false);
for(const invalid of [
 {...mesh,qualified:false},
 {...mesh,coverage:'unknown',center:[0,0],radius:30},
 {...mesh,triangles:[...mesh.triangles,[[100,100,10],[101,100,10],[101,101,NaN]]]},
 {...mesh,triangles:[...mesh.triangles,[[100,100,10],[100,100,10],[100,100,10]]]},
 {...mesh,triangles:[...mesh.triangles,[[2000000,100,10],[2000001,100,10],[2000001,101,10]]]},
 {...mesh,triangles:Array.from({length:4097},()=>mesh.triangles[0])}
]) {
 const refused=drive({surfaces:[invalid]});
 assert.equal(refused.transfers,0,'unqualified, unknown or malformed complete meshes never take GTA control');
 assert.equal(refused.uploads.length,0,'complete mesh validation precedes local triangle upload');
}
console.log('PASS: mesh mode refuses mixed legacy radius, missing-floor holes and invalid complete geometry');

const narrowMesh={...mesh,triangles:mesh.triangles.filter(t=>!t.some(v=>v[2]!==10))
 .map(t=>t.map(v=>[v[0],v[1]/20,v[2]]))};
const narrowRide=drive({surfaces:[narrowMesh],endAt:12});
assert.ok(narrowRide.maxPresented>=11,'narrow complete mesh keeps refreshing local windows despite small lateral extent');
assert.ok(narrowRide.replacements>=2);assert.equal(narrowRide.transfers,1);
assert.equal(narrowRide.control,true);assert.equal(narrowRide.camera,false);
console.log('PASS: narrow complete mesh streaming follows longitudinal motion');

const grazingRegion={...corridor,center:[0,199.9],radius:200};
const grazingRide=drive({surfaces:[grazingRegion],endAt:6});
assert.ok(grazingRide.maxPresented>=5.5,'legacy region near radial edge refreshes its local window while original ground remains qualified');
assert.ok(grazingRide.replacements>=1);assert.equal(grazingRide.transfers,1);
assert.equal(grazingRide.control,true);assert.equal(grazingRide.camera,false);
const grazingBoundary=drive({surfaces:[grazingRegion],endAt:10});
assert.ok(grazingBoundary.maxPresented>=5.5 && grazingBoundary.maxPresented<=6.32,'local refresh retains the original radial boundary');
assert.ok(grazingBoundary.logs.includes('COMBINE_SKATE ride-stopped:outside-qualified-surface'));
assert.equal(grazingBoundary.control,true);assert.equal(grazingBoundary.camera,false);
console.log('PASS: local streaming near legacy radial edge preserves refresh and true qualification boundary');
