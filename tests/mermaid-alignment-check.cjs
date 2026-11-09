const {chromium}=require('playwright'),{spawn}=require('node:child_process');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const dir=path.resolve(process.argv[2]||'work/mermaid-alignment'),audit=process.argv.includes('--audit'),port=8797;
(async()=>{
 const server=spawn('python3',['-m','http.server',String(port),'--bind','127.0.0.1','--directory',dir],{stdio:'ignore'});let browser;const results=[];
 try{
  for(let i=0;i<40;i++){try{await fetch(`http://127.0.0.1:${port}/cases.json`);break;}catch{await new Promise(r=>setTimeout(r,50));}}
  browser=await chromium.launch();const p=await browser.newPage({ignoreHTTPSErrors:true});
  for(const theme of ['light','dark'])for(const c of JSON.parse(fs.readFileSync(path.join(dir,'cases.json')))){
   await p.emulateMedia({colorScheme:theme,reducedMotion:'reduce'});await p.setViewportSize({width:1440,height:1000});await p.goto(`http://127.0.0.1:${port}/${c.id}-preview.html`);
   const f=p.frames().find(f=>f.parentFrame());await f.waitForSelector('.qv-loading-region[aria-busy="false"]');if(!c.kind)await f.evaluate(()=>document.querySelector('.qv-mermaid').qvReady);await p.waitForTimeout(60);
   async function measure(){return f.evaluate(()=>{
    const root=document.querySelector('.qv-mermaid')||document.querySelector('.qv-loading-content > [role=figure]'),scene=root.querySelector('.scene'),frame=root.querySelector('.journey-frame'),v=root.querySelector('.diagram-scroll'),canvas=frame||scene,title=root.querySelector('h3'),r=(frame?root:v||root).getBoundingClientRect(),s=canvas?.getBoundingClientRect(),t=title.getBoundingClientRect();
    const range=document.createRange();range.selectNodeContents(title);const text=range.getBoundingClientRect(),rootRect=root.getBoundingClientRect();
    return{state:root.dataset.state,renderer:root.dataset.renderer,width:s?.width,available:r.width,center:s?s.left+s.width/2-r.left-r.width/2:null,left:scene&&v?scene.getBoundingClientRect().left-v.getBoundingClientRect().left:null,steps:scene?.offsetWidth,scrollLeft:v?.scrollLeft||0,scrollMax:v? v.scrollWidth-v.clientWidth:0,titleAlign:getComputedStyle(title).textAlign,titleWidth:t.width,titleCenter:text.left+text.width/2-rootRect.left-rootRect.width/2,titleWrapped:title.scrollHeight>parseFloat(getComputedStyle(title).lineHeight)*1.5,titleVisible:!!title.offsetHeight,rootOverflow:root.scrollWidth-root.clientWidth};
   });}
   const wide=await measure();await p.setViewportSize({width:352,height:1000});await p.waitForTimeout(90);const narrow=await measure();
   await p.setViewportSize({width:1440,height:1000});await p.waitForTimeout(90);const restored=await measure();
   let error;try{
    if(!c.kind)assert.equal(wide.state,c.id==='fallback'?'native':'enhanced');
    if(c.id!=='fallback')for(const value of [wide,narrow,restored]){
     if(value.width<=value.available+.5)assert.ok(Math.abs(value.center)<1.1,'canvas not centered '+value.center);
     else assert.ok(value.left+value.scrollLeft>=-1,'left edge clipped');
     assert.equal(value.titleAlign,value.titleWrapped?'left':'center','title alignment');
     if(!value.titleWrapped)assert.ok(Math.abs(value.titleCenter)<1.1,'title text not centered '+value.titleCenter);
     assert.ok(value.rootOverflow<=2,'root overflow');
    }
    if(c.id==='journey')assert.equal(restored.steps,wide.steps,'Journey columns restore');
   }catch(e){error=e.message;}
   results.push({id:c.id,theme,wide,narrow,restored,...error?{error}:{}});console.log(error?'FAIL':'PASS',theme,c.id,error||'');
   if(!audit&&['git','timeline','block','state','long-title-sankey'].includes(c.id)&&theme==='light')await p.screenshot({path:path.join(dir,c.id+'.png')});
  }
  fs.writeFileSync(path.join(dir,audit?'alignment-before.json':'alignment-after.json'),JSON.stringify(results,null,2));
  console.log('Alignment:',results.length-results.filter(r=>r.error).length+'/'+results.length);if(!audit&&results.some(r=>r.error))process.exitCode=1;
 }finally{await browser?.close();server.kill('SIGTERM');}
})().catch(e=>{console.error(e);process.exitCode=1});
