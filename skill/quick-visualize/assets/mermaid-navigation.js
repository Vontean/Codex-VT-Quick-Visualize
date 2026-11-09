// 状态图的层级投影；流程图和架构图始终绘制完整模型。
function mermaidScopeView(model, scope = null) {
  const groups = new Map((model.groups || []).map(g => [g.id, g]));
  const all = new Map([...groups.values(), ...model.nodes].map(n => [n.id, n]));
  if (scope !== null && !groups.has(scope)) throw new Error('分组不存在：' + scope);
  const inside = (id, parent) => {
    if (parent === null) return true;
    for (let n = all.get(id); n; n = all.get(n.parent)) if (n.id === parent) return true;
    return false;
  };
  // 每个端点映射到当前层的直接孩子，外部端点映射到最近的外部边界。
  function representative(id) {
    if (id === scope) return {id, external:true};
    if (inside(id, scope)) {
      let n = all.get(id);
      while (n.parent && n.parent !== scope) n = all.get(n.parent);
      return {id:n.id, external:false};
    }
    let n = all.get(id);
    const ancestors = new Set();
    for (let p = all.get(scope); p; p = all.get(p.parent)) ancestors.add(p.id);
    while (n.parent && !ancestors.has(n.parent)) n = all.get(n.parent);
    return {id:n.id, external:true};
  }
  const visible = new Map();
  function add(id, external = false) {
    const key = external ? 'qv-external:' + id : id;
    if (visible.has(key)) return key;
    const raw = all.get(id), group = groups.has(id);
    const count = group ? model.nodes.filter(n => !n.junction && inside(n.id,id)).length : 0;
    visible.set(key, {...raw, id:key, parent:undefined, shape:group?'round':raw.shape,
      groupCard:group&&!external, external, count,
      targetGroup:group ? (id===scope?raw.parent||null:id) : undefined,
      description:raw.description||'',
      layer:0});
    return key;
  }
  for (const n of all.values()) if ((n.parent||null)===scope) add(n.id);
  const edges = [], bundles = new Map();
  model.edges.forEach((edge,index) => {
    if (!inside(edge.from,scope)&&!inside(edge.to,scope)) return;
    const a=representative(edge.from), b=representative(edge.to);
    // 折叠组内部的边留在原模型；真实叶节点自环仍显示。
    if (a.id===b.id && !(edge.from===edge.to&&!groups.has(a.id))) return;
    const from=add(a.id,a.external),to=add(b.id,b.external);
    const key=JSON.stringify([from,to,edge.async,edge.thick,edge.arrow,edge.startArrow,edge.marker,edge.invisible,edge.label||'']);
    if(bundles.has(key)){bundles.get(key).members.push(index);return;}
    const projected={...edge,from,to,points:undefined,labelPosition:undefined,
      fromSide:from===edge.from?edge.fromSide:undefined,toSide:to===edge.to?edge.toSide:undefined,members:[index]};
    edges.push(projected);bundles.set(key,projected);
  });
  for(const edge of edges)if(edge.members.length>1)edge.bundleCount=edge.members.length;
  return {nodes:[...visible.values()],edges,groups:[],layers:[],generic:true,navigation:true,
    direction:model.direction||'LR',grouped:false,scope,kind:model.kind};
}
