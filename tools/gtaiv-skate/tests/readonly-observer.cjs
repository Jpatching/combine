const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
function observe(mode,unavailablePose=false) {
 let frame=0,time=0;const calls=[],logs=[];
 const allowed=new Set(['COMBINE_SKATE_EVAL_TIME','COMBINE_SKATE_EVAL_OWNER','COMBINE_SKATE_VALUE','GET_CHAR_COORDINATES','IS_PAUSE_MENU_ACTIVE','HAS_CUTSCENE_LOADED','HAS_CUTSCENE_FINISHED','GET_GROUND_Z_FOR_3D_COORD','DOES_CAM_EXIST','COMBINE_SKATE_READY','IS_PLAYER_CONTROL_ON']);
 const surfaces=[{qualified:true,center:[100,200],radius:3,triangles:[[[95,195,10],[105,195,10],[105,205,10]],[[95,195,10],[105,205,10],[95,205,10]]]}];
 const source=fs.readFileSync('tools/gtaiv-skate/tests/live-readonly-observer.js','utf8').replace('MODE="lifecycle"','MODE='+JSON.stringify(mode)).replace('SURFACES=[]','SURFACES='+JSON.stringify(surfaces));
 const native=(name,...args)=>{calls.push(name);assert.ok(allowed.has(name),'observer must never call mutating native '+name);
  switch(name){
   case 'COMBINE_SKATE_EVAL_TIME':return time;
   case 'COMBINE_SKATE_EVAL_OWNER':return frame>=3?{player:-1,ped:-1,camera:-1}:{player:0,ped:7,camera:99};
   case 'COMBINE_SKATE_VALUE':return unavailablePose?0:[frame===1?100:104,200,11,0][args[0]];
   case 'GET_CHAR_COORDINATES':return {x:frame===1?100:104,y:200,z:12};
   case 'GET_GROUND_Z_FOR_3D_COORD':return 10;
   case 'DOES_CAM_EXIST':return frame<3;
   case 'COMBINE_SKATE_READY':case 'IS_PLAYER_CONTROL_ON':return true;
   default:return false;
  }
 };
 vm.runInNewContext(source,{native,log:s=>logs.push(s),wait:()=>{frame++;time+=50001;if(frame>5)throw Error('unbounded observer');},Number,Math,JSON});
 return {calls,logs};
}
const lifecycle=observe('lifecycle');
assert.ok(lifecycle.logs.some(s=>s.includes(' started ')));assert.ok(lifecycle.logs.some(s=>s.includes(' expired ')));
assert.ok(lifecycle.calls.every(s=>s==='COMBINE_SKATE_EVAL_TIME'));
const diagnostic=observe('diagnostic');
const ended=diagnostic.logs.find(s=>s.includes(' owner-ended '));assert.ok(ended);
const flags=JSON.parse(ended.slice(ended.indexOf(' owner-ended ')+13));
assert.equal(flags.last.pose_all_zero,false);
assert.equal(flags.last.pose_matches_char_xy,true);
assert.equal(flags.last.pose_observation_verified,true);
assert.equal(flags.last.qualified_support_present,false);assert.equal(flags.last.height_within_support,false);
assert.equal(flags.normal_control,true);assert.equal(flags.owned_camera_absent,true);
for(const s of diagnostic.logs){assert.ok(!/"(x|y|z|heading|player|ped|camera|triangles|center)"\s*:/.test(s),'only fixed flags may be logged');}


const unavailable=observe('diagnostic',true);
const invalidLine=unavailable.logs.find(s=>s.includes(' owner-started '));
const invalid=JSON.parse(invalidLine.slice(invalidLine.indexOf(' owner-started ')+15));
assert.equal(invalid.pose_all_zero,true);
assert.equal(invalid.pose_matches_char_xy,false);
assert.equal(invalid.pose_observation_verified,false);
assert.equal(invalid.qualified_support_present,null,'unverified getter must not report missing support');
assert.equal(invalid.height_within_support,null);
assert.equal(invalid.unique_ground_match,null);
assert.ok(!unavailable.calls.includes('GET_GROUND_Z_FOR_3D_COORD'),'unverified pose must not issue coordinate-derived query');

console.log('PASS: bounded read-only observer distinguishes valid unsupported pose from unavailable getters without exposing pose or identity');
