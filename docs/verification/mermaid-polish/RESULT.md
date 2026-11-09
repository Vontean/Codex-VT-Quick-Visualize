# Mermaid 产品规则迁移交付记录

2026-11-09。正式源码位于 `skill/quick-visualize/`，已同步至本机 `/Users/mac/.codex/skills/quick-visualize/`。代码、规范和自动验证已完成；会话中的真实宿主视觉验收等待用户反馈。

参考 MineCodex `v2.0.54` 的最终 `docs/verification/mermaid-polish/RESULT.md`（含末尾用户纠正和清理记录）、功能 DESIGN、正式构建组装器与适配模块。迁移状态导航修复 `449ac54`、象限居中 `b92a0eb`、雷达就近气泡 `5ac3d7e`、ER/Class/Journey及标题居中 `bb3e491`。没有修改 MineCodex 仓库，也没有发布 npm。

## 实现与规范

- [38条规则映射](RULES.md)：逐条列出正式文件、符号和验证证据。源渲染器直接拥有规则，没有增加运行时/构建后字符串补丁层。
- 流程按当前可用宽度比较作者方向与另一主轴，不再蛇形折叠；完整保留组框与连接。移除流程/架构的节点组开关和控制函数，状态图保留 `scope-nav`、`mermaidScopeView` 及自身导航。
- Sequence、XY、Mindmap、Architecture、Git、Timeline、Sankey、Radar、Legend、Quadrant按生产规则迁移。新增Git读取真实分支及父提交；横向泳道/纵向日志按可用宽度选择。
- 共享文件：`chart-motion.js`、`chart-detail-position.js`、`chart-legend.js`、`chart-polish.css`；既有Pie/Radar预设继续编译复用真实模板。实际复用的数据图同步动效曲线、图例与浮层 token，不扩展到选择器/表单。
- 修正加载模板遗留的 `!important` 固定色和600字重覆盖；加载模板只负责网点与加载生命周期，浮层规则归共享图表资产。CSS在root外，预设innerHTML替换后仍存在。
- `qvReady` Promise覆盖完整首次绘制；必须等待Promise、最终state及加载结束，不能仅检查enhanced。保留显式native回退，失败显示错误；回退不接入增强viewport。
- 同步SKILL、Mermaid/Radar reference、DESIGN、README及当前测试入口。旧navigation字段兼容接收但不再传入渲染配置；新spec不指导使用。

## 自动验证

| 检查 | 结果 / 证据 |
| --- | --- |
| Python回归 | 34/34通过，`python3 -m unittest discover -s tests -v`；新增4项覆盖远端候选淘汰、边缘距离边界、批次动画预算、Git合并父提交与标签 |
| 静态检查 | Python编译、runner JavaScript/placeholder/ID/size检查、`git diff --check`通过；正式Skill Validator通过（临时PyYAML依赖，仅验证使用） |
| 完整渲染矩阵 | [browser-results.json](browser-results.json)：38夹具×浅深色=76/76通过；32份正式常规/压测源码+6份标题/导航/回退/双向消息回归；等待qvReady后测量736→320→736px绘图区 |
| 动效 | 捕获1953个Web Animations调用；最大结束时间1200.0000000000002ms（浮点容差1e-6）；全部为共享cubic-bezier。D3/rAF固定650–1200ms并直接使用共享进度函数；没有把未捕获WA当作没有动画 |
| 图型与标题 | 复杂Architecture为16节点、无卡片重叠、ELK回退；Git常规lanes/压测rows；雷达轴标签无碰撞；Radar通用/预设及Sankey非空标题可见且居中 |
| 交互 | [interaction-results.json](interaction-results.json)：22条通过；通用/预设Radar真实hover及focus、边缘触发、浅深色浮层样式；气泡与触发点约16–32px；expanded事件/返回滚动、fallback不接viewport、reduced-motion |
| 边界 | [boundary-results.json](boundary-results.json)：20条通过；1440→352→1440窗口下Quadrant/ER/Class/Journey中心与左端可达、Journey列宽恢复、图例堆叠左对齐、两层state进入返回、流程hover完成入场及hover/resize不重播、改变预设tooltip实际offsetParent后仍就近 |
| 安装 | [install.json](install.json)：81份正式文件与安装入口逐字节及SHA-256核对；忽略test及缓存；旧副本备份保留以便恢复 |
| 会话样例 | 安装后通过该入口生成flow/git/radar/sankey/state/journey六张模拟图，并在真实Visualize sandbox完整等待qvReady，6/6为enhanced |

复现（`<visualize-dir>`使用当前安装的Visualize技能目录，`playwright`需可被Node解析；例如通过`NODE_PATH=$(npm root -g)`）：

```bash
python3 tests/render_mermaid_polish.py <visualize-dir> work/mermaid-polish
python3 -m http.server 8796 --bind 127.0.0.1 --directory work/mermaid-polish
node tests/mermaid-polish-check.cjs work/mermaid-polish
node tests/mermaid-polish-interactions.cjs work/mermaid-polish
node tests/mermaid-polish-boundaries.cjs work/mermaid-polish
```

测试使用正式Visualize sandbox wrapper，而不是删减脚本的假页面。本次发现缓存插件路径在会话中变化，最终以当前存在的`openai-bundled/visualize/1.0.84`包装并重跑全部矩阵。矩阵保留原生CDN加载链，固定依赖版本；没有离线替换Mermaid、ELK或D3来绕过真实加载。

## 截图与验收边界

代表性稳定态截图：[浅色流程](light-flow-normal.png)、[深色Git](dark-git-normal.png)、[深色通用雷达详情](dark-radar-generic-title-normal-bubble.png)、[深色预设雷达详情](dark-radar-preset-title-normal-bubble.png)。气泡截图等待140ms入场完成后采集。截图和自动几何检查不构成逐像素保真证明。

电脑控制工具禁止访问`com.openai.codex`，因此没有把浏览器/模拟mode事件记作真实Codex原生按钮验收。用户已要求安装后生成模拟数据自行验收；会话已提供可直接查看的内联图。真实宿主内联、原生展开/返回、物理键盘、主题切换的视觉感受及全部长文人工审阅仍待用户确认。Windows与系统剪贴板/保存未覆盖。

专用浏览器均由测试finally关闭；未复用或重建此前已清理的MCX隔离profile/Runtime。本任务的临时HTTP服务验证结束后关闭；保留正式证据、用户样例和安装恢复备份。没有剩余自动检查失败；待用户视觉反馈后继续修正。

## 画布与标题复核

用户发现默认对齐遗漏后，已统一全部增强图型的可容纳画布居中与短/长标题规则；58项对齐检查及20条直接依赖回归通过。详见[对齐补漏记录](alignment/RESULT.md)。当前本机安装清单以`alignment/install.json`为准。
