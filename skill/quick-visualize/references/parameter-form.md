# Parameter Form series specification

Use this series for 1-12 independent settings. Every field type is a composable unit: use it alone, repeat it with unique names, or mix it with other field types in any order. If one field changes the visibility, options, validation, or meaning of another field, use the general Visualize skill instead.

```json
{
  "question": "Configure the output.",
  "fields": [
    {
      "type": "text",
      "name": "project_name",
      "label": "Project name",
      "value": "Quick Visualize",
      "placeholder": "Enter a name",
      "required": true
    },
    {
      "type": "textarea",
      "name": "notes",
      "label": "Notes",
      "value": "",
      "placeholder": "Optional context"
    },
    {
      "type": "select",
      "name": "format",
      "label": "Output format",
      "options": [
        {"label": "HTML", "value": "html"},
        {"label": "Markdown", "value": "markdown"}
      ],
      "value": "html"
    },
    {
      "type": "radio",
      "name": "mode",
      "label": "Execution mode",
      "options": ["Fast", "Balanced", "Deep"],
      "value": "Balanced"
    },
    {
      "type": "switch",
      "name": "auto_save",
      "label": "Auto save",
      "control_label": "Enabled",
      "checked": true
    },
    {
      "type": "checkbox",
      "name": "include_summary",
      "label": "Summary",
      "control_label": "Include in output",
      "checked": true
    },
    {
      "type": "range",
      "name": "detail",
      "label": "Detail level",
      "min": 1,
      "max": 10,
      "step": 1,
      "value": 6,
      "unit": "/10"
    }
  ],
  "follow_up_prompt": "Use these parameters: {parameters}. Continue."
}
```

## Field rules

- Supported types: `text`, `textarea`, `select`, `radio`, `switch`, `checkbox`, and `range`.
- Any supported type can form a single-field form or participate in a mixed form; field order in JSON is the rendered row order.
- Every field requires a unique ASCII `name`, a visible `label`, and a `type`.
- `text` and `textarea` accept `value`, `placeholder`, and `required`.
- `select` and `radio` require 2-8 options. A string option uses the same label and value; an object option may define both. `value` selects the initial option.
- `switch` and `checkbox` accept `checked`, `control_label`, and `required`.
- `range` accepts numeric `min`, `max`, `step`, and `value`, plus an optional `unit`.
- `follow_up_prompt` is required and must contain `{parameters}`. The renderer replaces it with a semicolon-separated summary of the current visible values.
