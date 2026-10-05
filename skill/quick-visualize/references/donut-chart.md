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
- The center shows the total. Hover temporarily shows the active category and percentage; leaving restores the total.
- Up to 4 categories with every share at least 8%, short labels (up to 12 characters), and at least 420px available width use direct labels; otherwise use a centered bottom legend.
- Labels fade in during the ring reveal. Returning to view replays motion; reduced motion shows the final state. No click pinning.
