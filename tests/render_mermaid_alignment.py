"""Generate alignment audit previews using the real Visualize sandbox."""
import argparse
import json
import runpy
import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'skill/quick-visualize/scripts'))
from render import render_checked


def generate(visualize, output):
    output.mkdir(parents=True, exist_ok=True)
    wrapper = runpy.run_path(str(visualize / 'scripts/render.py'))['render']
    cases = [c for c in json.loads((ROOT / 'tests/fixtures/mermaid/polish/cases.json').read_text()) if c['scene'] == 'normal']
    for kind in ['block', 'c4', 'kanban']:
        cases.append({'id': kind, 'source': (ROOT / f'tests/fixtures/mermaid/adapted-{kind}.mmd').read_text()})
    cases += [{'id': 'long-title-' + c['id'], 'source': c['source'], 'title': '跨团队产品需求评审与交付验收状态追踪以及异常场景处理说明 / WorkspacePermissionSynchronizationWithoutAnyWhitespaceBoundary ' * 2} for c in cases if c['id'] in ['git', 'sankey', 'timeline']]
    cases.append({'id': 'compact-c4', 'source': 'C4Context\n Person(user, "用户")\n System(app, "应用")\n Rel(user, app, "使用")'})
    cases.append({'id': 'responsive-title-git', 'source': next(c['source'] for c in cases if c['id'] == 'git'), 'title': '跨团队产品需求评审与交付验收状态追踪以及异常场景处理说明'})
    cases.append({'id': 'fallback', 'source': 'flowchart LR\n A --> B\n style A fill:#f9f'})
    for kind in ['line-chart', 'grouped-bar-chart', 'donut-chart', 'radar-chart']:
        doc = (ROOT / f'skill/quick-visualize/references/{kind}.md').read_text()
        preset = json.loads(re.search(r'```json\n(.*?)\n```', doc, re.S).group(1))
        cases.append({'id': kind, 'kind': kind, 'spec': preset})
    for c in cases:
        spec = output / (c['id'] + '.json')
        spec.write_text(json.dumps(c.get('spec') or {'source': c['source'], 'title': c.get('title', '模拟图表标题 · 对齐检查')}, ensure_ascii=False))
        fragment = output / (c['id'] + '.html')
        result = render_checked(c.get('kind', 'mermaid'), spec, fragment)
        if not result['ok']:
            raise RuntimeError(result)
        (output / (c['id'] + '-preview.html')).write_text(wrapper(fragment))
    (output / 'cases.json').write_text(json.dumps(cases, ensure_ascii=False))
    print(f'Generated {len(cases)} alignment previews')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('visualize', type=Path)
    p.add_argument('output', type=Path)
    args = p.parse_args()
    generate(args.visualize, args.output)
