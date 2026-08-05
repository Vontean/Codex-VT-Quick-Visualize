# Radar Chart specification

Use this template for 1-4 objects measured across the same 3-8 dimensions on one shared non-negative scale.

```json
{
  "title": "多维指标对比",
  "max_value": 100,
  "value_prefix": "",
  "value_suffix": " 分",
  "decimals": 0,
  "dimensions": ["维度 A", "维度 B", "维度 C", "维度 D", "维度 E"],
  "series": [
    {"name": "对象 A", "values": [82, 68, 91, 74, 86]},
    {"name": "对象 B", "values": [70, 88, 76, 90, 65]}
  ]
}
```

- `title`, `dimensions`, and `series` are required.
- `dimensions` must contain 3-8 unique, concise labels. Each label may contain at most 12 characters.
- `series` must contain 1-4 uniquely named objects. Every `values` array must match the dimension order and length exactly.
- Every value must be finite, non-negative, and no greater than `max_value`.
- `max_value` must be a finite positive number and defaults to `100`. Every dimension uses this same scale.
- `value_prefix` and `value_suffix` are optional strings used for hover values.
- `decimals` accepts an integer from 0 to 2 and defaults to `0`.
- With multiple series, hover a legend item or point to focus it temporarily. Click a legend item to lock focus; click it again to restore all series.
- Hover a data point to compare every series on that dimension in one bubble.
