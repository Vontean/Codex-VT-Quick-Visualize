# sankey 自主审视记录

状态：2026-10-12 用户明确确认“All checked”，本图 checked，验收完成。

改动：近对象详情、原始流量及极小流保留。设计契约见仓库 DESIGN.md 及 Mermaid reference 的对应段落。源解析、布局、绘制职责分离，未删除真实节点／关系／数值来压缩图形。

样例：[sankey-normal.json](sankey-normal.json) 与 [sankey-stress.json](sankey-stress.json)。源语义以实际 Mermaid11.12 解析结果核对，不以重复作者数据代替。

## 验证

- 布局／响应式：常规与压力、light/dark、320/736px，共8组；文字外溢、场景边界、消息／分类标签重叠、根布局溢出检查。expanded 850px高度的完整场景 fit、返回inline与600/400px resize已检查。
- 交互：实际按钮键盘聚焦、Escape、详情是否溢出及与触发对象间距；保持真实图类型的交互语义。
- 动效：常规真实动效检查，hover／resize不重播，完整离场再重入重播；reduced模式最终静态。
- 明暗：真实computed样式检查主要文字和关键线条对比，记录contrast-results.json；不将此局部检测表述为整图WCAG认证。
- 数据：normal/stress解析模型与实际名称／节点／关系／标记或数值一一核对，记录semantic-results.json；额外fallback／零值／参数样例见extra-results.json。
- 完整证据汇总：[REVIEW.md](REVIEW.md)、results.json、behavior-results.json。以上是隔离浏览器和模拟宿主展开事件证据；真实Codex消息流、宿主toolbar／clipboard／可见性恢复由用户验收。

## 验收说明

先看常规的层级和视觉重心，再看压力图的长文本、完整内容和局部详情。若认可，由用户将 TODO 对应项勾选。

补查：桑基浮层首选200px宽，标题14px/20px／600，主标签＋次级灰色数值；标题组12px、条目6px间距。按真实曲线及带宽避让当前所有活跃流带，采样缓存且不改变场景尺寸。常规／压力 × 明暗 × 320/736px，8组核对节点与流带的首／中／末详情及展开；独立3px采样验证与高亮流带无交叉；真实鼠标流带悬浮另测通过。XY及常规／扩展雷达6组验证同一数值浮层层级，Python30项通过。证据 sankey-popover-results.json、sankey-popover-pointer-results.json、popover-hierarchy-results.json。仍待用户验收。
