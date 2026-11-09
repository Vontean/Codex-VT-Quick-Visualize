"""Shared chart assets; standalone compiles them, Mermaid owns one outer copy."""
from pathlib import Path

CHART_ASSETS = {
    'CHART_MOTION_JS': 'chart-motion.js',
    'CHART_DETAIL_POSITION_JS': 'chart-detail-position.js',
    'CHART_ALIGNMENT_JS': 'chart-alignment.js',
    'CHART_POLISH_CSS': 'chart-polish.css',
}


def compile_chart_assets(fragment: str, assets: Path) -> str:
    for token, name in CHART_ASSETS.items():
        fragment = fragment.replace('{{' + token + '}}', (assets / name).read_text(encoding='utf-8'))
    return fragment


def without_chart_assets(fragment: str) -> str:
    """Preset markup/runtime inherits shared assets from the Mermaid root."""
    for token in CHART_ASSETS:
        fragment = fragment.replace('{{' + token + '}}', '')
    return fragment
