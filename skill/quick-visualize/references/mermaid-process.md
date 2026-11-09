# Mermaid 过程与时间

按图型读取对应小节。输入契约见 [Mermaid](mermaid.md)，共享呈现规则见 [Charts](charts.md)。本文件只规定各图型的语义、专用布局与交互；局部入场时长受Charts的批次预算约束。

## Sequence

需要表达处理区间时，使用 `activate`／`deactivate` 或消息的 `+`／`-` 标记明确激活范围；渲染为浅蓝色激活条，嵌套向右错开。只表示执行顺序区间，不将柱长解读为实际耗时，也不为未声明的区间自动补柱。

- 保留 Mermaid11.12 的参与者顺序、角色、消息方向、虚实线和箭头类型、自动编号、激活条、self message、alt/loop/par/critical 等控制框及 note 的源位置；未支持的 box、rich label、properties 等明确原生回退。
- 参与者标题按实际 DOM 换行测高，内容宽最多240px；消息最多288px并完整换行。每条消息按自己的高度预留空间，长文本不会覆盖前一条消息或将后续消息统一撑高。共享 intrinsic scene，展开整体 fit，返回保留滚动。
- 消息线使用明色#727a82／暗色#a3aab3，8×8箭头为明色#4b5259／暗色#c4cad1，序号使用线起点徽标，lifeline 更轻；次级小字使用60%／68%前景混色。参与者悬浮突出真实邻接消息；消息浮层分列表示来源、目标，再显示完整正文，距离触发对象不超过32px。不重复展示没有额外说明的参与者标题。
- 消息420ms依次描画，stagger=min(140ms,900ms/(条数−1))，180ms标签和60ms箭头随线到达。减少动态和展开静态；悬浮、resize 不重播，完整退出后重入可重播。

## Timeline

- `timeline` reads actual Mermaid11.12 DB once, preserving source-order periods, contiguous sections and all events. Repeated names remain distinct entities; empty periods remain on the axis. No date parsing, inferred duration or event deduplication. Rich labels explicitly retain native rendering.
- Horizontal reading stays:216px columns/40px gap inline,184px/24px expanded. Scene width hugs actual columns and tail; expanded root is capped at its intrinsic width and centered, shrinking the whole scene only when needed. Source sections select stable theme series colors, reused when the same section name recurs. Columns stay transparent with12px padding; section captions use 15% stage-tinted capsules and stay in their contiguous source span using native horizontal sticky positioning; do not rewrite caption left from scroll events. Period names are complete wrapped14px medium text in theme foreground.
- 事件保留完整14px/22px文字，采用区段色7%软卡片，hover/focus为14%，8px圆角、8×10px内距、8px卡片间距。5.5px圆点与首行中心对齐；不添加多余浮层。
- Stage/header heights are measured to align the shared ordinal axis; column bodies keep independent heights.7px source-stage dots with theme-background rings sit on the continuous neutral1px axis. The axis extends120px beyond the final period and fades to transparent without adding a period. Each vertical rail ends at its own last event center; empty periods have no rail. Flat events retain their source relationship without invented child branches. Shared expanded fit and saved inline scroll remain unchanged.
- Existing1100ms normal entry/source-order point and column motion retained; full exit/reentry may replay, ordinary hover/resize does not, reduced/expanded remain static. Actual host visibility/native buttons remain a separate acceptance boundary.

## Journey

- `journey` preserves Mermaid11.12 source task order, contiguous sections, raw scores1–5 and actual people/actor participation. Steps without a section, repeated task names and tasks without actors remain visible. No elapsed time, aggregate rating, causality or participation strength is inferred. Read `getTasks` once and copy before any subsequent parsing because it appends to shared DB storage; read the actual `getActors` order. Journey has no DB task ID: `descriptions` uses stable source-order IDs `step-1`, `step-2`, etc.; unknown IDs are errors.
- Approved design uses phase blocks / experience curve / participation strips. Phase captions sit in light gray8px blocks; steps use circular numeric ordinals and complete names. Experience uses Lucide Frown/Meh/Smile markers, a smooth2px path, vertical score gradient1→red,3→yellow,5→green and a translucent fading area. Raw values remain on the permanent1–5 reference and accessible labels, without numeric labels beside faces. Curves remain within adjacent raw score bounds.
- Inline reserves112px for score and role references; columns adapt76–144px to the available drawing width. Expanded places the reference into the complete scene, uses120px columns and shared fit; return restores inline geometry and saved scroll. Scene and grid hug the actual columns rather than extending into unused viewport space. The step-region title 用户旅程 shares the style of the permanent score reference 体验曲线; role labels begin24px below the curve block including face extents, without a separate region heading. Phase captions remain within their contiguous source span.
- Actual actors use semantic Lucide16px icons and full text. Participation is neutral14px strips; adjacent participating source steps merge, non-participating steps remain gaps. Strip width encodes membership in successive steps. Roles stay neutral so score color owns the primary emphasis. Each role row uses its own measured text height with12px between rows; strips remain centered against that label. A long role name never expands unrelated rows.
- Hover/focus selects the whole step column, with background masks over all other columns; no separate title-card highlight and no journey tooltip/popover. Exact identity, score, actors and optional description remain in accessible labels. Escape and pointer leave restore the complete chart.
- Trace1000ms, area fade500ms, faces fade200ms by source order. Full exit/reentry/visibility restoration replays; ordinary hover/resize do not; reduced/expanded are static. Rich HTML and scores outside1–5 retain explicit native fallback without the qv viewport.
- ResizeObserver only schedules one animation frame for a changed width; layout writes occur outside the observer delivery. Height-only notifications do not trigger layout. Validate window error events during repeated resizes and display-mode return.
- `mermaid-journey-model.js` owns this version-sensitive DB access; `mermaid-journey.js` draws the independently designed view and shares the viewport controller. Do not upgrade Mermaid or replace DB access with regex parsing without comparing parser fixtures and actual rendered semantics.

## Kanban

- `kanban` preserves Mermaid11.12 actual column/task IDs, source order, column membership and assigned/ticket/priority fields. Keep empty columns and metadata-free tasks. Counts describe current cards, not workload, completion ratios or elapsed time. Use `getData`/`getSections`; do not author a second graph.
- Approved design uses softly tinted columns, dot/capsule category headings and matching counts. Author category names within12 characters; display at most12 characters including ellipsis while preserving full source identity in accessible labels. Inline columns272px/gap16px scroll horizontally; expanded columns248px share whole-scene fit. Common measured headings align columns; return restores inline geometry and saved position.
- Opaque cards use larger16px names with no shadow or visible default border. Hover/focus only adds a blue border; no stage tooltip/popover. Optional descriptions and ticket identifiers remain distinct complete secondary text above people. Assigned shows Lucide UserRound and full name. Priority uses four segments (Very Low1/Low2/High3/Very High4) plus the exact source grade; unknown values stay textual. Ticket is an identifier, not inferred description. Tab brings the task into the drawing viewport. No drag/edit/navigation or filtering.
- Headers300ms/8px, cards240ms/8px by source column/row. Exit/reentry/visibility restores entry; resize does not replay; reduced and expanded remain static. Rich HTML/icons and ticketBaseUrl preserve native semantics without qv viewport behavior. ResizeObserver schedules layout on the next animation frame.
- `mermaid-kanban-model.js` owns version-sensitive DB access; `mermaid-kanban.js` draws the independent view. Keep Mermaid11.12 pinned and rerun parser/visual checks before changes.

## Gantt

`gantt` uses the formal qv entrypoint and the approved grouped schedule design. Read Mermaid11.12 resolved `getTasks()` dates, flags, IDs, sections and `raw.startTime.startData` dependencies. Time bars retain true start/end positions; zero-duration milestones retain their exact date with 24px stage-color capsule labels. Date details and all prerequisites remain in hover/focus detail. Repeated/nearby milestones use separate label rows rather than hiding axis dates. Cross-month schedules show both endpoint months. The renderer uses pinned D3 7.9.0 time geometry, shared qv loading/viewport and reduced-motion behavior; bars animate 580–680ms. Custom date exclusions/includes, inclusive-end mode, clickable source links, custom today-marker styles, sub-day formats, rich labels/classes and unresolved dependencies explicitly fall back without the qv viewport. Default today marker remains when within the visible date range; `todayMarker off` disables it. Description keys are actual task IDs.
