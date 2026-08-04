#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_PATHS = {
    "multi-select-simple": SKILL_DIR / "assets" / "multi-select-simple.html",
    "multi-select-complete": SKILL_DIR / "assets" / "multi-select-complete.html",
}


def require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def normalize_options(spec: dict[str, Any], variant: str) -> list[dict[str, Any]]:
    raw_options = spec.get("options")
    if not isinstance(raw_options, list) or not 2 <= len(raw_options) <= 20:
        raise ValueError("options must be a list containing 2-20 items")

    selected = spec.get("selected", [])
    if not isinstance(selected, list) or not all(isinstance(item, str) for item in selected):
        raise ValueError("selected must be a list of strings")
    selected_set = set(selected)

    normalized: list[dict[str, Any]] = []
    seen_values: set[str] = set()
    for index, raw in enumerate(raw_options):
        if isinstance(raw, str):
            label = value = require_text(raw, f"options[{index}]")
            supporting_text = None
            initially_selected = False
        elif isinstance(raw, dict):
            label = require_text(raw.get("label"), f"options[{index}].label")
            value = require_text(raw.get("value", label), f"options[{index}].value")
            raw_supporting_text = raw.get("supporting_text")
            supporting_text = (
                require_text(raw_supporting_text, f"options[{index}].supporting_text")
                if raw_supporting_text is not None
                else None
            )
            initially_selected = bool(raw.get("selected", False))
        else:
            raise ValueError(f"options[{index}] must be a string or object")

        if value in seen_values:
            raise ValueError(f"duplicate option value: {value}")
        if variant == "multi-select-complete" and supporting_text is None:
            raise ValueError(
                f"options[{index}].supporting_text is required for multi-select-complete variant"
            )
        seen_values.add(value)
        normalized.append(
            {
                "label": label,
                "value": value,
                "supporting_text": supporting_text,
                "selected": initially_selected or label in selected_set or value in selected_set,
            }
        )
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
    variant = spec.get("variant", "multi-select-simple")
    if variant not in TEMPLATE_PATHS:
        raise ValueError(
            "variant must be 'multi-select-simple' or 'multi-select-complete'"
        )
    options = normalize_options(spec, variant)
    digest_source = json.dumps(spec, ensure_ascii=False, sort_keys=True) + str(output_path)
    root_id = "quick-multiselect-" + hashlib.sha256(digest_source.encode()).hexdigest()[:10]

    option_lines: list[str] = []
    for index, option in enumerate(options):
        option_id = f"{root_id}-option-{index + 1}"
        checked = " checked" if option["selected"] else ""
        if variant == "multi-select-simple":
            option_lines.extend(
                (
                    f'      <label class="form-check" for="{option_id}">',
                    f'        <input class="form-check-input" id="{option_id}" type="checkbox" value="{html.escape(option["value"], quote=True)}" data-label="{html.escape(option["label"], quote=True)}"{checked}>',
                    f'        <span class="form-check-label">{html.escape(option["label"])}</span>',
                    "      </label>",
                )
            )
        else:
            title_id = f"{option_id}-title"
            support_id = f"{option_id}-support"
            option_lines.extend(
                (
                    f'      <label class="form-check quick-choice-item" for="{option_id}">',
                    '        <span class="quick-choice-copy">',
                    f'          <span class="quick-choice-title" id="{title_id}">{html.escape(option["label"])}</span>',
                    f'          <span class="text-small text-muted" id="{support_id}">{html.escape(option["supporting_text"])}</span>',
                    "        </span>",
                    f'        <input class="form-check-input" id="{option_id}" type="checkbox" value="{html.escape(option["value"], quote=True)}" data-label="{html.escape(option["label"], quote=True)}" aria-labelledby="{title_id}" aria-describedby="{support_id}"{checked}>',
                    "      </label>",
                )
            )

    follow_up_prompt = spec.get("follow_up_prompt")
    if follow_up_prompt is None:
        submit_block = ""
        config = {"followUpPrompt": ""}
    else:
        follow_up_prompt = require_text(follow_up_prompt, "follow_up_prompt")
        submit_block = (
            '  <div class="viz-controls">\n'
            f'    <button class="btn btn-primary" id="{root_id}-submit" type="button">继续</button>\n'
            "  </div>"
        )
        config = {"followUpPrompt": follow_up_prompt}

    replacements = {
        "{{ROOT_ID}}": root_id,
        "{{QUESTION}}": html.escape(question),
        "{{OPTIONS_HTML}}": "\n".join(option_lines),
        "{{SUBMIT_BLOCK}}": submit_block,
        "{{CONFIG_JSON}}": safe_json(config),
    }

    fragment = TEMPLATE_PATHS[variant].read_text(encoding="utf-8")
    for token, replacement in replacements.items():
        fragment = fragment.replace(token, replacement)
    if "{{" in fragment or "}}" in fragment:
        raise ValueError("unresolved template token remains")
    return fragment


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a quick multi-select visualization")
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
