import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / 'skill' / 'quick-visualize'
sys.path.insert(0, str(SKILL / 'scripts'))
from render import render_checked


class MermaidContractTests(unittest.TestCase):
    def test_mmd_preserves_full_source(self):
        for fixture in (Path(__file__).parent / 'fixtures' / 'mermaid').glob('*.mmd'):
            with self.subTest(fixture=fixture.name), tempfile.TemporaryDirectory() as folder:
                out = Path(folder) / 'diagram.html'
                result = render_checked('mermaid', fixture, out)
                self.assertTrue(result['ok'], result)
                self.assertEqual(result['runtime'], 'pending-browser')
                config = re.search(r'cfg=JSON.parse\((.*?)\);', out.read_text()).group(1)
                self.assertEqual(json.loads(json.loads(config))['source'], fixture.read_text())

    def test_embedded_source_cannot_close_script(self):
        with tempfile.TemporaryDirectory() as folder:
            spec = {'source': 'flowchart LR\nA{{"</script><img src=x onerror=alert(1)>"}}',
                    'title': '<script>test</script>', 'descriptions': {'A': '</script> & <b>plain text</b>\u2028'}}
            src, out = Path(folder) / 'spec.json', Path(folder) / 'diagram.html'
            src.write_text(json.dumps(spec))
            self.assertTrue(render_checked('mermaid', src, out)['ok'])
            fragment = out.read_text()
            self.assertEqual(fragment.count('</script>'), 2)
            self.assertNotIn('<img', fragment)
            self.assertNotIn('{{', fragment)
            config = re.search(r'cfg=JSON.parse\((.*?)\);', fragment).group(1)
            self.assertEqual(json.loads(json.loads(config)), spec)

    def test_invalid_metadata_preserves_output(self):
        for spec in [{'source': ''}, {'source': 2}, {'source': 'x', 'nodes': []},
                     {'source': 'x', 'descriptions': {'A': []}}, {'source': 'x'*50001}]:
            with self.subTest(spec=str(spec)[:80]), tempfile.TemporaryDirectory() as folder:
                src, out = Path(folder) / 'spec.json', Path(folder) / 'diagram.html'
                src.write_text(json.dumps(spec)); out.write_text('previous')
                self.assertFalse(render_checked('mermaid', src, out)['ok'])
                self.assertEqual(out.read_text(), 'previous')

    def test_does_not_pretend_to_validate_mermaid_offline(self):
        with tempfile.TemporaryDirectory() as folder:
            src = Path(folder) / 'invalid.mmd'; src.write_text('not mermaid')
            result = render_checked('mermaid', src, Path(folder) / 'diagram.html')
            self.assertTrue(result['ok'])
            self.assertEqual(result['runtime'], 'pending-browser')
