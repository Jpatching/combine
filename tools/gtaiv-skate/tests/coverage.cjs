// Exercise the riding script across the GTA/Session native boundary.
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
function patch(center,layer=1,height=10) {
 return {layer,qualified:true,evidence:'authored-corridor',center:[center,0],radius:3,
  triangles:[[[center-3,-3,height],[center+3,-3,height],[center+3,3,height]],
             [[center-3,-3,height],[center+3,3,height],[center-3,3,height]]]};
}
function drive(options={}) {
 let frame=0,x=0,camera=false,control=true,transfers=0,pending=0,replacements=0,maxPresented=0;
 const logs=[];
 const native=(name,...args)=>{
  switch(name){
   case 'COMBINE_SKATE_READY':case 'COMBINE_SKATE_INPUT_MODE':return 1;
   case 'COMBINE_SKATE_INPUT_TOGGLE':return -1;
   case 'COMBINE_SKATE_TOGGLE':return frame===1 || x>=4;
   case 'GET_PLAYER_ID':case 'CONVERT_INT_TO_PLAYERINDEX':return 0;
   case 'GET_PLAYER_CHAR':return 7;
   case 'DOES_CHAR_EXIST':case 'IS_PLAYER_PLAYING':case 'IS_CHAR_ON_FOOT':return true;
   case 'IS_PAUSE_MENU_ACTIVE':case 'HAS_CUTSCENE_LOADED':return false;
   case 'IS_PLAYER_CONTROL_ON':return control;
   case 'GET_CHAR_COORDINATES':return {x:0,y:0,z:11};
   case 'GET_GROUND_Z_FOR_3D_COORD':return 10;
   case 'GET_CHAR_HEIGHT_ABOVE_GROUND':return 1;
   case 'GET_CHAR_HEADING':return 0;
   case 'COMBINE_SKATE_SURFACE_BEGIN':case 'COMBINE_SKATE_SURFACE_VERTEX':return 1;
   case 'COMBINE_SKATE_MOUNT_SURFACE':return 1;
   case 'COMBINE_SKATE_VALUE':return [x,0,10,0][args[0]];
   case 'COMBINE_SKATE_SURFACE_REPLACE':replacements++;if(options.refuse)return 0;if(options.retry && replacements===1)return 3;pending=2;return 2;
   case 'COMBINE_SKATE_POLL':if(options.neverReady)return 2;return --pending>0?2:1;
   case 'COMBINE_SKATE_TICK_SURFACE':assert.equal(pending,0,'do not tick unacknowledged collision');x+=0.75;return 1;
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
 try {vm.runInNewContext(script,{native,log:s=>logs.push(s),wait:()=>{if(++frame>50)throw Error('END');},Math,Number});}
 catch(e){if(e.message!=='END')throw e;}
 return {maxPresented,transfers,control,camera,replacements,logs};
}
const crossed=drive();
assert.ok(crossed.maxPresented>=4,'rider crosses the original qualified boundary');
assert.equal(crossed.transfers,1,'crossing does not remount');
assert.equal(crossed.control,true);assert.equal(crossed.camera,false);
console.log('PASS: asynchronous same-floor coverage crossing preserves one ride and dismount recovery');

for(const surfaces of [[patch(0)], [patch(0),patch(4,2)], [patch(0),patch(4,1,20)],
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
