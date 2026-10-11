async page => {
 const results=[];
 // ResizeObserver 通知循环通过 window.error 报告，不能只收集 pageerror。
 await page.addInitScript(()=>{window.runtimeErrors=[];window.addEventListener('error',e=>runtimeErrors.push(e.message));});
 for(const theme of ['light','dark'])for(const name of ['normal','stress','single']){
  await page.emulateMedia({colorScheme:theme,reducedMotion:'reduce'});
  await page.setViewportSize({width:736,height:900});
  await page.goto(`http://127.0.0.1:8794/journey-${name}-preview.html`);
  const frame=page.frames()[1];await frame.waitForSelector('[data-state=enhanced]',{timeout:60000});
  for(const mode of ['inline','fullscreen','inline']){
   await frame.evaluate(mode=>window.dispatchEvent(new CustomEvent('openai:set_globals',{detail:{globals:{displayMode:mode,maxHeight:750}}})),mode);
   for(const width of [320,360,400,480,600,736,640,500,380,320]){await page.setViewportSize({width,height:900});await page.waitForTimeout(60);}
  }
  await page.waitForTimeout(200);
  const result=await frame.evaluate(()=>{const r=document.querySelector('.qv-mermaid');return {errors:runtimeErrors,steps:r.querySelectorAll('.journey-step').length,textOverflow:[...r.querySelectorAll('.journey-step,.journey-actor')].some(n=>n.scrollHeight>n.clientHeight+1||n.scrollWidth>n.clientWidth+1),rootOverflow:r.scrollWidth>r.clientWidth+1};});
  if(result.errors.length||result.steps!==({normal:7,stress:25,single:1}[name])||result.textOverflow||result.rootOverflow)throw Error(JSON.stringify({theme,name,...result}));
  results.push({theme,name,...result});
 }
 return results;
}
