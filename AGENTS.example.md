# 可视化与提问路由

- 流程、关系、比较或数据适合用图说明时，主动在消息流中呈现，优先 `$quick-visualize`；预设无法覆盖时，静态图用原生 Mermaid（默认外观），动态交互用 `@Visualize`。简单事实用文字。
- 1–3 个简单、互斥的选择优先使用可用的 `request_user_input`；多选、排序、表单或带维度的方案比较使用 `$quick-visualize`。
