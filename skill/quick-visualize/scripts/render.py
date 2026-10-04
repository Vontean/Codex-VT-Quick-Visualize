#!/usr/bin/env python3
"""单次调用完成渲染与检查，只向 agent 返回简短结果。"""
from __future__ import annotations
import argparse
import importlib
import json
import os
import sys
import tempfile
from pathlib import Path
from check_fragment import check_fragment

RENDERERS = {
    "multi-select-simple": "render_multi_select",
    "multi-select-complete": "render_multi_select",
    "ranker": "render_ranker",
    "parameter-form": "render_parameter_form",
    "comparison": "render_comparison",
    "line-chart": "render_line_chart",
    "grouped-bar-chart": "render_grouped_bar_chart",
    "donut-chart": "render_donut_chart",
    "radar-chart": "render_radar_chart",
}


def render_checked(kind: str, spec_path: Path, output: Path) -> dict:
    stage = "spec"
    temporary = None
    fragment = None
    template = None
    try:
        output = output.resolve()
        if output.suffix.lower() != ".html":
            raise ValueError("Output must use the .html extension")
        spec = json.loads(spec_path.read_text(encoding="utf-8"))
        if not isinstance(spec, dict):
            raise ValueError("Spec root must be a JSON object")
        if kind.startswith("multi-select-"):
            if spec.get("variant", kind) != kind:
                raise ValueError("Spec variant must match the selected template")
            spec = {**spec, "variant": kind}
        stage = "render"
        renderer = importlib.import_module(RENDERERS[kind])
        template = getattr(renderer, "TEMPLATE_PATH", None)
        if template is None:
            template = getattr(renderer, "TEMPLATE_PATHS", {}).get(kind)
        fragment = renderer.render(spec, output)
        stage = "check"
        checks = check_fragment(fragment)
        stage = "write"
        output.parent.mkdir(parents=True, exist_ok=True)
        # 检查通过后原子替换，失败时不覆盖已有结果。
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=output.parent, suffix=".html", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(fragment)
        os.replace(temporary, output)
        temporary = None
        reference = "\ue200visualize\ue202" + json.dumps({"path": str(output)}, ensure_ascii=False, separators=(",", ":")) + "\ue201"
        return {"ok": True, "path": str(output), "checks": checks, "reference": reference}
    except Exception as error:
        detail = {"message": str(error)}
        line = getattr(error, "line", None) or getattr(error, "lineno", None)
        if line is not None:
            detail["line"] = line
        if stage == "check" and line is not None and fragment is not None:
            lines = fragment.splitlines()
            detail["context"] = [f"{index + 1}: {lines[index][:240]}" for index in range(max(0, line - 2), min(len(lines), line + 1))]
        if stage in {"render", "check"} and isinstance(template, Path):
            detail["template"] = str(template)
        return {"ok": False, "stage": stage, "error": detail}
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render and check a Quick Visualize preset")
    parser.add_argument("type", choices=RENDERERS)
    parser.add_argument("spec", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = render_checked(args.type, args.spec, args.output)
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return 0 if result["ok"] else 1

if __name__ == "__main__":
    sys.exit(main())
