# Quick Visualize routing

- 1–3 个简单且互斥的选择优先使用 `request_user_input`；完整数据和交互能由 `$quick-visualize` 任一现有 spec 承载时使用对应模板，否则使用通用 `Visualize`。
- `$quick-visualize` 按“识别模板 → 写 JSON spec → renderer 写入线程 visualization 目录 → 读取校验 → Markdown 说明 + Visualize content reference 呈现”执行；`继续` 只把结果写入输入框，由用户确认发送。
