#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
from datetime import date
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = SKILL_DIR / "assets" / "line-chart.html"


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


def normalize_points(raw_points: Any) -> list[dict[str, Any]]:
    if not isinstance(raw_points, list) or not 2 <= len(raw_points) <= 90:
        raise ValueError("points must be a list containing 2-90 entries")

    points: list[dict[str, Any]] = []
    seen_dates: set[str] = set()
    for index, raw in enumerate(raw_points):
        if not isinstance(raw, dict):
            raise ValueError(f"points[{index}] must be an object")

        date_text = require_text(raw.get("date"), f"points[{index}].date")
        try:
            parsed_date = date.fromisoformat(date_text)
        except ValueError as error:
            raise ValueError(
                f"points[{index}].date must use ISO YYYY-MM-DD format"
            ) from error
        if parsed_date.isoformat() != date_text:
            raise ValueError(f"points[{index}].date must use ISO YYYY-MM-DD format")
        if date_text in seen_dates:
            raise ValueError(f"duplicate point date: {date_text}")

        value = raw.get("value")
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or value < 0
        ):
            raise ValueError(f"points[{index}].value must be a finite non-negative number")

        seen_dates.add(date_text)
        points.append(
            {
                "date": date_text,
                "value": value,
                "description": optional_text(
                    raw.get("description"), f"points[{index}].description"
                ).strip(),
            }
        )

    return sorted(points, key=lambda point: point["date"])


def normalize_decimals(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 2:
        raise ValueError("decimals must be an integer from 0 to 2")
    return value


def safe_json(value: Any) -> str:
    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )


def render(spec: dict[str, Any], output_path: Path) -> str:
    title = require_text(spec.get("title"), "title")
    x_axis_label = require_text(spec.get("x_axis_label"), "x_axis_label")
    y_axis_label = require_text(spec.get("y_axis_label"), "y_axis_label")
    value_prefix = optional_text(spec.get("value_prefix"), "value_prefix")
    value_suffix = optional_text(spec.get("value_suffix"), "value_suffix")
    decimals = normalize_decimals(spec.get("decimals", 0))
    points = normalize_points(spec.get("points"))

    digest_source = json.dumps(spec, ensure_ascii=False, sort_keys=True) + str(output_path)
    root_id = "quick-line-chart-" + hashlib.sha256(digest_source.encode()).hexdigest()[:10]
    minimum = min(point["value"] for point in points)
    maximum = max(point["value"] for point in points)
    summary = (
        f"{title}，从 {points[0]['date']} 到 {points[-1]['date']}，"
        f"共 {len(points)} 个数据点，最低值 {minimum:g}，最高值 {maximum:g}。"
    )

    replacements = {
        "{{ROOT_ID}}": root_id,
        "{{TITLE}}": html.escape(title),
        "{{SUMMARY}}": html.escape(summary),
        "{{CONFIG_JSON}}": safe_json(
            {
                "title": title,
                "xAxisLabel": x_axis_label,
                "yAxisLabel": y_axis_label,
                "valuePrefix": value_prefix,
                "valueSuffix": value_suffix,
                "decimals": decimals,
                "points": points,
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
    parser = argparse.ArgumentParser(description="Render a simple smooth line chart")
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
