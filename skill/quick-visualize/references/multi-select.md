# Multi Select specification

Use `multi-select-simple` for concise labels and `multi-select-complete` when every option needs supporting text.

```json
{
  "variant": "multi-select-complete",
  "question": "Which items apply?",
  "options": [
    {
      "label": "First choice",
      "supporting_text": "Explain the impact or boundary of this choice.",
      "value": "first"
    },
    {
      "label": "Second choice",
      "supporting_text": "Add concise context that helps the user decide.",
      "value": "second",
      "selected": true
    }
  ],
  "selected": ["First choice"],
  "follow_up_prompt": "The user selected: {selected}. Continue from these choices.",
  "follow_up_title": "Confirm selection"
}
```

- `question` and 2-20 `options` are required.
- `variant` accepts `multi-select-simple` or `multi-select-complete`; it defaults to `multi-select-simple`.
- A string option uses the same label and value. An object option may set `label`, `supporting_text`, `value`, and `selected`.
- `multi-select-complete` requires `supporting_text` for every option.
- `selected` may contain option labels or values and supplements per-option `selected` flags.
- Omit `follow_up_prompt` to render selection only, without `继续`.
- When present, `follow_up_prompt` must contain `{selected}`; the renderer replaces it with the current comma-separated labels.
- `follow_up_title` is an optional 1-250 character string shown as the confirmation-dialog heading after the user selects 继续. It is ignored when `follow_up_prompt` is omitted.
