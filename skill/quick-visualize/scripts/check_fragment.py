"""固定模板的常规检查，不替代浏览器中的交互验收。"""
from __future__ import annotations
import re
import shutil
import subprocess
from html.parser import HTMLParser

class CheckError(ValueError):
    def __init__(self, message: str, line: int | None = None):
        super().__init__(message)
        self.line = line

class FragmentParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.references: list[tuple[str, int]] = []
        self.scripts: list[tuple[str, int]] = []
        self.script: list[str] | None = None
        self.script_line = 0
        self.root_id: str | None = None
        self.first_tag = True

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        line = self.getpos()[0]
        if tag in {"html", "head", "body"}:
            raise CheckError("Expected an HTML fragment, not a document", line)
        if self.first_tag:
            self.first_tag = False
            self.root_id = values.get("id")
            if tag != "div" or not self.root_id:
                raise CheckError("Fragment must start with a div with a unique id", line)
        element_id = values.get("id")
        if element_id:
            if element_id in self.ids:
                raise CheckError(f"Duplicate id: {element_id}", line)
            self.ids.add(element_id)
        for attr in ("for", "aria-labelledby", "aria-describedby", "aria-controls"):
            self.references.extend((item, line) for item in (values.get(attr) or "").split())
        if tag == "script" and not values.get("src"):
            self.script = []
            self.script_line = line

    def handle_data(self, data):
        if self.script is not None:
            self.script.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self.script is not None:
            self.scripts.append(("".join(self.script), self.script_line))
            self.script = None


def check_fragment(fragment: str) -> list[str]:
    if len(fragment.encode("utf-8")) >= 1_000_000:
        raise CheckError("Fragment must be smaller than 1 MB")
    token = re.search(r"\{\{.*?\}\}", fragment, re.DOTALL)
    if token:
        raise CheckError("Unresolved template token", fragment.count("\n", 0, token.start()) + 1)
    parsed = FragmentParser()
    parsed.feed(fragment)
    parsed.close()
    if not parsed.root_id or not parsed.scripts:
        raise CheckError("Missing root id or inline script")
    for reference, line in parsed.references:
        if reference not in parsed.ids:
            raise CheckError(f"Unknown element reference: {reference}", line)
    node = shutil.which("node")
    if node is None:
        raise CheckError("Node.js is required for JavaScript syntax checks; add node to PATH")
    for script, html_line in parsed.scripts:
        result = subprocess.run([node, "--check"], input=script, text=True, capture_output=True, timeout=15)
        if result.returncode:
            position = re.search(r"\[stdin\]:(\d+)", result.stderr)
            line = html_line + int(position.group(1)) - 1 if position else html_line
            message = next((item.strip() for item in result.stderr.splitlines() if "SyntaxError:" in item), "JavaScript syntax check failed")
            raise CheckError(message, line)
    return ["spec", "placeholders", "ids", "javascript", "size"]
