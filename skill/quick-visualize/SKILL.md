---
name: quick-visualize
description: Render preset multi-selects, rankings, independent parameter forms, same-dimension comparisons, and simple Line, Grouped Bar, Donut, or Radar Charts through Visualize. Use only when a bundled specification preserves the full data and interaction model; route 1-3 simple mutually exclusive choices to request_user_input and unmatched requests to general Visualize.
---

# Quick Visualize

Pair this skill with the installed and enabled `visualize@openai-bundled` plugin. The bundled templates and renderers create Visualize-compatible HTML fragments; Visualize supplies the thread-scoped surface and inline message contract.

## Route

Choose exactly one path before writing a spec:

- Use `request_user_input` for 1-3 simple, mutually exclusive choices when the tool is available.
- Use `multi-select-simple` for 2-20 concise, non-exclusive options.
- Use `multi-select-complete` for 2-20 non-exclusive options that each need supporting text.
- Use `ranker` when the user must order 2-20 one-line items.
- Use the `parameter-form` series for 1-12 independent fields.
- Use `comparison` when the user must choose one of 2-4 plans described by the same 2-8 dimensions.
- Use `line-chart` for one simple, non-negative measure changing over 2-90 dated observations.
- Use `grouped-bar-chart` for 2-3 series measured across the same 2-6 categories on one non-negative scale.
- Use `donut-chart` for 2-6 categories whose non-negative values form one whole.
- Use `radar-chart` for 1-4 objects measured across the same 3-8 dimensions on one shared non-negative scale.
- Use the general Visualize skill when no bundled specification can carry the complete requested data and interaction model.

## Render

1. Load the installed Visualize skill and follow its inline HTML output contract. Finish when the current thread's visualization directory and content-reference format are known.
2. Read only the reference selected during routing, then use its paired renderer:

   | Route | Reference | Renderer |
   | --- | --- | --- |
   | `multi-select-simple`, `multi-select-complete` | [Multi Select](references/multi-select.md) | `scripts/render_multi_select.py` |
   | `ranker` | [Ranker](references/ranker.md) | `scripts/render_ranker.py` |
   | `parameter-form` | [Parameter Form](references/parameter-form.md) | `scripts/render_parameter_form.py` |
   | `comparison` | [Comparison](references/comparison.md) | `scripts/render_comparison.py` |
   | `line-chart` | [Line Chart](references/line-chart.md) | `scripts/render_line_chart.py` |
   | `grouped-bar-chart` | [Grouped Bar Chart](references/grouped-bar-chart.md) | `scripts/render_grouped_bar_chart.py` |
   | `donut-chart` | [Donut Chart](references/donut-chart.md) | `scripts/render_donut_chart.py` |
   | `radar-chart` | [Radar Chart](references/radar-chart.md) | `scripts/render_radar_chart.py` |

3. Write a UTF-8 JSON spec in the task's `work/` directory or another safe task-owned location. Finish when every required value and interaction is explicit and valid under the selected reference.
4. Resolve this skill directory and run `python3 <renderer> <spec.json> <output-directory>/<title>.html`. The output directory is the thread-scoped visualization directory when it appears in the writable roots; otherwise use the task's supplied `work/` directory or an output directory under the authorized working directory. Never save fragments to system temp or Library. Finish when the renderer exits successfully and returns the requested fragment path.
5. Read the fragment once. Finish when it matches the spec, contains no unresolved `{{...}}` token, and its JavaScript parses.
6. Put any necessary question or explanation in normal Markdown, then emit the Visualize content reference with the renderer's exact output path on its own line. The reference is a client token wrapped in invisible private-use boundary characters, not plain Markdown. Its exact shape is U+E200, then the literal text `visualize`, then U+E202, then the JSON object, then U+E201:

   ```text
   visualize{"path":"<absolute-path>/<title>.html"}
   ```

   The wide variant is:

   ```text
   visualize{"path":"<absolute-path>/<title>.html","mode":"wide"}
   ```

   Resolve the absolute executor-side path from the current task environment; never hard-code a developer-machine directory or use a relative path. The JSON object may include `"title"` when useful. Add `"mode":"wide"` only for a full-screen desktop app mockup or when several compact chart panels must stay side by side to remain readable. Never add a Markdown link to the reference, and never announce it as an artifact, attachment, or download. Before sending, verify the emitted token actually contains U+E200, U+E202, and U+E201; a token missing them renders as literal text instead of a visualization. Finish when the reference points to the fragment generated in this invocation.

Never author or patch template markup for question-specific content. Change only the JSON spec; fall back to general Visualize when the preset cannot express the request.

## Composer handoff

- Render `继续` and call `await window.openai.sendFollowUpMessage({ prompt, title })`. Include `title` as the concise confirmation-dialog heading (1-250 characters) whenever the spec provides `follow_up_title`; omit the field when it is absent. Multi-select may omit the action by omitting `follow_up_prompt`, while Ranker, Parameter Form, and Comparison always include it.
- Keep Line Chart, Grouped Bar Chart, Donut Chart, and Radar Chart hover and inspection local to the visualization; they have no composer handoff.
- Treat the result as a composer handoff: Codex Desktop places the prompt in the input box for user review and manual sending. Never describe it as immediate sending.
- Do not use raw MCP Apps `ui/message`; it produces the same composer handoff. Never access or automate the parent composer from the visualization sandbox.
