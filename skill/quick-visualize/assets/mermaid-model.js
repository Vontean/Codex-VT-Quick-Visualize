// 只在这一层访问固定版本的 Mermaid 数据接口，不解析源码字符串。
async function readMermaidModel(mermaid, source, descriptions) {
  const parsed = await mermaid.parse(source);
  if (!['flowchart-v2', 'flowchart', 'flowchart-elk'].includes(parsed.diagramType)) {
    return {reason: `${parsed.diagramType} 尚未适配 qv 绘制`};
  }
  // Mermaid 11.12.0 没有公开通用 AST；将版本相关接口隔离在此处。
  const diagram = await mermaid.mermaidAPI.getDiagramFromText(source);
  const db = diagram.db;
  if (!db.getVertices || !db.getEdges || !db.getSubGraphs || !db.getDirection) {
    return {reason: 'Mermaid 数据接口不兼容'};
  }
  const vertices = [...db.getVertices().values()];
  const groups = db.getSubGraphs();
  const links = db.getEdges();
  const ids = new Set(vertices.map(v => v.id));
  const supportedShapes = new Set(['square', 'round']);
  if (!vertices.length || vertices.some(v => !supportedShapes.has(v.type || 'square') || v.labelType === 'markdown')) {
    return {reason: '此图包含尚未适配的节点形状或富文本'};
  }
  if (vertices.some(v => v.styles?.length || v.classes?.length) || links.some(e => e.style?.length || e.classes?.length)) {
    return {reason: '此图包含自定义样式，保留原始语义'};
  }
  if (links.some(e => !ids.has(e.start) || !ids.has(e.end) || !['arrow_point', 'arrow_open'].includes(e.type))) {
    return {reason: '此图包含分组端点或尚未适配的箭头类型'};
  }
  if (groups.some(g => g.nodes.some(id => !ids.has(id)))) {
    return {reason: '嵌套分组尚未适配 qv 绘制'};
  }
  const direction = db.getDirection() || 'TB';
  if (groups.length && (!['TB','BT'].includes(direction) || groups.some(g => g.dir))) return {reason: '此分组方向尚未适配 qv 布局'};
  if (links.some(e => e.start === e.end)) return {reason: '自环尚未适配 qv 连线'};
  const iconFor = label => {
    const rules = [
      [/网关|gateway/i, 'network'], [/web|网页|浏览器/i, 'monitor'],
      [/移动|手机|app\b/i, 'smartphone'], [/认证|登录|auth/i, 'key-round'],
      [/内容|文档|content/i, 'file-text'], [/搜索索引|index/i, 'scan-search'],
      [/搜索|search/i, 'search'], [/后台|任务|worker/i, 'workflow'],
      [/postgres|mysql|数据库|database|\bdb\b/i, 'database'], [/redis|缓存|cache/i, 'zap'],
      [/对象|文件存储|storage|object/i, 'archive'], [/队列|queue/i, 'list-tree'],
      [/api|服务|server/i, 'server']
    ];
    return rules.find(([pattern]) => pattern.test(label))?.[1] || null;
  };
  const nodes = vertices.map(v => ({id: v.id, name: v.text || v.id, icon: iconFor(v.text || v.id),
    description: descriptions[v.id] || '', layer: 0}));
  const byId = new Map(nodes.map(n => [n.id, n]));
  let layers;
  if (groups.length) {
    const memberships = new Map();
    for (const g of groups) for (const id of g.nodes) {
      if (memberships.has(id)) return {reason: '重叠分组尚未适配 qv 绘制'};
      memberships.set(id, g.id);
    }
    if (nodes.some(n => !memberships.has(n.id))) return {reason: '部分分组尚未适配 qv 绘制'};
    layers = groups.map(g => g.title || g.id);
    groups.forEach((g, i) => g.nodes.forEach(id => {byId.get(id).layer = i;}));
  } else {
    const degree = new Map(nodes.map(n => [n.id, 0]));
    links.forEach(e => degree.set(e.end, degree.get(e.end) + 1));
    const queue = nodes.filter(n => degree.get(n.id) === 0);
    for (let i = 0; i < queue.length; i++) {
      const n = queue[i];
      for (const e of links.filter(e => e.start === n.id)) {
        const next = byId.get(e.end);
        next.layer = Math.max(next.layer, n.layer + 1);
        degree.set(e.end, degree.get(e.end) - 1);
        if (degree.get(e.end) === 0) queue.push(next);
      }
    }
    if (queue.length !== nodes.length) return {reason: '无分组回路尚未适配 qv 布局'};
    layers = Array.from({length: Math.max(...nodes.map(n => n.layer)) + 1}, () => '');
  }
  if (links.some(e => Math.abs(byId.get(e.start).layer - byId.get(e.end).layer) !== 1)) return {reason: '同层或跨多层连线尚未适配 qv 路由'};
  return {data: {nodes, layers, direction, grouped: !!groups.length,
    edges: links.map(e => ({from: e.start, to: e.end, async: e.stroke === 'dotted',
      thick: e.stroke === 'thick', arrow: e.type !== 'arrow_open', label: e.text || ''}))}};
}
