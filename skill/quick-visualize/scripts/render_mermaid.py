"""Keep Mermaid source intact; add only presentation metadata."""
import hashlib
import html
import json
from pathlib import Path

TEMPLATE_PATH = Path(__file__).resolve().parents[1] / 'assets' / 'mermaid.html'


def render(spec, output_path):
    if set(spec) - {'source', 'title', 'descriptions', 'icons', 'legend', 'navigation'}:
        raise ValueError('Allowed fields: source, title, descriptions, icons, legend, navigation')
    source = spec.get('source')
    if not isinstance(source, str) or not source.strip():
        raise ValueError('source must contain Mermaid text')
    if len(source) > 50000:
        raise ValueError('source must be at most 50000 characters; split larger diagrams')
    title = spec.get('title', '')
    if not isinstance(title, str) or len(title) > 200:
        raise ValueError('title must be text of at most 200 characters')
    descriptions = spec.get('descriptions', {})
    if not isinstance(descriptions, dict) or any(
        not isinstance(k, str) or not k or not isinstance(v, str) or not v.strip() or len(v) > 2000
        for k, v in descriptions.items()
    ):
        raise ValueError('descriptions must map node IDs to nonempty text (at most 2000 characters each)')
    if spec.get('icons', 'auto') not in ('auto', 'none', 'required'):
        raise ValueError('icons must be auto, none or required')
    if spec.get('navigation', 'auto') not in ('auto', 'drilldown', 'expanded'):
        raise ValueError('navigation must be auto, drilldown or expanded')
    legend = spec.get('legend', {})
    if not isinstance(legend, dict) or set(legend) - {'solid', 'dotted'} or any(not isinstance(v, str) or not v.strip() or len(v) > 80 for v in legend.values()):
        raise ValueError('legend must map solid/dotted to nonempty labels of at most 80 characters')
    config = {'source': source, 'title': title, 'descriptions': descriptions}
    if 'navigation' in spec:
        config['navigation'] = spec['navigation']
    if 'legend' in spec:
        config['legend'] = legend
    if 'icons' in spec:
        config['icons'] = spec['icons']
    encoded = json.dumps(config, ensure_ascii=False)
    digest = hashlib.sha256((encoded + str(output_path)).encode()).hexdigest()[:10]
    # Mermaid hexagon syntax contains double braces; encode data before template validation.
    encoded = json.dumps(encoded, ensure_ascii=False)
    for char in '<>&{}\u2028\u2029':
        encoded = encoded.replace(char, '\\u%04x' % ord(char))
    values = {'{{ROOT_ID}}': 'qv-mermaid-' + digest, '{{TITLE}}': html.escape(title),
              '{{TITLE_HIDDEN}}': '' if title else 'hidden', '{{CONFIG_JSON}}': encoded}
    fragment = TEMPLATE_PATH.read_text(encoding='utf-8').replace('{{MODEL_JS}}', TEMPLATE_PATH.with_name('mermaid-model.js').read_text(encoding='utf-8')).replace('{{LAYOUT_JS}}', TEMPLATE_PATH.with_name('mermaid-layout.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{NAVIGATION_JS}}', TEMPLATE_PATH.with_name('mermaid-navigation.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{ARCHITECTURE_READER_JS}}', TEMPLATE_PATH.with_name('mermaid-architecture-reader.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{VIEWPORT_JS}}', TEMPLATE_PATH.with_name('mermaid-viewport.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{SEQUENCE_MODEL_JS}}', TEMPLATE_PATH.with_name('mermaid-sequence-model.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{SEQUENCE_JS}}', TEMPLATE_PATH.with_name('mermaid-sequence.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{STATE_MODEL_JS}}', TEMPLATE_PATH.with_name('mermaid-state-model.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{STATE_JS}}', TEMPLATE_PATH.with_name('mermaid-state.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{ER_MODEL_JS}}', TEMPLATE_PATH.with_name('mermaid-er-model.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{ER_JS}}', TEMPLATE_PATH.with_name('mermaid-er.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{CLASS_MODEL_JS}}', TEMPLATE_PATH.with_name('mermaid-class-model.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{CLASS_JS}}', TEMPLATE_PATH.with_name('mermaid-class.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{TIMELINE_MODEL_JS}}', TEMPLATE_PATH.with_name('mermaid-timeline-model.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{TIMELINE_JS}}', TEMPLATE_PATH.with_name('mermaid-timeline.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{JOURNEY_MODEL_JS}}', TEMPLATE_PATH.with_name('mermaid-journey-model.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{JOURNEY_JS}}', TEMPLATE_PATH.with_name('mermaid-journey.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{QUADRANT_MODEL_JS}}', TEMPLATE_PATH.with_name('mermaid-quadrant-model.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{QUADRANT_JS}}', TEMPLATE_PATH.with_name('mermaid-quadrant.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{BLOCK_MODEL_JS}}', TEMPLATE_PATH.with_name('mermaid-block-model.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{BLOCK_LAYOUT_JS}}', TEMPLATE_PATH.with_name('mermaid-block-layout.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{BLOCK_JS}}', TEMPLATE_PATH.with_name('mermaid-block.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{C4_MODEL_JS}}', TEMPLATE_PATH.with_name('mermaid-c4-model.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{C4_LAYOUT_JS}}', TEMPLATE_PATH.with_name('mermaid-c4-layout.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{C4_JS}}', TEMPLATE_PATH.with_name('mermaid-c4.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{SANKEY_MODEL_JS}}', TEMPLATE_PATH.with_name('mermaid-sankey-model.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{SANKEY_JS}}', TEMPLATE_PATH.with_name('mermaid-sankey.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{RADAR_MODEL_JS}}', TEMPLATE_PATH.with_name('mermaid-radar-model.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{RADAR_JS}}', TEMPLATE_PATH.with_name('mermaid-radar.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{XY_MODEL_JS}}', TEMPLATE_PATH.with_name('mermaid-xy-model.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{XY_JS}}', TEMPLATE_PATH.with_name('mermaid-xy.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{PIE_MODEL_JS}}', TEMPLATE_PATH.with_name('mermaid-pie-model.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{PIE_JS}}', TEMPLATE_PATH.with_name('mermaid-pie.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{KANBAN_MODEL_JS}}', TEMPLATE_PATH.with_name('mermaid-kanban-model.js').read_text(encoding='utf-8'))
    fragment = fragment.replace('{{KANBAN_JS}}', TEMPLATE_PATH.with_name('mermaid-kanban.js').read_text(encoding='utf-8'))
    for key, value in values.items():
        fragment = fragment.replace(key, value)
    return fragment
