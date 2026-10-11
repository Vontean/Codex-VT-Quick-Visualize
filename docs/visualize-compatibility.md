# Visualize 模型兼容性验证

验证日期：2026-10-11（Asia/Taipei）。

## 范围与结论

- 当前安装版本：`26.1007.21159`，build `20052`，prod。版本来自 Codex 更新检查，并由安装包内 package.json 核对。
- 更新器提供 `26.1007.30912`，build `20156`；本次未安装或运行该版本，不能声称最新版运行验收通过。
- 测试模型：`gpt-6.1-sol` 与 `opencode-go/deepseek-v4.1-flash`，均由实际 turn 配置核对。
- 模拟数据：donut-chart，A=60、B=40，沿用已安装模板。

无需按模型厂商分开生成图表。当前宿主接受 ASCII 展示指令，可以避开让模型生成 Unicode 私用区字符。旧的 U+E200 / U+E202 / U+E201 是展示协议的分隔码点，不构成厂商专属输出权限。

## 实测证据

1. DeepSeek 实际运行 runner，生成 HTML，通过 spec、placeholders、ids、javascript、size 静态检查。
2. 第一轮最终消息实际使用 `::codex-inline-vis{path="..."}`，不是原样输出 PUA 引用。因此本次证明 ASCII 路径可用，不证明该模型完整保真输出 PUA。
3. 第一轮用中文和空格命名 HTML。用户截图显示宿主可视化错误框；宿主主进程的 read 接口明确拒绝这种 basename。
4. 同一份 HTML 经 bundled Visualize 的独立预览 wrapper 在 Chrome 中显示 60% / 40% 环形图。此证据只覆盖浏览器预览；扩展产生的 `postMessage` origin 报错来自 chrome-extension，不是模板脚本。
5. 第二轮同一 spec 生成 `deepseek-donut-test.html`，使用 ASCII 指令。用户明确反馈“第一张正确”，确认当前安装版本的 DeepSeek 图表宿主渲染成功。
6. 同时生成零外部资源的最小交互，用户未确认其点击行为；不将它列为交互验收通过。
7. 修复并同步安装后，DeepSeek 重新读取技能，以 `--reference-format directive` 标准调用生成 `deepseek-skill-final.html`，静态校验通过；该次新文件尚未单独做用户界面验收。
8. ASCII 改为默认后，GPT-6.1 Sol 与 OpenCode Go DeepSeek V4.1 Flash 均重新读取更新后的技能；不传 `--reference-format` 的标准命令返回 `ok: true` 和纯 ASCII directive。最终消息原样输出该引用。
9. 两模型标准调用生成的 HTML 均在独立 bundled Visualize 浏览器预览中实际绘制两段圆环并结束加载（`aria-busy=false`）。这不等于两张新文件已完成原生 Codex 消息流验收；此前 DeepSeek 消息流的用户验收仍是独立证据。
10. Mermaid 独立暂存快照的 25 项测试通过；最终 ASCII 快照的 30 项回归测试覆盖默认 CLI 调用、两种引用、Mermaid wide 属性、英文文件名边界、已有输出保留和无效路径。

## 当前宿主契约

安装包内 `Resources/app.asar`，只读检查。

- `webview/assets/app-shared-2f2228189a8d.js` 中 `oSr` 将旧 PUA 引用转换成 `codex-inline-vis`，没有模型厂商条件。
- `webview/assets/app-initial-c468e3fd7f91.js` 中 `Erl` 为 `codex-inline-vis` 提供渲染入口。
- `.vite/build/main-39FdJ_vp.js` 中 visualization read 对 basename 使用 `/^[a-z0-9]+(?:-[a-z0-9]+)*\.html$/`；不符合则抛出 `Invalid visualization read request`。因此错误框不等于模板 JS 发生异常。

## 路由方案

| 路径 | 使用条件 | 用户效果 | 限制 |
| --- | --- | --- | --- |
| ASCII directive | 当前宿主支持；GPT 与三方模型均推荐 | 同一个消息流内 Visualize | 内部宿主契约，更新后需要复核 |
| Legacy visualize reference | 旧调用或宿主只支持旧格式 | 同一个消息流内 Visualize | 需原样复制 Unicode 分隔符 |
| Standalone wrapper + browser panel | 宿主无 Visualize 或两种引用均不可用 | 保留图表本地交互，改为独立预览 | 不等于消息流内嵌；表单回填需另外适配 |
| PNG / SVG | 仅需展示静态结果 | 图片展示 | 无 hover、筛选、表单交互 |

选择依据是宿主支持的格式，不是 GPT / DeepSeek 品牌。最小必要修复是文件名预检、ASCII 输出选项和技能调用说明；无需修改宿主、代理、模型或图表模板。

## 本次改动与边界

runner 默认返回 ASCII 引用，所有模型使用同一普通命令。只有旧宿主兼容场景才显式传 `--reference-format visualize`。原来不传格式的调用参数无需改动，但 `reference` 输出格式从 Unicode 改成 ASCII。Mermaid 保留 wide 属性。对宿主不接受的文件名、包含引号或换行的路径在写入前报错，保留已有文件。

未更新 Codex 安装版本。用户授权将 Mermaid 适配和 ASCII 默认路径按两个逻辑变更原子化提交并推送；本机已安装 skill 的对应文件同步前保留任务内备份。浏览器预览、模型普通调用、历史 DeepSeek 消息流验收和新文件的宿主验收分别记录，不互相替代。
