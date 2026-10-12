from pathlib import Path
import json,subprocess
repo=Path(__file__).resolve().parents[3]
audit=Path(__file__).resolve().parent
output=Path('/Users/mac/.codex/visualizations/2026/10/11/01a12b31-d03a-7830-89bd-a80ca5a79807')
compiler='/Users/mac/.codex/plugins/cache/openai-bundled/visualize/1.0.49/skills/visualize/scripts/render.py'
manifest=[]
for kind in ['flowchart','architecture','sequence','er','class','state','quadrant','xy','radar','sankey','block','c4','gantt','mindmap','pie','journey','kanban','timeline']:
 for sample in ['normal','stress']:
  spec=audit/f'{kind}-{sample}.json'
  if not spec.exists():
   folder={'class':'class-review','state':'state-review','quadrant':'quadrant-review','journey':'journey-review','kanban':'kanban-review','timeline':'timeline-review'}.get(kind)
   if folder:spec=repo/f'Progress/mermaid/{folder}/{kind}-{sample}.json'
  if kind=='flowchart':
   spec=audit/f'popover-audit-flowchart-{sample}.json';source='flowchart LR\n A[提交内容] --> B[核对资料] --> C[完成审核]';spec.write_text(json.dumps({'source':source,'descriptions':{'A':'核对跨地区客户的资料来源、访问权限与内容版本。\n审核通过后继续发布。'}},ensure_ascii=False))
  if kind=='flowchart' and sample=='stress':
   spec=audit/'popover-audit-flowchart-stress.json';data=json.loads((repo/'Progress/mermaid/state-review/flowchart-stress.json').read_text());data['descriptions']={'N1':'核对跨地区客户的资料来源、访问权限与内容版本。\n审核通过后继续发布。'};spec.write_text(json.dumps(data,ensure_ascii=False))
  if kind=='mindmap':
   spec=audit/f'popover-audit-mindmap-{sample}.json';source='mindmap\n root((内容管理))\n  收集资料\n  核对权限\n  发布内容';spec.write_text(json.dumps({'source':source,'descriptions':{'root':'归集内容与资料，核对权限，再完成发布。'}},ensure_ascii=False))
  if kind=='mindmap' and sample=='stress':
   data=json.loads(spec.read_text());data['source']=(repo/'tests/fixtures/mermaid/adapted-mindmap-complex.mmd').read_text();spec.write_text(json.dumps(data,ensure_ascii=False))
  if kind=='gantt':spec=repo/f'tests/fixtures/mermaid/adapted-gantt{"-boundary" if sample=="stress" else ""}.mmd'
  out=output/f'popover-audit-{kind}-{sample}.html'
  result=subprocess.run(['python3',str(repo/'skill/quick-visualize/scripts/render.py'),'mermaid',str(spec),str(out)],capture_output=True,text=True);assert result.returncode==0,result.stdout+result.stderr
  subprocess.run(['python3',compiler,str(out),str(audit/f'popover-audit-{kind}-{sample}-preview.html'),'--force'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  manifest.append({'kind':kind,'sample':sample,'spec':str(spec.relative_to(repo)),'path':str(out)})
for kind in ['donut-chart','radar-chart','line-chart','grouped-bar-chart']:
 spec=audit/f'{kind}-dark-detail.json';out=output/f'popover-audit-{kind}-normal.html'
 subprocess.run(['python3',str(repo/'skill/quick-visualize/scripts/render.py'),kind,str(spec),str(out)],check=True,stdout=subprocess.DEVNULL)
 subprocess.run(['python3',compiler,str(out),str(audit/f'popover-audit-{kind}-normal-preview.html'),'--force'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 manifest.append({'kind':kind,'sample':'normal','spec':str(spec.relative_to(repo)),'path':str(out)})
(audit/'popover-theme-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print('40 audit previews generated')
