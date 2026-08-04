---
name: quick-visualize
description: Render preset in-conversation interactions through the Visualize plugin. Use for concise or supported multi-selects, drag-to-rank lists, 1-12 independent form fields, or choosing one of 2-4 plans across shared dimensions; use request_user_input for 1-3 simple mutually exclusive choices and general Visualize for linked parameters, conditional forms, charts, simulations, or bespoke layouts.
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
- Use the general Visualize skill when no preset fits, fields depend on each other, plan structures differ, or the task needs charts, simulation, or bespoke interaction.

Finish routing when one path covers every requested interaction without changing the user's decision model.

## Render

1. Load the installed Visualize skill and follow its inline HTML output contract. Finish when the current thread's visualization directory and presentation directive are known.
2. Read the matching template reference:
   - [Multi Select](references/multi-select.md)
   - [Ranker](references/ranker.md)
   - [Parameter Form](references/parameter-form.md)
   - [Comparison](references/comparison.md)
3. Write a UTF-8 JSON spec in `work/` or another safe temporary directory. Finish when every visible label, value, initial state, and follow-up placeholder is explicit.
4. Resolve this skill directory and run only the matching renderer:

   ```bash
   python3 scripts/render_multi_select.py <spec.json> <thread-visualization-directory>/<title>.html
   python3 scripts/render_ranker.py <spec.json> <thread-visualization-directory>/<title>.html
   python3 scripts/render_parameter_form.py <spec.json> <thread-visualization-directory>/<title>.html
   python3 scripts/render_comparison.py <spec.json> <thread-visualization-directory>/<title>.html
   ```

   Finish when the renderer exits successfully and writes the requested fragment.
5. Read the fragment once. Finish when it matches the spec, contains no unresolved `{{...}}` token, and its JavaScript parses.
6. Put the question in normal Markdown, then emit `::codex-inline-vis{file="<title>.html"}` on its own line. Finish when the directive filename exactly matches the generated fragment.

Never author or patch template markup for question-specific content. Change only the JSON spec; fall back to general Visualize when the preset cannot express the request.

## Composer handoff

- Render `继续` and call only `await window.openai.sendFollowUpMessage({ prompt })`; multi-select may omit the action by omitting `follow_up_prompt`, while Ranker, Parameter Form, and Comparison always include it.
- Treat the result as a composer handoff: Codex Desktop places the prompt in the input box for user review and manual sending. Never describe it as immediate sending.
- Do not use raw MCP Apps `ui/message`; it produces the same composer handoff. Never access or automate the parent composer from the visualization sandbox.
