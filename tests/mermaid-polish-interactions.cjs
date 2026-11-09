const {chromium}=require('playwright');const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const dir=path.resolve(process.argv[2]||'work/mermaid-polish'),base=process.env.QV_TEST_URL||'http://127.0.0.1:8796';
(async()=>{const b=await chromium.launch();const results=[];try{
const p=await b.newPage({viewport:{width:1056,height:1000},ignoreHTTPSErrors:true});
async function open(slug,theme='light',reducedMotion='no-preference'){
 await p.emulateMedia({colorScheme:theme,reducedMotion});await p.goto(`${base}/${slug}-preview.html`);const f=p.frames().find(f=>f.parentFrame());await f.waitForSelector('.qv-mermaid');await f.evaluate(()=>document.querySelector('.qv-mermaid').qvReady);assert.equal(await f.locator('.qv-mermaid').getAttribute('data-state'),slug.startsWith('fallback')?'native':'enhanced');return f;
}
for(const theme of ['light','dark']){
 for(const slug of ['radar-generic-title-normal','radar-preset-title-normal']){
  const f=await open(slug,theme);await p.waitForTimeout(1100);
  const selector=slug.includes('generic')?'.radar-axis-label':'.dimension-key';
  const tips=slug.includes('generic')?'.radar-detail':'.quick-radar-tooltip';
  for(const index of [0,2]){
   const trigger=f.locator(selector).nth(index);await trigger.hover();await f.locator(tips).waitFor({state:'visible'});
   const detail=await f.evaluate(({selector,tips,index})=>{const t=document.querySelectorAll(selector)[index],tip=document.querySelector(tips),a=t.getBoundingClientRect(),r=tip.getBoundingClientRect(),x=a.x+a.width/2,y=a.y+a.height/2,css=getComputedStyle(tip),title=getComputedStyle(tip.querySelector('.radar-detail-title,.quick-radar-tooltip-dimension'));return{distance:Math.hypot(Math.max(r.left-x,0,x-r.right),Math.max(r.top-y,0,y-r.bottom)),pointerCovered:x>r.left&&x<r.right&&y>r.top&&y<r.bottom,background:css.backgroundColor,radius:css.borderRadius,padding:css.padding,font:css.fontSize,line:css.lineHeight,titleWeight:title.fontWeight,offsetParent:tip.offsetParent.className};},{selector,tips,index});
   assert.ok(detail.distance<=48.1,'near radar bubble '+JSON.stringify(detail));assert.ok(!detail.pointerCovered,'must not cover pointer');assert.equal(detail.radius,'12px');assert.equal(detail.padding,'12px 14px');assert.equal(detail.font,'12px');assert.equal(detail.line,'18px');assert.equal(detail.titleWeight,'500');
   await trigger.focus();await f.locator(tips).waitFor({state:'visible'});results.push({theme,slug,index,detail});
  }
  await p.waitForTimeout(180);await p.screenshot({path:path.join(dir,`${theme}-${slug}-bubble.png`)});
 }
 // 原有 mode 事件桥：完整图适配及返回，fallback 不接入。
 for(const slug of ['er-stress','class-stress','journey-normal','quadrant-stress','flow-stress','fallback-normal']){
  const f=await open(slug,theme);await p.waitForTimeout(100);
  const before=await f.evaluate(()=>{const v=document.querySelector('.diagram-scroll');v.scrollLeft=80;v.dispatchEvent(new Event('pointerdown'));return{scroll:v.scrollLeft,style:document.querySelector('.scene').getAttribute('style')}});
  await f.evaluate(()=>window.dispatchEvent(new CustomEvent('openai:set_globals',{detail:{globals:{displayMode:'fullscreen',maxHeight:760}}})));await p.waitForTimeout(150);
  const expanded=await f.locator('.qv-mermaid').evaluate(r=>({...r.dataset,style:r.querySelector('.scene').getAttribute('style'),running:r.getAnimations({subtree:true}).filter(a=>a.playState==='running'&&a.constructor.name==='Animation').length}));
  if(slug.startsWith('fallback')){assert.equal(expanded.style,before.style);assert.equal(expanded.viewportScale,undefined);}else{assert.equal(expanded.displayMode,'fullscreen');assert.ok(Number(expanded.viewportScale)<=1);assert.equal(expanded.running,0,slug+' entry animation must stop');}
  await f.evaluate(()=>window.dispatchEvent(new CustomEvent('openai:set_globals',{detail:{globals:{displayMode:'inline',maxHeight:1000}}})));await p.waitForTimeout(100);
  const after=await f.locator('.diagram-scroll').evaluate(v=>v.scrollLeft);assert.ok(Math.abs(after-before.scroll)<1);results.push({theme,slug,before,expanded,returnedScroll:after});
 }
 const f=await open('flow-normal',theme,'reduce');await p.waitForTimeout(200);assert.equal(await f.locator('.qv-mermaid').evaluate(r=>r.getAnimations({subtree:true}).filter(a=>a.playState==='running').length),0);results.push({theme,reducedMotion:true});
}
fs.writeFileSync(path.join(dir,'interaction-results.json'),JSON.stringify(results,null,2));console.log('PASS interactions',results.length);
}finally{await b.close();}})().catch(e=>{console.error(e);process.exitCode=1});
