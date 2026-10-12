async page => {
  const results=[];
  const check=(value,message)=>{if(!value)throw Error(message);};
  await page.emulateMedia({reducedMotion:'reduce'});
  for(const name of ['simple','complex','topology','architecture','navigation','shapes-arrows','groups-directions','architecture-ports','semantics','rich-label','fallback','gantt','classes','mindmap']) {
    await page.setViewportSize({width:736,height:850});
    await page.goto('http://localhost:8793/'+name+'-preview.html');
    const f=page.frames()[1];
    await f.waitForSelector('.qv-mermaid:not([data-state=loading])',{timeout:45000});
    await f.waitForSelector('[aria-busy=false]');
    const state=await f.locator('.qv-mermaid').getAttribute('data-state');
    check(state!=='error',name+': '+await f.locator('.qv-notice').innerText());
    if(state==='native') {
      const before=await f.evaluate(()=>({scene:document.querySelector('.scene').getAttribute('style'),svg:document.querySelector('.scene>svg').getAttribute('style'),viewport:document.querySelector('.diagram-scroll').getAttribute('style')}));
      await f.evaluate(()=>window.dispatchEvent(new CustomEvent('openai:set_globals',{detail:{globals:{displayMode:'fullscreen',maxHeight:650}}})));
      await page.waitForTimeout(120);
      const after=await f.evaluate(()=>({scene:document.querySelector('.scene').getAttribute('style'),svg:document.querySelector('.scene>svg').getAttribute('style'),viewport:document.querySelector('.diagram-scroll').getAttribute('style')}));
      check(JSON.stringify(before)===JSON.stringify(after),name+': fallback presentation changed');
      results.push({name,state,fallbackUnchanged:true});
      continue;
    }
    await f.evaluate(()=>{document.querySelector('.diagram-scroll').scrollLeft=50;});
    const scroll=await f.evaluate(()=>document.querySelector('.diagram-scroll').scrollLeft);
    await f.evaluate(()=>{window.dispatchEvent(new CustomEvent('openai:set_globals',{detail:{globals:{displayMode:'fullscreen',maxHeight:650}}}));});
    for(const width of [1440,736,320]) {
      await page.setViewportSize({width,height:850});
      await page.waitForTimeout(120);
      const actual=await f.evaluate(()=>{
        const root=document.querySelector('.qv-mermaid'),v=root.querySelector('.diagram-scroll'),box=v.getBoundingClientRect();
        const marks=root.dataset.state==='native'?[root.querySelector('.scene>svg')]:[...root.querySelectorAll('button.node,.qv-group,.edge-label,.edge-count')];
        const clipped=marks.filter(n=>{const r=n.getBoundingClientRect();return r.left<box.left-1||r.right>box.right+1||r.top<box.top-1||r.bottom>box.bottom+1;}).map(n=>n.textContent);
        return {mode:root.dataset.displayMode,scale:+root.dataset.viewportScale,height:root.offsetHeight,clipped,nodes:root.querySelectorAll('button.node').length,animations:root.getAnimations({subtree:true}).filter(a=>a.playState==='running').length};
      });
      check(actual.mode==='fullscreen'&&!actual.clipped.length&&(name==='gantt'?actual.scale===1:actual.height<=650)&&!actual.animations,name+': '+JSON.stringify(actual));
      results.push({name,width,state,...actual});
    }
    await page.setViewportSize({width:736,height:850});
    await f.evaluate(()=>{window.dispatchEvent(new CustomEvent('openai:set_globals',{detail:{globals:{displayMode:'inline'}}}));});
    await page.waitForTimeout(120);
    const restored=await f.evaluate(()=>document.querySelector('.diagram-scroll').scrollLeft);
    check(Math.abs(scroll-restored)<1,name+': inline scroll reset');
    if(name==='navigation') {
      await f.evaluate(()=>window.dispatchEvent(new CustomEvent('openai:set_globals',{detail:{globals:{displayMode:'fullscreen',maxHeight:650}}})));
      await f.locator('[data-node=platform]').click();
      await f.waitForSelector('[data-scope=platform]');
      await f.locator('[data-node=api]').click();
      await f.waitForSelector('[data-scope=api]');
      check(await f.locator('button.node').count()===6,'navigation lost nodes');
      await f.locator('.scope-toggle input').uncheck();
      await f.waitForSelector('[data-navigation=false]');
      check(await f.locator('button.node').count()===14,'complete view lost nodes');
      const actual=await f.evaluate(()=>{const v=document.querySelector('.diagram-scroll').getBoundingClientRect();return [...document.querySelectorAll('button.node')].every(n=>{const r=n.getBoundingClientRect();return r.left>=v.left-1&&r.right<=v.right+1&&r.top>=v.top-1&&r.bottom<=v.bottom+1;});});
      check(actual,'complete view clipped after navigation');
    }
  }
  return results;
}
