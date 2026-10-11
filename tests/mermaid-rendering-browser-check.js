async page => {
  const results=[];
  const check=(value,message)=>{if(!value)throw Error(message);};
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.route('https://cdn.jsdelivr.net/npm/elkjs@0.10.0/lib/elk.bundled.js',route=>route.abort());
  for(const scheme of ['light','dark']) {
    await page.emulateMedia({colorScheme:scheme});
    for(const name of ['qv-full-flow','qv-full-architecture']) {
      await page.setViewportSize({width:1440,height:850});
      await page.goto('http://localhost:8793/'+name+'-fixed-preview.html',{waitUntil:'domcontentloaded'});
      await page.waitForSelector('iframe');const f=page.frames()[1];
      await f.waitForSelector('[data-state=enhanced]',{timeout:60000});
      await f.evaluate(()=>window.dispatchEvent(new CustomEvent('openai:set_globals',{detail:{globals:{displayMode:'fullscreen',maxHeight:780}}})));
      await page.waitForTimeout(200);
      const actual=await f.evaluate(()=>{
        const r=document.querySelector('.qv-mermaid'),v=r.querySelector('.diagram-scroll').getBoundingClientRect(),n=r.querySelector('[data-node=store]'),paths=n?.querySelectorAll('.node-outline path');
        const probe=document.createElement('div');probe.style.background='var(--background)';r.append(probe);const theme=getComputedStyle(probe).backgroundColor;probe.remove();return {nodes:r.querySelectorAll('button.node').length,edges:r.querySelectorAll('.wire').length,fit:[...r.querySelectorAll('button.node,.qv-group,.edge-label')].every(n=>{const b=n.getBoundingClientRect();return b.left>=v.left-1&&b.right<=v.right+1&&b.top>=v.top-1&&b.bottom<=v.bottom+1}),background:n?getComputedStyle(n).backgroundColor:null,body:paths?.[0]?getComputedStyle(paths[0]).fill:null,arc:paths?.[1]?getComputedStyle(paths[1]).fill:null,theme};
      });
      check(actual.fit,name+': graph clipped');
      check(actual.nodes===(name==='qv-full-flow'?10:14)&&actual.edges===(name==='qv-full-flow'?11:17),name+': graph changed');
      if(name==='qv-full-flow')check(actual.background==='rgba(0, 0, 0, 0)'&&actual.arc==='none'&&actual.body===actual.theme,'cylinder fill: '+JSON.stringify(actual));
      await page.screenshot({path:'/Users/mac/.codex/visualizations/2026/10/07/01a1159e-cd3d-7ea1-a17e-250507d99939/mermaid-fit/'+name+'-fixed-'+scheme+'.png',fullPage:true});
      results.push({name,scheme,...actual});
    }
  }
  await page.route('https://unpkg.com/elkjs@0.10.0/lib/elk.bundled.js',route=>route.abort());
  await page.goto('http://localhost:8793/qv-full-architecture-fixed-preview.html',{waitUntil:'domcontentloaded'});
  await page.waitForSelector('iframe');const failed=page.frames()[1];
  await failed.waitForSelector('[data-state=error]',{timeout:60000});
  check((await failed.locator('.qv-notice').innerText()).includes('布局引擎加载失败'),'missing loading error');
  check(await failed.locator('.diagram-scroll[aria-busy=false]').count()===1,'loading field did not finish');
  results.push({bothOriginsUnavailable:'visible error, loading finished'});
  return results;
}
