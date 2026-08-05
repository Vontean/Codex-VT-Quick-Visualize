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
TEMPLATE_PATH = SKILL_DIR / "assets" / "radar-chart.html"


def require_text(value: Any, field: str, *, maximum: int | None = None) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    normalized = value.strip()
    if maximum is not None and len(normalized) > maximum:
        raise ValueError(f"{field} must contain at most {maximum} characters")
    return normalized


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


def normalize_maximum(value: Any) -> float:
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value <= 0
    ):
        raise ValueError("max_value must be a finite positive number")
    return value


def normalize_dimensions(raw_dimensions: Any) -> list[str]:
    if not isinstance(raw_dimensions, list) or not 3 <= len(raw_dimensions) <= 8:
        raise ValueError("dimensions must be a list containing 3-8 entries")

    dimensions = [
        require_text(value, f"dimensions[{index}]", maximum=12)
        for index, value in enumerate(raw_dimensions)
    ]
    if len(set(dimensions)) != len(dimensions):
        raise ValueError("dimension labels must be unique")
    return dimensions


def normalize_series(
    raw_series: Any, dimensions: list[str], maximum: float
) -> list[dict[str, Any]]:
    if not isinstance(raw_series, list) or not 1 <= len(raw_series) <= 4:
        raise ValueError("series must be a list containing 1-4 entries")

    series: list[dict[str, Any]] = []
    seen_names: set[str] = set()
    for series_index, raw in enumerate(raw_series):
        if not isinstance(raw, dict):
            raise ValueError(f"series[{series_index}] must be an object")
        name = require_text(raw.get("name"), f"series[{series_index}].name", maximum=32)
        if name in seen_names:
            raise ValueError(f"duplicate series name: {name}")

        raw_values = raw.get("values")
        if not isinstance(raw_values, list) or len(raw_values) != len(dimensions):
            raise ValueError(
                f"series[{series_index}].values must contain exactly "
                f"{len(dimensions)} entries"
            )

        values: list[int | float] = []
        for value_index, value in enumerate(raw_values):
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or not math.isfinite(value)
                or value < 0
                or value > maximum
            ):
                raise ValueError(
                    f"series[{series_index}].values[{value_index}] must be a finite "
                    f"number from 0 to max_value"
                )
            values.append(value)

        seen_names.add(name)
        series.append({"name": name, "values": values})
    return series


def safe_json(value: Any) -> str:
    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )


def render(spec: dict[str, Any], output_path: Path) -> str:
    title = require_text(spec.get("title"), "title")
    maximum = normalize_maximum(spec.get("max_value", 100))
    value_prefix = optional_text(spec.get("value_prefix"), "value_prefix")
    value_suffix = optional_text(spec.get("value_suffix"), "value_suffix")
    decimals = normalize_decimals(spec.get("decimals", 0))
    dimensions = normalize_dimensions(spec.get("dimensions"))
    series = normalize_series(spec.get("series"), dimensions, maximum)

    digest_source = json.dumps(spec, ensure_ascii=False, sort_keys=True) + str(output_path)
    root_id = "quick-radar-chart-" + hashlib.sha256(
        digest_source.encode()
    ).hexdigest()[:10]
    summary = (
        f"{title}，包含 {len(series)} 个对象与 {len(dimensions)} 个共同维度；"
        f"所有维度使用 0 到 {maximum:g} 的共享标尺。"
    )

    replacements = {
        "{{ROOT_ID}}": root_id,
        "{{TITLE}}": html.escape(title),
        "{{SUMMARY}}": html.escape(summary),
        "{{CONFIG_JSON}}": safe_json(
            {
                "title": title,
                "summary": summary,
                "maxValue": maximum,
                "valuePrefix": value_prefix,
                "valueSuffix": value_suffix,
                "decimals": decimals,
                "dimensions": dimensions,
                "series": series,
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
    parser = argparse.ArgumentParser(description="Render a radar chart")
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
