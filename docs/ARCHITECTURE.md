# Module 与 Interface

本文件服务源码维护者，说明现有设计的职责与变化成本。Agent生成契约从[SKILL](../skill/quick-visualize/SKILL.md)开始；产品取舍和文档权威归属见[DESIGN](../DESIGN.md)。

## 运行链与领域

调用方 → `render_checked(kind, spec_path, output, reference_format)` → 对应`render(spec, output_path)` → 模板编译 → fragment检查 → 原子写入与引用。

输入分为两个真实领域：固定交互/数据预设，以及Mermaid源图。预设的输入校验和归一化在各`render_<type>.py`；Mermaid的身份、关系、端口、日期、分数、量表由版本敏感model Adapter读取。图型专用layout计算几何，renderer拥有DOM、SVG及交互。共享呈现复用token、入场、详情定位、对齐和viewport。

## Module职责

| Module | Interface与调用方要知道的契约 | Depth与Locality |
| --- | --- | --- |
| `render.py` | `render_checked(...)`返回引用或带阶段错误；成功前不覆盖已有文件 | 深：路由、加载、校验、写入、错误集中在同一入口 |
| `render_<type>.py` | `render(spec, output_path)`返回fragment或输入错误；路径只参与稳定ID | 每个领域拥有约束与归一化，普通模板可独立演进 |
| `check_fragment.py` | `check_fragment(fragment)`；需要PATH中Node；可返回HTML行号 | 深：大小、占位符、引用与JS语法检查集中；不承诺浏览器成功 |
| `mermaid_assets.py` | `compile_mermaid_template(path)`；受信模板的`*_JS`对应`mermaid-*.js` | 隐藏模块拼装与预设复用，输入校验不用知道四十余个资产 |
| `chart_assets.py` | 编译共享资产或由Mermaid外层继承；共享占位符只在一个注册表维护 | 真实Seam：独立图表与嵌入预设有不同交付方式 |
| `mermaid_presets.py` | `compile_presets(assets)`；返回Pie/Radar的嵌入Adapter | 深但脆弱：隐藏宿主装配；仍依赖模板脚本结构，见下文 |
| `mermaid-model.js`及各model | Mermaid解析结果→`{data}`或`{reason}`；源语义保留，未知语义明确回退 | 领域划分真实。Node/Edge、状态、提交、任务、坐标、量表各有专用模型 |
| `mermaid-navigation.js` | `mermaidScopeView(model,scope)`；纯状态层级投影，保留外部转移、自环和真实状态数 | 清除已移除的Flowchart/Architecture预览分支，不再依赖DOM测量 |
| `mermaid-layout.js`及专用layout | 以真实模型测量和计算几何；保留显式方向与端口 | 共享ELK与图型专用几何有清晰分工，但部分依赖闭包环境 |
| `mermaid-<type>.js` | `renderMermaid<Type>(root,data)`；部分图型异步；完成条件由外层qvReady承担 | 绘制与图型交互同处；Git的model/render同文件，随同一语义变化 |
| `mermaid.html` | 装配运行环境、分发、Flowchart/Architecture绘制、ready/失败 | 深度不均：既是组合根，也拥有较大图型Implementation |
| `chart-alignment.js` | `alignChartPresentation(root)`；按实际宽度处理标题和数据图例 | 一个Interface、一次观察；内部细节不由调用方排序 |
| `chart-motion.js` | 显式入场及共享进度；同批预算；尊重调用方的重播语义 | 多调用方实际复用，入场曲线和预算有单一所有者 |
| `chart-detail-position.js` / `mermaid-presentation.js` | 近候选筛选或局部详情定位、hover及包含层底色 | 纯候选规则与DOM几何分开；各图型仍拥有遮挡语义 |
| `chart-polish.css` | 共享token、标题、图例与浮层外观；位于root外 | 样式不藏在加载层或临时JS注入中，预设替换后仍存在 |
| `mermaid-viewport.js` | 增强图fit/hug、mode事件、滚动恢复；不接原生回退 | 实际宿主Seam；不是第二套全屏外壳 |
| `chart-loading.html` | 加载就绪、失败、可见性、卸载相关监听的结束 | 只拥有加载生命周期，不拥有领域样式 |

## 已确认的结构限制

1. **组合根与领域绘制尚未完全分开。** Flowchart/Architecture的绘制仍在`mermaid.html`，部分layout/model访问闭包中的`root`、`cfg`、Lucide。调用方隐含知道加载顺序，Interface比参数表面更大。下一次改这些领域时，可把已实际变化的DOM测量/布局依赖传入；本次不为假想替换增加Port。
2. **预设Adapter依赖模板脚本文本。** 即使语义行为已回归到Donut源模板，`mermaid_presets.py`仍将独立模板的IIFE、ID和ResizeObserver转换为嵌入调用。真实风险是模板重排后静态成功、运行缺信息。后续适合把Donut/Radar运行体抽成接受root/config的Module，让独立与Mermaid两个Adapter调用；需单独验证尺寸观察、就绪和展开契约。
3. **可读性不均。** 多个renderer以很长的压缩行维护。文件数量不等于良好Locality；修改细节常需同时理解同一闭包。按发生实际变化的Module整理，避免全仓格式化掩盖行为修改。
4. **验证能力有层次。** Python数据测试、静态fragment检查、浏览器完整渲染、宿主视觉验收是不同Interface。用真实图型/交互夹具验证；不以内部标记或单个runner成功跨越验收层次。

这些限制不表示现有每个Module都应拆分。简单标量校验在各领域文件重复，当前变更收益低；没有引入通用Repository、DI容器或只转发的Adapter。未来抽取前先做deletion test：复杂度应从调用方消失，维护知识应更集中。

## 维护方法

- 文档变化更新权威reference；源码结构变化更新本文件；一次验证结果放入有范围的记录。
- 跨预设/编译Seam时从统一runner验证；浏览器检查完整qvReady、状态、内容与交互。
- 文件职责逐项清单是[本次审查快照](verification/skill-maintenance/inventory.json)，不是需要人工维护的第二套注册表。
