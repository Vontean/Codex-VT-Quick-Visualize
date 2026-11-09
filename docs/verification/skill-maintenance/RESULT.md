# 技能文档与Module职责审查

2026-11-09。使用`writing-for-agents`的context pointer、progressive disclosure、co-location、single source of truth与完成条件，以及`codebase-design`的Module / Interface / Seam / Depth / Locality审查正式技能。审查覆盖全部正式文件的职责清点，并追踪关键调用链；不是逐行安全审计或全语法/全平台认证。

## 文档发现与修正

| 发现 | 处理与权威归属 |
| --- | --- |
| Mermaid共性段仍要求规模阈值平衡、复杂容器下钻，与新规则冲突 | 清除过时指引；完整图与状态导航分清，当前主轴规则放到节点图专用reference |
| 浮层token、对齐、动效在SKILL、DESIGN、Mermaid/Radar多处复制 | `references/charts.md`拥有共享规则，其余位置用触发明确的pointer |
| 安装后的reference指向包外DESIGN与仓库测试文档 | 生成路径全部改为包内引用；维护时才区分来源仓库的结构与验证材料 |
| Mermaid文档同时承担输入、十九图型、实现路径与历史补丁说明 | 主文档只保留输入、路由和宿主契约；按节点关系/过程时间/数据图披露图型差异；维护机制单独归maintenance |
| README、DESIGN累积实现细节和重复规范 | README拥有安装/更新与索引；DESIGN拥有意图/取舍与归属；Architecture拥有Module与结构限制 |
| 旧review/TODO和验收记录可能被误当当前状态 | 验证索引明确历史快照职责；早期18图型清单加历史标记，保留原勾选与原始事实 |
| 技能元数据未清楚覆盖Mermaid | description与宿主short description同步当前用途，保持自动发现条件聚焦真实预设 |

入口负担：SKILL从62行到35行；Mermaid入口从275行到64行，专用规则按分支读取。DESIGN从229行到31行，README从237行到81行。行数只用于说明披露位置，不作为质量或Depth评分。

已核对其余输入reference与对应renderer的数据约束/默认值；未发现本轮需修改的Multi Select、Ranker、Comparison、Parameter Form schema。没有扩展这些交互功能。

## 代码结论

**领域设计基本具备，柔性设计部分具备，尚不能称为彻底解耦。**

- 统一runner的Interface较深：调用方获得校验、加载、原子写入、引用与错误定位。图型的真实语义Adapter及layout/renderer划分具有领域依据，未使用虚构业务模型取代Mermaid。
- 本轮收拢模板组装Module：输入校验不再知道四十余个资产；共享资产注册只有一处。组装重构阶段38份Mermaid夹具的完整fragment逐字节一致，见[compiler-equivalence.json](compiler-equivalence.json)。此等价验证不泛指后续对齐Module内部调整后的所有字节相同。
- `alignChartPresentation(root)`成为标题/图例的单一Interface，内部共用一次宽度观察；样式归共享CSS，不再通过JS向head注入全局图例规则。文件名改为`chart-alignment.js`以对应真实职责。
- State scope投影清除Flowchart/Architecture的旧预览、DOM测量和无用布局字段，成为只依赖模型的纯投影；保留真实计数、完整直接子状态、外部转移、自环及分组返回。替换两项旧预览测试，改测当前状态行为。
- Donut的原值、showData和系列循环逻辑回到源模板，预设编译器不再按字符串修改这些领域表现。

剩余结构限制见[Architecture](../../ARCHITECTURE.md)：Flowchart/Architecture绘制仍与组合根同处；部分Module仍依赖root/cfg等闭包环境；预设Adapter仍转换模板脚本结构；部分renderer长行降低可读性。这些是已识别的维护风险，不是本轮隐藏的失败，也没有引入尚无第二个真实Adapter的Port或DI框架来掩盖它们。

## 验证与安装

- Python回归及文档指针检查通过；最终数量见[python-tests.txt](python-tests.txt)。检查覆盖包内文件与章节引用、公开runner路由、仓库维护入口及现有数据/生成契约。
- [alignment.json](alignment.json)：29夹具×浅深色=58/58；覆盖19种增强Mermaid、长标题、小型C4、四种独立共享数据图与原生回退，宽→窄→宽。
- [interactions.json](interactions.json)：22条通过；Radar通用/预设hover与键盘、浮层样式、展开事件和滚动恢复、reduced-motion、回退不接viewport。
- [dependencies.json](dependencies.json)：20条通过；State两层进入返回、Journey列宽、堆叠图例、预设offsetParent及流程hover快进/不重播。
- Skill Validator、Python编译、runner的JS/placeholder/ID/size检查与git diff --check通过。
- [inventory.json](inventory.json)：全部87份正式技能文件的职责与审查范围；同时登记入口、维护及历史文档角色。
- [install.json](install.json)：本机正式技能逐文件核对；退役`chart-legend.js`在核对旧版本后移除，现入口使用`chart-alignment.js`。

修改按“职责整理”和“文档归属/证据”分组提交，没有推送或发布npm，没有修改MineCodex。运行使用本任务专用浏览器和服务，结束后关闭；正式证据与安装恢复备份保留。

本轮没有宣称新的用户可见宿主验收。既有内联、原生展开/返回与最终视觉确认仍以用户反馈为准；已记录的较大结构限制也没有假称全部完成重构。
