// Coverage window module against authored worlds: no native calls, no game.
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
// The module lives in combine_skate.js; its top-level declarations are the test seam.
const context={native:()=>undefined,log:()=>{},wait:()=>{throw Error('END');},Math,Number};
try {vm.runInNewContext(fs.readFileSync('tools/gtaiv-skate/combine_skate.js','utf8'),context);}
catch(e){if(e.message!=='END')throw e;}
const {coverageWindow,surfaceHeight,surfaceObservation}=context;
assert.equal(typeof coverageWindow,'function','combine_skate.js declares the Coverage window module');

const rider=[100,200,11];
function sample(world) {
 const queries=[];
 const result=coverageWindow((x,y,z)=>{queries.push([x,y,z]);return world(x,y);},...rider);
 return {result,queries};
}
// Interpolation error of a window against its world, sampled densely inside the window.
function maxError(world,window) {
 let worst=0;
 for(let i=0;i<=64;i++)for(let j=0;j<=64;j++) {
  const x=rider[0]-4+i*0.125,y=rider[1]-4+j*0.125,height=surfaceHeight(window,x,y);
  assert.notEqual(height,null,`window covers ${x},${y}`);
  worst=Math.max(worst,Math.abs(height-world(x,y)));
 }
 return worst;
}

const flat=()=>10, slope=x=>10+(x-100)*0.1, curb=x=>x>=101?10.25:10;
for(const [name,world] of [['flat',flat],['slope',slope],['curb below threshold',curb]]) {
 const {result,queries}=sample(world);
 assert.equal(result.gap,undefined,name+' gives triangles');
 assert.equal(queries.length,25,'5x5 grid');
 assert.ok(queries.every(q=>q[2]===rider[2]+2),'query from rider z + 2');
 assert.deepEqual([...new Set(queries.map(q=>q[0]))].sort((a,b)=>a-b),[96,98,100,102,104],'2 m spacing, +/-4 m');
 assert.equal(result.triangles.length,32,'2 triangles per grid cell');
 assert.equal(result.layer,1);
 assert.ok(result.triangles.every(t=>t.every(v=>v.every(Number.isFinite))));
 // Every vertex is a sample from the world, never a flattened copy of the rider's ground.
 assert.ok(result.triangles.every(t=>t.every(v=>v[2]===world(v[0],v[1]))));
 if(world!==curb)assert.ok(maxError(world,result)<1e-9,name+' is reproduced exactly');
 assert.equal(surfaceHeight(result,104.01,200),null,'the window ends at its edge');
}
console.log('PASS: flat, slope and curb-below-threshold worlds give 32 sampled triangles');

for(const [name,world,reason] of [
 ['wall above threshold',x=>x>=101?10.31:10,'wall'],
 ['non-finite',(x,y)=>x===104&&y===204?NaN:10,'non-finite'],
 ['near-zero (unloaded)',(x,y)=>y<=196?0:10,'near-zero'],
 ['missing sample',(x)=>x===96?undefined:10,'non-finite']]) {
 const {result}=sample(world);
 assert.equal(result.triangles,undefined,name+' gives no triangles');
 assert.equal(result.gap,reason,name+' states its reason');
}
assert.equal(sample(x=>x>=101?10.29:10).result.gap,undefined,'a step just under the wall threshold is rideable');
console.log('PASS: wall, non-finite and near-zero worlds give a coverage gap with its reason');

// Floor agreement (ADR 0004): host ground at the rider must lie on the floor the window
// describes, within the wall threshold. Rolling ground bends between samples while every
// sample step stays below the wall threshold, so only curvature (tightest radius
// R = 1/(amplitude*k^2)) drives the interpolation error.
function agreesEverywhere(world,window) {
 for(let i=0;i<=64;i++)for(let j=0;j<=64;j++) {
  const x=rider[0]-4+i*0.125,y=rider[1]-4+j*0.125;
  if(!surfaceObservation(window,x,y,world(x,y)))return false;
 }
 return true;
}
const report=[];
for(const [wavelength,amplitude] of [[16,0.25],[8,0.1],[8,0.2],[6,0.15]]) {
 const k=2*Math.PI/wavelength,radius=1/(amplitude*k*k);
 const rolling=(x,y)=>10+amplitude*Math.sin(k*(x-100)+0.5)*Math.cos(k*(y-200)+0.3);
 const {result}=sample(rolling);
 assert.equal(result.gap,undefined,`rolling R=${radius.toFixed(0)} m samples without a wall`);
 assert.ok(agreesEverywhere(rolling,result),`rolling R=${radius.toFixed(1)} m keeps floor agreement`);
 report.push(`R=${radius.toFixed(1)}m ${maxError(rolling,result).toFixed(3)}m`);
}
const curbWindow=sample(curb).result;
assert.ok(agreesEverywhere(curb,curbWindow),'a 0.25 m curb between samples keeps floor agreement');
report.push(`curb 0.25m step ${maxError(curb,curbWindow).toFixed(3)}m`);
// A planter between two samples: every sample is flat, but host ground under it is another floor.
const planter=(x,y)=>Math.abs(x-101)<0.4&&Math.abs(y-201)<0.4?10.5:10;
const flatWindow=sample(planter).result;
assert.equal(flatWindow.gap,undefined,'the planter falls between samples');
assert.equal(surfaceObservation(flatWindow,101,201,planter(101,201)),false,'riding onto the planter loses floor agreement');
assert.equal(surfaceObservation(flatWindow,101,201,10.29),true,'a rise just under the wall threshold keeps floor agreement');
console.log('REPORT: interpolation error (informational): '+report.join('; '));
console.log('PASS: curved ground and curbs keep floor agreement; a planter between samples loses it');
