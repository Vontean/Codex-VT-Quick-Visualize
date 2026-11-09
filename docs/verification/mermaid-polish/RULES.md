# Mermaid 2.0.54 产品规则迁移映射

正式源码：`skill/quick-visualize/`。参考 MineCodex `v2.0.54` 最终 RESULT（读至清理记录），含 `449ac54`、`b92a0eb`、`5ac3d7e`、`bb3e491` 后续修正。不迁移 MCX 宿主桥、提示删减和下载适配。

| 编号 | 产品规则 | 正式 assets 文件 / 符号 | 验证结果 |
| --- | --- | --- | --- |
| 1 | 保留可容纳的作者方向 | `mermaid-layout.js` — `prepareFlowchartLayout / prepareMermaidLayout` | 通过：browser-results.json（浅深色/常规压测/宽窄）；源码规则核对；宿主视觉待用户验收 |
| 2 | 超宽交换 LR/TB 重排 | `mermaid-layout.js` — `prepareFlowchartLayout / prepareMermaidLayout` | 通过：browser-results.json（浅深色/常规压测/宽窄）；源码规则核对；宿主视觉待用户验收 |
| 3 | 两轴均超宽取较窄者并滚动 | `mermaid-layout.js` — `prepareFlowchartLayout / prepareMermaidLayout` | 通过：browser-results.json（浅深色/常规压测/宽窄）；源码规则核对；宿主视觉待用户验收 |
| 4 | BALANCED 分支居中 | `mermaid-layout.js` — `prepareFlowchartLayout / prepareMermaidLayout` | 通过：browser-results.json（浅深色/常规压测/宽窄）；源码规则核对；宿主视觉待用户验收 |
| 5 | 同组回流反向端口、跨组外侧通道 | `mermaid-layout.js` — `prepareFlowchartLayout / prepareMermaidLayout` | 通过：browser-results.json（浅深色/常规压测/宽窄）；源码规则核对；宿主视觉待用户验收 |
| 6 | 流程 MODEL_ORDER 断环 | `mermaid-layout.js` — `prepareFlowchartLayout / prepareMermaidLayout` | 通过：browser-results.json（浅深色/常规压测/宽窄）；源码规则核对；宿主视觉待用户验收 |
| 7 | 连线起点序号徽标、双向消息避让、标签测量 | `mermaid-sequence.js` — `renderMermaidSequence` | 通过：browser-results.json（浅深色/常规压测/宽窄）；宿主视觉待用户验收 |
| 8 | 8×8 深色箭头 | `mermaid-sequence.js` — `renderMermaidSequence` | 通过：browser-results.json（浅深色/常规压测/宽窄）；宿主视觉待用户验收 |
| 9 | XY 分类至少 16px 并平分绘图区 | `mermaid-xy.js` — `renderMermaidXY` | 通过：browser-results.json（浅深色/常规压测/宽窄）；宿主视觉待用户验收 |
| 10 | 横轴抽稀、单行省略、完整 title、隐藏项键盘可达 | `mermaid-xy.js` — `renderMermaidXY` | 通过：browser-results.json（浅深色/常规压测/宽窄）；宿主视觉待用户验收 |
| 11 | 纵轴标题置顶并省略 | `mermaid-xy.js` — `renderMermaidXY` | 通过：browser-results.json（浅深色/常规压测/宽窄）；宿主视觉待用户验收 |
| 12 | 一级分支系列色及子树传递 | `mermaid-mindmap.js` — `renderMermaidMindmap` | 通过：browser-results.json（浅深色/常规压测/宽窄）；宿主视觉待用户验收 |
| 13 | 2/1.5/1px 层级连线 | `mermaid-mindmap.js` — `renderMermaidMindmap` | 通过：browser-results.json（浅深色/常规压测/宽窄）；宿主视觉待用户验收 |
| 14 | 中间层文字轻染色、分支 hover 色 | `mermaid-mindmap.js` — `renderMermaidMindmap` | 通过：browser-results.json（浅深色/常规压测/宽窄）；宿主视觉待用户验收 |
| 15 | 以实际卡片尺寸消除原生中心距过近问题 | `mermaid-layout.js` — `prepareNativeGeometry / prepareArchitectureLayout` | 通过：browser-results.json（浅深色/常规压测/宽窄）；源码规则核对；宿主视觉待用户验收 |
| 16 | 中心点按 24px 容差聚类、重排原生行列 | `mermaid-layout.js` — `prepareNativeGeometry / prepareArchitectureLayout` | 通过：browser-results.json（浅深色/常规压测/宽窄）；源码规则核对；宿主视觉待用户验收 |
| 17 | 格位冲突、组框覆盖或布线失败回退 ELK | `mermaid-layout.js` — `prepareNativeGeometry / prepareArchitectureLayout` | 通过：browser-results.json（浅深色/常规压测/宽窄）；源码规则核对；宿主视觉待用户验收 |
| 18 | Git 分支及提交读取 | `mermaid-git.js` — `readMermaidGitModel / renderMermaidGit` | 通过：browser-results.json（浅深色/常规压测/宽窄）；源码规则核对；宿主视觉待用户验收 |
| 19 | Git 横向泳道／纵向日志 | `mermaid-git.js` — `readMermaidGitModel / renderMermaidGit` | 通过：browser-results.json（浅深色/常规压测/宽窄）；源码规则核对；宿主视觉待用户验收 |
| 20 | 提交形状、七位自动哈希、分支高亮 | `mermaid-git.js` — `readMermaidGitModel / renderMermaidGit` | 通过：browser-results.json（浅深色/常规压测/宽窄）；源码规则核对；宿主视觉待用户验收 |
| 21 | 7%/14% 软卡片、8px 圆角与间距 | `mermaid-timeline.js` — `renderMermaidTimeline` | 通过：browser-results.json（浅深色/常规压测/宽窄）；源码规则核对；宿主视觉待用户验收 |
| 22 | 事件圆点对齐首行 | `mermaid-timeline.js` — `renderMermaidTimeline` | 通过：browser-results.json（浅深色/常规压测/宽窄）；源码规则核对；宿主视觉待用户验收 |
| 23 | 桑基宽度 320+(列数−1)×136 | `mermaid-sankey.js` — `renderMermaidSankey` | 通过：browser-results.json（浅深色/常规压测/宽窄）；源码规则核对；宿主视觉待用户验收 |
| 24 | 桑基高度与节点间距按标签计算 | `mermaid-sankey.js` — `renderMermaidSankey` | 通过：browser-results.json（浅深色/常规压测/宽窄）；源码规则核对；宿主视觉待用户验收 |
| 25 | 152px 两行标签及一致的测量结构 | `mermaid-sankey.js` — `renderMermaidSankey` | 通过：browser-results.json（浅深色/常规压测/宽窄）；源码规则核对；宿主视觉待用户验收 |
| 26 | 雷达填充 14%/24%/3%，通用与预设同步 | `mermaid-radar.js + radar-chart.html + chart-detail-position.js` — `renderMermaidRadar / nearbyRadarDetails` | 通过：browser-results.json（浅深色/常规压测/宽窄）；interaction-results.json；宿主视觉待用户验收 |
| 27 | 优先避让选中多边形，再避让其他图形与标签 | `mermaid-radar.js + radar-chart.html + chart-detail-position.js` — `renderMermaidRadar / nearbyRadarDetails` | 通过：browser-results.json（浅深色/常规压测/宽窄）；interaction-results.json；宿主视觉待用户验收 |
| 28 | 单行居中、换行单列居中且项左对齐、名称省略与 title | `chart-legend.js` — `alignMermaidLegends` | 通过：browser-results.json（浅深色/常规压测/宽窄）；boundary-results.json；宿主视觉待用户验收 |
| 29 | 雷达轴标签按方位锚定、两行省略、按侧排开 | `mermaid-radar.js` — `renderMermaidRadar` | 通过：browser-results.json（浅深色/常规压测/宽窄）；源码规则核对；宿主视觉待用户验收 |
| 30 | 象限／雷达／桑基非空标题显示 | `mermaid-title.js + mermaid-model.js` — `readMermaidTitle / readMermaidModel` | 通过：browser-results.json（浅深色/常规压测/宽窄）；源码规则核对；interaction-results.json；宿主视觉待用户验收 |
| 31 | 象限 6% 系列底色、外框、象限名外角 | `mermaid-quadrant.js` — `renderMermaidQuadrant` | 通过：browser-results.json（浅深色/常规压测/宽窄）；源码规则核对；宿主视觉待用户验收 |
| 32 | 显式统一 animate 调用、.92 淡入与共享曲线 | `chart-motion.js` — `animateMermaidEntry / mermaidEntryProgress` | 通过：browser-results.json（浅深色/常规压测/宽窄）；1953个WA调用≤1200ms；test_mermaid_polish.py；宿主视觉待用户验收 |
| 33 | 同批 Web Animations 延迟与时长同比压缩至 1200ms | `chart-motion.js` — `animateMermaidEntry / mermaidEntryProgress` | 通过：browser-results.json（浅深色/常规压测/宽窄）；1953个WA调用≤1200ms；test_mermaid_polish.py；宿主视觉待用户验收 |
| 34 | 流程 hover 先完成入场动画 | `mermaid.html` — `showTip / queueNodeHover` | 通过：browser-results.json（浅深色/常规压测/宽窄）；boundary-results.json；宿主视觉待用户验收 |
| 35 | 气泡 140ms/.97 入场，共享定位指向触发对象，相邻 hover 延迟为 0 | `mermaid-presentation.js + chart-polish.css` — `placeMermaidDetail / createMermaidHover` | 通过：browser-results.json（浅深色/常规压测/宽窄）；interaction-results.json；宿主视觉待用户验收 |
| 36 | 气泡共用边框、圆角、内边距、标题、数值与主题表面 | `chart-polish.css` — `共享浮层、文字 token` | 通过：browser-results.json（浅深色/常规压测/宽窄）；interaction-results.json；宿主视觉待用户验收 |
| 37 | h3、状态节点、时间线阶段、ER 类型、XY 刻度的文字层级 | `chart-polish.css` — `共享浮层、文字 token` | 通过：browser-results.json（浅深色/常规压测/宽窄）；源码规则核对；宿主视觉待用户验收 |
| 38 | 移除节点组开关、配置与下钻 | `mermaid.html + mermaid-navigation.js` — `完整图 / mermaidScopeView（状态专用）` | 通过：browser-results.json（浅深色/常规压测/宽窄）；boundary-results.json；宿主视觉待用户验收 |

附加回归：状态导航；Quadrant / ER / Class / Journey 宽窄及窄转宽；Radar / Sankey 非空标题；预设 offsetParent 坐标；原生展开返回；原生回退无增强 viewport。证据和最终状态见 RESULT.md。
