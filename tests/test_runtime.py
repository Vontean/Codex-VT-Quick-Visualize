import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SKILL = Path(__file__).resolve().parents[1] / 'skill' / 'quick-visualize'
sys.path.insert(0, str(SKILL / 'scripts'))
from check_fragment import CheckError, check_fragment
from render import RENDERERS, render_checked

class RuntimeTests(unittest.TestCase):
    def test_all_presets_and_references(self):
        for kind in RENDERERS:
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as folder:
                name = 'multi-select' if kind.startswith('multi-select-') else kind
                doc = (SKILL / 'references' / (name + '.md')).read_text()
                spec = json.loads(re.search(r'```json\n(.*?)\n```', doc, re.S).group(1))
                if kind.startswith('multi-select-'):
                    spec['variant'] = kind
                source = Path(folder) / 'spec.json'
                output = Path(folder) / 'chart.html'
                source.write_text(json.dumps(spec))
                result = render_checked(kind, source, output)
                self.assertTrue(result['ok'], result)
                self.assertTrue(output.exists())
                self.assertEqual(result['checks'], ['spec', 'placeholders', 'ids', 'javascript', 'size'])
                self.assertTrue(result['reference'].startswith(f'::codex-inline-vis{{path="{output.resolve()}"'))
                self.assertTrue(result['reference'].endswith('}'))
                self.assertNotIn('\ue200', result['reference'])

    def test_legacy_reference_requires_explicit_format(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'spec.json'
            output = Path(folder) / 'chart.html'
            source.write_text('{"title":"构成","items":[{"label":"A","value":60},{"label":"B","value":40}]}')
            result = render_checked('donut-chart', source, output, 'visualize')
            self.assertTrue(result['ok'], result)
            self.assertTrue(result['reference'].startswith('\ue200visualize\ue202'))
            self.assertTrue(result['reference'].endswith('\ue201'))
            payload = json.loads(result['reference'].split('\ue202')[1][:-1])
            self.assertEqual(payload['path'], str(output.resolve()))

    def test_cli_defaults_to_ascii_without_format_flag(self):
        import subprocess
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'spec.json'
            output = Path(folder) / 'chart.html'
            source.write_text('{"title":"构成","items":[{"label":"A","value":60},{"label":"B","value":40}]}')
            completed = subprocess.run([sys.executable, str(SKILL / 'scripts/render.py'), 'donut-chart', str(source), str(output)], capture_output=True, text=True)
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertEqual(result['reference'], f'::codex-inline-vis{{path="{output.resolve()}"}}')

    def test_invalid_spec_preserves_old_output(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'spec.json'
            output = Path(folder) / 'chart.html'
            source.write_text('{"points": []}')
            output.write_text('previous')
            result = render_checked('line-chart', source, output)
            self.assertFalse(result['ok'])
            self.assertNotIn('reference', result)
            self.assertEqual(output.read_text(), 'previous')
            self.assertEqual(sorted(p.name for p in Path(folder).iterdir()), ['chart.html', 'spec.json'])

    def test_directive_reference_preserves_path_and_wide_mode(self):
        with tempfile.TemporaryDirectory() as folder:
            directory = Path(folder) / '中文 directory'
            directory.mkdir()
            source = directory / 'spec.json'
            output = directory / 'chart.html'
            fragment = '<div id="root"><script>const x = 1;</script></div>'
            source.write_text('{}')
            for kind in ('donut-chart', 'mermaid'):
                with self.subTest(kind=kind), patch('render.importlib.import_module') as module:
                    module.return_value.render.return_value = fragment
                    result = render_checked(kind, source, output, 'directive')
                    self.assertTrue(result['ok'], result)
                    wide = ' mode="wide"' if kind == 'mermaid' else ''
                    self.assertEqual(result['reference'], f'::codex-inline-vis{{path="{output.resolve()}"{wide}}}')
                    self.assertNotIn('\ue200', result['reference'])

    def test_host_rejects_bad_filename_before_writing(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'spec.json'
            source.write_text('{}')
            for name in ('中文.html', 'Chart.html', 'chart name.html', 'chart_name.html', 'chart--name.html', 'chart.HTML'):
                with self.subTest(name=name):
                    output = Path(folder) / name
                    output.write_text('previous')
                    result = render_checked('donut-chart', source, output)
                    self.assertFalse(result['ok'])
                    self.assertEqual(result['stage'], 'spec')
                    self.assertNotIn('reference', result)
                    self.assertEqual(output.read_text(), 'previous')

    def test_reference_rejects_unsafe_path_and_unknown_format(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'spec.json'
            source.write_text('{}')
            for parent in ('quote"directory', 'line\nbreak', 'line\rbreak'):
                result = render_checked('donut-chart', source, Path(folder) / parent / 'chart.html', 'directive')
                self.assertFalse(result['ok'])
                self.assertIn('quotes or line breaks', result['error']['message'])
            result = render_checked('donut-chart', source, Path(folder) / 'chart.html', 'unknown')
            self.assertFalse(result['ok'])
            self.assertIn('Reference format', result['error']['message'])

    def test_json_error_location(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'spec.json'
            source.write_text('{\n invalid}')
            result = render_checked('line-chart', source, Path(folder) / 'chart.html')
            self.assertEqual(result['stage'], 'spec')
            self.assertEqual(result['error']['line'], 2)

    def test_variant_mismatch(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'spec.json'
            source.write_text('{"variant":"multi-select-complete"}')
            result = render_checked('multi-select-simple', source, Path(folder) / 'chart.html')
            self.assertFalse(result['ok'])
            self.assertIn('variant', result['error']['message'])

    def test_js_error_reports_html_line(self):
        with self.assertRaises(CheckError) as caught:
            check_fragment('<div id="root">\n<script>\nconst x = ;\n</script></div>')
        self.assertEqual(caught.exception.line, 3)

    def test_no_node_never_skips_check(self):
        with patch('check_fragment.shutil.which', return_value=None), self.assertRaisesRegex(CheckError, 'Node.js'):
            check_fragment('<div id="root"><script>const x = 1;</script></div>')

    def test_structural_errors(self):
        cases = {
            'placeholder': '<div id="root">{{TITLE}}<script>1</script></div>',
            'duplicate': '<div id="root"><i id="root"></i><script>1</script></div>',
            'missing reference': '<div id="root"><label for="missing">x</label><script>1</script></div>',
            'document': '<html><body><script>1</script></body></html>',
            'oversize': '<div id="root">' + 'x' * 1_000_000 + '<script>1</script></div>',
        }
        for name, fragment in cases.items():
            with self.subTest(name=name), self.assertRaises(CheckError):
                check_fragment(fragment)

    def test_js_failure_preserves_old_output(self):
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / 'spec.json'
            output = Path(folder) / 'chart.html'
            source.write_text('{}')
            output.write_text('previous')
            with patch('render.importlib.import_module') as module:
                module.return_value.render.return_value = '<div id="root"><script>const x = ;</script></div>'
                result = render_checked('line-chart', source, output)
            self.assertFalse(result['ok'])
            self.assertEqual(result['stage'], 'check')
            self.assertTrue(any('const x = ;' in line for line in result['error']['context']))
            self.assertNotIn('reference', result)
            self.assertEqual(output.read_text(), 'previous')

if __name__ == '__main__':
    unittest.main()
