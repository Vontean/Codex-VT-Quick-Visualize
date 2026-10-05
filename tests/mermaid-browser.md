# Mermaid architecture browser acceptance

The Python tests check input round-trip, escaping and fragment generation. They do not prove design fidelity or validate Mermaid syntax.

## Current acceptance: 2026-10-06

Use the real Visualize wrapper and its iframe in Chromium. Compare the same source/data against the user-approved architecture prototype at 736px content width:

- `simple.mmd`: 5 nodes, 4 edges. Every node's x/y/width/height/font and every edge's path/stroke/width matched the approved simple prototype.
- `complex.mmd`: 12 nodes, 16 edges. The same geometry comparison matched the approved layered prototype. Four captions retain source grouping; all 12 nodes have Lucide icons.
- Enhanced output reports `data-renderer="qv-architecture"`, contains HTML buttons and qv SVG wires, and has no permanent description panel or Mermaid-rendered graph SVG.
- Both examples show the optional dark tooltip on hover without shifting nodes. Check keyboard focus/blur and Escape when modifying this behavior. Custom tooltip CSS must target the tooltip div, not `button.node-tip`.
- Re-entry increments replay on the existing scene. Recorded node/line/arrow durations are 240/650/50ms. Reduced motion leaves zero animations.
- Dark theme computes node background `rgb(24,24,24)` and foreground white. At 736/640/320px, the complex drawing stays 736px wide and all five data nodes remain in one row. Only `.diagram-scroll` overflows; root scroll widths match 736/640/320px. At 320px, the focused queue tooltip stays within x=56–316px after scrolling.

## Honest fallback

- `boundaries.mmd` and `semantics.mmd`: native fallback with a visible unsupported-shape reason; do not restyle native output and call it qv.
- `ids.mmd`: native fallback with a self-loop reason, preserving the source graph.
- `fallback.mmd`: native sequence diagram and explicit notice.
- `invalid.mmd`: visible parser error; no enhanced graph.

The earlier SVG-styling adapter is rejected and its broad `enhanced` claims no longer apply. Keep unsupported constructs visible and intact until their qv layout/marks are implemented. Fixture counts alone are not acceptance: compare geometry, icons, ports, marker joins, tooltip behavior and real motion. Actual message-flow review remains the user's final visual acceptance.

## Shared loading region

All ten preset types share `assets/chart-loading.html`. Loading is now a Canvas dot field, adapted from the installed Codex `webview/assets/image-loading-state-3d884c5e3d97.js` and `image-loading-state-8c612077a546.css` inside `/Applications/ChatGPT.app/Contents/Resources/app.asar` (read-only inspection, 2026-10-06). The host React component is not imported; qv uses its motion parameters with theme-aware ink on a transparent surface.

Browser validation: consecutive Canvas frames differ; reduced-motion frames remain identical; the qv:ready event clears aria-busy and hides the field. Existing loading-to-ready checks cover Mermaid, line, bar, donut and synchronous radar. The continuous preview is for motion review only; production never delays ready content.

All-preset extension: browser checks confirm parameter-form, both multi-select variants, ranker and comparison reach aria-busy=false with visible content and hidden loading field immediately after initialization. Both checkbox variants and comparison radio selection remain interactive. No minimum-duration timer was added.

Mixed-direction ports: queue top and worker bottom each separate incoming/outgoing endpoints by 14px. Worker outgoing edges still share one port; complex example retains 12 nodes and 16 edges. This intentionally supersedes the earlier shared-center geometry at those two nodes.

Icon policy browser checks: the complex example renders 12/12 icons in auto mode; icons:none and one unmatched node each render 0/12. Explicit semantic legend labels display as 同步调用 / 异步事件. Authoring mixed styles requires semantic legend or edge labels; the renderer never guesses their meanings.
