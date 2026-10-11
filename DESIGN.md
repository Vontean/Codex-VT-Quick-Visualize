# Chart design

- Readability comes before reference-style fidelity. Evaluate label hierarchy, contrast and data lookup before visual decoration; comparison samples do not define qv's design language.
- Gantt task names stay inside their time bars: use one line when it fits, otherwise wrap to at most two lines and truncate the remainder. Hover/focus details retain the complete name. Never lengthen the time bar to fit its label. Do not repeat phases under every task; use meaningful group headings. Duration information must remain readable independently of bar color.
- Use host foreground, border, popover and stable `--viz-series-N` tokens. No imported Lieflat gallery code or fixed Mono palette.
- Figure top padding: 32px. Title-to-plot gap: 32px. Centered wrapping legend beneath plot, gap: 20px.
- Floating details: 12px radius, 12px × 14px padding, subtle shadow, boundary constrained. No pinned tooltips or helper footers. User data enters text nodes, never HTML.
- Cartesian frames keep left/bottom axes and internal grid lines only. Bar width is at most 24px; dense charts omit value labels.
- Entry motion replays after complete viewport exit and 20% re-entry, or document visibility restoration. Resizes and ordinary hovers do not replay; reduced motion disables entry animation.
- Bars grow upward in 580–680ms with simultaneous starts. Lines trace their path in 1200ms with a moving value and matching area reveal.
- Donut reveals outward around the ring in 650ms. Direct labels use 130ms + index × 32.5ms delay and 260ms ease fade; the centered number and subtitle share one centered wrapper. Zero values draw no slice or angular gap; gaps shrink with the smallest positive share without changing data proportions. Direct labels need <=4 categories, >=8% minimum share, short labels and adequate width.
- Radar vertices expand in 900ms quartic-out, keeping stroke and marker sizes constant. Numeric grid labels stay hidden. Points take priority over axes; axes compare objects, points/edges/areas describe one object. No native SVG title tooltip.
- Radar inactive strokes/markers: .10 opacity; fill: .003; legend: .32. Object markers belong in tooltip headings, not every dimension row. Nearby tooltip candidates use 16–40px pointer distance, minimizing polygon overlap within that range.

The runtime entrypoint stays minimal; data contracts live in each reference. Standalone browser checks do not replace actual Codex message-flow acceptance.

## 节点图表的共同设计原则

这些原则适用于流程图、状态图、架构图等节点关系图。先按共性自查，再核对该图表的独立语义；不把所有图表强行画成同一种图。

- 信息优先：默认只保留理解任务所需的名称、关系和层级。已经可见的信息不重复放进浮层；进入分组用箭头表达，不增加“外部 · 查看”等说明。
- 文本先测量再布局：短文本自然居中，超过阈值才换行；容器根据真实字体、字号、行高和说明内容增长。菱形等形状按内部可用区域测量，不能让短词被挤成逐字换行。独立行只使用自己的内容高度。
- 布局有阈值：普通图保留源码阅读方向；规模、长边和长宽比同时超限时，才在保留分组的前提下平衡布局，趋近1:1以便展开查看。当前流程图阈值为至少16节点、长边超过2400px、长宽比超过3:1。方向、回流、自环与所有关系始终保留。状态图有明确出入，保留源码纵向或横向展开，不使用蛇形折行平衡。
- 层级从里到外：叶节点使用主题背景；包一层用浅灰，再包一层回到背景，逐层交替。灰面使用 `color-mix(in srgb,var(--muted) 18%,var(--background))`，不累加透明度而越叠越深。形状图保留真实轮廓。
- 复杂层级可聚焦：复合容器支持点击下钻；当前层完整呈现直接孩子和跨边界关系，路径保留返回入口。路径分段可以切换同层分组，总览没有同层菜单。普通叶节点不承担层级导航。
- 悬浮稳定：突出当前节点及其实际关系，节点、线与箭头同步。快速扫过不反复播放进场动效；需要悬浮缓冲时，以最后一次停稳为准并取消旧计时。退出、滚动与切换视图清除旧详情。
- 主题分别校准：浅色沿用已确认的轻边界；暗色仅补足必要的连线、箭头和文字对比度。不要为了暗色把浅色灰面整体加深。
- 交互按需：浮层只补充不可见的说明，使用完整文本并避开节点、标签和方向证据。内容包含层次与关系时，按实际语义组织标题、关系和正文，不拼成一段长文本；状态转移浮层上方呈现起始状态 → 目标状态，下方分隔展示转移说明。普通消息流保留可读字号，只让绘图区滚动；展开适配完整图，减少动态效果时静态呈现。
- 验证按风险：每次核对常规与压力数据、宽窄视口、明暗主题、真实悬浮与层级切换；关系完整性和真实运行表现分别验证。用户确认后才勾选该图表，并按图表边界原子提交。

## Mermaid architecture renderer

- Mermaid is the input language and parser. Enhanced diagrams are drawn by qv; do not display Mermaid SVG with superficial CSS changes. Internal graph data is derived by the parser, never authored a second time by the agent.
- Flowchart nodes retain 32px title spacing, 10px corners, host colors and 16px Lucide icons. Labels stay on one line until the measured text exceeds 228px (minus icon space); then wrap and grow the node height (minimum 48px). Ordinary nodes cap at 262px (including borders and padding); diamonds and circles widen to fit the centered text safely. Flowcharts fold only when all thresholds are met: at least 16 nodes, long dimension above 2400px, aspect ratio above 3:1. Large elongated graphs balance toward 1:1 within each preserved group; LR/RL/TB/BT determines the initial reading direction, while arrows preserve every relationship. Compact diagrams retain the layered layout.
- Curves share each side's center port. Use 1px strokes with muted foreground mixed at 26% against the background. Integrated arrows are 5px long and 4.4px wide; stop the shaft at the arrow base. Dim unrelated nodes to .22 and lines to .055. Keep semantic thick/dotted line distinctions.
- Grow node contents from .08 scale over 240ms, stagger layers by 220ms, reveal line length over 650ms and then arrows over 50ms. Replay without rebuilding on full exit and re-entry; honor reduced motion.
- Optional dark tooltips use white 12px text, 1.6 line height, 7px radius and 10px/12px padding. Rank nearby positions by related-node/line overlap and cursor distance. No persistent description section.
- When a line-style legend is needed, keep it centered with 20px top gap and 16px vertical padding; do not infer that every dotted relation means an asynchronous event.
- Unsupported source constructs fall back visibly with a concrete reason. Never flatten nested groups, replace decision semantics with ordinary cards, or market native Mermaid output as the accepted qv design.

Mermaid 架构图在窄消息流中仅绘图区横向滚动，保留分层并排结构和字号；标题、图例不随之滚动。所有 qv 类型（图表、Mermaid、表单、多选、排序与方案比较）共用整区点阵加载态：透明底、主题次级文字色、双明暗场、30fps、1.75s 透明度呼吸（.38–.56），点半径至少 0.8 CSS px，按本机 image-loading-state 运动参数独立适配；减少动态效果时呈静态点阵。首次绘制就绪后移除，不人为延时，也不在滚动重播时重现。滚动清除悬浮提示，重新悬浮按滚动后的节点坐标避让。

加载生命周期：统一 runner 包装所有类型，各模板在内容初始化与事件绑定完成后发送 qv:ready。异步 Mermaid 等待解析与首次绘制完成；同步表单等立即就绪。不设置最短展示时长，不为演示加载而延迟内容。

架构图端口：同侧同时出入时，入口与出口各偏离中心 7px，间距 14px；同向连接仍共用端口，仅单向的侧保持居中。

架构图作者必须为服务声明语义图标，中文标签优先使用 flowchart 的 lucide: 原生图标声明；architecture-beta 内置语义图标也可使用。源码明确指定的图标优先保留，不因无关节点或 icons:none 而整体消失。architecture-beta 与 icons:required 检查所有服务的图标；缺失时显示可修正的错误，不静默隐藏。未声明图标的普通 flowchart 仍保留 auto / none；不使用装饰性通用图标补位。

架构图图例仅解释已知语义，使用可选 legend.solid / legend.dotted；生成时默认实线；仅在区分明确的关系语义时使用多种线型，并必须用图例或线上的标注解释。不能省略说明，也不能用“实线连接 / 虚线连接”充当含义。外部源含义不明时先结合上下文确认，不机械推断同步与异步。

复杂架构保留嵌套容器边界、节点形状和连接方向。常见分层图沿用已确认的布局；复杂图由 ELK 计算位置，独立分组方向和 architecture-beta 端口约束使用 Mermaid 原生布局坐标，均由 qv 重绘。过长 flowchart 在每层容器内按源顺序折行，保留分组、回路与独立节点，再重新避让连线；architecture-beta 保留原有端口布局。复杂连线采用避让节点的圆角折线；连接到分组时，组内节点的悬浮高亮和 Tooltip 避让包含组边。

## Group navigation

- Grouped diagrams default to group browsing; the header switch restores the full layered/grouped architecture. Optional navigation: expanded starts with that switch off. Input remains Mermaid, without a second authored graph.
- Render direct children of the current group. Show descendant previews inside 184px group containers whose height follows visible members, with a title-row Lucide chevron. Single services retain 48px height; external context nodes use 64px height.
- Breadcrumb navigation sits 24px above the drawing, with no redundant back action; a right-aligned “节点组” label followed by its switch replaces counts. Click, Enter and Space enter a group. Restore each scope's horizontal scroll position on return.
- Preserve cross-boundary connections as labeled external nodes. Aggregate only edges with the same endpoints, direction, markers, line style and label; show the source connection count. Keep the original model immutable.
- Group previews use a quiet neutral fill and border, visible semantic-icon members and subordinate subgroup captions; normal services stay neutral. External nodes carry a textual external label. Keep 16px semantic icons, thin wires and near-node optional tooltips; no decorative canvas grid or editor chrome.
- Initial loading ends on readiness. Scope navigation keeps the old view until its real layout is ready; node and line growth then applies to the new scope. Reduced motion remains static.

## Architecture overview previews

- Overview groups expose up to eight actual service names/icons, nested subgroup captions and internal directed links. Report remaining members explicitly; drilldown retains the complete graph.
- Group headers are 14px, members 12px, subgroup captions/footer 11px; rows 32px, captions 26px. Use neutral surfaces and 14px member icons; no arbitrary category coloring or quantitative node sizing.
- Small LR/RL overviews retain source group order, draw forward relationships as cubic curves and return relationships around the outside. Preserve other directions through the general layout engine.
- Hovering a preview member highlights its actual neighbors and matching aggregate connections. Group click/keyboard navigation and optional tooltips remain available. Internal context is kept visible rather than hidden behind a total count.

- Group entry chevrons align to the title row right edge; remove the generic entry footer. Aggregated relationships use 22px circular number markers at the measured path midpoint, retaining separate semantic edge labels. Nested views share neutral surfaces, fine outlines, 12px service labels and 14px icons.

## Node-group navigation boundary

- Drilldown simplifies group nesting only. Entering a group shows all its direct nodes, subgroup previews and relevant boundary connections together, including disconnected nodes. Never turn normal service nodes into navigation steps or filter to a selected neighborhood.
- No node index or upstream/current/downstream mode. Ordinary nodes retain hover highlighting and optional descriptions. Group clicks and breadcrumbs are the only hierarchy navigation.
- Overwide LR/RL local views may use a narrower top-down layout when explicit source ports do not constrain it; preserve every visible node and relationship. Full-view mode keeps all original groups and relationships; elongated flowcharts fold for a balanced overview.
- Keep origin-aware group transitions, keyboard/reduced-motion bypass and complete-view switch. Animation must not add steps or conceal graph content.

## Mermaid expanded preview

- Every Mermaid reference enables the native Codex expanded preview through mode:wide. No custom fullscreen overlay.
- Shared viewport presentation covers enhanced qv diagrams only. Native fallback keeps its original SVG sizing, styling and behavior; no qv viewport controller is initialized. Inline labels retain their size and only the drawing scrolls. Expanded mode fits the whole current view to available width and height, without changing graph geometry or omitting nodes.
- Preserve inline scroll per scope when returning. Group navigation and the complete-architecture switch remain available; expansion does not change scope.
- Expanded views are static on entry and use correctly scaled tooltip obstacle coordinates. Native Copy as image remains a visible-area capture; it includes the complete diagram only after fit. Full-resolution export is a separate capability.

Mermaid shape fills: shaped nodes keep a transparent HTML backplate even when layer/group rules apply. The closed cylinder body follows the theme background; its internal arc is a separate unfilled stroke. ELK loading retains version 0.10.0 and tries the CSP-approved unpkg origin after jsDelivr errors or a 15s timeout. Native fallback remains unchanged.

## Mermaid sequence renderer

- 保留 Mermaid11.12 的参与者顺序、角色、消息方向、虚实线和箭头类型、自动编号、激活条、self message、alt/loop/par/critical 等控制框及 note 的源位置；未支持的 box、rich label、properties 等明确原生回退。
- 参与者标题按实际 DOM 换行测高，内容宽最多240px；消息最多288px并完整换行。每条消息按自己的高度预留空间，长文本不会覆盖前一条消息或将后续消息统一撑高。共享 intrinsic scene，展开整体 fit，返回保留滚动。
- 消息线与箭头使用明色#727a82／暗色#a3aab3，lifeline 更轻；次级小字使用60%／68%前景混色。参与者悬浮突出真实邻接消息；消息浮层分列表示来源、目标，再显示完整正文，距离触发对象不超过32px。不重复展示没有额外说明的参与者标题。
- 消息420ms依次描画，stagger=min(140ms,900ms/(条数−1))，180ms标签和60ms箭头随线到达。减少动态和展开静态；悬浮、resize 不重播，完整退出后重入可重播。

## Mermaid state renderer

- Preserve state semantics with at least48px neutral cards, names/body wrapping after20 Unicode characters with measured16px/24px title and12px/18px body,20px terminal boxes (solid start, double-circle end),32px choice diamonds and64×6 fork/join bars. Compound states are initially complete; clicking a compound header enters its direct-child scope with boundary connections and breadcrumbs. The 总览 breadcrumb restores the full view; hide the entire breadcrumb bar in that root view. State diagrams have no group switch. Preserve the source vertical/horizontal direction without folding. Group entry arrows share the title row immediately to its right. Leaf cards and containing groups follow the common containment surfaces.
- Within each parent scope, order layout and entry from actual initial states along transitions; retain every backward link and route it peripherally. Retries use side ports independent from main incoming/outgoing connections. Preserve declared direction.
- Use8px rounded bends,5px integrated arrows,12px condition labels with18px line-height and8px clearance from the associated wire. State condition labels have a transparent background; their transient details retain the popover surface. Theme-aware nodes, boundaries, labels and transient12px details follow existing qv tokens.
- Trigger/label bounds outrank sampled line segments in tooltip collision placement. Hover and focus highlight one state neighborhood or transition without pinning or deleting content.
- Initial nodes240ms, trace650ms, arrows50ms, labels180ms. Labels follow their transfer; reduced motion/fullscreen stay static. Scroll restoration must work whether the host sends globals before or after resizing its frame.

## Mermaid ER renderer

- Mermaid11.12 DB 是实体、别名、字段顺序、类型、PK/FK/UK、注释和关系基数的唯一来源。读取 getData 实际端点标记，避免 relSpec.cardA/cardB 的反向对应；getDirection 保留方向，字段名称不推导关系。custom style/class/rich label 明确原生回退。
- 实体白底14px圆角、标题14px/20px，技术ID另行显示；字段置于4%前景混色、8px圆角的内区。实体宽240–360px；key/type/name按实测分配，字段12px/18px换行，各行=max(30px,内容高度+12px)，不继承其他行高度。完整别名及长字段保留。
- 中性1.4px关系线和crow-foot标记使用明色#727a82／暗色#a3aab3，保留 identifying 实线与 non-identifying 虚线。每条关系独立端口，self loop 横向绕回；展开保持原几何。
- 标题突出实体邻域；字段只突出本行，有注释才显示详情；关系浮层分来源／目标／基数及关系说明，保持距触发文字≤32px，避免远距离避障。键盘自动滚动后恢复详情，Escape取消恢复。
- 卡片240ms、关系650ms、基数50ms；共享视口保留返回滚动，hover/resize 不重播，reduced/expanded静态。

## Mermaid class renderer

- Class model reads the fixed Mermaid11.12 DB's members, methods, classifiers, annotations, generic type, alias, namespaces and normalized endpoint symbols. Source owns relationship direction, pattern and multiplicity.
- Code-editor hierarchy: theme-background cards with14px corners; transparent headers with14px/600 foreground class titles,12px muted stereotypes and16px horizontal inset. Attributes/methods occupy separate4% neutral panels with8px corners and10px horizontal inset. Members use12px/20px system monospace; types teal, methods blue, visibility/parameters muted. Light/dark token pairs are teal#287d7b/#80c3ba, blue#35659f/#98b9ed. Abstract remains italic, static underlined. Attribute/method captions show actual counts.
- Measure complete labels and signatures before layout. Card widths hug natural content within240–320px; longer text wraps and rows grow from30px. Optional source descriptions appear inside the card. Namespaces use dashed neutral borders, theme-background surfaces and transparent titles. Wires render above namespaces and below cards; all contents remain visible without navigation.
- UML marks use1.4px neutral stroke (#727a82 light/#a3aab3 dark) with round caps/joins: equilateral hollow triangle (12px sides), rotated square diamond (12px diagonals), filled composition/hollow aggregation, and6×3px open association/dependency arrows. Short terminal segments scale closed marks uniformly without changing their proportions; line trimming uses the matching rear join. Keep8px rounded wire bends and original solid/dashed meanings. Relation captions wrap at180px and seek free space alongside their own path, avoiding cards, namespace captions and multiplicities.
- Hover settles70ms before selection;120ms leave buffer avoids transient resets. Highlight the actual class and row; unrelated cards fade to.26, unrelated relationships to.14. Retain syntax colors and add a blue card border/current-row surface. Only relation text shows a structured source → target popover with exact multiplicities, UML kind and description; card/member details do not pop over. Popover candidates stay12–28px around the triggering relation text, with a32px maximum rectangle gap; prefer local overlap over moving to distant cards. Native keyboard focus restores selection after auto-scroll; Escape cancels restoration.
- Large-layout comparison uses the flowchart threshold: at least16 nodes,2400px longest dimension and3:1 aspect ratio. Compare opposite ELK direction only then; accept only improved aspect ratio with area increase≤30%. Ordinary sources keep their direction; no forced square or inferred relationships. Shared expanded fit and inline scroll restore remain.
- Motion retains240ms cards and650ms trace; endpoint marks/multiplicity50ms after trace, label100ms from600ms. Complete exit/reentry replays; hover/resize do not. Reduced/expanded static. Native fallback has no qv viewport.

## Mermaid timeline renderer

- Mermaid11.12 DB owns source period order, contiguous sections and complete events. Read mutable getTasks once and copy; repeated names and empty periods remain distinct. Position encodes ordinal sequence, not duration.
- Inline columns216px/gap40px; expanded184px/gap24px, horizontal reading retained. Scene width hugs the actual columns and tail; expanded root is capped at this intrinsic width and centered, with whole-scene shrinking only when it exceeds the viewport. Columns keep12px padding with transparent backgrounds so the continuous timeline owns the visual emphasis; same section name shares a stable host series color. Complete13px/500 period names use theme foreground. Complete stage captions use stage color mixed55% with foreground and15% stage-tinted capsules,4px/10px padding and999px radius, kept inside their original contiguous span during scrolling with native horizontal sticky positioning; never rewrite caption left from scroll events.
- Events are plain complete14px/22px text beside a vertical rail, with22px rail-to-text offset,4px vertical padding and12px gaps. No card fill, border or shadow. 5.5px event dots share the stage color of their7px period point. Hover accents the actual event text blue, retaining dot colors; keyboard focus adds an outline. Optional period descriptions are visible in the event region; no tooltip/popover or hidden-information duplication.
- Measure stage/header heights before aligning a shared axis; each column retains its own body height.A continuous1px neutral horizontal axis carries7px stage-colored dots with2px theme-background rings. The axis extends120px beyond the final period and fades to transparent, conveying continuation without adding a period. Each neutral vertical rail ends at its own last event center; empty periods have no rail. Event dots align to the measured text row centers. Flat events remain flat; no inferred child relations. Text, source order and stage ownership remain complete through expansion; return restores saved inline scroll.
- Existing axis/point/stem/column motion retained: normal6-period entry1100ms, capped source-order delays, no hover/resize replay; reduced/expanded static. Escape/scroll clears active state; keyboard focus scrolls the actual event into view. Native rich-text fallback unchanged.


## Mermaid journey renderer

- Mermaid11.12 owns source order, contiguous sections, raw1–5 scores and actual actor participation. Read getTasks once and copy; exact source identity and scores remain in each column's accessible label. This visual revision has passed user review.
- Block / curve / block hierarchy: gray phase cards with8px corners; numbered steps using20px circles and12px/20px complete names; a smooth experience curve; neutral continuous role participation strips. Inline reserves112px for the permanent score axis and role labels. Step widths76–144px fit ordinary sources to available drawing space, with local scrolling when needed. Expanded uses120px columns and the shared complete-scene fit. Scene and grid width hug the actual columns instead of stretching to the viewport. The step-region reference is titled 用户旅程 with the same style as 体验曲线; the score reference is titled 体验曲线; omit the role-region caption and leave24px between the curve block (including the face radius) and the first role block.
- Experience curve has2px stroke and fixed1–5 domain. Use semantic score tones: low light#cf6f68/dark#e79b94, middle#b49a49/#d8c175, high#6b9b7a/#96c5a4. Vertical gradient maps1→red,3→yellow,5→green; the area mask fades .22→.10→0. Cubic controls stay between adjacent source points to avoid overshoot. Replace dots with official Lucide Frown/Meh/Smile at24px; points carry no visible numeric labels. The fixed score reference retains1–5.
- Phase surface uses the existing muted18% mix composited over opaque host background. Role labels use semantic Lucide16px icons plus full text; unknown roles use UserRound. Consecutive actual participation steps merge into14px high strips with5px corners and foreground9% mixed into background. Gaps remain gaps; strip width expresses step participation, not duration. Each role row uses its own measured label height, with12px between rows; strips align with their own label center. Long labels do not enlarge other rows.
- Whole-column hover/focus retains the selected column and masks other columns with host background at.72 opacity over140ms. Step titles receive no separate selected card. No journey tooltip or popover; full identity, score, actors and supplied description remain accessible. Escape/leave clears the masks. Role labels are static references.
- Trace1000ms, area fade500ms, faces fade200ms by source order. Full exit/reentry and visibility restoration replay; hover/resize do not. Expanded/reduced stay static. ResizeObserver only queues one animation frame; layout writes happen outside its notification delivery.

## Mermaid kanban renderer

- Mermaid11.12 DB owns column/task order and actual IDs, parent membership, assigned/ticket/priority. No guessed throughput, elapsed time or completion ratio. Card counts derive from actual tasks; empty columns remain visible. The following visual revision has passed user review.
- Columns272px inline/248px expanded with16px gaps,12px padding/corners. Stable host series colors distinguish source columns; column surface mixes6% tone into background. Heading uses a capsule with15% tone,7px dot and matching count; tone55% mixed into foreground preserves text contrast. Show at most12 Unicode characters including ellipsis, preserving full column identity in accessible labels. Scene hugs columns and measured content.
- Cards have16px/24px medium-weight names,14px padding,9px corners,10px spacing and opaque host background (white in light mode), no shadow and no visible default border. Hover/focus adds only the series1 blue border with no fill change. No phase tooltip or popover.
- Optional description and ticket are distinct full-text12px/18px secondary rows above people. Secondary text uses foreground64%; people/priority use76%. Assignee uses official Lucide UserRound14px plus full name without a visible field prefix. Priority uses four6px×10px segments with2px gaps and the exact source grade: Very Low1, Low2, High3, Very High4. Unknown grades retain text without guessed segments. Metadata/long words wrap; full source details remain accessible.
- Header300ms/8px and card240ms/8px entry by source column/row. Complete exit/reentry and visibility restoration replay; resize/hover do not. Expanded/reduced remain static. Shared viewport handles whole-scene fit and inline restoration; rich HTML/icons/external ticket links remain native. ResizeObserver only schedules layout on the next frame.

## Mermaid pie renderer

- 从 Mermaid11.12 getSections Map 读取源顺序、独立名称、原始非负权重、showData、title，不合并极小份额或发明单位。正有限总量必须大于0；零总量与rich label明确原生回退，零值仍留在图例和详情。
- 通过 mermaid_presets.py 编译现有 donut-chart.html，再由 mermaid-pie.js 做语义映射；不维护第二套圆环样式。圆环约75%内径、中心总计、host系列色、短数据直标／长数据底部图例沿用已确认方案。Mermaid源数据可多于独立预设的6类，颜色按6个token循环，完整列表保留。
- 只有正权重绘制弧；角度严格按原值分配，零值没有扇区或缺口，极小份额不会被最小可视角度撑大。showData 在图例／直标带原值，详情使用原始值而非小数位截断。中心大数自动缩小以容纳，长名称换行。
- 650ms圆环入场，直标随入场淡入；普通resize/hover不重播，完整退出后重入可重播，reduced静态。图例和直标详情靠近触发对象，弧详情靠近圆环。使用宿主展开预览，无额外全屏容器。

## Mermaid XY renderer

- Mermaid11.12 getXYChartData owns real point coordinates, category order, numeric domains and bar/line types. Copy parser data, not source regex or a second graph. This version has no business series names: identify plots by source type/index, never invent meaning.
- Host series colors,1.5px lines/3px points, neutral grids, complete12px labels and axis titles. Bar thickness at most24px; actual zero baseline anchors positive/negative bars. Categories retain measured minimum readable slots and drawing-only horizontal scrolling. Half-column edge inset keeps the last label inside intrinsic geometry.
- Inline keeps a64px neutral reference region for value ticks/unit; the axis caption stays centered below the visible viewport. Expanded restores full SVG value reference and fits the complete scene. Return uses shared saved inline position. Wrapping series legend follows20px below the figure and stays centered.
- Pointer compares all source series at a category; keyboard/click category labels reveal the same complete values. Near-trigger transient themed details constrain to real root bounds and avoid labels/ticks/titles/legend/reference. Whole focused label enters the viewport; settled scrolling restores keyboard detail, Escape cancels delayed restoration.
-650ms simultaneous bars grow from actual zero,1200ms lines trace their unchanged paths. Hover/resize do not replay; expanded/reduced remain static. Complete exit/reentry and visibility restoration replay only when visible; hidden cancels incomplete entry and details.

## Mermaid Radar renderer

- Read ordered axes, normalized curve entries, labels, domain, ticks, grid shape and legend visibility from the pinned Mermaid DB. Radial distance encodes the value within its declared min/max; polygon area is not a total score.
- Reuse host series tokens, neutral 1px grid, 12px complete axis labels, 1.7px data lines and low-opacity .035 fills. Pair the first three series with circle/square/diamond and solid/dashed/dotted lines; keep legend identity consistent with the marks.
- Keep an intrinsic readable scene, wider labels and outer spacing for long multi-axis data. On initial narrow inline entry center the diagram and retain horizontal scrolling. Expanded mode fits the complete scene and remains static; returning restores the inline position.
- Axis labels and tolerant axis/point hits show same-dimension values across series. Series keys expose the complete named profile. Details use measured source coordinates and must not intersect the source, heading or other readable labels. Prefer nearby free space; use a transient natural-flow detail below the chart when no free overlay fits. Keyboard focus scrolls the complete axis label into view and restores details after scrolling; Escape closes details from both SVG mouse and button keyboard entry.
- Reveal vertices radially over 900ms with quartic easing; keep marker dimensions and strokes constant. Resize, expanded mode and reduced motion show final geometry without replay. Only complete exit followed by re-entry arms replay; actual document-hidden restoration remains a host verification boundary.

## Mermaid Sankey renderer

- Read actual Mermaid11.12 getGraph/getConfig, preserving source order, duplicate links, raw positive quantities, alignment, source/target/gradient color semantics, showValues and prefix/suffix. No second CSV parser or inferred complete reader paths. Pinned grammar accepts ASCII labels only; comparisons share the same valid source. Zero/nonpositive values, loops and custom literal link colors preserve native semantics with a visible reason.
- D3-sankey0.12.3 supplies proportional DAG coordinates; qv owns SVG bands, HTML labels, interactions and motion. Preserve exact quantitative link widths, including subpixel flows. A separate transparent hit path supplies tolerance without changing the visible width. Stable host series tokens identify nodes and band endpoints; no imported Mono palette.
- Complete14px names and12px raw values retain source identity. Measure label height for top/node gaps/bottom clearance; all label bounds belong to the scene. Inline uses readable intrinsic columns with drawing-only scroll and a conditional quiet scroll cue. Expanded uses tighter columns then the shared native fit; return restores intrinsic layout and saved scroll.
- Node details show actual incoming/outgoing quantities; edge details show raw flow with explicitly labeled shares of source outgoing and target incoming. Hover/click and native keyboard flow buttons share one transient themed detail. Avoid heading, readable labels and current focus; use measured trigger bounds. No persistent long flow list, filtering or invented end-to-end attribution.
- One1000ms quartic-out horizontal clip reveals unchanged proportional bands and nodes. Resize, expanded and reduced motion show complete geometry; complete exit followed by20% reentry may replay. Hidden cancels incomplete motion; real document-hidden remains a host verification boundary.

## Mermaid Quadrant renderer

- Preserve exact0–1 coordinates, source order, complete names, duplicate names and coincident entities; cross stays at.5. Capture raw original parser callbacks and restore all callbacks after success/failure. Point classes and color-only styles are supported; custom radii/strokes and rich labels retain visible native fallback.
- Two neutral1px cross axes without outer frame or numeric ticks. Four source axis ends sit at the cross ends,14px/500, complete wrapped text in content-width capsules:8px/12px padding,999px radius,8% muted-foreground mixed with background; no inferred primary/secondary split. Four source quadrant captions remain muted12px, grouped around the origin with12px clearance on each side of the cross. Intrinsic640–736px scene with128px horizontal and104px vertical endpoint clearance; plane remains square.
- Unclassified points use existing series1 blue, never quadrant colors. Class names map to stable source-order series2–6; explicit source colors override defaults. Same-class points share color. Fixed5px marks preserve source coordinates.
- Point labels are12px single-line ellipsis, max144px including4px/6px padding, with full accessible names and nearby placement only. Within96px,3 or more neighbors hide local labels;2 neighbors hide labels when measured text area exceeds14% of the neighborhood; labels without an adjacent collision-free position also hide. Hidden labels leave actual points, complete accessible names and keyboard focus intact. No distant packing or hidden entity merging.
- One nearest-point picker; coincident coordinates expose every source entity, raw coordinates, quadrant/boundary, category and descriptions together. Point-adjacent themed252px popover displays matching category dots when the diagram has any category; unclassified points then form an implicit blue default category, including among coincident entities. A diagram without categories keeps neutral details. It has12px radius and12px×14px padding, clamped to visible host bounds, scrolls long content within320px. It can cover surrounding text instead of moving far from its point. No reserved reading region or layout growth;100ms leave bridge allows entry into long-content popover. Escape/scroll/blur clear the old detail.
- Shared whole-scene expansion and saved inline scroll remain. Point240ms and visible label300ms/4px,80ms source-order stagger; reduced/full/resize remain static. Resize observer schedules one latest-width redraw in the next animation frame to avoid feedback loops.


## Mermaid Block renderer

- The canonical Mermaid tree owns columns, spans, explicit space and containment. Never replace manual positions with automatic topology or treat node area as a quantity. Layout and obstacle routing are separate from source adaptation and visual drawing.
- Intrinsic cell160px/gap24px inline,128px/gap20px expanded,24px nested padding. Complete names12px/18px measured before placement; normal nodes48px minimum and10px radius. Each actual source shape has one1px neutral outline; cylinder body follows theme and top arc remains unfilled. Groups use12px corners and actual source captions. Wires use7px bends and5px integrated markers.
- All nodes/groups/visible source edges retain native keyboard entry. Node details list real incident relations; groups list actual descendants; edge emphasis is exactly two endpoints plus one edge. No persistent relation list or filtering. Wide inline detail candidates avoid all node/caption/label rectangles. Expanded and narrow views reserve worst-case source detail height below the drawing, preserving unscaled12px complete reading without changing diagram geometry during focus. Themed detail uses12px radius,12px×14px padding and pointer transparency.
- Expanded is the shared whole-scene preview, followed by restored intrinsic inline layout and saved scroll. Source-order240ms/4px nodes,650ms solid-wire trace/35ms stagger and end markers after arrival. Complete exit/20% reentry may replay; reduced/full/resize static, timers and animation cleanup match the real complete state. Native fallback stays untouched.

## Mermaid C4 renderer

- Mermaid11.12 owns actual Context/Container/Component/Dynamic/Deployment identities, boundaries, technologies, descriptions and relationships. Retain per-kind declaration order, source row ceilings, external status, reverse/bidirectional endpoints and native Dynamic sequence numbers. Rich labels, custom style, sprites/tags/links and unsupported semantics preserve native fallback.
- Intrinsic cells200px, gap40px and nested padding32px. Root participants form a reading column beside actual boundaries; container components wrap into two columns. This changes placement only: no synthetic boundary, omitted relation or renamed type. Node names14px/20px weight500; stereotypes, technologies, descriptions and relation labels12px/18px. Nodes10px radius, boundaries12px, neutral1px outlines and semantic Lucide icons retain the common design language.
- Measure real relation-label rectangles before routing. Final compact paths must admit a label position without intersecting any node, actual boundary caption or earlier label. A route with no free position is rejected rather than choosing the least overlap. Details avoid those same obstacles and dock below the diagram when free nearby space is unavailable.
- Source nodes, actual boundaries and relationships retain native keyboard entry and complete details. Node emphasis follows actual incident edges; relationship emphasis is exactly two endpoints and one wire. No filtering or invented drilldown. Expanded/narrow views reserve maximum source-detail height below the diagram at unscaled12px. At<=420px expanded width, one labeled native select lists actual node names and opens the same detail, keeping the whole diagram visible and stable.
- Shared whole-scene fit preserves inline scroll on return. Source-order240ms/4px node entry,650ms wire trace with35ms stagger,240ms labels and endpoint markers after arrival. Complete exit/20% reentry may replay; resize, reduced motion and expanded mode remain final/static. Cancel timers and animations together. Native fallback never receives qv viewport behavior; host toolbar and clipboard acceptance remain separate from simulated mode-event tests.

## Architecture-beta resource reader

本轮沿用真实端口与原生约束几何，不强制折叠成方形。叶节点使用宿主底色，分组由内向外 muted18% 灰／白交替；灰色不叠加。分组z0、线z1、节点z2、标签z3，暗色连线48% muted-foreground混底、明色36%。详情resize延至下一帧处理，退出保留220ms缓冲，避免快速移动与ResizeObserver同步回写抖动。

Architecture-beta 保留 Mermaid 11.12.0 实际 DB 的服务、汇接点、嵌套分组、双向箭头与 T/B/L/R 端口；group 修饰仍附着服务所属边界，保留原始服务端点供详情追溯。使用原生约束几何，不另造拓扑。

- 完整服务名称使用 240px 宽卡片、14px/20px、500 字重，真实内容宽 184px 测高，保留 12px 上下内距和 1px 边框。分组浏览卡片 320px，成员使用 12px/18px 的完整换行文本。
- 完整组标题是真实按钮。服务和完整组标题只阅读详情；组浏览卡片仍按原来的 Enter/Space 下钻，不改变默认分组浏览行为。
- 未缩放的详情放在图下文档流，使用 host 前景色、12px/18px，显示完整源名称、类型、ID、可选中文说明、所属路径及直接关系与真实端口；组显示直接成员，group 边显示原服务端点。详情区按最宽内容实际测高预留空间，不遮住图形、标题或路径。
- 320px 和完整图模式提供原生对象 select，列出原模型所有服务、汇接点和分组；选择只读详情，不过滤图。完整图继续 fit 全部几何，返回保留 inline 滚动。
- 键盘聚焦将能容纳的完整卡片滚入可见区，滚动结束恢复详情。Escape 清除选择并取消尚未发生的详情恢复。缩放不作用于详情。
- 动效沿用 240ms 节点、650ms 连线、50ms 箭头，以及真实退出/重入重播；reduced-motion 和完整图静态。

Flowchart wires and arrowheads retain the light-theme 26% muted-foreground mix; dark theme uses 36% for a small visibility increase. Tooltip keyboard behavior and long descriptions are unchanged in the 2026-10-11 flowchart audit.

Flowchart hover commits only after the pointer stops moving on a node for 140ms; pointer movement restarts the timer. Rapid crossings retain the prior highlight; settled destinations transition directly without restoring the neutral state. Pointer leave clears after a 220ms grace period. External group portals show the group name plus a Lucide arrow-up-right, with action wording only in the accessible label; no visible action caption. Breadcrumb segments offer a native top-layer popover of sibling groups (overview has no popover). Hover opens after 120ms; pointer travel to the list has a 180ms grace period. ArrowDown opens and focuses the list; arrow keys move between groups, Escape closes, and selection directly navigates without returning to the parent. Diagram tooltip keyboard and long-description presentation otherwise retain the previous behavior.

Flowchart highlight transitions share 140ms easing across node borders, outlines, wires, arrowheads and edge labels; reduced motion removes these transitions. Flowchart containment surfaces are host background / original light gray (muted mixed 18% into background, composited over an opaque host background), alternating from leaves outward: leaf=0 background, direct container=1 gray, outer container=2 background. Compute each group level as one plus the maximum child level from the complete source hierarchy, independent of animation layer and current drilldown scope. Group cards and group portals retain their source container level.

Mermaid drawing is visible once ready; intersection-triggered entry motion never gates content visibility. Large diagrams in short viewports remain readable even when the entry threshold is unreachable.

## Mermaid mindmap renderer

Formal entry reuses the approved bilateral tree. Compute subtree height and per-depth column width from complete parsed hierarchy. Root remains centered, inline drawing scrolls locally, expanded view fits the complete scene. Names wrap at measured node widths; 12px text and 14px root retain host tokens. No areas or sizes represent values.

## Mermaid Gantt renderer

Formal Gantt reuses the approved ruler, section labels, stage-colored interval bars and 13% milestone capsules. Parse task dates and dependencies from Mermaid DB; never recreate schedules in a second data model. Preserve date ticks, move competing milestone captions to separate rows, and keep exact dates/prerequisites in details. Shared qv viewport/loading; reduced and expanded are static.

## Mermaid shared presentation contract

局部浮层先保持对象关联：在触发对象12／20／28px处找候选，距离最多32px，再在这些近候选中避让，不为了零遮挡把详情送到远端。优先使用已呈现的信息；只有说明、关系或成员需要补充时显示详情。100ms停稳与160ms退出缓冲避免快速跨节点反复还原。

`mermaid-presentation.js`只负责局部定位、hover时序和包含层底色；模型、布局和各图的交互语义保持独立。`mermaid_presets.py`在生成时编译现有模板，Pie／Radar适配源数据后调用，避免样式复制。ResizeObserver涉及重绘时延至requestAnimationFrame处理，禁止在观察器同一批通知内同步改写被观察对象的布局。
