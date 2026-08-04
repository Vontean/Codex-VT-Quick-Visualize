#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import re
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = SKILL_DIR / "assets" / "parameter-form.html"
FIELD_TYPES = {"text", "textarea", "select", "radio", "switch", "checkbox", "range"}
NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")


def require_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a non-empty string")
    return value.strip()


def optional_text(value: Any, field: str, default: str = "") -> str:
    if value is None:
        return default
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    return value


def require_number(value: Any, field: str) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{field} must be a finite number")
    return value


def number_text(value: int | float) -> str:
    return str(int(value)) if isinstance(value, float) and value.is_integer() else str(value)


def normalize_options(raw_options: Any, field: str) -> list[dict[str, str]]:
    if not isinstance(raw_options, list) or not 2 <= len(raw_options) <= 8:
        raise ValueError(f"{field} must contain 2-8 options")

    options: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, raw in enumerate(raw_options):
        if isinstance(raw, str):
            label = value = require_text(raw, f"{field}[{index}]")
        elif isinstance(raw, dict):
            label = require_text(raw.get("label"), f"{field}[{index}].label")
            value = require_text(raw.get("value", label), f"{field}[{index}].value")
        else:
            raise ValueError(f"{field}[{index}] must be a string or object")
        if value in seen:
            raise ValueError(f"duplicate option value in {field}: {value}")
        seen.add(value)
        options.append({"label": label, "value": value})
    return options


def normalize_fields(spec: dict[str, Any]) -> list[dict[str, Any]]:
    raw_fields = spec.get("fields")
    if not isinstance(raw_fields, list) or not 1 <= len(raw_fields) <= 12:
        raise ValueError("fields must be a list containing 1-12 entries")

    fields: list[dict[str, Any]] = []
    seen_names: set[str] = set()
    for index, raw in enumerate(raw_fields):
        if not isinstance(raw, dict):
            raise ValueError(f"fields[{index}] must be an object")
        field_type = require_text(raw.get("type"), f"fields[{index}].type")
        if field_type not in FIELD_TYPES:
            raise ValueError(f"fields[{index}].type must be one of {sorted(FIELD_TYPES)}")
        name = require_text(raw.get("name"), f"fields[{index}].name")
        if not NAME_PATTERN.fullmatch(name):
            raise ValueError(f"fields[{index}].name must match {NAME_PATTERN.pattern}")
        if name in seen_names:
            raise ValueError(f"duplicate field name: {name}")
        seen_names.add(name)

        field: dict[str, Any] = {
            "type": field_type,
            "name": name,
            "label": require_text(raw.get("label"), f"fields[{index}].label"),
            "required": bool(raw.get("required", False)),
        }

        if field_type in {"text", "textarea"}:
            field["value"] = optional_text(raw.get("value"), f"fields[{index}].value")
            field["placeholder"] = optional_text(
                raw.get("placeholder"), f"fields[{index}].placeholder"
            )
        elif field_type in {"select", "radio"}:
            field["options"] = normalize_options(raw.get("options"), f"fields[{index}].options")
            default_value = field["options"][0]["value"]
            field["value"] = require_text(raw.get("value", default_value), f"fields[{index}].value")
            if field["value"] not in {option["value"] for option in field["options"]}:
                raise ValueError(f"fields[{index}].value must match an option value")
        elif field_type in {"switch", "checkbox"}:
            field["checked"] = bool(raw.get("checked", False))
            default_control_label = "开启" if field_type == "switch" else "包含"
            field["control_label"] = require_text(
                raw.get("control_label", default_control_label),
                f"fields[{index}].control_label",
            )
        else:
            minimum = require_number(raw.get("min", 0), f"fields[{index}].min")
            maximum = require_number(raw.get("max", 100), f"fields[{index}].max")
            step = require_number(raw.get("step", 1), f"fields[{index}].step")
            value = require_number(raw.get("value", minimum), f"fields[{index}].value")
            if maximum <= minimum or step <= 0 or not minimum <= value <= maximum:
                raise ValueError(f"fields[{index}] has an invalid range")
            field.update(
                {
                    "min": minimum,
                    "max": maximum,
                    "step": step,
                    "value": value,
                    "unit": optional_text(raw.get("unit"), f"fields[{index}].unit"),
                }
            )
        fields.append(field)
    return fields


def safe_json(value: Any) -> str:
    return (
        json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )


def render_field(root_id: str, field: dict[str, Any], index: int) -> str:
    field_id = f"{root_id}-field-{index + 1}"
    label = html.escape(field["label"])
    name = html.escape(field["name"], quote=True)
    required = " required" if field["required"] else ""
    field_type = field["type"]

    if field_type == "text":
        return "\n".join(
            (
                '        <div class="quick-parameter-row">',
                f'          <label class="form-label quick-parameter-label" for="{field_id}">{label}</label>',
                f'          <input class="form-control quick-parameter-control" id="{field_id}" name="{name}" type="text" value="{html.escape(field["value"], quote=True)}" placeholder="{html.escape(field["placeholder"], quote=True)}"{required}>',
                "        </div>",
            )
        )

    if field_type == "textarea":
        return "\n".join(
            (
                '        <div class="quick-parameter-row">',
                f'          <label class="form-label quick-parameter-label" for="{field_id}">{label}</label>',
                f'          <textarea class="form-control quick-parameter-control" id="{field_id}" name="{name}" rows="3" placeholder="{html.escape(field["placeholder"], quote=True)}"{required}>{html.escape(field["value"])}</textarea>',
                "        </div>",
            )
        )

    if field_type == "select":
        options = []
        for option in field["options"]:
            selected = " selected" if option["value"] == field["value"] else ""
            options.append(
                f'            <option value="{html.escape(option["value"], quote=True)}" data-label="{html.escape(option["label"], quote=True)}"{selected}>{html.escape(option["label"])}</option>'
            )
        return "\n".join(
            (
                '        <div class="quick-parameter-row">',
                f'          <label class="form-label quick-parameter-label" for="{field_id}">{label}</label>',
                f'          <select class="form-select quick-parameter-control" id="{field_id}" name="{name}"{required}>',
                *options,
                "          </select>",
                "        </div>",
            )
        )

    if field_type == "radio":
        options = []
        for option_index, option in enumerate(field["options"]):
            option_id = f"{field_id}-option-{option_index + 1}"
            checked = " checked" if option["value"] == field["value"] else ""
            options.extend(
                (
                    '            <span class="form-check">',
                    f'              <input class="form-check-input" id="{option_id}" name="{name}" type="radio" value="{html.escape(option["value"], quote=True)}" data-label="{html.escape(option["label"], quote=True)}"{checked}{required}>',
                    f'              <label class="form-check-label" for="{option_id}">{html.escape(option["label"])}</label>',
                    "            </span>",
                )
            )
        return "\n".join(
            (
                '        <fieldset class="quick-parameter-row">',
                f'          <legend class="form-label quick-parameter-label">{label}</legend>',
                '          <div class="viz-row quick-parameter-control">',
                *options,
                "          </div>",
                "        </fieldset>",
            )
        )

    if field_type in {"switch", "checkbox"}:
        checked = " checked" if field["checked"] else ""
        switch_class = " form-switch" if field_type == "switch" else ""
        return "\n".join(
            (
                '        <div class="quick-parameter-row">',
                f'          <span class="form-label quick-parameter-label">{label}</span>',
                f'          <label class="form-check{switch_class} quick-parameter-control" for="{field_id}">',
                f'            <input class="form-check-input" id="{field_id}" name="{name}" type="checkbox"{checked}{required}>',
                f'            <span class="form-check-label">{html.escape(field["control_label"])}</span>',
                "          </label>",
                "        </div>",
            )
        )

    unit = html.escape(field["unit"], quote=True)
    value = number_text(field["value"])
    return "\n".join(
        (
            '        <div class="quick-parameter-row">',
            f'          <label class="form-label quick-parameter-label" for="{field_id}">{label}</label>',
            '          <div class="quick-parameter-range quick-parameter-control">',
            f'            <output id="{field_id}-output" for="{field_id}">{html.escape(value + field["unit"])}</output>',
            f'            <input class="form-range" id="{field_id}" name="{name}" type="range" min="{number_text(field["min"])}" max="{number_text(field["max"])}" step="{number_text(field["step"])}" value="{value}" data-unit="{unit}">',
            "          </div>",
            "        </div>",
        )
    )


def render(spec: dict[str, Any], output_path: Path) -> str:
    question = require_text(spec.get("question"), "question")
    follow_up_prompt = require_text(spec.get("follow_up_prompt"), "follow_up_prompt")
    if "{parameters}" not in follow_up_prompt:
        raise ValueError("follow_up_prompt must contain {parameters}")
    fields = normalize_fields(spec)
    digest_source = json.dumps(spec, ensure_ascii=False, sort_keys=True) + str(output_path)
    root_id = "quick-parameter-form-" + hashlib.sha256(digest_source.encode()).hexdigest()[:10]

    config_fields = [
        {
            "name": field["name"],
            "label": field["label"],
            "type": field["type"],
            "unit": field.get("unit", ""),
        }
        for field in fields
    ]
    replacements = {
        "{{ROOT_ID}}": root_id,
        "{{QUESTION}}": html.escape(question, quote=True),
        "{{FIELDS_HTML}}": "\n".join(
            render_field(root_id, field, index) for index, field in enumerate(fields)
        ),
        "{{CONFIG_JSON}}": safe_json(
            {"followUpPrompt": follow_up_prompt, "fields": config_fields}
        ),
    }

    fragment = TEMPLATE_PATH.read_text(encoding="utf-8")
    for token, replacement in replacements.items():
        fragment = fragment.replace(token, replacement)
    if "{{" in fragment or "}}" in fragment:
        raise ValueError("unresolved template token remains")
    return fragment


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a quick parameter form visualization")
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
