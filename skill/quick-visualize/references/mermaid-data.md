# Mermaid 数据图

按图型读取对应小节。输入契约见 [Mermaid](mermaid.md)，共享呈现规则见 [Charts](charts.md)。本文件只规定各图型的语义、专用布局与交互；局部入场时长受Charts的批次预算约束。

## Pie

- 从 Mermaid11.12 getSections Map 读取源顺序、独立名称、原始非负权重、showData、title，不合并极小份额或发明单位。正有限总量必须大于0；零总量与rich label明确原生回退，零值仍留在图例。
- 复用 Donut 的同一绘制实现并映射源数据。圆环约75%内径、中心总计、host系列色、短数据直标／长数据底部图例沿用已确认方案。Mermaid源数据可多于独立预设的6类，颜色按6个token循环，完整列表保留。
- 只有正权重绘制弧；角度严格按原值分配，零值没有扇区或缺口，极小份额不会被最小可视角度撑大。showData 在图例／直标带原值，原始值不做小数位截断；弧路径坐标保留9位小数，避免接近100%的弧线端点被舍入为同一点。中心大数自动缩小以容纳，长名称换行。
- 650ms圆环入场，直标随入场淡入；普通resize/hover不重播，完整退出后重入可重播，reduced静态。Pie的图例、直标及圆环悬浮只突出对应份额并更新中心信息，不显示popover；独立donut预设保留自身详情能力。使用宿主展开预览，无额外全屏容器。

## XY

分类至少16px，按绘图区平分；刻度抽稀且单行省略，完整名称保留title与键盘详情。

- Mermaid11.12 getXYChartData/getChartConfig 保留真实坐标、分类顺序、数值域、orientation和bar/line顺序。每个分类保留源数组索引，重复分类名称是不同的位置，不能用名称去重或将数据聚到首项。此版本无业务系列名，使用源类型／序号，不发明业务含义。
- 正负柱从实际零基线绘制，柱宽≤24px，折线连接真实坐标，横轴分类按可用宽度抽稀并单行省略，完整名称保留title及键盘详情。水平布局按分类数量和各标签可读槽位增长高度；窄消息流只滚动绘图区，值参考及标题保留，展开整体fit并恢复返回位置。
- 悬浮／键盘比较该索引下所有系列的精确值，突出当前分类的柱和点，其余降到.18。近对象详情距触发对象≤32px；滚动后恢复键盘详情，Escape取消。重复名称的导线、命中区、标签与详情全部使用同一索引。
- 详情使用共享主题底色、12px圆角、12px×14px内边距、最大240px宽；14px/20px标题与12px/18px数据行用分隔线区分。数据行对齐系列色标、次要色系列名和主文字色500字重等宽数字。以当前分类真实柱子和点的屏幕边界为避让对象，在侧边保留12px间距；可用空间不足时缩窄宽度并换行，不盖住当前标记。展开保留浮层字号，不随场景缩放。
- 柱650ms同时增长，线1200ms描画；hover/resize不重播，完整退出重入／可见性恢复按既有契约重播，reduced/expanded静态。rich axis HTML和额外说明明确回退。

## Radar

- 从 Mermaid11.12 DB 读取有序axis、positional/keyed curve、名称、min/max、ticks、graticule和showLegend；非零最小值必须保留。径向距离编码值，面积不解释为总分；非法范围／rich label／额外说明明确回退。
- 当min=0、polygon、5ticks、显示图例、≤8轴、≤4系列、轴名≤12字时，直接复用 Radar 预设的同一绘制实现。不能满足预设表达能力时，保留原增强绘制，支持非零min、circle、长名称、多轴多系列，不删除数据或更改语义以硬塞预设。
- 两条路径沿用相同设计：host系列色、细中性网格、隐藏数字刻度标签，900ms 共享曲线径向展开；点优先读取所属对象，轴比较全部对象，图例保持身份；填充、气泡与图例排版遵循 Charts 的 Radar 规则。
- 雷达详情首选188px宽，点／多边形显示完整对象指标，标题携带对象色标；轴对比行携带各系列色标。图例hover、click、focus只突出系列。层级及定位使用Charts中的Radar规则。
- 扩展绘制的可读intrinsic scene可横向滚动，展开fit并恢复返回位置。reduced/resize/展开不重播，完整离场再重入可重播；真实宿主可见性恢复仍需人工验收。

## Sankey

正文最小宽度为`320+(列数−1)×136`，高度与节点间距按152px两行标签的同结构测量计算。

- 实际 Mermaid11.12 getGraph/getConfig 保留源ID／顺序／重复边／原始正数量、alignment、source/target/gradient颜色、showValues及prefix/suffix，不另外解析CSV，不推导源到终点的完整路径。当前固定版本的Unicode语法限制应显式报告，不偷偷改名；采用合法ASCII源做样式验证。
- D3-sankey0.12.3计算DAG位置，宽度与高度按同一数值比例，包括subpixel极小流；透明命中路径提供容错，不能加宽可见流。节点值为max(inflow,outflow)，详情分别说明真实流入／流出，边说明原量及两端对应份额。
- 名称14px／值12px，152px标签最多两行省略，完整名称保留title；测量使用相同结构，高度参与节点间隔；inline intrinsic横向滚动，expanded紧凑列距后整体fit，返回恢复。浮层就近关联真实节点／流带，优先保证不遮挡当前活跃流带，不预留无用底部详情区。
- 桑基详情首选200px宽，表面与文字层级遵循Charts。按真实曲线及流带宽度采样，在触发对象附近避让当前活跃流带；节点详情避开其直接相连的活跃流带。滚动时转换实际屏幕坐标；详情不改变图表高度。
- 1000ms 共享曲线水平mask保持比例；hover/resize不重播，reduced/expanded静态，完整退出后20%重入可重播。零值／非正值／cycles／custom literal color 保留明确native fallback；原生自己无法绘制的循环应显示错误，不能假称回退成功。

## Quadrant

- Preserve source-order points, complete names, exact normalized0–1 coordinates, axis ends, four quadrant captions and title. Q1 upper-right, Q2 upper-left, Q3 lower-left, Q4 lower-right. Exactly.5 stays a boundary. Descriptions use source-order `point-1`, etc.; unknown IDs are errors.
- Pinned11.12 adapter captures original point/axis/class parser callbacks and restores them in `finally`. Native `parseStyles` interprets colors; no second source parser or SVG-derived data. Semantic categories use Mermaid `Point:::category: [x,y]` (class IDs use ASCII identifiers in pinned11.12); same category shares color. Optional `classDef category color: #109060` and color-only point styling preserve explicit colors. Classes without explicit color use host series2–6; unclassified points use series1 blue, never quadrant colors. Custom radii/strokes and rich labels visibly retain native fallback.
- Draw two cross axes, no outer grid frame or0/.5/1 ticks. Axis ends are complete wrapped14px medium text in shallow gray content-width capsules (8px/12px padding,999px radius,8% muted-foreground/background mix) at the four cross endpoints; ordinary text is not heuristically split into a key and explanation. Source quadrant captions remain muted12px and sit in their respective quadrants next to the origin with12px clearance. Coordinates never shift for label layout.
- Point labels stay adjacent when there is space, with one line and ellipsis at144px maximum width; full names remain accessible and in details. Local96px neighborhoods hide labels at3 points, or at2 points with measured text occupancy over14%. Any label without an adjacent collision-free placement also hides; the actual point and complete accessible name remain. No far-away label packing. Hidden points support keyboard focus; one nearest-point picker groups exact coincidences without merging entities.
- Details stay next to the point, clamped to visible bounds; long full content scrolls in a maximum320px themed popover. Complete coordinates, quadrant/boundary, category and descriptions remain available. When the diagram has any category, details show matching color dots; unclassified points form an implicit blue default category without requiring `:::default` in the source. Diagrams without categories keep neutral details. Coincident entity details preserve every represented category, including implicit default. No permanent reading region or reserved empty space, and no search for a distant text-free position.100ms pointer leave bridge permits moving into the popover. Escape/scroll/blur clear it.
- Intrinsic640–736px geometry with horizontal scroll; native expanded preview fits the complete scene and restores saved inline scroll. Point240ms and visible label300ms/4px with80ms source-order stagger; reduced/expanded/resize are static. Resize redraw is coalesced into the next frame. Real host document-hidden restoration and native buttons remain separate acceptance boundaries.

