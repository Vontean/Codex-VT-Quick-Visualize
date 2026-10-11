// Mermaid 11.12 成员已拆分属性/方法，并给出可见性和分类符，不再解析源码签名。
async function readMermaidClassModel(db,descriptions={}) {
 const classes=[...db.getClasses()],raw=db.getData(),marks=new Set(['none','extension','composition','aggregation','dependency']);
 if(db.getNotes().length||db.styleClasses?.size||classes.some(([,n])=>n.styles?.length||n.cssClasses!=='default'||n.link||n.haveCallback||hasRichMermaidLabel(n.label)||[...n.members,...n.methods].some(a=>[a.id,a.parameters,a.returnType].some(hasRichMermaidLabel)))||raw.edges.some(e=>!marks.has(e.arrowTypeStart)||!marks.has(e.arrowTypeEnd)||hasRichMermaidLabel(e.label)))return {reason:'此类图包含尚未适配的注释、棒棒糖接口、链接、回调、富文本或自定义样式，保留原生语义'};
 const members=(list,kind)=>list.map(a=>({name:a.getDisplayDetails().displayText,kind,visibility:a.visibility,classifier:a.classifier}));
 const nodes=classes.map(([id,n])=>({id,name:(n.label||id)+(n.type?'<'+n.type+'>':''),technicalName:id,parent:n.parent||undefined,annotations:[...n.annotations],members:members(n.members,'attribute'),methods:members(n.methods,'method'),description:descriptions[id]||'',shape:'class'}));
 const groups=raw.nodes.filter(n=>n.isGroup).map(n=>({id:n.id,name:n.label||n.id,parent:n.parentId||undefined}));
 const unknown=Object.keys(descriptions).filter(id=>![...nodes,...groups].some(n=>n.id===id));if(unknown.length)throw new Error('说明引用了未知类或命名空间：'+unknown.join('、'));
 return {data:{kind:'class',direction:db.getDirection()||'TB',nodes,groups,layers:[],edges:raw.edges.map(e=>({id:e.id,from:e.start,to:e.end,label:e.label||'',startMark:e.arrowTypeStart,endMark:e.arrowTypeEnd,startMultiplicity:e.startLabelRight||'',endMultiplicity:e.endLabelLeft||'',async:e.pattern==='dashed'}))}};
}
async function prepareMermaidClassLayout(data) {
 const context=document.createElement('canvas').getContext('2d');context.font='12px '+getComputedStyle(document.body).fontFamily;const measure=s=>Math.ceil(context.measureText(s).width);
 for(const n of data.nodes){n.headerHeight=n.annotations.length?64:48;n.layoutWidth=Math.max(224,measure(n.name)+40,...[...n.members,...n.methods].map(a=>measure(a.name)+32));n.layoutHeight=n.headerHeight+(n.members.length+n.methods.length)*30+(n.members.length&&n.methods.length?1:0)+12;}
 for(const e of data.edges)if(e.from===e.to)e.fromSide=e.toSide=['LR','RL'].includes(data.direction)?'SOUTH':'EAST';
 await prepareMermaidLayout(data);
 // 自关联单独留出阅读通道，保留源端点及 UML 方向。
 const map=new Map(data.nodes.map(n=>[n.id,n]));
 for(const e of data.edges.filter(e=>e.from===e.to)){
  const n=map.get(e.from),a=e.points[0],b=e.points.at(-1),labelWidth=measure(e.label||'连接')+12;
  if(e.fromSide==='EAST'){
   const x=n.x+n.w+88;e.points=[a,[x,a[1]],[x,b[1]],b];e.labelPosition={x:x+labelWidth/2+8,y:(a[1]+b[1])/2};
   const right=x+labelWidth+24;data.layout.width=Math.max(data.layout.width,right+28);
   for(let id=n.parent;id;){const g=data.layout.groups.find(g=>g.id===id);if(!g)break;g.w=Math.max(g.w,right-g.x);id=g.parent;}
  }else{
   const y=n.y+n.h+72;e.points=[a,[a[0],y],[b[0],y],b];e.labelPosition={x:(a[0]+b[0])/2,y:y+20};
   const bottom=y+42;data.layout.height=Math.max(data.layout.height,bottom+28);
   for(let id=n.parent;id;){const g=data.layout.groups.find(g=>g.id===id);if(!g)break;g.h=Math.max(g.h,bottom-g.y);id=g.parent;}
  }
 }

}
