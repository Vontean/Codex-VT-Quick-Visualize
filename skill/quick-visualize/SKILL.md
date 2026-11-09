---
name: quick-visualize
description: Render in-conversation multi-selects, rankings, independent parameter forms, plan comparisons, line/bar/donut/radar charts, and standard Mermaid diagrams when a preset covers the data and interactions.
---

# Quick Visualize

Requires enabled Visualize, Python 3 and Node.js on PATH.

## Select

Read the matching input contract. For charts, also read [shared presentation](references/charts.md). Mermaid routes to the relevant type section. When no preset covers the full data and interaction model, use general Visualize and retain the applicable shared design rules.

| Type | Task | Contract |
| --- | --- | --- |
| `multi-select-simple` / `multi-select-complete` | Non-exclusive choices; complete adds supporting text | [Multi Select](references/multi-select.md) |
| `ranker` | Order all items | [Ranker](references/ranker.md) |
| `parameter-form` | Independent settings | [Parameter Form](references/parameter-form.md) |
| `comparison` | Select one plan across shared dimensions | [Comparison](references/comparison.md) |
| `line-chart` | One measure over dates | [Line](references/line-chart.md) |
| `grouped-bar-chart` | Series across shared categories | [Grouped Bar](references/grouped-bar-chart.md) |
| `donut-chart` | Non-negative parts of a whole | [Donut](references/donut-chart.md) |
| `radar-chart` | Objects on shared dimensions and scale | [Radar](references/radar-chart.md) |
| `mermaid` | Standard diagram source, enhanced drawing or explicit native fallback | [Mermaid](references/mermaid.md) |

## Execute

1. Write a UTF-8 JSON spec, or `.mmd` for Mermaid, in the current task's visualization directory; otherwise use task-owned `work/`. Complete this step when the data satisfies the matching contract.
2. Run `python3 <skill-dir>/scripts/render.py <type> <spec> <output-directory>/<slug>.html`. Use lowercase ASCII words separated by single hyphens for the filename; keep Chinese display text in the spec.
3. On `ok:true`, emit the returned `reference` unchanged on its own line, without a code fence or Markdown link. The default ASCII directive works across model providers. Only older hosts that reject ASCII use explicit `--reference-format visualize`; preserve Mermaid's returned wide-mode field. Completion means generation and static checks passed; Mermaid remains `runtime:pending-browser` until runtime checks finish.
4. On `ok:false`, fix the reported input or source location and rerun; use the newly returned result. For a template defect or suspected layout/interaction defect, read [maintenance](references/maintenance.md) and validate in the browser. Normal preset use needs neither generated-HTML inspection nor the full Visualize skill.

`Confirm` puts chosen values in the composer for user review and manual sending. Chart interactions stay local. Add concise explanation outside the visual when it helps the user interpret the result.

When maintaining this skill’s source, contracts or documents, read [maintenance](references/maintenance.md) first.
