"""Installed skill pointers stay self-contained; routes cover the public runner."""
import re
import sys
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skill/quick-visualize'
sys.path.insert(0, str(SKILL / 'scripts'))
from render import RENDERERS


def headings(path):
    text = path.read_text(encoding='utf-8')
    text = re.sub(r'```[\s\S]*?```', '', text)
    result = set()
    for heading in re.findall(r'^#+\s+(.+)', text, re.M):
        slug = re.sub(r'[^\w\-\s]', '', heading.replace('`', '').lower())
        result.add(slug.replace(' ', '-'))
    return result


class SkillDocsTests(unittest.TestCase):
    def test_installed_pointers_are_resolvable_inside_package(self):
        files = [SKILL / 'SKILL.md', *sorted((SKILL / 'references').glob('*.md'))]
        for file in files:
            text = re.sub(r'```[\s\S]*?```', '', file.read_text())
            for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
                with self.subTest(file=file.name, target=target):
                    url = urlsplit(target)
                    if url.scheme:
                        continue
                    path = (file.parent / unquote(url.path)).resolve() if url.path else file
                    self.assertTrue(path.is_relative_to(SKILL.resolve()), 'installed skill depends on repository-only material')
                    self.assertTrue(path.exists(), str(path))
                    if url.fragment and path.suffix == '.md':
                        self.assertIn(unquote(url.fragment), headings(path))

    def test_public_runner_types_have_route_and_input_contract(self):
        entry = (SKILL / 'SKILL.md').read_text()
        for kind in RENDERERS:
            with self.subTest(kind=kind):
                self.assertIn('`' + kind + '`', entry)
                name = 'multi-select' if kind.startswith('multi-select-') else kind
                self.assertTrue((SKILL / 'references' / (name + '.md')).exists())

    def test_repository_guides_reach_existing_owners(self):
        for file in [ROOT / 'README.md', ROOT / 'DESIGN.md', ROOT / 'docs/ARCHITECTURE.md', ROOT / 'docs/verification/README.md']:
            text = re.sub(r'```[\s\S]*?```', '', file.read_text())
            for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)', text):
                url = urlsplit(target)
                if url.scheme:
                    continue
                with self.subTest(file=file.name, target=target):
                    path = (file.parent / unquote(url.path)).resolve()
                    self.assertTrue(path.exists(), str(path))
                    if url.fragment and path.suffix == '.md':
                        self.assertIn(unquote(url.fragment), headings(path))


if __name__ == '__main__':
    unittest.main()
