# 画布与标题对齐补漏

2026-11-09。用户复核要求检查默认靠左的图表与标题；本次在原迁移基础上补齐共享对齐规则，并同步本机技能。

## 审查结论

19种增强Mermaid图型均检查宽、窄及窄转宽。原常规样例中可容纳画布仍居左的有Git横向泳道、Timeline、Block、Kanban；C4同样缺少可容纳时的居中规则，另加小型C4夹具验证。宽容器内Git画布454px、中心偏差−477px，Timeline1032px、偏差−188px，Block992px、偏差−208px，Kanban1160px、偏差−124px；修正后均为0px。

原本已正确的有ER、Class、Quadrant及Journey整体外框；流程、架构、Sequence、State、XY、Mindmap、Gantt及通用数据图通常铺满可用宽度或在内部居中，不把它们误报为同一种左对齐遗漏。C4常规样例超宽，应保留滚动；补充的小型C4宽760px，可容纳时中心偏差为0px。

标题原先只有Radar/Sankey做过完整容器居中，其余17种增强图型大多沿用左对齐及90px单侧留白。Pie/Radar复用模板以及独立Line/Grouped Bar/Donut/Radar的标题一并按真实共享关系修正。

## 正式规则

- 所有增强Mermaid的可容纳scene采用自动水平外边距；超宽时外边距归零，左端可达、横向滚动。Journey保持参考轴与步骤整体居中，不单独挪步骤scene。
- 不改变图内节点、卡片正文、图例项或轴文字的语义对齐。
- 单行标题与**可见容器**同心；不按超宽scene的中点定位标题，避免标题滚出视野。标题和绘图区分离沿用Sankey规则。
- 多行长标题自然换行并左对齐；宽度足够回到单行后恢复居中。去掉旧90px单侧留白，顶部与标题间距仍用原有token。
- 共享`chart-legend.js`的尺寸观察同时更新标题换行标记；无新增重复观察器。原生回退不接入增强scene居中规则。
- Mindmap保留原有根节点初始视野；其窄屏scene左偏来自可恢复的scrollLeft，并非裁切。验证超宽左端时检查scene.left+scrollLeft，防止把初始滚动误报为不可达。

正式文件：`assets/chart-polish.css`、`assets/chart-legend.js`及Mermaid/图表标题的样式所有者。同步SKILL、Mermaid reference与DESIGN。

## 验证

- [before.json](before.json)：原始对齐测量，仅保留几何和样式事实，不将按新规则产生的预期断言失败当作旧版运行失败。
- [after.json](after.json)：29夹具×浅深色=58/58通过；包含19种Mermaid、3个长标题、可随宽度换行的标题、小型C4、原生回退及4种独立共享数据图。窗口1440→352→1440；可容纳中心误差<1.1px，超宽左端可达；多行标题左对齐、回到单行恢复居中；无根容器溢出。
- [dependencies.json](dependencies.json)：20条直接依赖回归通过，含状态两层导航、Journey列宽恢复、图例、雷达offsetParent定位、流程hover快进与不重播。
- [python-tests.txt](python-tests.txt)：34/34通过。Python编译、runner静态检查和git diff --check通过。
- [install.json](install.json)：最终81份正式技能文件与本机入口逐字节一致；本记录取代上一轮安装清单作为当前版本的核对依据。
- [samples.json](samples.json)：安装入口新生成Git、Timeline、Sankey三张会话样例，浅深色6/6完整渲染及对齐检查通过。
- 稳定截图：[Git居中](git.png)、[长Sankey标题左对齐](long-title-sankey.png)。会话样例由安装后的runner生成，不复用旧HTML。

复现：

```bash
python3 tests/render_mermaid_alignment.py <visualize-dir> work/mermaid-alignment
NODE_PATH=$(npm root -g) node tests/mermaid-alignment-check.cjs work/mermaid-alignment
```

runner自行创建8797临时服务，finally关闭浏览器与服务。真实Codex用户可见内联、原生展开与返回仍以用户验收为准，不用浏览器测量代替。没有修改MineCodex或发布npm。
