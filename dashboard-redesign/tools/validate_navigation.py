#!/usr/bin/env python3
"""Validate navigation HTML injection across final redesign dashboards."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NAV_HTML = ROOT / "navigation" / "html"
OUT = ROOT / "dashboard-redesign" / "dashboards"
VAL = ROOT / "validation"

from inject_navigation import DASHBOARD_MAP, is_nav_widget, load_nav_html  # noqa: E402


def extract_hrefs(html: str) -> list[str]:
    return re.findall(r'href="([^"]+)"', html)


def count_current(html: str) -> int:
    # Approved nav uses sa-nav-current-label CURRENT and/or CURRENT text
    return len(re.findall(r"sa-nav-current-label|>\s*CURRENT\s*<", html))


def validate_one(did: str, rel: str, html_file: str) -> dict:
    path = OUT / rel
    html_path = NAV_HTML / html_file
    row = {
        "dashboard": did,
        "file": rel.replace("\\", "/"),
        "nav_file_found": html_path.is_file(),
        "nav_updated": False,
        "current_correct": False,
        "links_validated": False,
        "json_valid": False,
        "notes": [],
    }
    if not path.is_file():
        row["notes"].append("dashboard JSON missing")
        return row
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        row["json_valid"] = True
    except json.JSONDecodeError as e:
        row["notes"].append(str(e))
        return row

    nav_widgets = [w for w in (data.get("widgets") or []) if is_nav_widget(w)]
    if len(nav_widgets) != 1:
        row["notes"].append(f"nav widget count={len(nav_widgets)}")
        return row

    content = (nav_widgets[0].get("config") or {}).get("content") or ""
    source = load_nav_html(html_file)
    row["nav_updated"] = content.strip() == source.strip()
    if not row["nav_updated"]:
        row["notes"].append("content does not match navigation HTML source")

    currents = count_current(content)
    # Exactly one CURRENT label block expected
    row["current_correct"] = currents == 1 and f"You are viewing <b>{did}" in content or (
        currents == 1 and f">{did} -" in content
    )
    # More precise: one sa-nav-current block
    current_blocks = content.count('class="sa-nav-current"')
    row["current_correct"] = current_blocks == 1 and currents >= 1

    src_hrefs = extract_hrefs(source)
    content_hrefs = extract_hrefs(content)
    placeholders = [h for h in content_hrefs if "{{" in h]
    row["links_validated"] = (
        content_hrefs == src_hrefs
        and len(src_hrefs) >= 17
        and not placeholders
        and all(h.startswith("https://") for h in content_hrefs)
    )
    if not row["links_validated"]:
        row["notes"].append(
            f"hrefs={len(content_hrefs)} expected={len(src_hrefs)} placeholders={len(placeholders)}"
        )

    name = data.get("name") or ""
    row["name"] = name
    return row


def main() -> None:
    VAL.mkdir(parents=True, exist_ok=True)
    rows = []
    for did, (rel, html_file) in DASHBOARD_MAP.items():
        rows.append(validate_one(did, rel, html_file))

    lines = [
        "# Navigation Validation",
        "",
        "Source of truth: `navigation/html/*.html`. Injected into final redesign dashboards under `dashboard-redesign/dashboards/`.",
        "",
        "| Dashboard | Navigation File Found | Navigation Updated | Current Dashboard Correct | Links Validated | JSON Valid |",
        "| --------- | --------------------- | ------------------ | ------------------------- | --------------- | ---------- |",
    ]
    for r in rows:
        def yn(v: bool) -> str:
            return "Yes" if v else "No"

        lines.append(
            f"| {r['dashboard']} — {r.get('name', '')} | {yn(r['nav_file_found'])} | "
            f"{yn(r['nav_updated'])} | {yn(r['current_correct'])} | "
            f"{yn(r['links_validated'])} | {yn(r['json_valid'])} |"
        )

    failed = [
        r
        for r in rows
        if not all(
            [
                r["nav_file_found"],
                r["nav_updated"],
                r["current_correct"],
                r["links_validated"],
                r["json_valid"],
            ]
        )
    ]
    lines.extend(["", "## Notes", ""])
    if not failed:
        lines.append("All 17 dashboards passed navigation validation.")
    else:
        for r in failed:
            lines.append(f"- **{r['dashboard']}** (`{r['file']}`): {'; '.join(r['notes']) or 'failed checks'}")

    lines.extend(
        [
            "",
            "## Method",
            "",
            "1. Locate the Suite Navigation Menu text widget.",
            "2. Compare widget HTML to the matching file under `navigation/html/`.",
            "3. Confirm exactly one `sa-nav-current` block.",
            "4. Confirm all hrefs match the navigation source (no `{{...}}` placeholders).",
            "5. Confirm JSON parses.",
            "",
            "Portal UI rendering was **not** tested in this pass.",
            "",
        ]
    )
    out = VAL / "navigation-validation.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {out}; failures={len(failed)}")
    for r in failed:
        print(" FAIL", r["dashboard"], r["notes"])


if __name__ == "__main__":
    main()
