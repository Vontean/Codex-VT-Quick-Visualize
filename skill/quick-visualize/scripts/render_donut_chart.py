#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = SKILL_DIR / "assets" / "donut-chart.html"


def require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def optional_text(value: Any, field: str) -> str:
    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    return value


def normalize_decimals(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 2:
        raise ValueError("decimals must be an integer from 0 to 2")
    return value


def normalize_items(raw_items: Any) -> list[dict[str, Any]]:
    if not isinstance(raw_items, list) or not 2 <= len(raw_items) <= 6:
        raise ValueError("items must be a list containing 2-6 entries")

    items: list[dict[str, Any]] = []
    seen_labels: set[str] = set()
    for index, raw in enumerate(raw_items):
        if not isinstance(raw, dict):
            raise ValueError(f"items[{index}] must be an object")
        label = require_text(raw.get("label"), f"items[{index}].label")
        if label in seen_labels:
            raise ValueError(f"duplicate item label: {label}")

        value = raw.get("value")
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or value < 0
        ):
            raise ValueError(f"items[{index}].value must be a finite non-negative number")

        seen_labels.add(label)
        items.append(
            {
                "label": label,
                "value": value,
                "description": optional_text(
                    raw.get("description"), f"items[{index}].description"
                ).strip(),
            }
        )

    if sum(item["value"] for item in items) <= 0:
        raise ValueError("the sum of item values must be greater than zero")
    return items


def safe_json(value: Any) -> str:
    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )


def percent_text(value: float) -> str:
    return f"{value:.1f}".rstrip("0").rstrip(".") + "%"


def render(spec: dict[str, Any], output_path: Path) -> str:
    title = require_text(spec.get("title"), "title")
    value_prefix = optional_text(spec.get("value_prefix"), "value_prefix")
    value_suffix = optional_text(spec.get("value_suffix"), "value_suffix")
    decimals = normalize_decimals(spec.get("decimals", 0))
    items = normalize_items(spec.get("items"))
    total = sum(item["value"] for item in items)
    largest = max(items, key=lambda item: item["value"])
    largest_percent = percent_text(largest["value"] / total * 100)

    digest_source = json.dumps(spec, ensure_ascii=False, sort_keys=True) + str(output_path)
    root_id = "quick-donut-chart-" + hashlib.sha256(
        digest_source.encode()
    ).hexdigest()[:10]
    summary = (
        f"{title}，包含 {len(items)} 个类别；占比最高的是 {largest['label']}，"
        f"占 {largest_percent}。"
    )

    replacements = {
        "{{ROOT_ID}}": root_id,
        "{{TITLE}}": html.escape(title),
        "{{SUMMARY}}": html.escape(summary),
        "{{CONFIG_JSON}}": safe_json(
            {
                "title": title,
                "valuePrefix": value_prefix,
                "valueSuffix": value_suffix,
                "decimals": decimals,
                "items": items,
            }
        ),
    }

    fragment = TEMPLATE_PATH.read_text(encoding="utf-8")
    for token, replacement in replacements.items():
        fragment = fragment.replace(token, replacement)
    if "{{" in fragment or "}}" in fragment:
        raise ValueError("unresolved template token remains")
    return fragment


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a donut chart")
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
