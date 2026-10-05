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
