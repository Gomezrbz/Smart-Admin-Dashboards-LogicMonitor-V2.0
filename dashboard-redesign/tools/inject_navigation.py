#!/usr/bin/env python3
"""Inject approved navigation HTML into final redesign dashboard JSON files.

Source of truth: navigation/html/*.html
Updates individual dashboard JSON and the Connected Experience group export.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NAV_HTML = ROOT / "navigation" / "html"
OUT = ROOT / "dashboard-redesign" / "dashboards"

# Dashboard ID -> (relative JSON path under dashboards/, html filename)
DASHBOARD_MAP = {
    "00": ("executive/00_Home_Introductory_redesign_v2.json", "00-home-introductory.html"),
    "10": ("executive/10_Executive_Command_Center_redesign_v2.json", "10-executive-command-center.html"),
    "11": ("executive/11_Platform_Value_Overview_redesign_v2.json", "11-platform-value-overview.html"),
    "12": ("executive/12_Environment_Health_Executive_redesign_v2.json", "12-environment-health-executive.html"),
    "13": ("executive/13_Availability_and_Service_Health_redesign_v2.json", "13-availability-service-health.html"),
    "14": ("executive/14_Capacity_and_Risk_Overview_redesign_v2.json", "14-capacity-risk-overview.html"),
    "20": ("operational/20_Operational_Command_Center_redesign_v2.json", "20-operational-command-center.html"),
    "21": ("operational/21_Active_Alerts_redesign_v2.json", "21-active-alerts.html"),
    "22": ("operational/22_Resource_Health_redesign_v2.json", "22-resource-health.html"),
    "23": ("operational/23_Websites_and_Services_redesign_v2.json", "23-websites-services.html"),
    "24": ("operational/24_Coverage_Capacity_Licenses_redesign_v2.json", "24-coverage-capacity-licenses.html"),
    "25": ("operational/25_Access_and_Administration_redesign_v2.json", "25-access-administration.html"),
    "30": ("technical/30_Technical_Resource_Investigation_redesign_v2.json", "30-technical-resource-investigation.html"),
    "31": ("technical/31_Collector_Diagnostics_redesign_v2.json", "31-collector-diagnostics.html"),
    "32": ("technical/32_LogicModule_and_Content_redesign_v2.json", "32-logicmodule-content.html"),
    "33": ("technical/33_Adoption_and_Optimization_redesign_v2.json", "33-adoption-optimization.html"),
    "34": ("technical/34_Technology_Dashboard_Directory_redesign_v2.json", "34-technology-dashboard-directory.html"),
}

NAV_WIDGET_NAMES = {"Suite Navigation Menu"}
NAV_DESC_SNIPPET = "Global navigation across Executive, Operational, and Technical groups."


def load_nav_html(html_file: str) -> str:
    path = NAV_HTML / html_file
    if not path.is_file():
        raise FileNotFoundError(path)
    return path.read_text(encoding="utf-8").strip()


def is_nav_widget(widget: dict) -> bool:
    cfg = widget.get("config") or {}
    if cfg.get("type") != "text":
        return False
    if cfg.get("name") in NAV_WIDGET_NAMES:
        return True
    desc = cfg.get("description") or ""
    return NAV_DESC_SNIPPET in desc


def inject_dashboard(data: dict, html: str) -> int:
    """Replace nav widget content. Returns number of widgets updated."""
    updated = 0
    for w in data.get("widgets") or []:
        if is_nav_widget(w):
            w["config"]["content"] = html
            w["config"]["name"] = "Suite Navigation Menu"
            w["config"]["description"] = NAV_DESC_SNIPPET
            updated += 1
    return updated


def dashboard_id_from_name(name: str) -> str | None:
    m = re.match(r"^(\d{2})\b", name or "")
    return m.group(1) if m else None


def main() -> None:
    results = []
    for did, (rel, html_file) in DASHBOARD_MAP.items():
        path = OUT / rel
        html = load_nav_html(html_file)
        data = json.loads(path.read_text(encoding="utf-8"))
        n = inject_dashboard(data, html)
        if n != 1:
            raise SystemExit(f"{path}: expected 1 nav widget, updated {n}")
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        results.append({"id": did, "file": rel, "html": html_file, "updated": n})
        print(f"Updated {rel} from {html_file}")

    # Sync group export from individual files
    group_path = OUT / "SmartAdmin_Connected_Experience_redesign_v2.json"
    group = json.loads(group_path.read_text(encoding="utf-8"))

    by_id: dict[str, dict] = {}
    for did, (rel, _) in DASHBOARD_MAP.items():
        by_id[did] = json.loads((OUT / rel).read_text(encoding="utf-8"))

    # Root dashboards (Home)
    for i, d in enumerate(group.get("dashboards") or []):
        did = dashboard_id_from_name(d.get("name", ""))
        if did and did in by_id:
            group["dashboards"][i] = by_id[did]

    for sg in group.get("subGroups") or []:
        for i, d in enumerate(sg.get("dashboards") or []):
            did = dashboard_id_from_name(d.get("name", ""))
            if did and did in by_id:
                sg["dashboards"][i] = by_id[did]

    group_path.write_text(json.dumps(group, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Synced group export: {group_path.name}")
    print(f"Done. {len(results)} dashboards updated.")


if __name__ == "__main__":
    main()
