from pathlib import Path
import subprocess,json
base=Path(__file__).parent
out=Path('/Users/mac/.codex/visualizations/2026/10/11/01a12b31-d03a-7830-89bd-a80ca5a79807')
extra={'title':'激活条：嵌套、自调用与未关闭区间','source':'''sequenceDiagram
 participant A as 编辑者
 participant B as 内容服务
 A->>+B: 核对特别长的完整业务说明与全部历史资料和权限记录并保留每一次历史变更用于后续审查
 B->>+B: 嵌套核对
 B-->>-B: 内层核对完成
 B-->>-A: 返回结果
 activate A
 deactivate A
 activate B
 B->>B: 后续处理
'''}
(base/'sequence-activation-nested.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2))
for sample in ['normal','stress','nested']:
 spec=base/(f'sequence-{sample}.json' if sample!='nested' else 'sequence-activation-nested.json')
 html=out/f'sequence-activation-{sample}.html'
 subprocess.run(['python3','skill/quick-visualize/scripts/render.py','mermaid',str(spec),str(html)],check=True)
 instrument=base/f'sequence-activation-{sample}-instrumented.html'
 instrument.write_text(html.read_text().replace('const model=await readMermaidModel(mermaid,cfg.source,cfg.descriptions);','const model=await readMermaidModel(mermaid,cfg.source,cfg.descriptions);root.__reviewModel=model.data;'))
 subprocess.run(['python3','/Users/mac/.codex/plugins/cache/openai-bundled/visualize/1.0.49/skills/visualize/scripts/render.py',str(instrument),str(base/f'sequence-activation-{sample}-preview.html'),'--force'],check=True,stdout=subprocess.DEVNULL)
