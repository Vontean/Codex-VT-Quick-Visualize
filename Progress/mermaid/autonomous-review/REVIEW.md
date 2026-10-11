# 剩余9种 Mermaid 图表：自主审视

2026-10-12。本轮自主优化已完成，9种图表均待用户明天验收。主清单保持9/18 checked；不把自动测试等同于视觉确认。

## 逐图改动与验收入口

| 图 | 核心改动 | 检查记录 |
| --- | --- | --- |
| architecture-beta | 白灰包含层、端口保留、详情resize与退出时序 | [architecture](architecture-REVIEW.md) |
| sequenceDiagram | 参与者及消息实际换行测高、分层关系详情、总入场时长收敛 | [sequence](sequence-REVIEW.md) |
| erDiagram | 白底分区卡片、独立字段行高、真实关系基数与近详情 | [ER](er-REVIEW.md) |
| pie | 直接复用已确认donut模板，零值无弧，大数与原始值保留 | [Pie](pie-REVIEW.md) |
| xychart-beta | 分类聚焦、重复名称独立位置、水平布局长文本容纳 | [XY](xy-REVIEW.md) |
| radar-beta | 简单参数复用radar模板，复杂参数保留原语义扩展绘制 | [Radar](radar-REVIEW.md) |
| sankey-beta | 近节点／流详情、保持极小流比例、明确失败／回退 | [Sankey](sankey-REVIEW.md) |
| block-beta | 手动网格和展开几何一致、包含层、长组名测高 | [Block](block-REVIEW.md) |
| C4 | 白灰边界、线与次级文字对比、近详情、去除无效详情区 | [C4](c4-REVIEW.md) |

## 验证证据与边界

- `results.json`：72组，9图×常规／压力×明暗×320／736px。实际DOM检查文字外溢、场景边界、根溢出、消息／分类标签相交、reduced静态、展开fit及返回／resize错误。检查脚本遇到失败会退出非零。
- `semantic-results.json`：18组解析模型对实际节点／名称／关系／字段／坐标标记／份额核对。Pie零项仍在图例，极小份额不聚合；XY重复名按源顺序占独立位置。
- `behavior-results.json`：9图实际动效，hover与resize不重播，完整退出重入重播；不将140ms样式transition误算成入场重播。Sequence压力入口将消息stagger总窗口限制900ms。
- `contrast-results.json`：18组computed color采样。主要文字与关键线条在明暗主题可读；局部采样不等于全图WCAG认证。
- `extra-results.json`：13组零值、showData、水平XY重复分类、Radar非零min与circle、unsupported style/box回退、非法语法及Sankey循环明确错误。非法语法和原生不能绘制的图不承诺成功回退。
- `detail-results.json`：42组常规／压力的首、中、末关系或分类，详情距离≤32px、完整文本、Escape后即使再次收到scroll也不重开。Architecture沿用原先的独立未缩放资源详情区，不适用瞬态浮层≤32px规则。
- `python-tests.txt`：Python30项通过；40个Mermaid JavaScript模块语法检查通过。使用实际parser模型，不新增第二份图数据。
- `.png`是本机浏览器截图，保留作视觉证据；源JSON与构建脚本已提交，可重建全部样例。消息流HTML位于当前线程visualizations目录。

这些是隔离浏览器与模拟宿主事件的结果。真实Codex消息流、toolbar、clipboard和宿主可见性恢复仍待人工验收。未重启日常Codex，未推送或发布。

## 结构审视

公共定位／hover／包含层集中在mermaid-presentation.js；各图模型保持源语义、布局保留几何职责。Pie／Radar通过mermaid_presets.py编译既有模板，避免两套样式漂移。ResizeObserver对重绘使用下一帧处理。Block／C4移除不再使用的底部详情容器和无效select，不为隐藏详情增加空白。

## 复现

仓库根运行 `python3 Progress/mermaid/autonomous-review/build.py` 和 `python3 Progress/mermaid/autonomous-review/extra-build.py`，启动 `python3 -m http.server 8801 --bind 127.0.0.1`，再运行此目录的check.cjs／semantics.cjs／behavior.cjs／contrast.cjs／extra-check.cjs／details.cjs。脚本使用本机已安装Playwright与Visualize包装器路径，跨机器时需调整这两条工具路径和线程输出目录。业务JSON可直接用skill render.py生成，不依赖测试注入。

## 逐图提交

- ffe2a5d feat(mermaid): refine architecture for design review
- fe2f3bc feat(mermaid): refine sequence for design review
- 2db86d6 feat(mermaid): refine er for design review
- b990b21 feat(mermaid): refine pie for design review
- 31b4504 feat(mermaid): refine xy for design review
- 3452536 feat(mermaid): refine radar for design review
- 2cc3a00 feat(mermaid): refine sankey for design review
- e3e38b5 feat(mermaid): refine block for design review
- 1f73dcb feat(mermaid): refine c4 for design review

公共能力与先前已确认的Donut修复分别提交；检查矩阵和待验收清单作为独立证据提交。本机qv19个相关技能文件已逐字节同步核对。

补查发现并修复：时序图键盘自动滚动会清掉消息详情；Block／C4聚焦关系时将来源节点居中，把触发关系文字送出视口。现按触发文字定位并恢复键盘上下文，三图各自独立修复提交。
