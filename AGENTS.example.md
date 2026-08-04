# Quick Visualize routing

- 1–3 个简单且互斥的选择优先使用 `request_user_input`；多选、拖拽排序、独立参数表单或共享维度方案对比使用 `$quick-visualize`；联动参数、异构布局、图表或模拟使用通用 `Visualize`。
- `$quick-visualize` 按“识别模板 → 写 JSON spec → renderer 写入线程 visualization 目录 → 读取校验 → Markdown 提问 + inline-vis 呈现”执行；`继续` 只把结果写入输入框，由用户确认发送。
