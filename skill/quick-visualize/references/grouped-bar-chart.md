# Grouped Bar Chart specification

Use this template for 2-3 series measured across the same 2-6 categories on one non-negative numeric scale.

```json
{
  "title": "对象对比",
  "x_axis_label": "类别",
  "y_axis_label": "数值",
  "value_prefix": "",
  "value_suffix": "",
  "decimals": 0,
  "categories": ["类别 A", "类别 B", "类别 C"],
  "series": [
    {"name": "对象 1", "values": [42, 58, 51]},
    {"name": "对象 2", "values": [36, 63, 47]},
    {"name": "对象 3", "values": [49, 54, 60]}
  ]
}
```

- `title`, `x_axis_label`, `y_axis_label`, 2-6 unique `categories`, and 2-3 `series` are required.
- Every series requires a unique `name` and a `values` array matching the category count and order.
- Every value must be a finite, non-negative number. All series share one scale and unit.
- `value_prefix` and `value_suffix` are optional strings used for axes and hover details.
- `decimals` accepts an integer from 0 to 2 and defaults to `0`.
