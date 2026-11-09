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
| `mermaid` | `flowchart` / `architecture-beta` / `sequenceDiagram` / `stateDiagram-v2` / `erDiagram` / `classDiagram` / `timeline` / `journey` / `kanban` / `pie` / `xychart-beta` / `radar-beta` / `sankey-beta` / `quadrantChart` / `block-beta` / C4 / `mindmap` / `gantt` / `gitGraph`; qv drawing, explicit fallback outside scope | [Mermaid](references/mermaid.md) |
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

Mermaid references include `mode="wide"` (ASCII) or `"mode":"wide"` (legacy) for the native expanded preview. Keep it unchanged; enhanced qv diagrams fit the current view on expansion, except Gantt, whose container hugs its content at 1:1 scale. Native fallback retains its existing renderer behavior.

An inline visualization error means the host recognized the reference but failed to load or run the content. Check the filename, path and runtime before blaming model compatibility; `ok: true` confirms generation and static checks, not host rendering.

Architecture-beta preserves full wrapped names. Hover, focus or click reads structured resource/group details in a nearby theme-aware tooltip, independent of scene scaling; no detail panel or object selector below the diagram.

数据浮层使用共享 token：浅色为 `--popover`，深色为 `--popover-foreground` 向 `--popover` 混入 6%；文字为 `--popover-foreground`，名称为 `--muted-foreground`，数值为主文字色、500 字重及等宽数字。1px `--border`、12px 圆角、12×14px 内距；标题14px/20px、500字重，正文12px/18px。阴影为浅色前景9%、深色黑色50%；140ms 淡入和 .97 浮起，reduced-motion 关闭过渡。

For node-based Mermaid diagrams, proactively apply the shared design principles in the Mermaid reference: measured threshold-based wrapping, available-width axis comparison, alternating containment surfaces, stable hover, state-only hierarchy navigation and separately calibrated themes. Preserve each diagram type's semantic shapes and relationships; do not wait for the user to repeat accepted principles.

For Mermaid, declare semantic icons for all architecture services; use groups for semantic containment, always showing the complete flowchart/architecture. State diagrams retain their own hierarchy navigation. Explain distinct edge styles with semantic legends or edge labels.

Add concise explanation outside the visual when needed. Never replace the reference with a Markdown link. Use the returned absolute executor path.

`Confirm` places the chosen values in the composer for user review and manual sending. Chart interactions stay local. All presets share a dot-field loading state that ends on initialization readiness, with no minimum display time.


图表与标题对齐：增强 Mermaid 的可容纳画布居中，超宽时保留左端可达和横向滚动；Journey 的参考轴与步骤区整体居中。单行图表标题与可见容器居中，去掉单侧90px留白；长标题自然换行后左对齐，窄转宽后恢复单行居中。超宽绘图区滚动时标题保持在可见容器内，沿用Sankey标题与绘图区分离的规则。原生回退保留原生输出。
