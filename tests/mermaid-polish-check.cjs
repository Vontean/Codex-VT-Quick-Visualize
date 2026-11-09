// 使用正式 Visualize sandbox；完整等待 qvReady，再校验最终状态及真实几何。
const {chromium}=require('playwright');
const fs=require('node:fs'),assert=require('node:assert/strict'),path=require('node:path');
const directory=path.resolve(process.argv[2]||'work/mermaid-polish'),url=process.env.QV_TEST_URL||'http://127.0.0.1:8796';
const cases=JSON.parse(fs.readFileSync(path.join(directory,'cases.json')));
(async()=>{
 const browser=await chromium.launch({headless:true});const results=[];
 try{
  const context=await browser.newContext({ignoreHTTPSErrors:true});
  for(const theme of ['light','dark']){
   const page=await context.newPage();await page.emulateMedia({colorScheme:theme});
   let errors=[];page.on('pageerror',e=>errors.push(String(e)));
   for(const c of cases){
    errors=[];await page.setViewportSize({width:768,height:1000});
    await page.goto(`${url}/${c.id}-${c.scene}-preview.html`);
    await page.waitForSelector('iframe');const frame=page.frames().find(f=>f.parentFrame());
    try{
     await frame.waitForSelector('.qv-mermaid',{timeout:30000});
     await frame.evaluate(async()=>{const root=document.querySelector('.qv-mermaid');if(!root.qvReady)throw Error('missing rendering Promise');await root.qvReady;});
     await frame.waitForFunction(()=>document.querySelector('.diagram-scroll')?.getAttribute('aria-busy')==='false'||document.querySelector('.qv-mermaid').dataset.preset==='radar-chart'||document.querySelector('.qv-mermaid').dataset.renderer==='qv-pie');
     const measure=()=>frame.evaluate(()=>{
      const root=document.querySelector('.qv-mermaid'),scene=root.querySelector('.scene'),v=root.querySelector('.diagram-scroll'),h=root.querySelector('h3');
      const rr=root.getBoundingClientRect(),r=scene?.getBoundingClientRect(),vr=v?.getBoundingClientRect();
      const labels=[...root.querySelectorAll('.radar-axis-label')].map(e=>e.getBoundingClientRect());let collisions=0;for(let i=0;i<labels.length;i++)for(let j=i+1;j<labels.length;j++){const a=labels[i],b=labels[j];if(a.left<b.right-.5&&b.left<a.right-.5&&a.top<b.bottom-.5&&b.top<a.bottom-.5)collisions++;}
      const nodes=[...root.querySelectorAll('button.node')].map(e=>e.getBoundingClientRect());let overlaps=0;for(let i=0;i<nodes.length;i++)for(let j=i+1;j<nodes.length;j++){const a=nodes[i],b=nodes[j];if(a.left<b.right-1&&b.left<a.right-1&&a.top<b.bottom-1&&b.top<a.bottom-1)overlaps++;}
      return {...root.dataset,sceneWidth:scene?.offsetWidth,sceneHeight:scene?.offsetHeight,center:r&&vr?r.left+r.width/2-vr.left-vr.width/2:null,left:r&&vr?r.left-vr.left:null,rootOverflow:root.scrollWidth-root.clientWidth,scrollWidth:v?.scrollWidth,viewportWidth:v?.clientWidth,notice:root.querySelector('.qv-notice')?.textContent||'',title:h?.textContent,titleVisible:h?!!h.offsetHeight:false,titleCenter:h?h.getBoundingClientRect().left+h.getBoundingClientRect().width/2-rr.left-rr.width/2:null,collisions,overlaps,nodeCount:nodes.length,viewport:!!root.__qvViewport};
     });
     const wide=await measure();assert.equal(wide.state,c.id==='fallback'?'native':'enhanced',wide.notice);assert.equal(wide.collisions,0,'radar label overlaps');if(c.id==='architecture')assert.equal(wide.overlaps,0,'architecture overlaps');
     if(c.id.includes('title')){assert.ok(wide.titleVisible,'title visible');assert.ok(Math.abs(wide.titleCenter)<1,'title centered');}
     // 捕获真实 WA 调用；保留原型原样，触发既有可见性恢复路径。
     const motion=await frame.evaluate(async()=>{window.__qvMotion=[];const original=animateMermaidEntry;animateMermaidEntry=(...args)=>{const a=original(...args);window.__qvMotion.push(a);return a;};Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'));delete document.hidden;document.dispatchEvent(new Event('visibilitychange'));await new Promise(r=>setTimeout(r,180));return window.__qvMotion.map(a=>{const t=a.effect.getTiming();return {end:Number(t.delay)+Number(t.duration),ease:t.easing}});});
     assert.ok(motion.every(t=>t.end<=1200.000001),'motion budget');assert.ok(motion.every(t=>t.ease==='cubic-bezier(0.23, 1, 0.32, 1)'),'motion easing');
     await page.setViewportSize({width:352,height:1000});await page.waitForTimeout(250);const narrow=await measure();assert.ok(narrow.rootOverflow<=2,'root must not overflow');
     for(const result of [wide,narrow])if(['quadrant','er','class'].includes(c.id)&&result.sceneWidth<=result.viewportWidth)assert.ok(Math.abs(result.center)<1.1,'scene centered');
     await page.setViewportSize({width:768,height:1000});await page.waitForTimeout(250);const restored=await measure();if(c.id==='journey')assert.equal(restored.sceneWidth,wide.sceneWidth,'Journey column width restored');
     if(c.id==='state-nested'){
      await frame.locator('.state-group button').first().click();await frame.waitForFunction(()=>document.querySelector('.scope-nav')?.hidden===false&&document.querySelector('.diagram-scroll').getAttribute('aria-busy')==='false');
      await frame.locator('.scope-nav button').first().click();await frame.waitForFunction(()=>document.querySelector('.scope-nav').hidden&&document.querySelector('.diagram-scroll').getAttribute('aria-busy')==='false');
     }
     if(c.id==='git')assert.equal(wide.gitLayout,c.scene==='normal'?'lanes':'rows');
     if(c.id==='architecture'&&c.scene==='stress')assert.equal(wide.layoutMode,'arch-elk');
     assert.equal(errors.length,0,errors.join('\n'));
     results.push({id:c.id,scene:c.scene,theme,wide,narrow,restored,motionCount:motion.length,motionMax:Math.max(0,...motion.map(t=>t.end)),errors});
     console.log('PASS',theme,c.id,c.scene);
    }catch(error){results.push({id:c.id,scene:c.scene,theme,error:String(error),errors});console.log('FAIL',theme,c.id,c.scene,String(error));}
    fs.writeFileSync(path.join(directory,'browser-results.json'),JSON.stringify(results,null,2));
   }await page.close();
  }
 }finally{await browser.close();}
 const failed=results.filter(r=>r.error);console.log(`${results.length-failed.length}/${results.length} passed`);if(failed.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
