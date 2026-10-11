from pathlib import Path
import subprocess,json
base=Path(__file__).parent
out=Path('/Users/mac/.codex/visualizations/2026/10/11/01a12b31-d03a-7830-89bd-a80ca5a79807')
long='核对跨地区企业客户的完整业务说明与历史修改记录并确认所有团队的资料和权限'
stress={}
stress['pie']='pie showData\n'+ '\n'.join(f' "{("跨地区企业客户反馈与资料来源说明" if i==0 else "来源"+str(i+1))}" : {v}' for i,v in enumerate([9876553211.13,0,0.01,0,34,2800,0,400,1,24]))
stress['radar']='radar-beta\n axis '+', '.join(f'a{i}["{("跨地区企业客户体验与可访问性核对" if i==0 else "指标"+str(i+1))}"]' for i in range(10))+'\n'+ '\n'.join(' curve s%d["团队%d"]{%s}'%(i,i+1,','.join(str((i*17+j*11)%101) for j in range(10))) for i in range(5))+'\n max 100\n min 0\n ticks 5\n graticule polygon\n'
stress['xy']='xychart-beta\n x-axis "交付周期" ['+','.join('"'+(long if i in [2,13] else '周期'+str(i+1))+'"' for i in range(24))+']\n y-axis "增减量" -40 --> 100\n bar ['+','.join(str((i*17)%135-35) for i in range(24))+']\n line ['+','.join(str((i*13)%101) for i in range(24))+']\n'
stress['er']='erDiagram\n direction TB\n'+'\n'.join(' E%d["%s"] {\n uuid id PK\n string %s\n string name\n }'%(i,long if i==4 else '资料实体'+str(i+1),'complete_historical_revision_and_customer_permission_record' if i==4 else 'status') for i in range(14))+'\n'+'\n'.join(f' E{i} ||--o{{ E{i+1} : '+('核对完整业务说明与资料权限记录' if i==4 else '包含') for i in range(13))+'\n E4 |o..o{ E4 : 关联\n'
stress['sequence']='sequenceDiagram\n autonumber\n'+'\n'.join(f' participant A{i} as '+(long if i==2 else '团队'+str(i+1)) for i in range(7))+'\n activate A0\n loop 核对完整业务资料\n'+'\n'.join(f' A{i%7}->>+A{(i+1)%7}: '+(long if i%5==0 else '核对资料与权限'+str(i+1))+'\n deactivate A'+str(i%7) for i in range(25))+'\n deactivate A4\n end\n Note over A2,A4: '+long+'\n activate A6\n A6->>A6: '+long+'\n deactivate A6\n'
stress['block']='block-beta\n columns 5\n block:g1:5\n columns 3\n a["资料接收"] b["'+long+'"] c["权限核对"]\n end\n space:5\n d["处理与复核"]:2 space e["跨团队协作"]:2\n space:5\n block:g2:5\n columns 3\n f["发布"] g[("历史资料库")] h["归档"]\n end\n a --> b\n b --> c\n c --> d\n d --> e\n e --> f\n f --> g\n g --> h\n'
stress['c4']='C4Container\n Person(customer, "企业客户", "'+long+'")\n System_Boundary(platform, "跨团队内容与权限平台") {\n'+'\n'.join(' Container(c%d, "%s", "HTTP API", "%s")'%(i,'资料服务'+str(i+1),long if i in [2,6] else '核对资料与记录') for i in range(10))+'\n }\n Rel(customer,c0,"提交资料","HTTPS")\n'+'\n'.join(f' Rel(c{i},c{i+1},"'+('核对完整资料与权限后转交下一团队' if i==3 else '传递资料')+'","HTTPS")' for i in range(9))+'\n'
stress['sankey']='sankey-beta\n\n'+'\n'.join(f'{("跨地区企业客户资料来源与业务反馈入口" if i==0 else "入口"+str(i+1))},审核{j+1},{1 if (i+j)%3==0 else 1000+(i+j)*320}' for i in range(8) for j in range(4))+'\n'+'\n'.join(f'审核{j+1},归档{k+1},{1800+j*280+k*130}' for j in range(4) for k in range(3))+'\n'
stress['architecture']='architecture-beta\n group platform(cloud)[跨团队资料平台]\n'+ '\n'.join(f' group g{i}(server)[资料与权限团队{i+1}] in platform\n'+ '\n'.join(f' service s{i}_{j}(server)[{long if i==1 and j==1 else "资料服务"+str(i+1)+str(j+1)}] in g{i}' for j in range(3)) for i in range(4))+'\n'+'\n'.join(f' s{i}_{j}:R --> L:s{i}_{j+1}' for i in range(4) for j in range(2))+'\n'+'\n'.join(f' s{i}_2:B --> T:s{i+1}_0' for i in range(3))+'\n'
# The pinned architecture lexer requires ASCII labels; keep long-label pressure valid.
import re
stress['architecture']=re.sub(r'\[([^]]+)\]', lambda m:'[Customer records and complete historical permissions verification service]' if len(m[1])>20 else '[Team service]',stress['architecture'])
(base/'sankey-unicode-invalid.mmd').write_text(stress['sankey'])
stress['sankey']=stress['sankey'].replace('跨地区企业客户资料来源与业务反馈入口','Customer records and complete historical business feedback source').replace('入口','Source ').replace('审核','Review ').replace('归档','Archive ')
stress['sankey']='sankey-beta\n\n'+'\n'.join(','.join(json.dumps(v,ensure_ascii=False) if i<2 else v for i,v in enumerate(line.split(','))) for line in stress['sankey'].splitlines()[2:])+'\n'
for kind in ['architecture','sequence','er','pie','xy','radar','sankey','block','c4']:
 for sample in ['normal','stress']:
  fixture=Path('tests/fixtures/mermaid')/('architecture.mmd' if kind=='architecture' else f'adapted-{kind}.mmd')
  spec={'title':f'{kind} · '+('常规' if sample=='normal' else '压力：多数据与长文本'),'source':fixture.read_text() if sample=='normal' else stress[kind]}
  if kind=='architecture': spec['navigation']='expanded'
  path=base/f'{kind}-{sample}.json';path.write_text(json.dumps(spec,ensure_ascii=False,indent=2))
  html=out/f'{kind}-review-{sample}.html'
  r=subprocess.run(['python3','skill/quick-visualize/scripts/render.py','mermaid',str(path),str(html)],capture_output=True,text=True)
  if r.returncode:raise RuntimeError(r.stdout)
  # Expose the parser model only in task-owned browser evidence, never in shipped output.
  preview_source=base/f'{kind}-{sample}-instrumented.html'
  preview_source.write_text(html.read_text().replace('const model=await readMermaidModel(mermaid,cfg.source,cfg.descriptions);','const model=await readMermaidModel(mermaid,cfg.source,cfg.descriptions);root.__reviewModel=model.data;'))
  subprocess.run(['python3','/Users/mac/.codex/plugins/cache/openai-bundled/visualize/1.0.49/skills/visualize/scripts/render.py',str(preview_source),str(base/f'{kind}-{sample}-preview.html'),'--force'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
print('18 review previews built')
