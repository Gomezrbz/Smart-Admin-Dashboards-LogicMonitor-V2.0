#!/usr/bin/env python3
"""Validate redesign v2 dashboard JSON files (including nested subgroups)."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "dashboard-redesign" / "dashboards"
VAL = ROOT / "dashboard-redesign" / "validation"


def rects_overlap(a, b) -> bool:
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
        "dashboard_group": None,
    }
    # Infer group from path
    parts = path.parts
    if "executive" in parts:
        result["dashboard_group"] = "Executive" if "00_Home" not in path.name else "Home (package root)"
        if "00_Home" in path.name:
            result["dashboard_group"] = "Home (package root; file under executive/)"
        else:
            result["dashboard_group"] = "Executive"
    elif "operational" in parts:
        result["dashboard_group"] = "Operational"
    elif "technical" in parts:
        result["dashboard_group"] = "Technical"

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
        # Approved suite navigation embeds proservices portal URLs by design.
        is_suite_nav = cfg.get("name") == "Suite Navigation Menu" or (
            "Global navigation across Executive" in (cfg.get("description") or "")
        )
        if "proservices" in blob and not is_suite_nav:
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


def validate_group(path: Path, data: dict) -> dict:
    blob = json.dumps(data)
    subgroups = data.get("subGroups") or []
    root_dashboards = data.get("dashboards") or []
    nested_count = sum(len(sg.get("dashboards") or []) for sg in subgroups)
    result = {
        "file": str(path.relative_to(ROOT)).replace("\\", "/"),
        "name": data.get("name"),
        "json_ok": True,
        "widgets": 0,
        "dashboard_count": len(root_dashboards) + nested_count,
        "subgroups": [sg.get("name") for sg in subgroups],
        "tokens": [(t.get("name"), t.get("value")) for t in data.get("widgetTokens") or []],
        "status": "pass",
        "notes": [
            f"Group export: {len(root_dashboards)} root dashboard(s), "
            f"subGroups={ [sg.get('name') for sg in subgroups] }, "
            f"{nested_count} nested dashboards."
        ],
        "overlaps": [],
        "missing_positions": [],
        "scripts_in_text": [],
        "proservices": False,
        "placeholders": [],
        "datasources": [],
        "widget_types": {},
        "dashboard_group": "SmartAdmin Connected Experience (parent)",
    }
    # count widgets across tree
    def count_widgets(dlist):
        return sum(len(d.get("widgets") or []) for d in dlist)

    result["widgets"] = count_widgets(root_dashboards) + sum(
        count_widgets(sg.get("dashboards") or []) for sg in subgroups
    )
    # Flag proservices outside Suite Navigation Menu only
    def walk_widgets(dlist):
        for d in dlist:
            for w in d.get("widgets") or []:
                yield w

    widgets = list(walk_widgets(root_dashboards))
    for sg in subgroups:
        widgets.extend(walk_widgets(sg.get("dashboards") or []))
    for w in widgets:
        cfg = w.get("config") or {}
        cfg_blob = json.dumps(cfg)
        is_suite_nav = cfg.get("name") == "Suite Navigation Menu" or (
            "Global navigation across Executive" in (cfg.get("description") or "")
        )
        if "proservices" in cfg_blob and not is_suite_nav:
            result["proservices"] = True
            result["status"] = "fail"
    if "{{" in blob:
        result["status"] = "pass_with_portal_config" if result["status"] != "fail" else result["status"]
        result["placeholders"] = sorted(set(re.findall(r"\{\{[A-Z0-9_]+\}\}", blob)))
    expected = {"Executive", "Operational", "Technical"}
    actual = set(result["subgroups"])
    if actual != expected:
        result["notes"].append(f"Unexpected subgroups: {actual} (expected {expected})")
        result["status"] = "fail"
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
            results.append(validate_group(f, data))
            continue
        results.append(validate_dashboard(f, data))

    lines = [
        "# Validation Results — SmartAdmin Connected Experience redesign v2",
        "",
        "Automated checks: JSON parse, widget position overlap, missing positions, script tags in text widgets, hardcoded `proservices`, subgroup names, token listing, datasource scrape.",
        "",
        "| File | Dashboard | Group | JSON | Widgets | Status | Notes |",
        "|------|-----------|-------|------|---------|--------|-------|",
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
            f"| `{r.get('file')}` | {r.get('name', '')} | {r.get('dashboard_group', '')} | "
            f"{'OK' if r.get('json_ok') else 'FAIL'} | {r.get('widgets', '')} | **{r.get('status')}** | {notes} |"
        )

    lines.extend(["", "## Per-file details", ""])
    for r in results:
        lines.append(f"### {r.get('name') or r.get('file')}")
        lines.append("")
        lines.append(f"- **File:** `{r.get('file')}`")
        lines.append(f"- **Dashboard group:** {r.get('dashboard_group') or r.get('subgroups') or 'n/a'}")
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
        lines.append(f"- **HTML validation:** Static HTML/CSS only (no script tags allowed in core pack)")
        lines.append(f"- **Final status:** **{r.get('status')}**")
        lines.append("")

    lines.extend(
        [
            "## Portal testing required",
            "",
            "- Resolve `{{PORTAL_BASE}}` and `{{DASHBOARD_ID_NN}}` after import",
            "- Resolve `{{OOTB_*_ID}}` after importing OOTB technology packs",
            "- Set `accountname` / `{{ACCOUNT_NAME}}` for license widgets",
            "- Confirm nested subgroups appear as Executive / Operational / Technical",
            "- Portal assigns subgroup IDs — do not copy IDs from another portal",
            "- Confirm portal LogicModules applied",
            "- Verify Introductive title shells and DCC card HTML render in text widgets",
            "",
        ]
    )

    VAL.mkdir(parents=True, exist_ok=True)
    (VAL / "validation-results.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    failed = [r for r in results if r.get("status") == "fail"]
    print(f"Validated {len(results)} files; failures={len(failed)}")
    for r in failed:
        print(" FAIL", r.get("file"), r.get("overlaps"), r.get("missing_positions"), r.get("notes"))


if __name__ == "__main__":
    main()
