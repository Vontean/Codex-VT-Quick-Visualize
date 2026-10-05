"""Keep Mermaid source intact; add only presentation metadata."""
import hashlib
import html
import json
from pathlib import Path

TEMPLATE_PATH = Path(__file__).resolve().parents[1] / 'assets' / 'mermaid.html'


def render(spec, output_path):
    if set(spec) - {'source', 'title', 'descriptions', 'icons', 'legend'}:
        raise ValueError('Allowed fields: source, title, descriptions, icons, legend')
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
    if spec.get('icons', 'auto') not in ('auto', 'none'):
        raise ValueError('icons must be auto or none')
    legend = spec.get('legend', {})
    if not isinstance(legend, dict) or set(legend) - {'solid', 'dotted'} or any(not isinstance(v, str) or not v.strip() or len(v) > 80 for v in legend.values()):
        raise ValueError('legend must map solid/dotted to nonempty labels of at most 80 characters')
    config = {'source': source, 'title': title, 'descriptions': descriptions}
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
    fragment = TEMPLATE_PATH.read_text(encoding='utf-8').replace('{{MODEL_JS}}', TEMPLATE_PATH.with_name('mermaid-model.js').read_text(encoding='utf-8'))
    for key, value in values.items():
        fragment = fragment.replace(key, value)
    return fragment
