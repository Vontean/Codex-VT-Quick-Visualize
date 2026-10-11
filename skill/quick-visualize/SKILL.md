---
name: quick-visualize
description: Render preset multi-selects, rankings, parameter forms, plan comparisons, and line, grouped bar, donut or radar charts, and Mermaid diagrams in conversation. Use when a preset covers the full data and interaction model.
---

# Quick Visualize

Requires the enabled `visualize@openai-bundled` plugin, Python 3 and Node.js on PATH.

## Select

Read only the matching specification. If no preset covers the required data and interactions, create a custom chart with general Visualize; use this skill’s chart styles and layouts as references to keep typography, spacing, colors and motion consistent, while choosing a structure that fits the actual data.

| Type | Scope | Specification |
| --- | --- | --- |
| `multi-select-simple` / `multi-select-complete` | 2–20 non-exclusive choices; complete adds supporting text | [Multi Select](references/multi-select.md) |
| `ranker` | Order 2–20 one-line items | [Ranker](references/ranker.md) |
| `parameter-form` | 1–12 independent fields | [Parameter Form](references/parameter-form.md) |
| `comparison` | Choose among 2–4 plans across the same 2–8 dimensions | [Comparison](references/comparison.md) |
| `line-chart` | One non-negative measure, 2–90 dates | [Line Chart](references/line-chart.md) |
| `grouped-bar-chart` | 2–4 series, 2–6 shared categories, non-negative scale | [Grouped Bar Chart](references/grouped-bar-chart.md) |
| `donut-chart` | 2–6 non-negative parts, positive total | [Donut Chart](references/donut-chart.md) |
| `mermaid` | `flowchart` / `architecture-beta` / `sequenceDiagram` / `stateDiagram-v2` / `erDiagram` / `classDiagram` / `timeline` / `journey` / `kanban` / `pie` / `xychart-beta` / `radar-beta` / `sankey-beta` / `quadrantChart` / `block-beta` / C4 / `mindmap` / `gantt`; qv drawing, explicit fallback outside scope | [Mermaid](references/mermaid.md) |
| `radar-chart` | 1–4 objects, 3–8 shared dimensions, non-negative scale | [Radar Chart](references/radar-chart.md) |

## Execute

1. Write a UTF-8 JSON spec in a task-owned location; `mermaid` also accepts a standard `.mmd` file.
2. Run `python3 <skill-dir>/scripts/render.py <type> <spec.json> <output-directory>/<slug>.html`. The runner defaults to the ASCII directive for every model. The filename must use lowercase ASCII letters, numbers and single hyphens, for example `donut-chart.html`; keep the display title in the spec, where Chinese is supported. Prefer the current thread's writable visualization directory; otherwise use task-owned `work/`. Never use system temp or Library.
3. On `ok: true`, emit the returned `reference` unchanged on its own line in the final answer. Do not read the HTML or load the full Visualize skill for a preset. The runner validates data, placeholders, element references, JavaScript syntax and size before writing. Mermaid syntax and layout are validated in the browser; runner success alone does not confirm a rendered diagram.
4. On `ok: false`, fix the reported spec error or inspect only the relevant source around the reported line, then rerun. Template defects require a source fix; do not customize template markup for a single question. Browser checks are for template changes or suspected interaction/layout defects, not every invocation.

Current Codex Desktop supports an ASCII directive. Use it for GPT and third-party models alike; copy the returned `reference` unchanged, without a code fence or Markdown link:

```text
::codex-inline-vis{path="<absolute-path>/<slug>.html"}
```

Only for older hosts that do not recognize the ASCII directive, explicitly run with `--reference-format visualize`. This legacy reference contains Unicode private-use code points U+E200 / U+E202 / U+E201; they are not a model-vendor permission gate:

```text
visualize{"path":"<absolute-path>/<slug>.html"}
```

Mermaid references include `mode="wide"` (ASCII) or `"mode":"wide"` (legacy) for the native expanded preview. Keep it unchanged; enhanced qv diagrams fit the current view on expansion. Native fallback retains its existing renderer behavior.

An inline visualization error means the host recognized the reference but failed to load or run the content. Check the filename, path and runtime before blaming model compatibility; `ok: true` confirms generation and static checks, not host rendering.

Architecture-beta preserves full wrapped names and offers unscaled resource/group details with a native object selector on narrow or expanded views. Selection reads the complete model without filtering it.

For node-based Mermaid diagrams, proactively apply the shared design principles in the Mermaid reference: measured threshold-based wrapping, threshold-based layout balancing, alternating containment surfaces, stable hover, focused group navigation and separately calibrated themes. Preserve each diagram type's semantic shapes and relationships; do not wait for the user to repeat accepted principles.

For Mermaid, declare semantic icons for all architecture services; use groups for overview/drilldown. Explain distinct edge styles with semantic legends or edge labels.

Add concise explanation outside the visual when needed. Never replace the reference with a Markdown link. Use the returned absolute executor path.

`Confirm` places the chosen values in the composer for user review and manual sending. Chart interactions stay local. All presets share a dot-field loading state that ends on initialization readiness, with no minimum display time.
