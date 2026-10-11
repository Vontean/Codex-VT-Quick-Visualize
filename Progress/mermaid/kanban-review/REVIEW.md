# Kanban 首轮审视

2026-10-12。使用当前正式模板，未修改渲染器，未checked，未提交。模拟常规4列/6卡，压力7列/39卡；压力含空列、重复名称、无元数据卡、长中文与连续英文标题、长负责人、票据和说明。正式产物位于当前会话visualizations目录，kanban-review-normal.html与kanban-review-stress.html。

## 核对结果

- 数据：实际Mermaid DB列/卡ID、顺序、名称、列归属、元数据与计数逐项一致。空列保留，全部39卡保留；卡片不表达任务时长或完成率。
- 布局：卡片文字与元数据正常换行，无卡片间重叠。连续英文列标题溢出：列232px，内容scrollWidth596px。中文长标题能换行并保持共同行头高度。长说明浮层虽在root内，实际覆盖14个正文/元数据/标题元素。
- 响应式：双主题320/736px共8组；消息流局部横向滚动，root无横向溢出。展开无卡片框裁切，但736px压力图scale约0.354，14px正文约5px显示，完整性与可读性冲突；320px约0.183。返回恢复原scrollLeft300。连续400/600/736/320宽度与模式切换无window.error。
- 对比：真实sandbox背景及半透明文字合成后，亮色标题/正文约17.08:1，元数据7.81:1，计数3.24:1；暗色分别17.76:1、10.61:1、5.21:1。亮色12px计数偏淡，卡片边界轻。contrast-results.json为最终对比证据（解析CSS token原文不能当计算后背景色）。
- 动效：常规最长完成680ms、压力1150ms；标题300ms/8px、卡片240ms/8px，按列/行错峰。常规hover/resize未重播，完整离场再进入replays从1变2；减少动态效果为0动画。浏览器检查不替代真实宿主帧率与加载时机体验。
- 交互：常规6卡/压力39卡逐一Tab，全部自动横向入视口；Escape取消浮层，hover仅激活当前卡。常规阶段浮层无正文遮挡，但信息与所在列标题重复；长说明有遮挡。卡片属于查看行为，当前无拖拽/编辑/筛选。
- 回退：富文本与ticketBaseUrl实例均为native，有明确原因，不启用qv viewport。

## 证据

build.py、check.cjs、extra.py、extra.cjs、contrast.cjs可复现本轮。results.json（8组）与extra-results.json（Tab/回退/动画），contrast-results.json、normal/stress双主题宽窄及展开截图。仅建立审视基准；待用户指定值得修复的项后修改模板。

## 胶囊看板设计试作

按用户参考试作列6%色底、圆点胶囊与同色计数，白色无阴影/无默认边框卡片，内容16px，人员图标+姓名，四段优先级+原等级。列标题显示限制12字，完整原始名称保留可访问标签。票据保持标识符语义，灰色置于人员上方；真实description单独在卡内完整展示，不再弹阶段浮层。悬浮仅蓝色边框。深色模式使用对应宿主背景，不强制白色。

redesign-check.cjs对照实际Mermaid DB核对列/任务/字段与分段等级、字数限制、默认边框/阴影、ticket顺序、无浮层、hover仅改变边框，双主题普通/压力4组及320/400/600/736变化与展开返回无错误。redesign-results.json及redesign-*.png。Python30项通过。源码与本机qv同步，尚未checked、未提交此设计。

## 完成

2026-10-12用户确认checked，Kanban完成。永久回归tests/mermaid-kanban-review-check.cjs，对应普通fixture与kanban-review-stress.json；当前进度5/18。渲染职责仍独立于模型，复用共享viewport，ResizeObserver延后一帧布局。
