// 固定 Mermaid 11.12 的状态 DB 已提供语义形状和 parentId，不按 ID 后缀猜起止点。
async function readMermaidStateModel(db,descriptions={}) {
  const raw=db.getData(),shapes=new Set(['rect','roundedWithTitle','stateStart','stateEnd','choice','fork','join']);
  if(!raw.nodes.length||Object.keys(db.getClasses?.()||{}).length||raw.nodes.some(n=>!shapes.has(n.shape)||n.cssStyles?.length||n.cssCompiledStyles?.length||hasRichMermaidLabel(n.label)||n.description?.some?.(hasRichMermaidLabel))||raw.edges.some(e=>hasRichMermaidLabel(e.label)))return {reason:'此状态图包含尚未适配的注释、并发区域、富文本或自定义样式，保留原生语义'};
  const all=raw.nodes.map(n=>({id:n.id,name:['stateStart','stateEnd'].includes(n.shape)?(n.shape==='stateStart'?'起点':'终点'):n.shape==='choice'?'选择':n.label||n.id,shape:n.shape,parent:n.parentId,description:descriptions[n.id]||'',lines:n.description||[],direction:n.dir,group:n.isGroup}));
  const unknown=Object.keys(descriptions).filter(id=>!all.some(n=>n.id===id));if(unknown.length)throw new Error('说明引用了未知状态：'+unknown.join('、'));
  return {data:{kind:'state',direction:raw.direction||'TB',nodes:all.filter(n=>!n.group),groups:all.filter(n=>n.group),edges:raw.edges.map((e,i)=>({id:e.id||String(i),from:e.start,to:e.end,label:e.label||'',arrow:true})),layers:[]}};
}

async function prepareMermaidStateLayout(data) {
  // 复用 qv 的布局引擎，状态符号保留独立尺寸，不转换成普通服务卡。
  const context=document.createElement('canvas').getContext('2d');context.font='14px '+getComputedStyle(document.body).fontFamily;
  for(const n of data.nodes){const terminal=['stateStart','stateEnd'].includes(n.shape),bar=['fork','join'].includes(n.shape);n.layoutWidth=terminal?20:n.shape==='choice'?32:bar?64:Math.max(128,Math.ceil(context.measureText(n.name).width)+32);n.layoutHeight=terminal?20:n.shape==='choice'?32:bar?6:48+18*n.lines.length;}
  const all=[...data.groups,...data.nodes],rank=new Map();
  // 每个复合状态内部独立从起点遍历；回流只改变布局通道，不改变转移。
  for(const parent of [undefined,...data.groups.map(g=>g.id)]){
    const siblings=all.filter(n=>n.parent===parent),ids=new Set(siblings.map(n=>n.id)),queue=siblings.filter(n=>n.shape==='stateStart').map(n=>n.id);let index=0;
    while(queue.length){const id=queue.shift();if(rank.has(id))continue;rank.set(id,index++);for(const e of data.edges.filter(e=>e.from===id&&ids.has(e.to)))queue.push(e.to);}
    for(const n of siblings)if(!rank.has(n.id))rank.set(n.id,index++);
  }
  data.order=rank;
  for(const e of data.edges){if(e.from===e.to){e.fromSide=e.toSide=['LR','RL'].includes(data.direction)?'SOUTH':'EAST';continue;}if(all.find(n=>n.id===e.from)?.parent===all.find(n=>n.id===e.to)?.parent&&rank.get(e.from)>rank.get(e.to)){e.fromSide=e.toSide=['LR','RL'].includes(data.direction)?'NORTH':'WEST';}}
  await prepareMermaidLayout(data);
  for(const n of data.nodes)n.layer=Math.min(6,rank.get(n.id)||0);
}
