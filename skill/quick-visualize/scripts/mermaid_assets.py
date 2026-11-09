"""Assemble the owned Mermaid template; source data is inserted only afterwards."""
import re
from pathlib import Path
from chart_assets import compile_chart_assets
from mermaid_presets import compile_presets


def compile_mermaid_template(template: Path) -> str:
    assets = template.parent
    fragment = compile_chart_assets(template.read_text(encoding='utf-8'), assets)

    def module(match):
        name = match.group(1)
        if name == 'CHART_PRESETS':
            return compile_presets(assets)
        source = assets / ('mermaid-' + name.lower().replace('_', '-') + '.js')
        return source.read_text(encoding='utf-8')

    return re.sub(r'\{\{([A-Z0-9_]+)_JS\}\}', module, fragment)
