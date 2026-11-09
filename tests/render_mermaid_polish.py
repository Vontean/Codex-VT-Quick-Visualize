"""Generate portable regression fixtures with the installed Visualize sandbox wrapper."""
import argparse
import json
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skill/quick-visualize/scripts'))
from render import render_checked


def generate(visualize_dir, output):
    output.mkdir(parents=True, exist_ok=True)
    wrapper = runpy.run_path(str(visualize_dir / 'scripts/render.py'))['render']
    cases = json.loads((ROOT / 'tests/fixtures/mermaid/polish/cases.json').read_text())
    cases += [
        {'id': 'radar-preset-title', 'scene': 'normal', 'source': '---\ntitle: "雷达预设标题"\n---\nradar-beta\n axis a["设计"], b["交付"], c["性能"], d["可达性"]\n curve x["方案甲"]{75,80,65,90}\n curve y["方案乙"]{90,65,80,70}\n max 100\n min 0\n ticks 5\n graticule polygon'},
        {'id': 'radar-generic-title', 'scene': 'normal', 'source': '---\ntitle: >-\n  通用雷达长标题验证\n---\nradar-beta\n axis a["设计方案与使用体验"], b["持续交付与协作"], c["性能及稳定性"], d["可达性与键盘访问"]\n curve x["第一组长名称"]{75,80,65,90}\n curve y["第二组长名称"]{90,65,80,70}\n max 100\n min 10'},
        {'id': 'sankey-title', 'scene': 'normal', 'source': '---\ntitle: 桑基流向标题\n---\nsankey-beta\nDemand,Design,30\nDesign,Delivery,25\nDesign,Review,5'},
        {'id': 'fallback', 'scene': 'normal', 'source': 'flowchart LR\n A --> B\n style A fill:#f9f'},
        {'id': 'state-nested', 'scene': 'normal', 'source': 'stateDiagram-v2\n [*] --> Composite\n state Composite {\n [*] --> A\n A --> Nested\n state Nested {\n [*] --> B\n B --> C\n }\n }\n Composite --> [*]'},
        {'id': 'sequence-bidirectional', 'scene': 'normal', 'source': 'sequenceDiagram\n autonumber\n participant A\n participant B\n A<<->>B: 双向消息完整标签\n B->>A: 返回'}
    ]
    for c in cases:
        slug = c['id'] + '-' + c['scene']
        spec = output / (slug + '.json')
        spec.write_text(json.dumps({'source': c['source']}, ensure_ascii=False))
        fragment = output / (slug + '.html')
        result = render_checked('mermaid', spec, fragment)
        if not result['ok']:
            raise RuntimeError(result)
        (output / (slug + '-preview.html')).write_text(wrapper(fragment))
    (output / 'cases.json').write_text(json.dumps(cases, ensure_ascii=False))
    print(f'Generated {len(cases)} sandbox previews in {output}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('visualize_dir', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    generate(args.visualize_dir, args.output)
