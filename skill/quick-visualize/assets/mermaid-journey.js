function renderMermaidJourney(root,data) {
 const scene=root.querySelector('.scene'),viewport=root.querySelector('.diagram-scroll'),svg=scene.querySelector('svg'),NS='http://www.w3.org/2000/svg';
 root.classList.add('qv-journey');root.dataset.state='enhanced';root.dataset.renderer='qv-journey';root.querySelector('.edge-key').hidden=true;viewport.setAttribute('aria-label','用户旅程：体验评分和角色参与，可横向滚动');
 if(data.title&&root.querySelector('h3').hidden){root.querySelector('h3').textContent=data.title;root.querySelector('h3').hidden=false;}
 const frame=document.createElement('div'),reference=document.createElement('div'),axis=document.createElementNS(NS,'svg');frame.className='journey-frame';reference.className='journey-reference';axis.classList.add('journey-reference-axis');reference.append(axis);viewport.before(frame);frame.append(reference,viewport);
 const style=document.createElement('style');style.textContent=`
 #${root.id} .journey-frame{display:flex;align-items:flex-start}
 #${root.id} .journey-frame>.diagram-scroll{flex:1;min-width:0}
 #${root.id} .journey-reference{position:relative;width:128px;flex:none;background:var(--background)}
 #${root.id} .journey-reference-axis{position:absolute;left:0;top:0;width:128px;overflow:visible;pointer-events:none}
 #${root.id} .journey-step{position:absolute;top:36px;width:168px;border:0;border-radius:6px;background:none;padding:6px 8px;font:inherit;font-size:14px;line-height:22px;text-align:left;color:var(--foreground);white-space:normal;overflow-wrap:anywhere;cursor:var(--cursor-interaction,pointer)}
 #${root.id} .journey-step[data-active=true],#${root.id} .journey-actor[data-active=true]{background:var(--accent)}
 #${root.id} .journey-section{position:absolute;top:0;font-size:12px;color:var(--muted-foreground);padding-bottom:10px;border-bottom:1px solid var(--border)}
 #${root.id} .journey-line{fill:none;stroke:var(--viz-series-1);stroke-width:1.5}
 #${root.id} .journey-grid{stroke:var(--border);stroke-width:1;fill:none}
 #${root.id} .journey-dot{fill:var(--background);stroke:var(--viz-series-1);stroke-width:1.5}
 #${root.id} .journey-axis-label{font-size:12px;fill:var(--muted-foreground)}
 #${root.id} .journey-actor{position:absolute;left:12px;width:110px;min-height:30px;border:0;border-radius:6px;background:var(--background);color:var(--foreground);padding:4px 6px;font:inherit;font-size:12px;line-height:18px;text-align:left;white-space:normal;overflow-wrap:anywhere;cursor:var(--cursor-interaction,pointer)}
 #${root.id} .journey-participation{position:absolute;width:32px;height:32px;min-height:0;border:0;border-radius:6px;background:none;padding:0;transform:translate(-50%,-50%);cursor:var(--cursor-interaction,pointer)}
 #${root.id} .journey-participation:before{content:'';display:block;width:6px;height:6px;margin:auto;border-radius:50%;background:var(--muted-foreground)}
 #${root.id} .journey-participation[data-active=true]:before{background:var(--viz-series-1)}
 #${root.id} .journey-score{position:absolute;transform:translate(-50%,-50%);min-width:32px;min-height:24px;border:0;background:var(--background);padding:2px 4px;font:inherit;font-size:12px;color:var(--foreground);cursor:var(--cursor-interaction,pointer)}
 #${root.id} .journey-tip{position:absolute;z-index:10;border-radius:12px;padding:12px 14px;background:var(--popover);color:var(--popover-foreground);font-size:12px;line-height:1.6;box-shadow:0 3px 12px #0002;pointer-events:none}
 `;root.append(style);
 const el=(tag,attrs)=>{const n=document.createElementNS(NS,tag);for(const[k,v]of Object.entries(attrs))n.setAttribute(k,v);(attrs.class==='journey-axis-label'?axis:svg).append(n);return n;},objects=[],roles=[],sections=[];
 let start=0,phase=data.tasks[0].section;for(let i=1;i<=data.tasks.length;i++)if(i===data.tasks.length||data.tasks[i].section!==phase){if(phase){const box=document.createElement('div');box.className='journey-section';const caption=document.createElement('span');caption.textContent=phase;caption.style.position='relative';caption.style.display='inline-block';caption.style.overflowWrap='anywhere';box.append(caption);scene.append(box);sections.push({box,caption,start,end:i});}if(i<data.tasks.length){start=i;phase=data.tasks[i].section;}}
 const grid=Array.from({length:5},(_,i)=>({path:el('path',{class:'journey-grid'}),label:el('text',{class:'journey-axis-label','text-anchor':'end'})}));grid.forEach((g,i)=>g.label.textContent=5-i);
 const quantity=el('text',{class:'journey-axis-label'});quantity.textContent='体验评分';const roleCaption=el('text',{class:'journey-axis-label'});roleCaption.textContent='参与角色';
 const line=el('path',{class:'journey-line'});
 data.tasks.forEach(t=>{const b=document.createElement('button');b.type='button';b.className='journey-step';b.dataset.step=t.id;b.textContent=t.name;b.setAttribute('aria-label',[t.section,t.name,`体验评分${t.score}/5`,t.actors.join('、')||'未指定角色'].filter(Boolean).join(' · '));scene.append(b);const dot=el('circle',{class:'journey-dot',r:5,'data-score-point':t.id}),score=document.createElement('button');score.type='button';score.className='journey-score';score.textContent=t.score;score.setAttribute('aria-label',b.getAttribute('aria-label'));score.dataset.score=t.id;scene.append(score);objects.push({t,b,dot,score});});
 data.actors.forEach(actor=>{const b=document.createElement('button');b.type='button';b.className='journey-actor';b.textContent=actor;b.dataset.actor=actor;reference.append(b);const dots=objects.filter(o=>o.t.actors.includes(actor)).map(o=>{const b=document.createElement('button');b.type='button';b.className='journey-participation';b.dataset.actor=actor;b.dataset.step=o.t.id;b.setAttribute('aria-label',`${actor} · ${o.t.name} · 体验评分${o.t.score}/5`);scene.append(b);return {b,o};});roles.push({actor,b,dots});});
 const tip=document.createElement('div');tip.className='journey-tip';tip.id=root.id+'-journey-tip';tip.setAttribute('role','tooltip');tip.hidden=true;root.append(tip);
 const stepDetail=t=>t.description||[`体验评分${t.score}/5`,t.actors.length?'参与角色：'+t.actors.join('、'):'未指定角色'].join(' · ');
 const scoreDetail=t=>[t.name,t.actors.length?'参与角色：'+t.actors.join('、'):'未指定角色'].join(' · ');
 const actorDetail=r=>r.actor+' · 参与'+r.dots.length+'个步骤';
 const participationDetail=(actor,t)=>actor+' · '+t.name;
 const view=createMermaidViewport(root);let plotTop=0,plotBottom=0,roleTop=0,width=0,height=0;
 function layout(){
  // 内联参照与绘图区分列；完整图把参照放回场景，一起进行原生适配。
  if(view.expanded)scene.append(reference);else frame.prepend(reference);
  reference.style.position=view.expanded?'absolute':'relative';reference.style.left='0';reference.style.top='0';
  const w=view.expanded?144:Math.min(168,Math.max(96,viewport.clientWidth-24)),gap=view.expanded?16:24,left=view.expanded?140:12;
  sections.forEach(s=>{s.left=left+s.start*(w+gap);s.box.style.left=s.left+'px';s.box.style.width=(s.end-s.start)*(w+gap)-gap+'px';s.box.style.fontSize=view.expanded?'14px':'12px';s.caption.style.maxWidth=(view.expanded?s.box.offsetWidth:Math.min(s.box.offsetWidth,viewport.clientWidth-24))+'px';});
  const stepTop=Math.max(36,...sections.map(s=>s.box.offsetHeight+16));
  objects.forEach((o,i)=>{o.b.style.width=w+'px';o.b.style.left=left+i*(w+gap)+'px';o.b.style.height='auto';o.b.style.fontSize='14px';o.b.style.top=stepTop+'px';});
  const headerHeight=Math.max(...objects.map(o=>o.b.offsetHeight));objects.forEach(o=>o.b.style.height=headerHeight+'px');
  plotTop=stepTop+headerHeight+38;plotBottom=plotTop+160;roleTop=plotBottom+62;
  roles.forEach(r=>r.b.style.fontSize=view.expanded?'14px':'12px');const rowHeight=Math.max(34,...roles.map(r=>r.b.offsetHeight+8));
  tip.style.maxWidth=detailWidth()+'px';tip.hidden=false;
  const detailTexts=[...objects.flatMap(o=>[stepDetail(o.t),scoreDetail(o.t)]),...roles.map(actorDetail),...roles.flatMap(r=>r.dots.map(d=>participationDetail(r.actor,d.o.t)))];
  const clearance=Math.max(80,...detailTexts.map(text=>{tip.textContent=text;return tip.offsetHeight+24;}));tip.hidden=true;
  width=Math.max(viewport.clientWidth,left+objects.length*(w+gap)-gap+28);height=roleTop+roles.length*rowHeight+clearance;
  scene.style.width=scene.style.minWidth=width+'px';scene.style.height=height+'px';svg.style.height=height+'px';svg.setAttribute('viewBox',`0 0 ${width} ${height}`);reference.style.height=height+'px';axis.style.height=height+'px';axis.setAttribute('viewBox',`0 0 128 ${height}`);
  const x=i=>left+i*(w+gap)+w/2,y=score=>plotBottom-(score-1)*40;
  objects.forEach((o,i)=>{o.x=x(i);o.y=y(o.t.score);o.dot.setAttribute('cx',o.x);o.dot.setAttribute('cy',o.y);o.score.style.left=o.x+'px';o.score.style.top=o.y-22+'px';});
  line.setAttribute('d',objects.map((o,i)=>(i?'L':'M')+o.x+' '+o.y).join(' '));
  grid.forEach((g,i)=>{const yy=plotTop+i*40;g.path.setAttribute('d',`M${view.expanded?128:0} ${yy}H${width-28}`);g.label.setAttribute('x',114);g.label.setAttribute('y',yy+4)});
  quantity.setAttribute('x',12);quantity.setAttribute('y',plotTop-20);roleCaption.setAttribute('x',12);roleCaption.setAttribute('y',roleTop-20);roleCaption.style.display=roles.length?'':'none';
  placeSections();
  roles.forEach((r,i)=>{const cy=roleTop+i*rowHeight;r.b.style.top=cy-r.b.offsetHeight/2+'px';r.dots.forEach(d=>{d.b.style.left=d.o.x+'px';d.b.style.top=cy+'px';})});view.refresh();
 }
 root.addEventListener('qv:display-mode',()=>{layout();if(!view.expanded)viewport.scrollLeft=view.savedInlinePosition?.left||0;});layout();
 function clear(){tip.hidden=true;root.querySelectorAll('[data-active]').forEach(n=>n.removeAttribute('data-active'));objects.forEach(o=>{o.dot.style.fill='';[o.b,o.score].forEach(b=>b.removeAttribute('aria-describedby'))});roles.forEach(r=>{r.b.removeAttribute('aria-describedby');r.dots.forEach(d=>d.b.removeAttribute('aria-describedby'))});}
 function detailWidth(){return root.clientWidth<400?Math.max(96,viewport.clientWidth-12):Math.min(280,root.clientWidth-8);}
 function placeSections(){sections.forEach(s=>s.caption.style.left=(view.expanded?0:Math.max(0,Math.min(s.box.offsetWidth-s.caption.offsetWidth,viewport.scrollLeft-s.left)))+'px');}
 function show(trigger,text,ids,actor){
  clear();const set=new Set(ids);objects.forEach(o=>{if(set.has(o.t.id)){o.b.dataset.active='true';o.dot.style.fill='var(--viz-series-1)';}});roles.forEach(r=>{if(actor===r.actor)r.b.dataset.active='true';r.dots.forEach(d=>{if(set.has(d.o.t.id)&&(!actor||actor===r.actor))d.b.dataset.active='true'})});
  tip.textContent=text;tip.style.maxWidth=detailWidth()+'px';tip.hidden=false;trigger.setAttribute('aria-describedby',tip.id);
  const rr=root.getBoundingClientRect(),r=trigger.getBoundingClientRect(),tw=tip.offsetWidth,th=tip.offsetHeight,x=r.left-rr.left,y=r.top-rr.top,vr=viewport.getBoundingClientRect(),bottom=vr.bottom-rr.top;
  const box=n=>{const b=n.getBoundingClientRect();return {x:b.left-rr.left,y:b.top-rr.top,w:b.width,h:b.height};};
  const obstacles=[...root.querySelectorAll('.journey-step,.journey-score,.journey-actor,.journey-section span,.journey-participation,.journey-axis-label,.journey-dot'),root.querySelector('h3')].map(box).filter(b=>b.x+b.w>0&&b.x<root.clientWidth);
  // 只避开真实曲线，网格不抢占详情空间。分段取样避免把整段斜线当大矩形。
  for(let i=1;i<objects.length;i++){const a=box(objects[i-1].dot),b=box(objects[i].dot),ax=a.x+a.w/2,ay=a.y+a.h/2,bx=b.x+b.w/2,by=b.y+b.h/2,count=Math.ceil(Math.hypot(bx-ax,by-ay)/20);for(let j=0;j<count;j++){const x1=ax+(bx-ax)*j/count,y1=ay+(by-ay)*j/count,x2=ax+(bx-ax)*(j+1)/count,y2=ay+(by-ay)*(j+1)/count;if(Math.max(x1,x2)<vr.left-rr.left||Math.min(x1,x2)>vr.right-rr.left)continue;obstacles.push({x:Math.min(x1,x2)-3,y:Math.min(y1,y2)-3,w:Math.abs(x2-x1)+6,h:Math.abs(y2-y1)+6});}}
  const xs=[x,x+(r.width-tw)/2,x+r.width+12,x-tw-12,vr.left-rr.left+6],ys=[y-th-12,y+r.height+12,y,bottom-th-8,...obstacles.flatMap(b=>[b.y-th-12,b.y+b.h+12])];
  const candidates=xs.flatMap(x=>ys.map(y=>({x:Math.max(4,Math.min(root.clientWidth-tw-4,x)),y:Math.max(4,Math.min(root.clientHeight-th-4,y))})));
  for(const c of candidates)c.score=obstacles.reduce((s,b)=>s+Math.max(0,Math.min(c.x+tw,b.x+b.w)-Math.max(c.x,b.x))*Math.max(0,Math.min(c.y+th,b.y+b.h)-Math.max(c.y,b.y)),0);
  const distance=c=>Math.hypot(Math.max(c.x-r.right+rr.left,r.left-rr.left-c.x-tw,0),Math.max(c.y-r.bottom+rr.top,r.top-rr.top-c.y-th,0));
  candidates.sort((a,b)=>a.score-b.score||distance(a)-distance(b));tip.style.left=candidates[0].x+'px';tip.style.top=candidates[0].y+'px';
 }
 let focused=null,epoch=0,closed=false;function restore(){const e=++epoch;requestAnimationFrame(()=>requestAnimationFrame(()=>{if(e===epoch&&!closed&&focused&&document.activeElement===focused.b&&focused.b.matches(':focus-visible'))focused.show();}));}const bind=(b,show)=>{b.onpointerenter=b.onclick=()=>{closed=false;show()};b.onpointerleave=clear;b.onfocus=()=>{focused={b,show};closed=false;show();restore()};b.onblur=()=>{focused=null;++epoch;clear()};};objects.forEach(o=>{const detail=()=>show(o.b,stepDetail(o.t),[o.t.id]);bind(o.b,detail);bind(o.score,()=>show(o.score,scoreDetail(o.t),[o.t.id]));});roles.forEach(r=>{bind(r.b,()=>show(r.b,actorDetail(r),r.dots.map(d=>d.o.t.id),r.actor));r.dots.forEach(d=>bind(d.b,()=>show(d.b,participationDetail(r.actor,d.o.t),[d.o.t.id],r.actor)));});viewport.addEventListener('scroll',()=>{placeSections();clear();restore()},{passive:true});root.addEventListener('qv:display-mode',()=>{focused=null;++epoch;placeSections();clear()});document.addEventListener('keydown',e=>{if(e.key==='Escape'){closed=true;++epoch;clear()}});
 const reduced=matchMedia('(prefers-reduced-motion:reduce)');let running=[],armed=true;function replay(){running.forEach(a=>a.cancel());running=[];if(reduced.matches||view.expanded)return;const length=line.getTotalLength();line.style.strokeDasharray=`${length} ${length}`;running.push(line.animate([{strokeDashoffset:length},{strokeDashoffset:0}],{duration:1200,fill:'backwards'}));objects.forEach((o,i)=>{const delay=i/Math.max(1,objects.length-1)*1200;running.push(o.dot.animate([{opacity:0,r:'.4px'},{opacity:1,r:'5px'}],{duration:240,delay,fill:'backwards'}));running.push(o.score.animate([{opacity:0},{opacity:1}],{duration:100,delay:delay+180,fill:'backwards'}));running.push(o.b.animate([{opacity:0,transform:'translateY(8px)'},{opacity:1,transform:'translateY(0)'}],{duration:300,delay:Math.min(i,8)*80,fill:'backwards'}));roles.forEach(r=>r.dots.filter(d=>d.o===o).forEach(d=>running.push(d.b.animate([{opacity:0},{opacity:1}],{duration:240,delay,fill:'backwards'}))));});root.dataset.replays=String(+(root.dataset.replays||0)+1);}
 new IntersectionObserver(es=>{if(!es[0].isIntersecting)armed=true;else if(es[0].intersectionRatio>=.2&&armed){armed=false;replay()}},{threshold:[0,.2]}).observe(root);document.addEventListener('visibilitychange',()=>{if(document.hidden)armed=true;else if(armed){armed=false;replay()}});root.addEventListener('qv:display-mode',()=>running.forEach(a=>a.cancel()));reduced.addEventListener('change',()=>running.forEach(a=>a.cancel()));let lastWidth=root.clientWidth,layoutFrame=0;
 // 尺寸通知只排队；下一帧再改布局，避免高度变化反过来触发同批通知。
 new ResizeObserver(()=>{if(lastWidth===root.clientWidth||layoutFrame)return;layoutFrame=requestAnimationFrame(()=>{layoutFrame=0;const nextWidth=root.clientWidth;if(!root.isConnected||lastWidth===nextWidth)return;lastWidth=nextWidth;running.forEach(a=>a.cancel());line.style.strokeDasharray='';layout();clear();restore();});}).observe(root);view.refresh();
}
