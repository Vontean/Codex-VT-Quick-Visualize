# Codex VT Quick Visualize

与Codex Desktop Visualize配合使用的固定交互和图表技能：填写JSON，或提供标准Mermaid源码，由统一runner生成可在会话中展示的HTML fragment。

支持多选、排序、独立参数表单、方案比较、Line／Grouped Bar／Donut／Radar，以及受支持的Mermaid图型。完整输入、选择条件和调用流程由[SKILL](skill/quick-visualize/SKILL.md)与其链接的references维护。

## 使用

```text
使用 $quick-visualize，把下面的数据按匹配的预设显示在会话中。
```

```bash
python3 skill/quick-visualize/scripts/render.py mermaid diagram.mmd work/diagram.html
```

使用runner返回的`reference`原样交付。默认使用纯ASCII的`::codex-inline-vis{...}`；只有旧宿主不识别时才显式选择`--reference-format visualize`。显示标题可以是中文，HTML文件名使用英文slug。`ok:true`确认生成和静态检查；浏览器加载、布局及真实宿主展示需分别验证。

Confirm将结果放入输入框，等待用户检查和手动发送；图表交互留在本地。Mermaid增强保留真实语义，未覆盖语法明确回退原生。

## 安装与更新

需要启用Visualize，并在PATH中提供Python 3和Node.js。技能运行只依赖Python标准库；绘图依赖在浏览器按固定CDN版本加载。

推荐使用Codex Skill Installer：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo Vontean/Codex-VT-Quick-Visualize \
  --path skill/quick-visualize
```

安装器会在同名技能目录已存在时停止。更新前备份旧目录；安装后按宿主的技能发现机制重新加载或开启新任务。

手动安装已提交版本时，仅分发受版本控制的正式技能：

```bash
mkdir -p ~/.codex/skills/quick-visualize
git archive HEAD:skill/quick-visualize | tar -x -C ~/.codex/skills/quick-visualize
```

技能默认位于`${CODEX_HOME}/skills`，未设置时通常为`~/.codex/skills`。源码中的忽略测试材料、缓存、spec、HTML和截图不进入分发包。开发中的本机同步以当前正式源码为准，并逐文件核对。

## 文档职责

| 读者与任务 | 入口 |
| --- | --- |
| Agent选择、生成与交付 | [SKILL](skill/quick-visualize/SKILL.md) |
| 修改数据契约或渲染器 | [Maintenance](skill/quick-visualize/references/maintenance.md) |
| 理解产品取舍与规则归属 | [DESIGN](DESIGN.md) |
| 理解Module、Interface、依赖和待处理结构问题 | [Architecture](docs/ARCHITECTURE.md) |
| 查已执行的验证与限制 | [验证记录](docs/verification/) |
| 排查模型/宿主引用兼容问题 | [兼容性历史记录](docs/visualize-compatibility.md) |

[AGENTS.example.md](AGENTS.example.md)是可供用户手动合并的路由示例。技能调用不改宿主配置、用户路由或插件安装。

## 维护与验证

正式源码在`skill/quick-visualize/`。`assets/`拥有模板与绘制，`scripts/`拥有数据校验和编译，`references/`拥有Agent按需读取的契约。

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile skill/quick-visualize/scripts/*.py
git diff --check
```

具体浏览器验证入口与证据见[Maintenance](skill/quick-visualize/references/maintenance.md)及[当前审查记录](docs/verification/skill-maintenance/RESULT.md)。真实Codex内联、原生展开、返回和主题验收与浏览器结构检查分别报告。

旧单模板脚本保留兼容用途；Agent统一调用`scripts/render.py`。样式、动画和图型限制在对应reference维护，此README不再复制它们。

## License

项目采用[MIT](LICENSE)。运行时依赖未打包进仓库：

- [Mermaid 11.12.0，MIT](https://cdn.jsdelivr.net/npm/mermaid@11.12.0/LICENSE)
- [ELKjs 0.10.0，EPL-2.0](https://github.com/kieler/elkjs/blob/v0.10.0/LICENSE.md)
- [D3 7.9.0，ISC](https://github.com/d3/d3/blob/v7.9.0/LICENSE)
- [d3-sankey 0.12.3，BSD-3-Clause](https://github.com/d3/d3-sankey/blob/v0.12.3/LICENSE)
- [js-yaml 4.1.1，MIT](https://github.com/nodeca/js-yaml/blob/4.1.1/LICENSE)

Lucide图标由宿主提供，技能不另外下载图标库。
