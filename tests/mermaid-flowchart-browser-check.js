// Generate the three flowchart-review fixtures as flowchart-{normal,shapes,stress}-refined-preview.html.
async page => {
 const results=[],check=(ok,message)=>{if(!ok)throw Error(message);};
 await page.emulateMedia({reducedMotion:'reduce'});
 for(const theme of ['light','dark'])for(const width of [736,320])for(const [slug,count,edges] of [['normal',9,10],['shapes',8,10],['stress',28,33]]){
  await page.emulateMedia({colorScheme:theme});await page.setViewportSize({width,height:900});
  await page.goto('http://127.0.0.1:8792/flowchart-'+slug+'-refined-preview.html');const f=page.frames()[1];
  await f.waitForSelector('[data-state=enhanced]',{timeout:60000});
  const geometry=await f.evaluate(()=>{
   const root=document.querySelector('.qv-mermaid'),scene=root.querySelector('.scene'),nodes=[...root.querySelectorAll('button.node')];
   const boxes=nodes.map(n=>({id:n.dataset.node,x:n.offsetLeft,y:n.offsetTop,w:n.offsetWidth,h:n.offsetHeight}));
   const overflow=nodes.filter(n=>n.scrollWidth>n.clientWidth+1||n.scrollHeight>n.clientHeight+1).map(n=>n.dataset.node);
   const overlaps=[],crossings=[];for(let i=0;i<boxes.length;i++)for(let j=i+1;j<boxes.length;j++){const a=boxes[i],b=boxes[j];if(Math.min(a.x+a.w,b.x+b.w)>Math.max(a.x,b.x)+1&&Math.min(a.y+a.h,b.y+b.h)>Math.max(a.y,b.y)+1)overlaps.push([a.id,b.id]);}
   for(const edge of root.querySelectorAll('.wire'))for(let d=8;d<edge.getTotalLength()-8;d+=5){const p=edge.getPointAtLength(d);if(boxes.some(n=>n.id!==edge.dataset.from&&n.id!==edge.dataset.to&&p.x>n.x+3&&p.x<n.x+n.w-3&&p.y>n.y+3&&p.y<n.y+n.h-3))crossings.push(edge.dataset.edge);}
   const centered=nodes.filter(n=>!n.classList.contains('group-card')&&!n.classList.contains('external')).every(n=>{const a=n.getBoundingClientRect(),b=n.querySelector('.name').getBoundingClientRect();return Math.abs(a.x+a.width/2-b.x-b.width/2)<1&&Math.abs(a.y+a.height/2-b.y-b.height/2)<1;});const shortDiamonds=nodes.filter(n=>n.dataset.shape==='diamond'&&n.textContent.length<=10).every(n=>{const label=n.querySelector('.name');return label.offsetHeight<=parseFloat(getComputedStyle(label).lineHeight)+1;});
   return {balanced:root.dataset.balanced,centered,shortDiamonds,nodes:boxes.length,ids:boxes.map(n=>n.id),edges:root.querySelectorAll('.wire').length,overflow,overlaps,crossings,ratio:scene.clientWidth/scene.clientHeight,pageOverflow:document.documentElement.scrollWidth>innerWidth,wire:getComputedStyle(root.querySelector('.wire')).stroke};
  });
  check(geometry.centered&&geometry.shortDiamonds,slug+': labels are not centered or short diamonds wrapped');
  if(slug!=='stress')check(geometry.balanced==='false',slug+': small graph was folded');
  check(geometry.nodes===count&&geometry.edges===edges,slug+': graph identity lost');
  check(!geometry.overflow.length&&!geometry.overlaps.length&&!geometry.crossings.length&&!geometry.pageOverflow,slug+': '+JSON.stringify(geometry));
  if(slug==='stress')check(geometry.ratio>.7&&geometry.ratio<1.3,'stress: aspect ratio remains elongated');
  await page.setViewportSize({width:1440,height:900});
  await f.evaluate(()=>window.dispatchEvent(new CustomEvent('openai:set_globals',{detail:{globals:{displayMode:'fullscreen',maxHeight:650}}})));await page.waitForTimeout(150);
  const expanded=await f.evaluate(()=>{const root=document.querySelector('.qv-mermaid'),b=root.querySelector('.diagram-scroll').getBoundingClientRect();return [...root.querySelectorAll('button.node,.qv-group,.edge-label')].filter(n=>{const r=n.getBoundingClientRect();return r.left<b.left-1||r.right>b.right+1||r.top<b.top-1||r.bottom>b.bottom+1;}).map(n=>n.textContent);});check(!expanded.length,slug+': expanded view clips marks');
  await f.evaluate(()=>window.dispatchEvent(new CustomEvent('openai:set_globals',{detail:{globals:{displayMode:'inline'}}})));await page.waitForTimeout(150);
  if(slug==='stress'){
   await f.locator('.scope-toggle input').check();
   await f.waitForSelector('[data-scope=overview]');
   check(await f.locator('button.group-card').count()===3,'overview groups lost');
   check(await f.locator('.preview-item').evaluateAll(items=>items.every(n=>n.scrollWidth<=n.clientWidth+1)),'preview long names overflow');
   await f.locator('[data-node=processing]').click();await f.waitForSelector('[data-scope=processing]');
   check(await f.locator('button.group-card').count()===2,'nested groups lost');
   await f.locator('.scope-toggle input').uncheck();await f.waitForSelector('[data-scope=expanded]');
   check(await f.locator('button.node').count()===28&&await f.locator('.wire').count()===33,'complete graph not restored');
  }
  results.push({theme,width,slug,...geometry});
 }
 return results;
}
