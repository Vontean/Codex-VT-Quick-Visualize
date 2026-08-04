#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = SKILL_DIR / "assets" / "ranker.html"


def require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def normalize_items(spec: dict[str, Any]) -> list[dict[str, str]]:
    raw_items = spec.get("items")
    if not isinstance(raw_items, list) or not 2 <= len(raw_items) <= 20:
        raise ValueError("items must be a list containing 2-20 entries")

    normalized: list[dict[str, str]] = []
    seen_values: set[str] = set()
    for index, raw in enumerate(raw_items):
        if isinstance(raw, str):
            label = value = require_text(raw, f"items[{index}]")
        elif isinstance(raw, dict):
            label = require_text(raw.get("label"), f"items[{index}].label")
            value = require_text(raw.get("value", label), f"items[{index}].value")
        else:
            raise ValueError(f"items[{index}] must be a string or object")

        if value in seen_values:
            raise ValueError(f"duplicate item value: {value}")
        seen_values.add(value)
        normalized.append({"label": label, "value": value})
    return normalized


def safe_json(value: Any) -> str:
    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )


def render(spec: dict[str, Any], output_path: Path) -> str:
    question = require_text(spec.get("question"), "question")
    follow_up_prompt = require_text(spec.get("follow_up_prompt"), "follow_up_prompt")
    if "{ordered}" not in follow_up_prompt:
        raise ValueError("follow_up_prompt must contain {ordered}")
    items = normalize_items(spec)
    digest_source = json.dumps(spec, ensure_ascii=False, sort_keys=True) + str(output_path)
    root_id = "quick-ranker-" + hashlib.sha256(digest_source.encode()).hexdigest()[:10]

    item_lines: list[str] = []
    for index, item in enumerate(items):
        item_id = f"{root_id}-item-{index + 1}"
        label = html.escape(item["label"])
        value = html.escape(item["value"], quote=True)
        item_lines.extend(
            (
                f'      <div class="quick-rank-item" id="{item_id}" role="listitem" draggable="true" data-label="{html.escape(item["label"], quote=True)}" data-value="{value}">',
                f'        <button class="btn btn-ghost quick-rank-handle" type="button" draggable="true" aria-label="拖动 {html.escape(item["label"], quote=True)}；按上或下方向键调整顺序">',
                '          <i data-lucide="grip-vertical" aria-hidden="true"></i>',
                "        </button>",
                f'        <span class="quick-rank-label">{label}</span>',
                "      </div>",
            )
        )

    replacements = {
        "{{ROOT_ID}}": root_id,
        "{{QUESTION}}": html.escape(question, quote=True),
        "{{ITEMS_HTML}}": "\n".join(item_lines),
        "{{CONFIG_JSON}}": safe_json({"followUpPrompt": follow_up_prompt}),
    }

    fragment = TEMPLATE_PATH.read_text(encoding="utf-8")
    for token, replacement in replacements.items():
        fragment = fragment.replace(token, replacement)
    if "{{" in fragment or "}}" in fragment:
        raise ValueError("unresolved template token remains")
    return fragment


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a quick ranker visualization")
    parser.add_argument("spec", type=Path, help="UTF-8 JSON specification")
    parser.add_argument("output", type=Path, help="destination HTML fragment")
    args = parser.parse_args()

    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    if not isinstance(spec, dict):
        raise ValueError("spec root must be a JSON object")
    fragment = render(spec, args.output)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(fragment, encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
