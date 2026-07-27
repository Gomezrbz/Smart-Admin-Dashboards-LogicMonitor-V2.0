#!/usr/bin/env python3
"""Final package verification checklist."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from inject_navigation import DASHBOARD_MAP, is_nav_widget

checks: list[tuple[str, bool, object]] = []

dash = [
    p
    for p in (ROOT / "dashboard-redesign" / "dashboards").rglob("*_redesign_v2.json")
    if "level-" not in p.parts and p.name != "SmartAdmin_Connected_Experience_redesign_v2.json"
]
checks.append(("final_dashboard_count_17", len(dash) == 17, len(dash)))
checks.append(
    (
        "no_client_experience",
        not (ROOT / "SmartAdmin_Client_Experience_Dashboards.json").exists(),
        True,
    )
)
checks.append(("no_new_dashboards", not (ROOT / "New Dashboards").exists(), True))
checks.append(
    (
        "no_level_dirs",
        not any((ROOT / "dashboard-redesign" / "dashboards").glob("level-*")),
        True,
    )
)
for rel in [
    "README.md",
    "CLEANUP_REPORT.md",
    "modules/README.md",
    "validation/navigation-validation.md",
    "validation/dashboard-validation.md",
    "validation/dependency-validation.md",
    "config/lm_export_config.example.json",
]:
    checks.append((f"exists:{rel}", (ROOT / rel).is_file(), True))

bad = []
for did, (rel, _) in DASHBOARD_MAP.items():
    data = json.loads((ROOT / "dashboard-redesign" / "dashboards" / rel).read_text(encoding="utf-8"))
    nav = [w for w in data["widgets"] if is_nav_widget(w)]
    marker = 'class="sa-nav-current"'
    c = (nav[0]["config"]["content"]).count(marker) if nav else -1
    if c != 1:
        bad.append((did, c, len(nav)))
checks.append(("one_CURRENT_each", not bad, bad))

failed = 0
for name, ok, detail in checks:
    print(("OK" if ok else "FAIL"), name, detail if not ok else "")
    if not ok:
        failed += 1
raise SystemExit(failed)
