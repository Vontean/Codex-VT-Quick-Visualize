# Chart design

- Readability comes before reference-style fidelity. Evaluate label hierarchy, contrast and data lookup before visual decoration; comparison samples do not define qv's design language.
- Gantt task names stay inside their time bars: use one line when it fits, otherwise wrap to at most two lines and truncate the remainder. Hover/focus details retain the complete name. Never lengthen the time bar to fit its label. Do not repeat phases under every task; use meaningful group headings. Duration information must remain readable independently of bar color.
- Use host foreground, border, popover and stable `--viz-series-N` tokens. No imported Lieflat gallery code or fixed Mono palette.
- Figure top padding: 32px. Title-to-plot gap: 32px. Centered wrapping legend beneath plot, gap: 20px.
- Floating details: 12px radius, 12px × 14px padding, subtle shadow, boundary constrained. No pinned tooltips or helper footers. User data enters text nodes, never HTML.
- Cartesian frames keep left/bottom axes and internal grid lines only. Bar width is at most 24px; dense charts omit value labels.
- Entry motion replays after complete viewport exit and 20% re-entry, or document visibility restoration. Resizes and ordinary hovers do not replay; reduced motion disables entry animation.
- Bars grow upward in 580–680ms with simultaneous starts. Lines trace their path in 1200ms with a moving value and matching area reveal.
- Donut reveals outward around the ring in about 1050ms. Direct labels use 325ms + index × 50ms delay and 450ms ease fade; the centered number and subtitle share one centered wrapper. Direct labels need <=4 categories, >=8% minimum share, short labels and adequate width.
- Radar vertices expand in 900ms quartic-out, keeping stroke and marker sizes constant. Numeric grid labels stay hidden. Points take priority over axes; axes compare objects, points/edges/areas describe one object. No native SVG title tooltip.
- Radar inactive strokes/markers: .10 opacity; fill: .003; legend: .32. Object markers belong in tooltip headings, not every dimension row. Nearby tooltip candidates use 16–40px pointer distance, minimizing polygon overlap within that range.

The runtime entrypoint stays minimal; data contracts live in each reference. Standalone browser checks do not replace actual Codex message-flow acceptance.

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

- Use the same theme surfaces, 48px participant cards, 10px node radius, 12px floating details and shared viewport. Actors retain a host Lucide user icon. No permanent detail panel or pin state.
- HTML labels and SVG lifelines/frames share a fixed intrinsic scene width. Expanded preview transforms that scene as a whole; no separate SVG stretching. Notes preserve left/right/over; canvas extends to fit notes and self messages.
- Lifelines stay lightest, messages clearer, activation/frame boundaries visible in both themes. Preserve direction and source solid/dotted/open/cross/bidirectional markers.
- Trace messages in order with masks (420ms, stagger140ms), reveal labels180ms and arrowheads60ms near trace completion. Reduced motion and expansion skip entry; hover/resize never restart it.
- Unsupported constructs retain visible native fallback and never initialize the qv viewport.

## Mermaid state renderer

- Preserve state semantics with48px neutral cards,20px terminal boxes (solid start, double-circle end),32px choice diamonds and64×6 fork/join bars. Compound states remain visible together with their contents; no state drilldown.
- Within each parent scope, order layout and entry from actual initial states along transitions; retain every backward link and route it peripherally. Retries use side ports independent from main incoming/outgoing connections. Preserve declared direction.
- Use8px rounded bends,5px integrated arrows,12px condition labels with18px line-height and8px clearance from the associated wire. Theme-aware nodes, boundaries, labels and transient12px details follow existing qv tokens.
- Trigger/label bounds outrank sampled line segments in tooltip collision placement. Hover and focus highlight one state neighborhood or transition without pinning or deleting content.
- Initial nodes240ms, trace650ms, arrows50ms, labels180ms. Labels follow their transfer; reduced motion/fullscreen stay static. Scroll restoration must work whether the host sends globals before or after resizing its frame.

## Mermaid ER renderer

- Actual Mermaid11.12 DB owns entities, aliases, attribute order/keys/comments and relationship end cardinalities. Read endpoint marker names from getData, because relSpec's cardA/cardB names reverse their source endpoint association. Read direction from getDirection; do not infer FK bindings from field names.
- Entity containers keep10px radius,48px header,12px fields,30px rows,14px horizontal padding. Key/name/type columns follow actual canvas text measures; preserve all fields. Notes stay in transient12px details. Empty entities remain visible. Header hover highlights the entity neighborhood; field hover/focus highlights only its own row.
- ER wires and crow-foot/optional/one markers use1px neutral strokes at80% muted foreground mix. Solid/dashed retain identifying/non-identifying semantics and a legend. Selected line and both endpoint markers share one active theme color; no flow arrows.
- Each ER relationship has distinct side ports. Self relationships use a lateral loop (EAST/EAST in TB/BT, SOUTH/SOUTH in LR/RL), separate from primary-axis endpoints. Expanded geometry stays identical.
- Tooltip candidates include outside the complete current/related entities; obstacles include all entity fields, trigger, title and actual endpoint bounds. Keyboard details restore after focus-induced scroll at final coordinates; Escape cancels pending restoration.
- Cards240ms, relation trace650ms, cardinality50ms after trace. Labels100ms from600ms into their trace, finishing with cardinality. Full exit/re-entry/visibility restoration replays; hover/resize do not. Reduced motion and expanded view stay static.
- Shared viewport captures current scroll immediately for same-width expansion; when the host first changes width, preserve the last matching inline-width snapshot. Native fallback never creates a viewport controller.

## Mermaid class renderer

- Class model reads the fixed Mermaid11.12 DB's members, methods, classifiers, annotations, generic type, alias, namespaces and normalized endpoint symbols. Source owns relationship direction, pattern and multiplicity.
- Shared structural container:10px radius,48px title or64px with stereotype,14px horizontal padding,12px member text,30px rows. Abstract italic, static underline. Namespace12px radius and neutral caption; no drilldown. Full signatures determine intrinsic width.
- UML marks use1px theme-aware neutral stroke: hollow triangle, filled/hollow diamond and open arrow. Unique relationship ports and self-loop outer channels preserve all endpoints; labels keep8px path clearance. No category palette is invented.
- Class title highlights its neighborhood; member highlights only itself; relationship highlights exactly its wire and endpoint marks. Tooltip12px radius and12px×14px padding, pointer-transparent and theme-aware. Whole-card avoidance takes priority, then distance to the trigger avoids far-away details. Keyboard scroll settles before details restore; Escape cancels pending restoration.
- Motion shares240ms cards and650ms trace. Endpoint marks/multiplicity50ms after trace; label100ms starts600ms into trace. Complete exit/reentry replays; hover/resize do not. Reduced/expanded stay static. Native fallback has no qv viewport.

## Mermaid timeline renderer

- Fixed Mermaid11.12 Timeline DB owns period order, section and all event text. getTasks mutates a shared array: read once and copy. Repeated names and empty periods remain separate actual periods. Position encodes ordinal sequence, never inferred duration.
- Inline columns216px/gap40px, period and section12px, complete event14px with22px line height. Periods have primary foreground/500 weight, event400. Measure all period headers to align a single axis; keep long labels above it. Section caption stays inside its original contiguous span during scrolling.
- Expanded columns184px/gap24px and14px periods/sections improve complete-view reading. All text wraps before measured height and shared fitting. Scope/order never change. Returning restores intrinsic216/40 geometry before applying the shared savedInlinePosition; do not maintain a second competing scroll snapshot.
- Neutral1px axis and stem,4px outline point, no implied causal arrows or arbitrary series colors. Event hover emphasizes only that event and its period point. Details12px radius/padding12px×14px/theme-aware/pointer-transparent; avoid all period/section/event text, use tallest-column-bottom free space when nearby candidates overlap. Escape cancels pending focus recovery.
- Axis duration is min(last period index,10)×160ms with480ms minimum; point radius.32→4px and matching stem trace240ms begin at each period delay. Point center is fixed for every frame. Column300ms translate8px+opacity. Complete exit/reentry replays; reduced/full stay static; resize/hover do not replay. Native fallback never receives qv viewport behavior.


## Mermaid journey renderer

- Mermaid11.12 owns source order, sections, raw1–5 scores and actor sets. Read getTasks once and copy, then actual getActors order. Derived source-order step IDs support optional descriptions; no second authored graph.
- Full step names14px/22px line-height, inline sections/roles/values12px, expanded sections/roles14px. Inline columns at most168px/gap24px fit the drawing width; expanded144px/gap16px. Measured common step-header and actor-row heights preserve alignment and complete text. A128px independent inline reference column keeps1–5 and actor names while only steps/curve/participation scroll. Expanded reference rejoins the scene for shared whole-scene fit.
- Single series1 score path1.5px, hollow5px markers, neutral1px score grid and6px actual participation dots. No invented average, duration, causality or category palette. A section caption follows visibility only inside its actual contiguous span. Role hover highlights actual participating columns; step/score/point highlight local participation without filtering.
- Details use12px radius,12px×14px padding, theme-aware popover and pointer transparency. Step details add score and full actors to already visible step/section text. Score/participation details preserve full task identity; actor details show complete actor name and actual participation count without repeating all visible task names. Narrow details fit drawing space; candidates consider actual headings, references, text, points and sampled curve segments, prefer zero overlap then boundary distance. Use measured footer clearance only when nearby positions are unavailable. Wheel/Escape clear, focus restores after automatic scrolling. Native fallback never receives shared viewport behavior.
- Trace1200ms; dot growth240ms, value100ms, participation240ms by source step; step labels300ms/8px. Complete exit/reentry and document visibility restoration replay; hover/resize do not. Expanded/reduced motion remain static. Root-width reflow keeps complete text and resets incomplete motion to static without replay.

## Mermaid kanban renderer

- Mermaid11.12 DB owns column/task order and actual IDs, parent membership, assigned/ticket/priority. No guessed throughput, elapsed time or completion ratio. Card counts derive from actual tasks; empty columns remain visible.
- Neutral columns232px/gap24px inline,204px/gap20px expanded. Complete task text14px/22px; metadata12px/18px uses theme foreground76% mixed with background for contrast. Cards use10px radius,14px padding,24px top spacing; measured common headers preserve aligned starts.
- Task hover/click/focus highlights only that task and shows transient phase detail; complete task identity and metadata remain visible and in aria-label. Optional descriptions stay complete. Details use12px radius and12px×14px padding, prefer nearby positions avoiding actual readable text and headings. Keyboard focus scrolls the whole card into the drawing viewport before detail restoration; wheel/Escape clears. No drag, edit, filter or drilldown.
- Header300ms/8px and card240ms/8px entry by source column/row. Complete exit/reentry and visibility restoration replay; resize/hover do not. Expanded/reduced remain static. Shared viewport handles whole-scene fit and inline restoration; rich HTML/icons/external ticket links remain native.

## Mermaid pie renderer

- Mermaid11.12 Map owns source order and unique labels, raw nonnegative weights, showData and title; no second authored data or aggregation of small shares. Positive total required. Zero-weight items stay in the complete list.
- Circle radius112px, no decorative stroke/gaps or explosion; exact angle proportional to raw value. Stable host series colors pair with labeled9px swatches. Complete names14px/22px, raw/showData values and percent12px with readable theme contrast. Desktop circle plus aligned list; below560px stack circle and complete list. Shared expanded fit is static and preserves readable text.
- Real SVG slice hover and keyboard/click-accessible category buttons reveal full label, raw value, share and optional description. One themed12px-radius/12px×14px transient detail prefers near trigger, avoids actual labels/values/title and uses reserved footer only when needed. No native title competing tooltip. No persistent selection or filtering.
- Shared1050ms clockwise clipPath reveal preserves actual data paths and proportions. Categories appear according to cumulative share with300ms/8px motion. Exit/reentry and visibility restoration replay; resize/hover do not; reduced/full cancels masking and returns complete static geometry.

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

- Source positions stay exact within0–1; cross at.5. Preserve full source names and source-order identity, including coincident points and duplicate names. Original parser callbacks supply raw coordinates; restore them after success/failure. Rich text, class and custom point styling remain native.
- Neutral1px frame/cross,12px axes/captions, single series1 radius4px marks. Intrinsic width640–736px, square plane with128px left reference and32px right clearance. Complete12px labels max176px,4px/6px padding,4px separation, nearest free placement and neutral1px leaders. Label packing never changes point coordinates.
- One nearest-coordinate pointer picker; same-position records are shown together with the exact source count. Complete native label buttons retain individual focus/click access. No hidden entity merging or invented priority colors.
- Transient themed12px detail,12px radius,12px×14px padding. Wide view compact one-line X/Y raw values plus full name/source quadrant; axis ends stay visible. At<=420px, reserve the maximum measured detail height once in a labeled reading region, keeping frame geometry stable while hovering. That region preserves all axis semantics and coincident entity names at unscaled12px. Expanded narrow view explicitly provides whole-view/individual-reading/return-to-inline instructions.
- Shared whole-scene viewport and saved inline scroll; native fallback unchanged. Point240ms and label300ms/4px,80ms source-order stagger, backwards fill during delay. Full exit then20% reentry replays; reduced/full/resize remain final and static.


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
