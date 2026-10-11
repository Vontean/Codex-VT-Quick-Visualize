async page => {
  const results = [];
  const check = (value, message) => { if (!value) throw new Error(message); };
  await page.emulateMedia({reducedMotion:'reduce'});
  for (const [name,count,links,state] of [
    ['simple',5,4,'enhanced'],['complex',12,16,'enhanced'],
    ['topology',7,9,'enhanced'],['boundaries',6,8,'enhanced'],
    ['ids',3,4,'enhanced'],['architecture',5,4,'enhanced'],
    ['groups-directions',4,4,'enhanced'],['architecture-ports',3,2,'enhanced'],
    ['shapes-arrows',7,7,'enhanced'],['semantics',0,0,'native'],
    ['rich-label',0,0,'native'],['fallback',0,0,'native'],['invalid',0,0,'error']
  ]) {
    await page.goto('http://localhost:8777/'+name+'-preview.html');
    const frame = page.frames()[1];
    await frame.waitForSelector('.qv-mermaid:not([data-state=loading])');
    const actual = await frame.evaluate(() => {
      const r=document.querySelector('.qv-mermaid');
      const nodes=[...r.querySelectorAll('button.node')].map(n=>({id:n.dataset.node,x:n.offsetLeft,y:n.offsetTop,w:n.offsetWidth,h:n.offsetHeight}));
      const edges=[...r.querySelectorAll('.wire')];
      const collisions=[];
      for (const e of edges) for (let d=8;d<e.getTotalLength()-8;d+=4) {
        const p=e.getPointAtLength(d);
        for (const n of nodes) if(n.id!==e.dataset.from&&n.id!==e.dataset.to&&p.x>n.x+3&&p.x<n.x+n.w-3&&p.y>n.y+3&&p.y<n.y+n.h-3)collisions.push(e.dataset.edge+' through '+n.id);
      }
      return {state:r.dataset.state,nodes,edges:edges.length,collisions:[...new Set(collisions)],animations:r.getAnimations({subtree:true}).length,notice:r.querySelector('.qv-notice').textContent};
    });
    check(actual.state===state,name+': '+JSON.stringify(actual));
    if(state==='enhanced') {
      check(actual.nodes.length===count&&actual.edges===links,name+': missing graph elements');
      check(!actual.collisions.length,name+': '+actual.collisions.join(', '));
      check(!actual.animations,name+': reduced motion still animating');
      const n=Object.fromEntries(actual.nodes.map(n=>[n.id,n]));
      if(name==='groups-directions')check(n.A.y<n.B.y,'subgroup TB direction lost');
      if(name==='architecture-ports')check(n.c.y>n.b.y&&Math.abs(n.c.x-n.b.x)<2,'B/T architecture ports lost');
      if(name==='architecture')check(Math.abs(n.hub.y+5-n.db.y-n.db.h/2)<2,'junction and horizontal service are misaligned');
    } else check(actual.notice.length>0,name+': silent fallback/error');
    results.push({name,state,nodes:actual.nodes.length,edges:actual.edges});
  }
  await page.emulateMedia({reducedMotion:'no-preference'});
  await page.goto('http://localhost:8777/topology-preview.html');
  let f=page.frames()[1];
  await f.waitForSelector('[data-motion=running]');
  const motion=await f.evaluate(()=>document.querySelector('.qv-mermaid').getAnimations({subtree:true}).map(a=>a.effect.getTiming().duration));
  check(motion.includes(240)&&motion.includes(650)&&motion.includes(50),'node/line/arrow motion missing');
  await f.waitForSelector('[data-motion=complete]');
  await f.locator('[data-node=gateway]').hover();
  await f.waitForSelector('.node-tip:not([hidden])');
  const tip=await f.evaluate(()=>{const t=document.querySelector('.node-tip').getBoundingClientRect(),n=document.querySelector('[data-node=gateway]').getBoundingClientRect();return Math.max(0,Math.min(t.right,n.right)-Math.max(t.left,n.left))*Math.max(0,Math.min(t.bottom,n.bottom)-Math.max(t.top,n.top));});
  check(tip===0,'tooltip covers bound node');
  for(const width of [736,320]) {
    await page.setViewportSize({width,height:900});
    await f.waitForFunction(()=>{const r=document.querySelector('.qv-mermaid');return r.clientWidth===r.scrollWidth;});
    const dimensions=await f.evaluate(()=>{const r=document.querySelector('.qv-mermaid'),v=r.querySelector('.diagram-scroll');return {root:r.clientWidth,scroll:r.scrollWidth,viewport:v.clientWidth,scene:v.scrollWidth};});
    check(dimensions.scroll===dimensions.root,'root overflows at '+width);
    results.push({width,...dimensions});
  }
  const before=await f.evaluate(()=>+document.querySelector('.qv-mermaid').dataset.replays);
  await f.evaluate(()=>{const spacer=document.createElement('div');spacer.id='replay-probe';spacer.style.height='3000px';document.querySelector('.qv-mermaid').before(spacer);});
  await page.waitForTimeout(250);
  await f.evaluate(()=>document.getElementById('replay-probe').remove());
  await f.waitForFunction(before=>+document.querySelector('.qv-mermaid').dataset.replays>before,before);
  return {fixtures:results,motion,tooltipOverlap:tip,reentryReplay:true};
}
