// 详情留在未缩放的文档流中，完整图只负责展示资源和连接的全貌。
function createArchitectureReader(root, model, viewport, controller, highlight) {
  const entries=[...(model.groups||[]).map(g=>({...g,isGroup:true})),...model.nodes];
  const byId=new Map(entries.map(n=>[n.id,n]));
  const readout=document.createElement('div');readout.className='architecture-readout';
  const cue=document.createElement('div');cue.className='architecture-cue';
  const picker=document.createElement('label');picker.className='form-label';picker.append(document.createTextNode('对象详情'));
  const select=document.createElement('select');select.className='form-select';select.setAttribute('aria-label','选择架构对象查看详情');
  const placeholder=document.createElement('option');placeholder.value='';placeholder.textContent='选择资源或分组';select.append(placeholder);
  for(const n of entries){const option=document.createElement('option');option.value=n.id;option.textContent=(n.isGroup?'分组 · ':'')+n.name;select.append(option);}
  picker.append(select);
  const detail=document.createElement('div');detail.className='architecture-detail';detail.id=root.id+'-architecture-detail';detail.setAttribute('role','tooltip');detail.hidden=true;
  readout.append(cue,picker,detail);viewport.after(readout);
  let selected=null,epoch=0,scrollTimer,width=0;
  const sides={NORTH:'T',SOUTH:'B',WEST:'L',EAST:'R'};
  function path(n){const chain=[];for(let parent=byId.get(n.parent);parent;parent=byId.get(parent.parent))chain.unshift(parent.name);return chain.join(' / ');}
  function content(id){
    const n=byId.get(id);if(!n)return [];
    const lines=[n.name,(n.isGroup?'分组':n.junction?'汇接点':'资源'+(n.resource?' · '+n.resource:''))+' · '+n.id];
    if(n.description)lines.push(n.description);
    if(n.parent)lines.push('所属：'+path(n));
    if(n.isGroup){const children=entries.filter(c=>c.parent===id);if(children.length)lines.push('成员：'+children.map(c=>c.name).join(' · '));}
    const links=model.edges.filter(e=>e.from===id||e.to===id);
    for(const e of links){const arrow=e.startArrow&&e.arrow?'↔':e.startArrow?'←':e.arrow?'→':'—';
      lines.push((byId.get(e.from)?.name||e.from)+' ['+sides[e.fromSide]+(e.fromGroup?' group':'')+'] '+arrow+' '+(byId.get(e.to)?.name||e.to)+' ['+sides[e.toSide]+(e.toGroup?' group':'')+']');
      if(e.fromGroup||e.toGroup)lines.push('源端点：'+e.sourceFrom+' '+arrow+' '+e.sourceTo);
    }
    return lines;
  }
  function fill(id){detail.replaceChildren();for(const [i,text] of content(id).entries()){const row=document.createElement('div');row.textContent=text;if(i===0)row.className='architecture-detail-name';detail.append(row);}}
  function clear(){epoch++;clearTimeout(scrollTimer);selected=null;detail.hidden=true;cue.hidden=false;select.value='';root.querySelectorAll('[aria-describedby="'+detail.id+'"]').forEach(n=>n.removeAttribute('aria-describedby'));}
  function reveal(pending){if(pending!==epoch||!selected)return;fill(selected.id);detail.hidden=false;cue.hidden=true;select.value=selected.id;selected.anchor?.setAttribute('aria-describedby',detail.id);highlight(selected.id);}
  function choose(id,anchor,ensure=false){
    if(!byId.has(id))return;
    const pending=++epoch;clearTimeout(scrollTimer);selected={id,anchor};
    if(ensure&&anchor&&!controller.expanded){const a=anchor.getBoundingClientRect(),v=viewport.getBoundingClientRect();if(a.width<=v.width){if(a.left<v.left+8)viewport.scrollLeft-=v.left+8-a.left;else if(a.right>v.right-8)viewport.scrollLeft+=a.right-v.right+8;}}
    requestAnimationFrame(()=>requestAnimationFrame(()=>reveal(pending)));
  }
  function onScroll(){if(!selected)return;detail.hidden=true;const pending=epoch;clearTimeout(scrollTimer);scrollTimer=setTimeout(()=>reveal(pending),80);}
  function refresh(){
    const nextWidth=root.clientWidth;picker.hidden=!(controller.expanded||nextWidth<=420);cue.textContent=controller.expanded?'完整图概览 · 选择资源或分组查看详情':'可左右滚动 · 聚焦资源或分组查看详情';
    if(width===nextWidth&&readout.dataset.picker===String(!picker.hidden))return;
    width=nextWidth;readout.dataset.picker=String(!picker.hidden);
    const current=selected;detail.hidden=false;detail.style.visibility='hidden';let max=0;
    for(const n of entries){fill(n.id);max=Math.max(max,detail.offsetHeight);}
    readout.style.minHeight=(max+Math.max(28,cue.offsetHeight)+(picker.hidden?0:picker.offsetHeight+12))+'px';
    detail.style.visibility='';detail.hidden=true;if(current){fill(current.id);detail.hidden=false;cue.hidden=true;}else cue.hidden=false;
    controller.refresh();
  }
  select.addEventListener('change',()=>{if(select.value)choose(select.value,select);else clear();});
  select.addEventListener('blur',clear);
  return {choose,clear,onScroll,refresh,get focused(){return !!selected&&selected.anchor===document.activeElement;}};
}
