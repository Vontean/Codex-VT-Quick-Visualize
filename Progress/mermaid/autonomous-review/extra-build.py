from pathlib import Path
import subprocess,json
base=Path(__file__).parent
out=Path('/Users/mac/.codex/visualizations/2026/10/11/01a12b31-d03a-7830-89bd-a80ca5a79807')
long='完整业务资料与跨团队历史记录核对'
cases={
 'pie-zero':('pie\n"全部":100\n"没有":0\n"仍然没有":0\n','enhanced'),
 'pie-direct':('pie showData\n"编辑":40\n"审核":35\n"归档":25\n','enhanced'),
 'pie-empty':('pie\n"空值":0\n"空值二":0\n','native'),
 'sequence-fallback':('sequenceDiagram\nbox Team\nparticipant A\nparticipant B\nend\nA->>B: Send\n','native'),
 'er-fallback':('erDiagram\nA ||--o{ B: owns\nclassDef red fill:#f00\nclass A red\n','native'),
 'block-fallback':('block-beta\ncolumns 2\na b\nclassDef red fill:#f00\nclass a red\n','native'),
 'c4-fallback':('C4Context\nPerson(a,"User")\nSystem(b,"System")\nRel(a,b,"Uses")\nUpdateElementStyle(a,$bgColor="#f00")\n','native'),
 'radar-circle':('radar-beta\naxis a["Research"], b["Accuracy"], c["Delivery"]\ncurve x["Team"]{2,4,6}\nmin 1\nmax 8\nticks 4\ngraticule circle\n','enhanced'),
 'sankey-zero':('sankey-beta\n\nA,B,0\n','native'),
 'sankey-cycle':('sankey-beta\n\nA,B,2\nB,A,2\n','error'),
 'xy-horizontal':('xychart-beta horizontal\nx-axis ['+','.join('"'+(long if i%3==0 else '周期'+str(i+1))+'"' for i in range(18))+']\ny-axis "数量" -20 --> 100\nbar ['+','.join(str(i*7-15) for i in range(18))+']\n','enhanced'),
 'syntax-error':('architecture-beta\nservice A(server)[跨地区企业客户]\n','error'),
 'sankey-unicode-invalid':((base/'sankey-unicode-invalid.mmd').read_text(),'error'),
}
manifest={}
for name,(source,state) in cases.items():
 spec={'title':name,'source':source};p=base/(name+'.json');p.write_text(json.dumps(spec,ensure_ascii=False));html=out/(name+'.html')
 subprocess.run(['python3','skill/quick-visualize/scripts/render.py','mermaid',str(p),str(html)],check=True,stdout=subprocess.DEVNULL)
 subprocess.run(['python3','/Users/mac/.codex/plugins/cache/openai-bundled/visualize/1.0.49/skills/visualize/scripts/render.py',str(html),str(base/(name+'-preview.html')),'--force'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 manifest[name]=state
(base/'extra-manifest.json').write_text(json.dumps(manifest,indent=2))
