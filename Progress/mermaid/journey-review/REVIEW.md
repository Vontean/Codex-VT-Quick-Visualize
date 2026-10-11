# Journey 本轮审视

常规：7 步骤、3 角色；边界：25 步骤、8 角色、无 section 首步骤、重复步骤名、无角色步骤、长阶段/步骤/角色名、评分1与5；单步骤：一个5分步骤，无角色。

初始基准由当时正式模板生成，双主题320/736px共12组实际sandbox检查。每组ready/enhanced，无浏览器异常；全部步骤保留，文字无溢出，根无横向溢出，模拟原生展开包含全部步骤/角色/评分标记。详情、真实角色参与与数值来自Mermaid DB；横轴是源步骤顺序，不表达时间。

证据 results.json 与各组 inline/expanded PNG。当时只准备审视基准，未修改Journey模板、未勾选、未提交Journey变更；等待用户指定值得修的问题。

## ResizeObserver 修复

用户消息流报错已在真实 sandbox 复现。旧版在 ResizeObserver 回调中同步布局、改变 root 高度；30 次宽度变化及3次模式切换产生20次 window.error。新版监听只合并安排一个 requestAnimationFrame，下一帧重新读当前宽度并更新；同操作为0错误，25步骤完整。永久回归捕获 window.error 而不是仅 pageerror，覆盖三样例、双主题与连续缩放/展开返回。证据 resize-results.json、resize-regression-results.json。Journey 仍待整体审视确认，TODO 不勾选。

## 常规样例设计试作

按用户要求暂不审视边界，保留常规7步骤/3角色/原评分与真实参与。阶段改浅灰块、圈内序号；体验改24px官方Lucide表情+红黄绿曲线及渐变面积；角色用16px官方图标+文字与14px灰参与条。仅连续参与步骤合并；全列悬浮/聚焦保留本列、其他列白底遮罩，不再弹详情或显示点边数字。

实际源数据对照与参与条还原、分值对应纵坐标、双主题、整列遮罩、resize/mode错误监听核对；design-regression-results.json与redesign-*.png。宿主svg.lucide强制16px，使用表情局部--icon-size:24px保留官方图标实现。Python30项通过。原模板/图表快照保存在redesign-before。该轮为设计试作，等待用户确认，未勾选Journey或提交该设计。

## 常规微调与压力复核

常规效果已获用户认可，按追加意见收拢 scene/grid 至实际列宽（展开120px/列），将参考标题改为“体验曲线”，去掉“参与角色”标题，首角色从曲线底部68px移至38px。压力模拟数据去除人工“步骤n”前缀，保留25步骤/8角色与长文本、未指定角色、重复名称、1和5评分。

实际 sandbox 双主题分别核对常规与压力源评分、表情坐标、参与条覆盖、整列遮罩、1600px展开固有宽度、320/400/600/736px缩放及模式切换，runtimeErrors为空。设计回归应过滤Mermaid未指定角色的空字符串，避免把空项当成人员。证据 design-regression-results.json、stress-refined-results.json及stress-refined-*.png；Python30项通过。该轮压力图等待视觉确认，Journey仍未checked。

## 区块标题与16px间距

用户追加：阶段与步骤区左侧标题为“用户旅程”，与“体验曲线”同为12px muted文本；体验曲线块含底部表情15px外缘，与首人员标签/参与条的上边界保留16px，按首人员实际高度计算中心，避免用中心距代替区块间距。常规与压力双主题、展开/返回、320–1600px变化核对；等待用户视觉确认。

## 完成验收与架构检查

2026-10-12 用户确认完成，最终区块间距24px。架构核对：模型适配器只读Mermaid DB并复制实际语义，renderer独立负责DOM/曲线/参与条，展开与滚动仍复用共享viewport；无需新增解析器、宿主补丁或布局框架。ResizeObserver继续延后一帧布局，动画与hover只操作展示状态。末行标签底部空间改为实测高度，并加入长末行角色fixture。

最终常规/25步骤压力/长末行角色双主题设计检查6组；normal/stress/single双主题连续尺寸与模式检查6组，无window.error/文字或根外溢。Python30项通过。TODO journey checked，总进度4/18；仅提交Journey源码、规范、测试和验收记录，保留独立donut改动。

## 人员行独立高度补充

用户发现压力图长角色行扩大了所有人员行。原因是所有行共用max(labelHeight+12)。改为每行累加自身实测标签高度+12px间距；参与条按该行自身中心定位，首块24px外缘间距保留。末行与无角色场景保持完整视图边界。回归新增逐行间距与参与条中心检查；双主题三数据源6组设计检查与6组连续resize检查通过。补充证据role-rows-results.json、role-rows-compact.png。Journey保留已完成状态，本补充独立提交。
