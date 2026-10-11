# sequence 自主审视记录

状态：已完成本轮自主优化与浏览器核对，待用户验收；尚未 checked。

改动：参与者与消息按实测换行、来源／目标详情及密集动效时长。设计契约见仓库 DESIGN.md 及 Mermaid reference 的对应段落。源解析、布局、绘制职责分离，未删除真实节点／关系／数值来压缩图形。

样例：[sequence-normal.json](sequence-normal.json) 与 [sequence-stress.json](sequence-stress.json)。源语义以实际 Mermaid11.12 解析结果核对，不以重复作者数据代替。

## 验证

- 布局／响应式：常规与压力、light/dark、320/736px，共8组；文字外溢、场景边界、消息／分类标签重叠、根布局溢出检查。expanded 850px高度的完整场景 fit、返回inline与600/400px resize已检查。
- 交互：实际按钮键盘聚焦、Escape、详情是否溢出及与触发对象间距；保持真实图类型的交互语义。
- 动效：常规真实动效检查，hover／resize不重播，完整离场再重入重播；reduced模式最终静态。
- 明暗：真实computed样式检查主要文字和关键线条对比，记录contrast-results.json；不将此局部检测表述为整图WCAG认证。
- 数据：normal/stress解析模型与实际名称／节点／关系／标记或数值一一核对，记录semantic-results.json；额外fallback／零值／参数样例见extra-results.json。
- 完整证据汇总：[REVIEW.md](REVIEW.md)、results.json、behavior-results.json。以上是隔离浏览器和模拟宿主展开事件证据；真实Codex消息流、宿主toolbar／clipboard／可见性恢复由用户验收。

## 明天验收

先看常规的层级和视觉重心，再看压力图的长文本、完整内容和局部详情。若认可，由用户将 TODO 对应项勾选。

补查：时序图自动滚动停稳后恢复键盘详情，Escape同时取消待恢复对象。 常规／压力的首、中、末详情定位已核对。
