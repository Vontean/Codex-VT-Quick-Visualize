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
- Hover a legend item to focus that object temporarily; no click locking.
- Hover an axis to compare all objects on that dimension. Hover a point, polygon edge, or polygon interior to inspect one object's full profile. Points take precedence over axes; overlaps use the nearest outline.
- One tooltip stays near the pointer and chooses nearby positions with less polygon overlap. Object identity appears only in its heading; dimension comparisons retain one marker per object.
- Numeric grid labels are hidden. Vertices expand from the center with constant stroke/marker sizes, replaying on return to view; reduced motion disables entry animation.

数据浮层使用共享 token：浅色为 `--popover`，深色为 `--popover-foreground` 向 `--popover` 混入 6%；文字为 `--popover-foreground`，名称为 `--muted-foreground`，数值为主文字色、500 字重及等宽数字。1px `--border`、12px 圆角、12×14px 内距；标题14px/20px、500字重，正文12px/18px。阴影为浅色前景9%、深色黑色50%；140ms 淡入和 .97 浮起，reduced-motion 关闭过渡。

填充默认14%、当前24%、其他3%。气泡候选先排除覆盖指针的位置，优先32px内；受边界限制取最近可用距离+16px，再比较遮挡。定位转换使用实际offsetParent。入场900ms共享曲线，保持描边与标记尺寸。图例换行后单列居中、项内左对齐。
