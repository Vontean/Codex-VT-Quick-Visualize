// 固定 Mermaid 11.12 DB；getData 的端点标记已处理 relSpec 左右命名反转。
async function readMermaidErModel(db,descriptions={}) {
 const entities=[...db.getEntities()],raw=db.getData(),cards=new Set(['only_one','zero_or_one','one_or_more','zero_or_more']);
 if(Object.keys(db.getClasses()).length||entities.some(([,n])=>n.cssStyles?.length||n.cssCompiledStyles?.length||n.cssClasses!=='default'||hasRichMermaidLabel(n.alias||n.label)||n.attributes.some(a=>[a.name,a.type,a.comment].some(hasRichMermaidLabel)))||raw.edges.some(e=>!cards.has(e.arrowTypeStart)||!cards.has(e.arrowTypeEnd)||hasRichMermaidLabel(e.label)))return {reason:'此实体关系图包含尚未适配的样式、富文本或关系标记，保留原生语义'};
 const nodes=entities.map(([id,n])=>({id,name:n.alias||n.label,technicalName:n.label,attributes:n.attributes.map(a=>({...a,keys:[...a.keys]})),description:descriptions[id]||'',shape:'er'})),ids=new Map(entities.map(([id,n])=>[n.id,id]));
 const unknown=Object.keys(descriptions).filter(id=>!nodes.some(n=>n.id===id));if(unknown.length)throw new Error('说明引用了未知实体：'+unknown.join('、'));
 return {data:{kind:'er',direction:db.getDirection()||'TB',nodes,groups:[],layers:[],edges:raw.edges.map(e=>({id:e.id,from:ids.get(e.start),to:ids.get(e.end),label:e.label||'',startCard:e.arrowTypeStart,endCard:e.arrowTypeEnd,async:e.pattern==='dashed'}))}};
}
async function prepareMermaidErLayout(data) {
 const context=document.createElement('canvas').getContext('2d'),font=getComputedStyle(document.body).fontFamily;
 context.font='12px '+font;const measure=s=>Math.ceil(context.measureText(s||'').width);
 for(const n of data.nodes){n.columns={key:Math.max(26,...n.attributes.map(a=>measure(a.keys.join(', ')))),name:Math.max(68,...n.attributes.map(a=>measure(a.name))),type:Math.max(40,...n.attributes.map(a=>measure(a.type)))};n.layoutWidth=Math.max(220,measure(n.name)+32,n.columns.key+n.columns.name+n.columns.type+64);n.layoutHeight=48+n.attributes.length*30+12;}
 // 自关联独占侧面端口，避免与主轴上的关系基数叠合。
 for(const e of data.edges)if(e.from===e.to)e.fromSide=e.toSide=['LR','RL'].includes(data.direction)?'SOUTH':'EAST';
 await prepareMermaidLayout(data);
}
