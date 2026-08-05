# Line Chart specification

Use this template for one non-negative measure across 2-90 unique dates, with an optional description on each point.

```json
{
  "title": "单序列趋势",
  "x_axis_label": "时间",
  "y_axis_label": "数值",
  "value_prefix": "",
  "value_suffix": "",
  "decimals": 0,
  "points": [
    {"date": "2026-07-07", "value": 42},
    {"date": "2026-07-08", "value": 58, "description": "可选说明"},
    {"date": "2026-07-09", "value": 51}
  ]
}
```

- `title`, `x_axis_label`, `y_axis_label`, and 2-90 `points` are required.
- Every point requires a unique ISO `YYYY-MM-DD` `date` and a finite, non-negative numeric `value`.
- A point may include a short `description`. Omit it to keep the hover bubble to date and value only; the renderer never invents or derives a description.
- Input points may be unordered; the renderer sorts them chronologically.
- `value_prefix` and `value_suffix` are optional strings used for axis values and hover details.
- `decimals` accepts an integer from 0 to 2 and defaults to `0`.
- The renderer uses a smoothed line, zero-baseline gradient area, visible observations, and a hover bubble.
