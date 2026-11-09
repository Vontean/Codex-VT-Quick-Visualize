"""Compile shared chart presentation assets for standalone and Mermaid presets."""
from pathlib import Path


def compile_chart_assets(fragment, assets):
    for token, name in [('CHART_MOTION_JS', 'chart-motion.js'),
                        ('CHART_DETAIL_POSITION_JS', 'chart-detail-position.js'),
                        ('CHART_LEGEND_JS', 'chart-legend.js'),
                        ('CHART_POLISH_CSS', 'chart-polish.css')]:
        fragment = fragment.replace('{{' + token + '}}', (assets / name).read_text(encoding='utf-8'))
    return fragment
