# Skill maintenance

修改技能源码、契约或验证流程时读取。先定位技能来源仓库，在正式`skill/quick-visualize/`修改，再同步安装副本。若只有安装副本，先确认来源与现有安装方式。

## Ownership

| 变化 | Module / 文档所有者 |
| --- | --- |
| 任务路由、调用与结果交付 | `SKILL.md`；`scripts/render.py` |
| 数据校验、归一化与默认值 | 对应`references/<type>.md`及`scripts/render_<type>.py` |
| 共享样式、入场、浮层候选、标题/图例对齐 | `references/charts.md`；`assets/chart-*.js`及`chart-polish.css` |
| Mermaid输入、回退与类型路由 | `references/mermaid.md`；`assets/mermaid-model.js`及`mermaid.html` |
| 图型语义、布局、绘制 | 对应`mermaid-graphs.md`／`mermaid-process.md`／`mermaid-data.md`；`mermaid-<type>-model.js`、专用layout与renderer |
| 状态层级 | `mermaid-navigation.js`与`mermaid-state.js`；Flowchart/Architecture保持完整图 |
| 预设复用与模板组装 | `scripts/mermaid_presets.py`、`mermaid_assets.py`和`chart_assets.py` |
| 内联/展开/返回 | `mermaid-viewport.js`；预设沿用自身响应式路径 |
| fragment静态校验 | `scripts/check_fragment.py` |
| 架构取舍、一次验收结果 | 源码仓库的`docs/ARCHITECTURE.md`、`docs/verification/`；这些不作为技能分发依赖 |

## Workflow

1. **定位。** 找到拥有该规则的reference、Module及所有实际调用方。完成条件：说明改变的是输入、语义、布局、呈现还是宿主契约，并识别直接依赖。
2. **实现。** 更新规则的单一权威位置与源实现。保持语义模型与绘制区分；共享能力通过小Interface接入，优先复用现有真实Adapter。完成条件：修改可由实际调用方使用，旧冲突规则与不可达路径已清理。
3. **验证。** 源码仓库运行`python3 -m unittest discover -s tests -v`；视觉行为按变更范围覆盖常规/压力、主题、宽窄及相关交互。编译或预设复用变化需覆盖Pie/Radar两条路径；状态导航变化覆盖进入与返回；viewport变化覆盖原生回退。完成条件：等待完整渲染及readiness，记录失败与未覆盖范围。
4. **交付。** 用项目现有流程同步本机技能，逐文件核对正式资产与文档；保留当前交付物和证据，清理任务临时环境。完成条件：来源与安装入口一致，报告代码验证和宿主视觉验收各自状态。

## Interfaces and change cost

- 统一runner是调用方的入口：输入spec与输出路径，返回可交付引用或带阶段的失败；原子写入保护已有结果。
- Mermaid版本敏感读取集中在model Adapter；保留源ID、方向、端口、形状及数值。升级解析器时用真实浏览器夹具验证语义和回退。
- 模板`*_JS`占位符属于源码编译协议。Mermaid模块名映射对应资产文件；共享资产和预设由编译Module处理。新增图型先完成真实model/renderer，再接入路由。
- Pie/Radar是已有两种调用场景的真实复用。当前预设编译仍依赖模板脚本结构；修改模板runtime时检查生成结果，避免静态成功但运行失败。
- 测试通过调用方使用的Interface检查可见行为。已有浏览器夹具优先复用；只有真实变化需要不同Adapter时才增加Seam。
