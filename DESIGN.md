# 设计决策与规则归属

本文件服务技能维护者，记录设计意图及取舍。当前产品契约由正式技能内的references拥有，安装后的技能可以独立读取它们。

## 规则归属

| 维护内容 | 权威位置 |
| --- | --- |
| 选择模板、执行、成功与失败处理 | [SKILL](skill/quick-visualize/SKILL.md) |
| 各预设的数据约束、默认值、交互 | [对应reference](skill/quick-visualize/references/) |
| 图表标题、图例、文字层级、浮层、动效、加载 | [Charts](skill/quick-visualize/references/charts.md) |
| Mermaid输入、图型路由、回退、内联与展开 | [Mermaid](skill/quick-visualize/references/mermaid.md) |
| Mermaid专用语义与布局 | [节点关系](skill/quick-visualize/references/mermaid-graphs.md)、[过程时间](skill/quick-visualize/references/mermaid-process.md)、[数据图](skill/quick-visualize/references/mermaid-data.md) |
| 修改位置与完成条件 | [Maintenance](skill/quick-visualize/references/maintenance.md) |
| Module职责、Interface、依赖与结构风险 | [Architecture](docs/ARCHITECTURE.md) |
| 一次验证的输入、环境、结果、未覆盖项目 | [验证记录](docs/verification/) |

修改规则时更新其权威位置，再同步实现和相关证据。历史结果描述当时状态，不追加为新的产品规则。

## 设计意图

- **输入只有一份。** Mermaid拥有图形身份与关系，JSON预设拥有观测值与量表。绘制层由真实输入计算几何；名称、面积或空间不用于推导未声明业务含义。
- **阅读优先。** 完整文字可达、连接语义清楚、真实数量与日期保持准确。长文本先测量，画布不足时滚动，局部详情保持与触发对象关联。
- **同义能力共用实现。** Pie与Donut、受约束的Mermaid Radar与Radar预设复用绘制。表达能力不足时使用能保留原语义的增强路径或明确回退。
- **交互按图型发生。** 状态图有复合状态；Flowchart与Architecture展示完整结构。图表的hover、详情及图例行为不转化为数据编辑或自动发送。
- **宿主拥有展示外壳。** 技能输出fragment和引用，保留宿主主题、原生展开及返回。渲染完成、结构测量和真实宿主视觉验收分别记录。
- **共享规则有单一所有者。** 样式token在共享图表资产实现，调用方采用同一规则。加载层只拥有加载生命周期；数据约束和图型语义留在领域Module。

## 当前依据

已发布Mermaid产品规则回迁及后续对齐复核的证据见[交付记录](docs/verification/mermaid-polish/RESULT.md)。这些记录用于追溯，不作为生成技能时需要读取的材料。
