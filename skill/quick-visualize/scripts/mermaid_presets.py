"""Compile the existing chart templates into Mermaid's semantic adapters."""
import json
import re
from pathlib import Path
from chart_assets import without_chart_assets


def compile_presets(assets: Path) -> str:
    functions = []
    for name, function in [('donut-chart', 'renderMermaidDonutPreset'), ('radar-chart', 'renderMermaidRadarPreset')]:
        source = (assets / (name + '.html')).read_text(encoding='utf-8')
        source = without_chart_assets(source)
        scripts = re.findall(r'<script(?:\s[^>]*)?>([\s\S]*?)</script>', source)
        runtime = next(script for script in scripts if '{{CONFIG_JSON}}' in script)
        runtime = re.sub(r'const config\s*=\s*\{\{CONFIG_JSON\}\};', '', runtime)
        runtime = runtime.replace("document.getElementById('{{ROOT_ID}}')", 'presetRoot')
        runtime = runtime.replace('{{ROOT_ID}}', "${presetRoot.id}")
        # Selectors containing an ID are ordinary strings in the preset source.
        runtime = re.sub(r"(['\"])([^'\"\n]*\$\{presetRoot.id\}[^'\"\n]*)\1", r'`\2`', runtime)
        runtime = runtime.replace('new ResizeObserver(', 'new PresetResizeObserver(')
        markup = re.sub(r'<script(?:\s[^>]*)?>[\s\S]*?</script>', '', source)
        markup = markup[markup.index('>')+1:markup.rfind('</div>')]
        markup = markup.replace('{{ROOT_ID}}', '@@ID@@').replace('{{TITLE}}', '@@TITLE@@').replace('{{SUMMARY}}', '@@SUMMARY@@')
        literal = json.dumps(markup, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e')
        loader = "const d3=await import('https://cdn.jsdelivr.net/npm/d3@7.9.0/+esm');" if name == 'donut-chart' else ''
        functions.append(f'''async function {function}(presetRoot,config,summary){{
 {loader}
 class PresetResizeObserver{{constructor(callback){{let frame=0;this.observer=new ResizeObserver(()=>{{if(!frame)frame=requestAnimationFrame(()=>{{frame=0;callback();}});}});}}observe(target){{this.observer.observe(target);}}}}
 const escape=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
 presetRoot.innerHTML={literal}.replaceAll('@@ID@@',presetRoot.id).replaceAll('@@TITLE@@',escape(config.title)).replaceAll('@@SUMMARY@@',escape(summary));
 {runtime}
}}''')
    return '\n'.join(functions)
