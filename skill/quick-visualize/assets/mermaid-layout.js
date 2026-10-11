// ELK 只负责复杂拓扑的布局；节点、边、提示和动效仍由 qv 绘制。
let elkLoad;
async function loadMermaidLayoutEngine() {
  if(window.ELK)return;
  if(!elkLoad)elkLoad=(async()=>{
    for(const src of ['https://cdn.jsdelivr.net/npm/elkjs@0.10.0/lib/elk.bundled.js','https://unpkg.com/elkjs@0.10.0/lib/elk.bundled.js']) {
      try {
        await new Promise((resolve,reject)=>{
          const script=document.createElement('script');let timer;
          const finish=error=>{clearTimeout(timer);script.onload=script.onerror=null;if(error){script.remove();reject(error);}else resolve();};
          script.src=src;script.onload=()=>finish(typeof window.ELK==='function'?null:new Error('布局引擎未初始化'));script.onerror=()=>finish(new Error('布局引擎加载失败'));
          timer=setTimeout(()=>finish(new Error('布局引擎加载超时')),15000);document.head.append(script);
        });
        return;
      } catch(error) { if(window.ELK)return; }
    }
    throw new Error('布局引擎加载失败，请稍后重试');
  })().catch(error=>{elkLoad=null;throw error;});
  await elkLoad;
}
async function prepareMermaidLayout(data) {
  await loadMermaidLayoutEngine();
  const direction={TB:'DOWN',BT:'UP',LR:'RIGHT',RL:'LEFT'};
  const graph={id:'qv-layout',layoutOptions:{'elk.algorithm':'layered','elk.direction':direction[data.direction]||'DOWN','elk.hierarchyHandling':'INCLUDE_CHILDREN','elk.edgeRouting':'ORTHOGONAL','elk.json.edgeCoords':'ROOT','elk.spacing.nodeNode':'38','elk.layered.spacing.nodeNodeBetweenLayers':data.navigation?'56':'84','elk.padding':'[top=28,left=28,bottom=28,right=28]',...(['er','class'].includes(data.kind)?{'elk.spacing.edgeNode':'28','elk.layered.spacing.edgeNodeBetweenLayers':'28'}:{}),...(data.kind==='state'?{'elk.layered.cycleBreaking.strategy':'MODEL_ORDER','elk.layered.considerModelOrder.strategy':'NODES_AND_EDGES','elk.layered.spacing.nodeNodeBetweenLayers':'48'}:{})},children:[],edges:[]};
  const byId=new Map([[null,graph]]);
  for(const g of data.groups||[])byId.set(g.id,{id:g.id,children:[],layoutOptions:{'elk.padding':'[top=44,left=24,bottom=24,right=24]',...(g.direction?{'elk.direction':direction[g.direction]}:{}),...(data.kind==='state'?{'elk.layered.cycleBreaking.strategy':'MODEL_ORDER'}:{})}});
  for(const g of data.groups||[])(byId.get(g.parent)||graph).children.push(byId.get(g.id));
  for(const n of data.nodes){const shaped=['diamond','hexagon','circle','doublecircle'].includes(n.shape),w=n.junction?10:Math.max(shaped?128:154,Math.min(260,[...n.name].reduce((s,c)=>s+(c.charCodeAt(0)>255?14:8),0)+52)),h=n.junction?10:['circle','doublecircle'].includes(n.shape)?w:shaped?94:48;
    const node={id:n.id,width:n.layoutWidth??(n.groupCard?Math.max(184,w):w),height:n.layoutHeight??(n.groupCard?(n.preview?.height||76):n.external?64:h),ports:[],layoutOptions:{'elk.portConstraints':'FIXED_SIDE',...(data.kind==='state'&&['stateStart','stateEnd'].includes(n.shape)?{'elk.layered.layering.layerConstraint':n.shape==='stateStart'?'FIRST':'LAST'}:{})}};
    n.w=node.width;n.h=node.height;byId.set(n.id,node);(byId.get(n.parent)||graph).children.push(node);
  }
  const port=(id,face,incoming,edgeIndex)=>{const n=byId.get(id),pid=id+'::'+face+'::'+(incoming?'in':'out')+(['er','class'].includes(data.kind)?'::'+edgeIndex:'');n.ports??=[];if(!n.ports.some(p=>p.id===pid))n.ports.push({id:pid,width:0,height:0,layoutOptions:{'elk.port.side':face}});return pid;};
  const defaultFaces={TB:['SOUTH','NORTH'],BT:['NORTH','SOUTH'],LR:['EAST','WEST'],RL:['WEST','EAST']}[data.direction]||['SOUTH','NORTH'];
  data.edges.forEach((e,i)=>{const label=e.label?{id:'label'+i,text:e.label,width:Math.max(30,[...e.label].length*12+12),height:22}:null;graph.edges.push({id:'edge'+i,sources:[port(e.from,e.fromSide||defaultFaces[0],false,i)],targets:[port(e.to,e.toSide||defaultFaces[1],true,i)],...(label?{labels:[label]}:{})});});
  if(data.order)for(const node of byId.values())if(node.children)node.children.sort((a,b)=>(data.order.get(a.id)||0)-(data.order.get(b.id)||0));
  const result=await new window.ELK().layout(graph),positions=new Map(),groups=[];
  function visit(g,x=0,y=0){const gx=x+(g.x||0),gy=y+(g.y||0);positions.set(g.id,{x:gx,y:gy,w:g.width,h:g.height});if(g!==result&&g.children)groups.push({...data.groups.find(n=>n.id===g.id),x:gx,y:gy,w:g.width,h:g.height});for(const c of g.children||[])visit(c,gx,gy);}
  visit(result);
  const routes=new Map();function collect(g,ox=0,oy=0){const x=ox+(g.x||0),y=oy+(g.y||0);for(const e of g.edges||[]){const points=(e.sections||[]).flatMap(s=>[s.startPoint,...s.bendPoints||[],s.endPoint].map(p=>[p.x,p.y]));routes.set(e.id,{points,labelPosition:e.labels?.[0]?{x:e.labels[0].x+e.labels[0].width/2,y:e.labels[0].y+11}:null});}for(const c of g.children||[])collect(c,x,y);}collect(result);
  data.nodes.forEach(n=>Object.assign(n,positions.get(n.id)));
  data.edges.forEach((e,i)=>{Object.assign(e,routes.get('edge'+i));if(!e.points?.length)throw new Error('布局缺少连线：'+e.from+' → '+e.to);});
  data.layout={width:result.width,height:result.height,groups};
  // 动效按空间层级推进，回路不会导致无限拓扑遍历。
  const ys=[...new Set(data.nodes.map(n=>Math.round(data.direction==='LR'||data.direction==='RL'?n.x:n.y)))].sort((a,b)=>['RL','BT'].includes(data.direction)?b-a:a-b);
  data.nodes.forEach(n=>n.layer=Math.min(6,ys.indexOf(Math.round(data.direction==='LR'||data.direction==='RL'?n.x:n.y))));
}

// 使用 Mermaid 自己的方向约束布局；只读取显式节点 ID 对应的几何，不从图形猜测关系。
async function prepareNativeGeometry(data,mermaid,source,db,architecture) {
 if(window.lucide){const icons={};for(const name of new Set(data.nodes.map(n=>n.icon).filter(Boolean))){const key=name.replace(/(^|-)([a-z0-9])/g,(_,dash,c)=>c.toUpperCase()),definition=window.lucide.icons[key];if(!definition)continue;const svg=window.lucide.createElement(definition),group=document.createElementNS(svg.namespaceURI,'g');for(const a of svg.attributes)if(!['width','height','viewBox','xmlns','class'].includes(a.name))group.setAttribute(a.name,a.value);for(const child of [...svg.children])group.append(child);icons[name]={body:group.outerHTML};}mermaid.registerIconPacks([{name:'lucide',icons:{prefix:'lucide',width:24,height:24,icons}}]);}
 const id='qv-measure-'+Math.random().toString(36).slice(2),result=await mermaid.render(id,source),host=document.createElement('div');host.style.cssText='position:absolute;left:-100000px;visibility:hidden;pointer-events:none';host.innerHTML=result.svg;document.body.append(host);
 try {
  const svg=host.querySelector('svg'),view=svg.viewBox.baseVal;svg.style.cssText=`width:${view.width}px;height:${view.height}px;max-width:none`;const sr=svg.getBoundingClientRect();
  const scaleX=architecture?1.8:1.65,scaleY=architecture?1.2:1.45;
  const rect=(id,service=false)=>{const el=host.querySelector('#'+CSS.escape(id));if(!el)throw new Error('缺少布局节点：'+id);let b=el.getBoundingClientRect();if(service){const matrix=el.getScreenCTM(),size=db.getConfigField('iconSize'),p=new DOMPoint(0,0).matrixTransform(matrix);b={x:p.x,y:p.y,width:size*matrix.a,height:size*matrix.d};}return {x:(b.x-sr.x)*scaleX+24,y:(b.y-sr.y)*scaleY+24,w:b.width*scaleX,h:b.height*scaleY};};
  const measureText=(name,width,size=14)=>{const text=document.createElement('span');text.style.cssText='position:absolute;left:-100000px;width:'+width+'px;font:'+'500 '+size+'px/'+(size===14?20:18)+'px '+getComputedStyle(root).fontFamily+';white-space:normal;overflow-wrap:anywhere';text.textContent=name;root.append(text);const height=text.offsetHeight;text.remove();return height;};
  for(const n of data.nodes){const b=rect(architecture?(n.junction?'node-':'service-')+n.id:db.lookUpDomId(n.id),architecture&&!n.junction);n.w=n.junction?10:Math.max(154,Math.min(260,b.w));n.h=n.junction?10:['circle','doublecircle'].includes(n.shape)?n.w:['diamond','hexagon'].includes(n.shape)?94:48;if(architecture&&!n.junction){n.w=240;n.h=Math.max(48,26+measureText(n.name,n.w-56));}n.x=b.x+b.w/2-n.w/2;n.y=b.y+b.h/2-n.h/2;}
  const groups=data.groups.map(g=>({...g,...rect(architecture?'group-'+g.id:g.id)}));
  // 将原生图标布局转换成卡片后重新包住后代，并为标题留空间。
  const children=id=>[...data.nodes.filter(n=>n.parent===id),...groups.filter(g=>g.parent===id)];
  function bounds(g){for(const child of groups.filter(n=>n.parent===g.id))bounds(child);const list=children(g.id);if(list.length){const x=Math.min(...list.map(n=>n.x))-24,y=Math.min(...list.map(n=>n.y))-44;g.w=Math.max(Math.max(...list.map(n=>n.x+n.w))+24-x,architecture?240:0);g.h=Math.max(...list.map(n=>n.y+n.h))+24-y;g.x=x;g.y=y;}}
  for(const g of groups.filter(g=>!g.parent))bounds(g);
  const all=[...groups,...data.nodes],dx=24-Math.min(...all.map(n=>n.x)),dy=24-Math.min(...all.map(n=>n.y));for(const n of all){n.x+=dx;n.y+=dy;}
  const map=new Map(all.map(n=>[n.id,n])),face=(a,b,out)=>{if(architecture)return out.fromSide;const vertical=['TB','BT'].includes(data.direction);return vertical?(b.y>a.y?'SOUTH':'NORTH'):(b.x>a.x?'EAST':'WEST');};
  const dir={NORTH:[0,-1],SOUTH:[0,1],EAST:[1,0],WEST:[-1,0]},usages=new Map();
  for(const e of data.edges){const a=map.get(e.from),b=map.get(e.to);e.fs=e.fromSide||face(a,b,e);e.ts=e.toSide||({NORTH:'SOUTH',SOUTH:'NORTH',EAST:'WEST',WEST:'EAST'}[e.fs]);for(const [id,s,role] of [[e.from,e.fs,'out'],[e.to,e.ts,'in']]){const key=id+':'+s;if(!usages.has(key))usages.set(key,new Set());usages.get(key).add(role);}}
  function point(n,s,incoming){const split=usages.get(n.id+':'+s).size>1,offset=split?(incoming?-7:7):0;return s==='NORTH'?[n.x+n.w/2+offset,n.y]:s==='SOUTH'?[n.x+n.w/2+offset,n.y+n.h]:s==='WEST'?[n.x,n.y+n.h/2+offset]:[n.x+n.w,n.y+n.h/2+offset];}
  for(const e of data.edges){const a=map.get(e.from),b=map.get(e.to),start=point(a,e.fs,false),end=point(b,e.ts,true),u=dir[e.fs],v=dir[e.ts],s=[start[0]+u[0]*20,start[1]+u[1]*20],t=[end[0]+v[0]*20,end[1]+v[1]*20];e.points=[start,...routeAroundNodes(s,t,data.nodes),end];}
  const width=Math.max(...all.map(n=>n.x+n.w),...data.edges.flatMap(e=>e.points.map(p=>p[0])))+32,height=Math.max(...all.map(n=>n.y+n.h),...data.edges.flatMap(e=>e.points.map(p=>p[1])))+32;
  data.layout={width,height,groups};const coordinate=n=>Math.round(!architecture&&['LR','RL'].includes(data.direction)?n.x:n.y),levels=[...new Set(data.nodes.map(coordinate))].sort((a,b)=>['RL','BT'].includes(data.direction)?b-a:a-b);data.nodes.forEach(n=>n.layer=Math.min(6,levels.indexOf(coordinate(n))));
 } finally{host.remove();}
}
function routeAroundNodes(start,end,nodes){
 const blocks=nodes.filter(n=>!n.junction).map(n=>({l:n.x-8,r:n.x+n.w+8,t:n.y-8,b:n.y+n.h+8}));
 const xs=[...new Set([start[0],end[0],...blocks.flatMap(b=>[b.l-8,b.r+8])])].sort((a,b)=>a-b),ys=[...new Set([start[1],end[1],...blocks.flatMap(b=>[b.t-8,b.b+8])])].sort((a,b)=>a-b);
 const cross=(a,b)=>blocks.some(r=>a[0]===b[0]?a[0]>r.l&&a[0]<r.r&&Math.max(a[1],b[1])>r.t&&Math.min(a[1],b[1])<r.b:a[1]>r.t&&a[1]<r.b&&Math.max(a[0],b[0])>r.l&&Math.min(a[0],b[0])<r.r);
 const id=(x,y)=>y*xs.length+x,first=id(xs.indexOf(start[0]),ys.indexOf(start[1])),last=id(xs.indexOf(end[0]),ys.indexOf(end[1])),dist=new Map([[first,0]]),prev=new Map(),open=new Set([first]);
 while(open.size){let current,score=Infinity;for(const k of open){const d=dist.get(k)+Math.abs(xs[k%xs.length]-end[0])+Math.abs(ys[Math.floor(k/xs.length)]-end[1]);if(d<score){score=d;current=k;}}if(current===last){const path=[];for(let k=last;k!==undefined;k=prev.get(k))path.push([xs[k%xs.length],ys[Math.floor(k/xs.length)]]);return path.reverse();}open.delete(current);const x=current%xs.length,y=Math.floor(current/xs.length);for(const [nx,ny] of [[x-1,y],[x+1,y],[x,y-1],[x,y+1]]){if(nx<0||ny<0||nx>=xs.length||ny>=ys.length)continue;const a=[xs[x],ys[y]],b=[xs[nx],ys[ny]],next=id(nx,ny);if(cross(a,b))continue;const cost=dist.get(current)+Math.abs(a[0]-b[0])+Math.abs(a[1]-b[1])+1;if(cost<(dist.get(next)??Infinity)){dist.set(next,cost);prev.set(next,current);open.add(next);}}}
 throw new Error('没有找到避开节点的连线路径');
}
