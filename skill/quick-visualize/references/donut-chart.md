# Donut Chart specification

Use this template for 2-6 categories whose non-negative values form one whole. The renderer derives the total, percentages, and largest category.

```json
{
  "title": "类别构成",
  "value_prefix": "",
  "value_suffix": "",
  "decimals": 0,
  "items": [
    {"label": "类别 A", "value": 38},
    {"label": "类别 B", "value": 24, "description": "可选说明"},
    {"label": "类别 C", "value": 18}
  ]
}
```

- `title` and 2-6 unique `items` are required.
- Every item requires a unique `label` and a finite, non-negative numeric `value`.
- The sum of all values must be greater than zero.
- An item may include a short `description`. Omit it to keep the hover bubble to label, value, and percentage only.
- `value_prefix` and `value_suffix` are optional strings used for hover values.
- `decimals` accepts an integer from 0 to 2 and defaults to `0`.
- The default center shows the largest category and its percentage. Hover temporarily switches the center to the active category and restores the default on pointer leave.
