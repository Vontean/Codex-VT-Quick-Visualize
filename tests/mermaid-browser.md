# Mermaid architecture browser acceptance

The Python tests check input round-trip, escaping and fragment generation. They do not prove design fidelity or validate Mermaid syntax.

## Release smoke check: 2026-10-11

Before the Mermaid integration commit, 16 representative sources were generated with the current qv runner, wrapped with bundled Visualize, and loaded in Chrome's real sandboxed iframes: flowchart, architecture-beta, sequence, state, ER, class, timeline, journey, kanban, pie, XY, radar, sankey, quadrant, block and C4. Every root reached `data-state="enhanced"`, every loading region reached `aria-busy="false"`, and every notice was empty. Chrome-extension `postMessage` errors came from the installed extension, not the chart scripts.

Portable new-type sources are retained as `tests/fixtures/mermaid/adapted-*.mmd`; the existing `simple.mmd` and `architecture.mmd` cover the other two types. Generate each through `scripts/render.py mermaid`, wrap it with bundled Visualize's `scripts/render.py`, and open the preview to repeat this check. This is a fresh rendering smoke check, not a repeat of all historical geometry, animation, narrow-screen or native Codex toolbar acceptance below.

## Current acceptance: 2026-10-06

Use the real Visualize wrapper and its iframe in Chromium. Compare the same source/data against the user-approved architecture prototype at 736px content width:

- `simple.mmd`: 5 nodes, 4 edges. Every node's x/y/width/height/font and every edge's path/stroke/width matched the approved simple prototype.
- `complex.mmd`: 12 nodes, 16 edges. The same geometry comparison matched the approved layered prototype. Four captions retain source grouping; all 12 nodes have Lucide icons.
- Enhanced output reports `data-renderer="qv-architecture"`, contains HTML buttons and qv SVG wires, and has no permanent description panel or Mermaid-rendered graph SVG.
- Both examples show the optional dark tooltip on hover without shifting nodes. Check keyboard focus/blur and Escape when modifying this behavior. Custom tooltip CSS must target the tooltip div, not `button.node-tip`.
- Re-entry increments replay on the existing scene. Recorded node/line/arrow durations are 240/650/50ms. Reduced motion leaves zero animations.
- Dark theme computes node background `rgb(24,24,24)` and foreground white. At 736/640/320px, the complex drawing stays 736px wide and all five data nodes remain in one row. Only `.diagram-scroll` overflows; root scroll widths match 736/640/320px. At 320px, the focused queue tooltip stays within x=56–316px after scrolling.

## Expanded architecture acceptance

The expanded fixtures cover `topology` (7 nodes/9 edges), `boundaries` (6/8), `ids` (3/4), `architecture` (5/4 including a junction), `groups-directions` (4/4), `architecture-ports` (3/2) and `shapes-arrows` (7/7). These now use qv marks, not native fallback.

`tests/mermaid-browser-check.js` is a Playwright page function. Generate each fixture through the qv runner and real Visualize wrapper, serve the previews at localhost:8777, then pass the function to Playwright `run-code`. It checks:

- No missing nodes or edges; no sampled wire crossing an unrelated node interior.
- A TB subgroup stays vertical in an LR parent; architecture B/T ports place the destination below its source; horizontal junction/service centers align.
- Nodes, wires and markers have actual 240/650/50ms animations; reduced-motion output has none; viewport re-entry replays.
- Optional tooltip does not cover its bound node; only the drawing scrolls at 736/320px. Resizing the outer region clears an old tooltip position.

Manual screenshot review also checks grouping boundaries, shapes, text, marker joins and spacing. Mermaid's native architecture layout emits upstream Cytoscape warnings about absent edge labels; no browser errors were observed. Actual message-flow appearance remains subject to user acceptance.

## Honest fallback

- `semantics.mmd`: source-authored custom styling is kept in native Mermaid, with a visible reason.
- `rich-label.mmd`: HTML line-break labels remain native instead of exposing literal tags.
- `fallback.mmd`: native sequence diagram and explicit notice.
- `invalid.mmd`: visible parser error; no enhanced graph.
- Specialized shapes, rich labels and source CSS outside the documented scope must not silently become ordinary qv cards.

The version-specific DB adapter preserves graph identity. ELK supplies complex topology coordinates. For explicit subgroup direction and architecture side constraints, native Mermaid SVG is measured offscreen by parser-provided IDs; qv then rebuilds the visible marks, routing, interaction and animation. Native SVG is visible only for explicit fallback.

## Shared loading region

All ten preset types share `assets/chart-loading.html`. Loading is now a Canvas dot field, adapted from the installed Codex `webview/assets/image-loading-state-3d884c5e3d97.js` and `image-loading-state-8c612077a546.css` inside `/Applications/ChatGPT.app/Contents/Resources/app.asar` (read-only inspection, 2026-10-06). The host React component is not imported; qv uses its motion parameters with theme-aware ink on a transparent surface.

Browser validation: consecutive Canvas frames differ; reduced-motion frames remain identical; the qv:ready event clears aria-busy and hides the field. Existing loading-to-ready checks cover Mermaid, line, bar, donut and synchronous radar. The continuous preview is for motion review only; production never delays ready content.

All-preset extension: browser checks confirm parameter-form, both multi-select variants, ranker and comparison reach aria-busy=false with visible content and hidden loading field immediately after initialization. Both checkbox variants and comparison radio selection remain interactive. No minimum-duration timer was added.

Mixed-direction ports: queue top and worker bottom each separate incoming/outgoing endpoints by 14px. Worker outgoing edges still share one port; complex example retains 12 nodes and 16 edges. This intentionally supersedes the earlier shared-center geometry at those two nodes.

Icon policy browser checks: the complex example renders 12/12 icons in auto mode; icons:none and one unmatched node each render 0/12. Explicit semantic legend labels display as 同步调用 / 异步事件. Authoring mixed styles requires semantic legend or edge labels; the renderer never guesses their meanings.

## Group navigation and declared icons

2026-10-06: `navigation.mmd` uses 14 explicitly icon-bearing services and nested groups. Real Visualize wrapper checks passed: overview has three group cards; platform → API supports two-level drilldown, breadcrumb return, external-group context and keyboard Enter. API view has six visible nodes and six icons. Data view has five nodes and five icons. At 320px content width only the drawing scrolls; the document does not overflow. Gateway tooltip overlap with its node is zero; reduced motion leaves zero animations.

An explicit Lucide flowchart with subgroup direction renders two icons through the native-geometry path. An unknown icon returns an actionable error. Tests also cover source immutability, boundary endpoints, real self-loops and aggregation preserving labels/styles/directions (`test_mermaid_navigation.py`).

Design references: [IcePanel](https://docs.icepanel.io/getting-started) and [Structurizr navigation](https://docs.structurizr.com/ui/diagrams/navigation) support progressive architecture views; [Unreal collapsed graphs](https://dev.epicgames.com/documentation/en-us/unreal-engine/collapsing-graphs-in-unreal-engine) supports the group-entry interaction. Lieflat G7 is a tree reference, not a ready-made architecture drilldown renderer. No reference implementation code was copied.

Overview preview revision: the 14-service fixture now exposes all 14 member names/icons, two nested captions, five real internal links and five aggregate cross-group relationships. Hovering Content keeps Auth, Search, PostgreSQL, Queue and Storage visible and highlights only the two corresponding group connections. Two-level navigation and return still work. The overview fits 736px without scrolling; narrower views retain local scroll. Projection tests cap previews at eight members and report the exact remainder. Browser reduced-motion check is performed after the media-change event is processed.

Additional design references: [G6 combos](https://g6.antv.vision/manual/transform/overview/) and [yFiles folding](https://www.yworks.com/demos/application-features/folding/). Lieflat B1/B2 informed adjacency emphasis and subdued secondary relationships; no source code or palette was copied.

Group-browsing switch revision: overview → platform → API → switch off restores 14 services, five nested group boundaries and 17 source edges; switching on restores two aggregate-number circles without duplicates. No back button or “查看内部” footer remains. The separate layered fixture restores its four layer captions, 12 services and 16 source edges when browsing is disabled. Switch state is local; disabling from a nested scope shows the complete source graph.


Correction after user review: removed per-node focus mode and the node index. API scope renders all four internal services plus two external boundary nodes and eight projected edges together. Clicking Content leaves the six nodes and API scope unchanged. A 736px browser check shows the full local view within 736px width using top-down layout. Unit coverage explicitly preserves disconnected internal nodes.


## Native expanded preview: 2026-10-07

`tests/mermaid-viewport-browser-check.js` runs against the real Visualize iframe wrapper and simulated `openai:set_globals` events. Eight enhanced fixtures cover simple/layered/complex/group-navigation/shape/direction/port layouts at 1440, 736 and 320px: all visible marks fit within the drawing region and 650px available height, expansion has no running animations, and exit restores inline scroll. Two-level group navigation and the complete-view switch retain the expected nodes.

Six native fixtures (sequence, Gantt, class, mindmap, custom styles and rich labels) keep their SVG, scene and viewport style attributes unchanged after the same event. The qv viewport controller is initialized only after enhanced rendering is selected; the native fallback branch is unchanged.

Thirty browser checks passed without page errors. The existing full-layout regression also passed all thirteen fixtures, both narrow-width checks, 240/650/50ms entry timing, tooltip non-overlap and viewport re-entry replay. The delivered examples retain 14 nodes/17 edges (architecture) and 10 nodes/11 edges (publication flow). These prove layout and mode-event handling, not a real native-toolbar click or clipboard round trip. Message-flow expansion and Copy as image remain a user acceptance check. Native copy captures the current preview; no independent export was added.


## Shape fill and layout-loader repair: 2026-10-07

Dark-theme computed styles exposed the cylinder's HTML backplate as `rgba(54,54,54,.96)`: the later layer background selector overrode the earlier shaped-node rule. Shaped backplates are now transparent after layer/group rules; the cylinder uses a closed body plus a separate unfilled arc. Light/dark checks confirm the body matches the theme background and the arc fill is `none`.

`tests/mermaid-rendering-browser-check.js` blocks jsDelivr's ELK URL. The same pinned 0.10.0 bundle loads from unpkg and both delivered examples render completely in both themes: publication flow 10 nodes/11 edges, platform architecture 14/17. Their expanded marks fit the viewport. The test also blocks both origins and checks a visible error and completed loading region. Native fallback rendering is untouched.

## Sequence adaptation: 2026-10-08

Independent GPT-6.1 Sol xhigh design review rejected v0 and v1, then approved final v2 after two substantive revisions and final text-fit correction. Source, immutable prior snapshots, final hashes, screenshots and reports are in ignored Progress/mermaid/sequence; mock inputs are in ignored skill/quick-visualize/test/mermaid.

Real sandboxed iframe checks cover both themes, 736/320 inline →1440 fullscreen globals → original width: participant centers and lifelines remain aligned within1px. Click-first then focus-last updates details; first arrow and tooltip do not overlap. Stress retains actor icon, custom autonumber, self message, parallel/optional ranges and right note. Left/right/over variants and long self-label retain positions. Colored rect native fallback leaves scene styles unchanged under expansion. 14 interaction/geometry checks and25 Python tests pass. Native and Lieflat comparison fragments both render without page errors; Lieflat uses its documented library-out L11 translation, not an existing Sequence template.

Motion checks show masked420ms traces,140ms stagger,180ms labels and60ms arrow reveal, preserving reply dashes; reduced-motion transitions are none. Independent review confirms hover/resize do not replay and complete exit/re-entry does. These are runtime and simulated host-mode evidence; actual Codex toolbar expansion, return and Copy as image remain separate GUI acceptance.

## State adaptation: 2026-10-08

GPT-6.1 Sol xhigh rejected v0/v1 and approved v2 after two substantive visual/interaction/motion revisions. Version fragments/snapshots, actual iframe previews and review reports are in ignored Progress/mermaid/state; mock data is in ignored skill/quick-visualize/test/mermaid. Main8 states/9 transfers, compound12 states/11 transfers/two containers and fork/join6 states/6 transfers all render and fit.

Independent final review measured7 main labels8px from wires; compound labels8.16–8.20px. Choice tooltip has zero overlap and11.826px clearance. Retry side ports are independent from vertical main flow. Both resize-first and globals-first expanded-mode sequences restore390px inline scroll. Motion includes240/650/50ms marks and180ms labels; hover/resize preserve replay count, complete exit/re-entry replays. Four additional light/dark320/736 mode/interaction cases pass, as do30 shared viewport regression checks covering flow/architecture/navigation and six unchanged native fallback cases. Native and Lieflat G6 comparison fragments render without page errors. These remain simulated host globals/runtime evidence; real Codex toolbar and clipboard acceptance are separate.

State viewport revision also passes14 fresh Sequence interaction/geometry checks against the current shared source; original approved Sequence v2 artifacts remain frozen. Nine installed state-related files are byte-verified with backups and SHA-256 records.

## ER adaptation: 2026-10-08

GPT-6.1 Sol xhigh reviewed v0/v1/v2 and approved v2 after two substantive revisions. All mock sources live under ignored skill/quick-visualize/test/mermaid; frozen versions, source snapshots, actual sandbox previews, screenshots and review measurements live in ignored Progress/mermaid/er. Basic5 entities/16 fields/4 relationships and stress5 entities/11 fields/4 relationships retain aliases, combinedPK/FK, optional/mandatory cardinalities, self relation, long names and isolated empty entity.

Independent final visual review verifies all25 keyboard targets in actual320px iframe, Escape not reopening, field-only active states, zero tooltip overlap with all5 entity cards in wide light/dark, distinct per-relationship/self ports, two immediate-scroll50px fit/restore orders, trace/reveal frames80/450/1200ms, real full-exit/re-entry and reduced/static expanded motion. True visibilitychange could not be generated by the independent browser (events=[]), so real visibility recovery is explicitly unverified; no fake event is reported as real. Native styled ER fallback preserves scene/viewport/SVG styles across expanded globals.

Current shared source passes30 existing flow/architecture/native cases,14 Sequence interaction/geometry cases,4 State mode/interaction cases and25 Python tests. Lieflat uses documented G6 library-out translation, with endpoint cardinality labels and full entity field details; native/Lieflat previews render without page errors. Real Codex toolbar/clipboard proof remains separate from independent iframe/global tests.


## Architecture-beta final adaptation: 2026-10-08

Same GPT-6.1 Sol xhigh reviewer rejected v0/v1 and approved v2 after two substantive revisions. Actual Mermaid DB identity, nested membership, junctions, T/B/L/R, both arrowheads and group-modified donor services are retained. Pinned11.12 has restricted architecture label grammar; all three comparisons use identical valid ASCII source, with optional Chinese qv descriptions.

Final independent sandbox proof covers 12 light/dark320/736/1024 cases, full fit/scroll restoration, 240px complete wrapped names, correct two-line66px card height, 320px group previews, all16 actual object choices, true Tab scrolling of5 groups/10services/junction, settled detail restoration, Escape cancellation, group navigation, and unscaled12px detail without diagram overlap. Whole root truly leaves the iframe (bottom=-573.59) then replays3→4;240/650/50 timing and reduced-motion0 animations pass. Real Codex toolbar/clipboard/document-hidden remain separate acceptance boundaries. Native fallback returns before qv viewport and resource reader initialization.

Mock sources/specs remain in ignored skill/quick-visualize/test/mermaid, frozen versions/reports/evidence in ignored Progress/mermaid/architecture. Lieflat comparison honestly follows library-out G6 translation; boundaries preserve source membership, straight connections preserve logical direction and port metadata in detail, without claiming qv's port geometry.

## Flowchart review: 2026-10-11

The current flowchart layout supersedes the historical fixed 48px/single-line geometry acceptance above. Generate `flowchart-review-{normal,shapes,stress}.mmd` as `flowchart-{normal,shapes,stress}-refined.html`, wrap with bundled Visualize, and serve the previews at `127.0.0.1:8792`. Use `navigation: expanded` for the stress source. Pass `tests/mermaid-flowchart-browser-check.js` to Playwright as a page function.

The check covers light/dark at 736/320px, all 9/8/28 nodes and 10/10/33 edges, wrapped labels, node overlap and sampled wire collisions, stress aspect ratio, complete expanded bounds, nested group navigation, wrapped preview labels, and restoring the full graph. The stress diagram now measures about 1534×1678 instead of 14114×685. Browser theme and fullscreen globals are simulated with the actual bundled iframe wrapper; the final Codex message-flow review remains user acceptance. Keyboard tooltip and long-description behavior were deliberately excluded from this fix.

The refined checks also assert centered labels, single-line short diamonds and no folding of the two small fixtures. `tests/mermaid-flowchart-interaction-check.js` verifies sibling/ancestor breadcrumb jumps, keyboard dismissal, and one stable tooltip appearance while moving across a node after switching group mode off. Continuous Codex host hovering still requires user acceptance because the reported host flicker was not reproduced in the independent wrapper.

`tests/mermaid-flowchart-hover-check.js` uses `flowchart-stress-layers-preview.html`. It moves the real mouse rapidly across several nodes in light/dark fullscreen mode, checks that no intermediate or neutral highlight is committed, then verifies settled transfer and delayed exit. It also checks the arrow-only external group portal and actual navigation.

The timing regression now also moves inside one large node continuously for over 400ms, then returns to the prior node before testing cross-node transfer. The previous pending-target short circuit fails this case; the idle timer passes. Containment checks assert leaf/direct/outer levels 0/1/2, opaque composited white/gray/white pixels in both themes, outer-before-inner paint order and wires above container surfaces.

Flowchart regression: use a 180px viewport with the 28-node stress fixture. After enhanced readiness, nodes must be visible even if intersection stays below 20%; check both themes, resize and expanded-mode return. Gray composite pixels should retain baseline light 251 and dark 27 against backgrounds 255 and 24.
