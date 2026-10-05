---
name: quick-visualize
description: Render preset multi-selects, rankings, parameter forms, plan comparisons, and line, grouped bar, donut or radar charts in conversation. Use when a preset covers the full data and interaction model.
---

# Quick Visualize

Requires the enabled `visualize@openai-bundled` plugin, Python 3 and Node.js on PATH.

## Select

Read only the matching specification. If none fits, use general Visualize.

| Type | Scope | Specification |
| --- | --- | --- |
| `multi-select-simple` / `multi-select-complete` | 2–20 non-exclusive choices; complete adds supporting text | [Multi Select](references/multi-select.md) |
| `ranker` | Order 2–20 one-line items | [Ranker](references/ranker.md) |
| `parameter-form` | 1–12 independent fields | [Parameter Form](references/parameter-form.md) |
| `comparison` | Choose among 2–4 plans across the same 2–8 dimensions | [Comparison](references/comparison.md) |
| `line-chart` | One non-negative measure, 2–90 dates | [Line Chart](references/line-chart.md) |
| `grouped-bar-chart` | 2–4 series, 2–6 shared categories, non-negative scale | [Grouped Bar Chart](references/grouped-bar-chart.md) |
| `donut-chart` | 2–6 non-negative parts, positive total | [Donut Chart](references/donut-chart.md) |
| `radar-chart` | 1–4 objects, 3–8 shared dimensions, non-negative scale | [Radar Chart](references/radar-chart.md) |

## Execute

1. Write a UTF-8 JSON spec in a task-owned location.
2. Run `python3 <skill-dir>/scripts/render.py <type> <spec.json> <output-directory>/<title>.html`. Prefer the current thread's writable visualization directory; otherwise use task-owned `work/`. Never use system temp or Library.
3. On `ok: true`, emit the returned `reference` unchanged on its own line in the final answer. Do not read the HTML or load the full Visualize skill for a preset. The runner validates data, placeholders, element references, JavaScript syntax and size before writing.
4. On `ok: false`, fix the reported spec error or inspect only the relevant source around the reported line, then rerun. Template defects require a source fix; do not customize template markup for a single question. Browser checks are for template changes or suspected interaction/layout defects, not every invocation.

The reference contains U+E200 / U+E202 / U+E201:

```text
visualize{"path":"<absolute-path>/<title>.html"}
```

Add concise explanation outside the visual when needed. Never replace the reference with a Markdown link. Use the returned absolute executor path.

`Confirm` places the chosen values in the composer for user review and manual sending. Chart interactions stay local.
