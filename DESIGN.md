# Chart design

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
- Preserve the accepted architecture design: 32px top/title spacing, single-line icon nodes, 48px node height, up to 160px width, 10px corners, 12px/14px padding, host colors and 16px Lucide icons. Simple architecture uses columns; explicit flat groups use captioned layers and subtle rules.
- Curves share each side's center port. Use 1px strokes with muted foreground mixed at 26% against the background. Integrated arrows are 5px long and 4.4px wide; stop the shaft at the arrow base. Dim unrelated nodes to .22 and lines to .055. Keep semantic thick/dotted line distinctions.
- Grow node contents from .08 scale over 240ms, stagger layers by 220ms, reveal line length over 650ms and then arrows over 50ms. Replay without rebuilding on full exit and re-entry; honor reduced motion.
- Optional dark tooltips use white 12px text, 1.6 line height, 7px radius and 10px/12px padding. Rank nearby positions by related-node/line overlap and cursor distance. No persistent description section.
- When a line-style legend is needed, keep it centered with 20px top gap and 16px vertical padding; do not infer that every dotted relation means an asynchronous event.
- Unsupported source constructs fall back visibly with a concrete reason. Never flatten nested groups, replace decision semantics with ordinary cards, or market native Mermaid output as the accepted qv design.

Mermaid 架构图在窄消息流中仅绘图区横向滚动，保留分层并排结构和字号；标题、图例不随之滚动。所有 qv 类型（图表、Mermaid、表单、多选、排序与方案比较）共用整区点阵加载态：透明底、主题次级文字色、双明暗场、30fps、1.75s 透明度呼吸（.38–.56），点半径至少 0.8 CSS px，按本机 image-loading-state 运动参数独立适配；减少动态效果时呈静态点阵。首次绘制就绪后移除，不人为延时，也不在滚动重播时重现。滚动清除悬浮提示，重新悬浮按滚动后的节点坐标避让。

加载生命周期：统一 runner 包装所有类型，各模板在内容初始化与事件绑定完成后发送 qv:ready。异步 Mermaid 等待解析与首次绘制完成；同步表单等立即就绪。不设置最短展示时长，不为演示加载而延迟内容。

架构图端口：同侧同时出入时，入口与出口各偏离中心 7px，间距 14px；同向连接仍共用端口，仅单向的侧保持居中。

架构图图标为整图可选项：默认优先匹配语义明确的图标，所有节点都匹配时统一显示；有任一节点不能匹配则整图不显示。支持 icons: none 明确关闭，不用通用图标补位。

架构图图例仅解释已知语义，使用可选 legend.solid / legend.dotted；生成时默认实线；仅在区分明确的关系语义时使用多种线型，并必须用图例或线上的标注解释。不能省略说明，也不能用“实线连接 / 虚线连接”充当含义。外部源含义不明时先结合上下文确认，不机械推断同步与异步。
