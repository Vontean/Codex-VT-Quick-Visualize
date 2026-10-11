async page => {
 const check=(ok,message)=>{if(!ok)throw Error(message);},results=[];
 await page.setViewportSize({width:1440,height:1000});
 for(const theme of ['light','dark']){
  await page.emulateMedia({colorScheme:theme,reducedMotion:'no-preference'});
  await page.goto('http://127.0.0.1:8792/flowchart-stress-stable-preview.html');const f=page.frames()[1];await f.waitForSelector('[data-state=enhanced]',{timeout:60000});
  await f.evaluate(()=>window.dispatchEvent(new CustomEvent('openai:set_globals',{detail:{globals:{displayMode:'fullscreen',maxHeight:950}}})));await page.waitForTimeout(180);
  const center=async id=>{const b=await f.locator('[data-node='+id+']').boundingBox();return [b.x+b.width/2,b.y+b.height/2];};
  const move=async id=>{const [x,y]=await center(id);await page.mouse.move(x,y);};
  const hover=()=>f.locator('.qv-mermaid').getAttribute('data-hover-node');
  await move('N1');await page.waitForTimeout(180);check(await hover()==='N1','Settled node did not highlight');
  await move('N2');const movingBox=await f.locator('[data-node=N2]').boundingBox();
  for(let i=0;i<14;i++){await page.mouse.move(movingBox.x+movingBox.width/2+i%4,movingBox.y+movingBox.height/2+i%3);await page.waitForTimeout(30);check(await hover()==='N1','Moving inside a node committed a hover before stopping');}
  await move('N1');await page.waitForTimeout(180);check(await hover()==='N1','Returning to active node committed a stale target');
  await f.evaluate(()=>{window.hoverChanges=[];new MutationObserver(es=>es.forEach(e=>{if(e.attributeName==='data-hover-node')hoverChanges.push(e.target.dataset.hoverNode);})).observe(document.querySelector('.qv-mermaid'),{attributes:true});});
  for(const id of ['N2','N1','N4','N5','N6','N8']){await move(id);await page.waitForTimeout(35);check(await hover()==='N1','Rapid crossing changed highlight to '+await hover());}
  await move('N9');await page.waitForTimeout(200);check(await hover()==='N9','Settled destination did not highlight');
  const transfer=await f.evaluate(()=>hoverChanges);check(!transfer.includes(''),'Cross-node transfer restored neutral state');
  await page.mouse.move(20,30);await page.waitForTimeout(100);check(await hover()==='N9','Leave buffer cleared too early');await page.waitForTimeout(180);check(await hover()==='','Leaving graph did not clear');
  const surfaces=await f.evaluate(()=>{
   const r=document.querySelector('.qv-mermaid'),leaf=r.querySelector('[data-node=N15]'),inner=r.querySelector('[data-group=checks]'),outer=r.querySelector('[data-group=processing]');
   const containers=[...r.querySelectorAll('.qv-group')];if(containers.indexOf(outer)>containers.indexOf(inner))throw Error('Outer surface covers inner surface');if(+getComputedStyle(r.querySelector('.wires')).zIndex<=+getComputedStyle(inner).zIndex)throw Error('Opaque surface covers wires');const canvas=document.createElement('canvas'),ctx=canvas.getContext('2d');return [leaf,inner,outer].map(n=>{const probe=document.createElement('span');probe.style.backgroundColor='var(--node-surface)';n.append(probe);const background=getComputedStyle(probe).backgroundColor;probe.remove();ctx.clearRect(0,0,1,1);ctx.fillStyle=getComputedStyle(leaf).backgroundColor;ctx.fillRect(0,0,1,1);ctx.fillStyle=background;ctx.fillRect(0,0,1,1);return {level:+n.dataset.containmentLevel,background,pixel:[...ctx.getImageData(0,0,1,1).data]};});
  });check(surfaces.map(n=>n.level).join(',')==='0,1,2','Containment levels were derived from drawing layers');check(surfaces[0].pixel.join(',')===surfaces[2].pixel.join(',')&&Math.abs(surfaces[0].pixel[0]-surfaces[1].pixel[0])>=2&&Math.abs(surfaces[0].pixel[0]-surfaces[1].pixel[0])<=5&&surfaces[1].pixel[3]===255,'Opaque white/gray alternating surfaces failed');
  await f.locator('.scope-toggle input').check();await f.waitForSelector('[data-scope=overview]');const overview=f.locator('[data-crumb=overview]');check(await overview.getAttribute('aria-haspopup')===null,'Overview advertises a menu');await overview.hover();await page.waitForTimeout(180);check(await f.locator('.scope-peers:popover-open').count()===0,'Overview opens a menu');await f.locator('[data-node=processing]').click();await f.waitForSelector('[data-scope=processing]');
  const portal=f.locator('button.external-group').first();const portalId=await portal.getAttribute('data-node');
  check(await portal.locator('.external-label').count()===0,'Portal retained visible action text');check(await portal.locator('.lucide-arrow-up-right').count()===1,'Portal arrow missing');
  const a11y=await portal.getAttribute('aria-label');check(a11y.includes('进入此分组'),'Portal accessible action missing');const before=await f.locator('.qv-mermaid').getAttribute('data-scope');await portal.click();await f.waitForFunction(before=>document.querySelector('.qv-mermaid').dataset.scope!==before,before);const after=await f.locator('.qv-mermaid').getAttribute('data-scope');check(before!==after,'Portal did not navigate');
  results.push({theme,transfer,surfaces,portalId,a11y,after});
 }
 return results;
}
