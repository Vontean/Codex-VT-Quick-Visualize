#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = SKILL_DIR / "assets" / "comparison.html"


def require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def optional_text(value: Any, field: str) -> str:
    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    return value.strip()


def normalize_dimensions(raw_dimensions: Any, field: str) -> list[dict[str, str]]:
    if not isinstance(raw_dimensions, list) or not 2 <= len(raw_dimensions) <= 8:
        raise ValueError(f"{field} must contain 2-8 entries")

    dimensions: list[dict[str, str]] = []
    seen_labels: set[str] = set()
    for index, raw in enumerate(raw_dimensions):
        if not isinstance(raw, dict):
            raise ValueError(f"{field}[{index}] must be an object")
        label = require_text(raw.get("label"), f"{field}[{index}].label")
        value = require_text(raw.get("value"), f"{field}[{index}].value")
        if label in seen_labels:
            raise ValueError(f"duplicate dimension label in {field}: {label}")
        seen_labels.add(label)
        dimensions.append({"label": label, "value": value})
    return dimensions


def normalize_plans(spec: dict[str, Any]) -> list[dict[str, Any]]:
    raw_plans = spec.get("plans")
    if not isinstance(raw_plans, list) or not 2 <= len(raw_plans) <= 4:
        raise ValueError("plans must be a list containing 2-4 entries")

    requested_selected = spec.get("selected")
    if requested_selected is not None:
        requested_selected = require_text(requested_selected, "selected")

    plans: list[dict[str, Any]] = []
    seen_values: set[str] = set()
    expected_dimension_labels: list[str] | None = None
    requested_selected_matched = requested_selected is None
    for index, raw in enumerate(raw_plans):
        if not isinstance(raw, dict):
            raise ValueError(f"plans[{index}] must be an object")
        title = require_text(raw.get("title"), f"plans[{index}].title")
        value = require_text(raw.get("value", title), f"plans[{index}].value")
        if value in seen_values:
            raise ValueError(f"duplicate plan value: {value}")
        seen_values.add(value)

        dimensions = normalize_dimensions(raw.get("dimensions"), f"plans[{index}].dimensions")
        dimension_labels = [dimension["label"] for dimension in dimensions]
        if expected_dimension_labels is None:
            expected_dimension_labels = dimension_labels
        elif dimension_labels != expected_dimension_labels:
            raise ValueError("every plan must use the same dimension labels in the same order")

        matches_requested = requested_selected in {title, value}
        requested_selected_matched = requested_selected_matched or matches_requested
        plans.append(
            {
                "title": title,
                "value": value,
                "summary": optional_text(raw.get("summary"), f"plans[{index}].summary"),
                "dimensions": dimensions,
                "selected": bool(raw.get("selected", False)) or matches_requested,
            }
        )

    selected_plans = [plan for plan in plans if plan["selected"]]
    if len(selected_plans) > 1:
        raise ValueError("comparison may have at most one selected plan")
    if not requested_selected_matched:
        raise ValueError("selected must match a plan title or value")
    return plans


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
    if "{selected}" not in follow_up_prompt:
        raise ValueError("follow_up_prompt must contain {selected}")
    plans = normalize_plans(spec)
    digest_source = json.dumps(spec, ensure_ascii=False, sort_keys=True) + str(output_path)
    root_id = "quick-comparison-" + hashlib.sha256(digest_source.encode()).hexdigest()[:10]

    plan_lines: list[str] = []
    for index, plan in enumerate(plans):
        plan_id = f"{root_id}-plan-{index + 1}"
        checked = " checked" if plan["selected"] else ""
        summary_html = (
            f'        <p class="quick-comparison-summary">{html.escape(plan["summary"])}</p>'
            if plan["summary"]
            else ""
        )
        dimension_lines: list[str] = []
        for dimension in plan["dimensions"]:
            dimension_lines.extend(
                (
                    '          <li class="quick-comparison-dimension">',
                    f'            <span class="text-small quick-comparison-dimension-label">{html.escape(dimension["label"])}</span>',
                    f'            <span class="quick-comparison-dimension-value">{html.escape(dimension["value"])}</span>',
                    "          </li>",
                )
            )
        plan_lines.extend(
            (
                f'      <label class="card quick-comparison-option" for="{plan_id}">',
                '        <span class="quick-comparison-header">',
                f'          <span class="quick-comparison-title">{html.escape(plan["title"])}</span>',
                '          <span class="form-check">',
                f'            <input class="form-check-input" id="{plan_id}" name="comparison-plan" type="radio" value="{html.escape(plan["value"], quote=True)}" data-label="{html.escape(plan["title"], quote=True)}" required{checked}>',
                f'            <span class="form-check-label sr-only">选择 {html.escape(plan["title"])}</span>',
                "          </span>",
                "        </span>",
                summary_html,
                '        <ul class="quick-comparison-dimensions">',
                *dimension_lines,
                "        </ul>",
                "      </label>",
            )
        )

    replacements = {
        "{{ROOT_ID}}": root_id,
        "{{QUESTION}}": html.escape(question),
        "{{PLANS_HTML}}": "\n".join(line for line in plan_lines if line),
        "{{CONFIG_JSON}}": safe_json({"followUpPrompt": follow_up_prompt}),
    }
    fragment = TEMPLATE_PATH.read_text(encoding="utf-8")
    for token, replacement in replacements.items():
        fragment = fragment.replace(token, replacement)
    if "{{" in fragment or "}}" in fragment:
        raise ValueError("unresolved template token remains")
    return fragment


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a quick comparison visualization")
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
