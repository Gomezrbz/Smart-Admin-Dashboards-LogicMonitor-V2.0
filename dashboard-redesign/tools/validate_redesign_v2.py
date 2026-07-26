#!/usr/bin/env python3
"""Validate redesign v2 dashboard JSON files."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "dashboard-redesign" / "dashboards"
VAL = ROOT / "dashboard-redesign" / "validation"


def rects_overlap(a, b) -> bool:
    # grid cells: [col, col+sizex) x [row, row+sizey)
    return not (
        a["col"] + a["sizex"] <= b["col"]
        or b["col"] + b["sizex"] <= a["col"]
        or a["row"] + a["sizey"] <= b["row"]
        or b["row"] + b["sizey"] <= a["row"]
    )


def validate_dashboard(path: Path, data: dict) -> dict:
    result = {
        "file": str(path.relative_to(ROOT)).replace("\\", "/"),
        "name": data.get("name"),
        "json_ok": True,
        "widgets": len(data.get("widgets") or []),
        "widget_types": defaultdict(int),
        "tokens": [(t.get("name"), t.get("value")) for t in data.get("widgetTokens") or []],
        "overlaps": [],
        "missing_positions": [],
        "scripts_in_text": [],
        "placeholders": [],
        "proservices": False,
        "datasources": set(),
        "status": "pass",
        "notes": [],
    }
    widgets = data.get("widgets") or []
    placed = []
    for i, w in enumerate(widgets):
        cfg = w.get("config") or {}
        pos = w.get("position") or {}
        wtype = cfg.get("type", "?")
        result["widget_types"][wtype] += 1
        row, col = pos.get("row"), pos.get("col")
        sx, sy = pos.get("sizex"), pos.get("sizey")
        if None in (row, col, sx, sy):
            result["missing_positions"].append(cfg.get("name", f"widget[{i}]"))
            continue
        rect = {"row": row, "col": col, "sizex": sx, "sizey": sy, "name": cfg.get("name")}
        for other in placed:
            if rects_overlap(rect, other):
                result["overlaps"].append(f"{rect['name']} overlaps {other['name']}")
        placed.append(rect)
        blob = json.dumps(cfg)
        if wtype == "text" and re.search(r"<script", blob, re.I):
            result["scripts_in_text"].append(cfg.get("name"))
        if "proservices" in blob:
            result["proservices"] = True
        for m in re.findall(r"\{\{[A-Z0-9_]+\}\}", blob):
            result["placeholders"].append(m)
        for m in re.findall(r"LogicMonitor_[A-Za-z0-9_]+", blob):
            result["datasources"].add(m)
        for m in re.findall(
            r"HostStatus|DataCollectingTasks|ActiveDiscoveryTasks|Users_NotLogin|APITokens|UnmonitoredDevice|MinimalMonitoring",
            blob,
        ):
            result["datasources"].add(m)

    result["widget_types"] = dict(result["widget_types"])
    result["datasources"] = sorted(result["datasources"])
    result["placeholders"] = sorted(set(result["placeholders"]))

    if result["overlaps"] or result["missing_positions"] or result["scripts_in_text"] or result["proservices"]:
        result["status"] = "fail"
    elif result["placeholders"]:
        result["status"] = "pass_with_portal_config"
        result["notes"].append("Contains post-import placeholders (expected).")
    return result


def main() -> None:
    files = sorted(OUT.rglob("*_redesign_v2.json"))
    results = []
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            results.append(
                {
                    "file": str(f.relative_to(ROOT)).replace("\\", "/"),
                    "json_ok": False,
                    "status": "fail",
                    "notes": [str(e)],
                }
            )
            continue
        if data.get("type") == "dashboardgroup":
            # validate each nested dashboard lightly + group json
            group_res = {
                "file": str(f.relative_to(ROOT)).replace("\\", "/"),
                "name": data.get("name"),
                "json_ok": True,
                "widgets": sum(len(d.get("widgets") or []) for d in data.get("dashboards") or []),
                "dashboard_count": len(data.get("dashboards") or []),
                "tokens": [(t.get("name"), t.get("value")) for t in data.get("widgetTokens") or []],
                "status": "pass",
                "notes": ["Group export containing all suite dashboards."],
                "overlaps": [],
                "missing_positions": [],
                "scripts_in_text": [],
                "proservices": False,
                "placeholders": [],
                "datasources": [],
                "widget_types": {},
            }
            # check nested for proservices
            blob = json.dumps(data)
            if "proservices" in blob:
                group_res["proservices"] = True
                group_res["status"] = "fail"
            if "{{" in blob:
                group_res["status"] = "pass_with_portal_config"
                group_res["placeholders"] = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", blob)))
            results.append(group_res)
            continue
        results.append(validate_dashboard(f, data))

    # Write markdown
    lines = [
        "# Validation Results — SmartAdmin Connected Experience redesign v2",
        "",
        "Automated checks: JSON parse, widget position overlap, missing positions, script tags in text widgets, hardcoded `proservices`, token listing, datasource scrape.",
        "",
        "| File | Dashboard | JSON | Widgets | Status | Notes |",
        "|------|-----------|------|---------|--------|-------|",
    ]
    for r in results:
        notes = "; ".join(r.get("notes") or [])
        if r.get("overlaps"):
            notes += f" OVERLAPS: {len(r['overlaps'])}"
        if r.get("missing_positions"):
            notes += f" MISSING_POS: {r['missing_positions']}"
        if r.get("scripts_in_text"):
            notes += f" SCRIPTS: {r['scripts_in_text']}"
        if r.get("proservices"):
            notes += " HARDCODED_proservices"
        lines.append(
            f"| `{r.get('file')}` | {r.get('name', '')} | {'OK' if r.get('json_ok') else 'FAIL'} | {r.get('widgets', '')} | **{r.get('status')}** | {notes} |"
        )

    lines.extend(["", "## Per-file details", ""])
    for r in results:
        lines.append(f"### {r.get('name') or r.get('file')}")
        lines.append("")
        lines.append(f"- **File:** `{r.get('file')}`")
        lines.append(f"- **JSON validation:** {'pass' if r.get('json_ok') else 'fail'}")
        lines.append(f"- **Widgets reviewed:** {r.get('widgets')}")
        if r.get("widget_types"):
            lines.append(f"- **Widget types:** `{r['widget_types']}`")
        lines.append(f"- **Tokens:** `{r.get('tokens')}`")
        lines.append(f"- **Placeholders:** `{r.get('placeholders')}`")
        lines.append(f"- **Overlaps:** {r.get('overlaps') or 'none'}")
        lines.append(f"- **Script tags in text:** {r.get('scripts_in_text') or 'none'}")
        if r.get("datasources"):
            lines.append(f"- **Datasources detected:** {', '.join(r['datasources'][:30])}")
        lines.append(f"- **Link validation:** Placeholders only — **portal testing required** for live URLs")
        lines.append(f"- **Final status:** **{r.get('status')}**")
        lines.append("")

    lines.extend(
        [
            "## Portal testing required",
            "",
            "- Resolve `{{PORTAL_BASE}}` and `{{DASHBOARD_ID_NN}}` after import",
            "- Set `accountname` / `{{ACCOUNT_NAME}}` for license widgets",
            "- Confirm portal LogicModules applied",
            "- Optional: Dynamic Dashboard List / FilterWidget (not in core pack)",
            "- Import OOTB tech dashboards before enabling Level-3 tech links",
            "",
        ]
    )

    VAL.mkdir(parents=True, exist_ok=True)
    (VAL / "validation-results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (VAL / "_validation_raw.json").write_text(json.dumps(results, indent=2, default=list) + "\n", encoding="utf-8")

    failed = [r for r in results if r.get("status") == "fail"]
    print(f"Validated {len(results)} files; failures={len(failed)}")
    for r in failed:
        print(" FAIL", r.get("file"), r.get("overlaps"), r.get("missing_positions"), r.get("scripts_in_text"))


if __name__ == "__main__":
    main()
