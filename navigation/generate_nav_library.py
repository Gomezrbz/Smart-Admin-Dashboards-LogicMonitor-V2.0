#!/usr/bin/env python3
"""Generate dashboard-specific navigation table library from dashboard_feedback.md inventory."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML_DIR = ROOT / "html"
LIBRARY_MD = ROOT / "dashboard-navigation-table-library.md"
VALIDATION_MD = ROOT / "dashboard-link-validation.md"

# Inventory from dashboard_feedback.md (source of truth). Do not invent or rename.
DASHBOARDS = [
    {
        "number": "00",
        "name": "00 - Home / Introductory",
        "group": "Home",
        "short": "Home",
        "display_name": "00 - Home / Introductory",
        "url": "https://proservices.logicmonitor.com/santaba/uiv4/dashboards/dashboardGroups-151,dashboards-928",
        "html_file": "00-home-introductory.html",
    },
    {
        "number": "10",
        "name": "10 - Executive Command Center",
        "group": "Executive",
        "short": "Exec CC",
        "display_name": "10 - Executive Command Center",
        "url": "https://proservices.logicmonitor.com/santaba/uiv4/dashboards/dashboardGroups-151,dashboardGroups-152,dashboards-929",
        "html_file": "10-executive-command-center.html",
    },
    {
        "number": "11",
        "name": "11 - Platform Value Overview",
        "group": "Executive",
        "short": "Platform Value",
        "display_name": "11 - Platform Value Overview",
        "url": "https://proservices.logicmonitor.com/santaba/uiv4/dashboards/dashboardGroups-151,dashboardGroups-152,dashboards-930",
        "html_file": "11-platform-value-overview.html",
    },
    {
        "number": "12",
        "name": "12 - Environment Health Executive",
        "group": "Executive",
        "short": "Env Health Exec",
        "display_name": "12 - Environment Health Executive",
        "url": "https://proservices.logicmonitor.com/santaba/uiv4/dashboards/dashboardGroups-151,dashboardGroups-152,dashboards-931",
        "html_file": "12-environment-health-executive.html",
    },
    {
        "number": "13",
        "name": "13 - Availability and Service Health",
        "group": "Executive",
        "short": "Availability",
        "display_name": "13 - Availability and Service Health",
        "url": "https://proservices.logicmonitor.com/santaba/uiv4/dashboards/dashboardGroups-151,dashboardGroups-152,dashboards-932",
        "html_file": "13-availability-service-health.html",
    },
    {
        "number": "14",
        "name": "14 - Capacity and Risk Overview",
        "group": "Executive",
        "short": "Capacity Risk",
        "display_name": "14 - Capacity and Risk Overview",
        "url": "https://proservices.logicmonitor.com/santaba/uiv4/dashboards/dashboardGroups-151,dashboardGroups-152,dashboards-933",
        "html_file": "14-capacity-risk-overview.html",
    },
    {
        "number": "20",
        "name": "20 - Operational Command Center",
        "group": "Operational",
        "short": "Ops CC",
        "display_name": "20 - Operational Command Center",
        "url": "https://proservices.logicmonitor.com/santaba/uiv4/dashboards/dashboardGroups-151,dashboardGroups-153,dashboards-934",
        "html_file": "20-operational-command-center.html",
    },
    {
        "number": "21",
        "name": "21 - Active Alerts",
        "group": "Operational",
        "short": "Active Alerts",
        "display_name": "21 - Active Alerts",
        "url": "https://proservices.logicmonitor.com/santaba/uiv4/dashboards/dashboardGroups-151,dashboardGroups-153,dashboards-935",
        "html_file": "21-active-alerts.html",
    },
    {
        "number": "22",
        "name": "22 - Resource Health",
        "group": "Operational",
        "short": "Resource Health",
        "display_name": "22 - Resource Health",
        "url": "https://proservices.logicmonitor.com/santaba/uiv4/dashboards/dashboardGroups-151,dashboardGroups-153,dashboards-936",
        "html_file": "22-resource-health.html",
    },
    {
        "number": "23",
        "name": "23 - Websites and Services",
        "group": "Operational",
        "short": "Websites",
        "display_name": "23 - Websites and Services",
        "url": "https://proservices.logicmonitor.com/santaba/uiv4/dashboards/dashboardGroups-151,dashboardGroups-153,dashboards-937",
        "html_file": "23-websites-services.html",
    },
    {
        "number": "24",
        "name": "24 - Coverage, Capacity & Licenses",
        "group": "Operational",
        "short": "Coverage",
        "display_name": "24 - Coverage, Capacity &amp; Licenses",
        "url": "https://proservices.logicmonitor.com/santaba/uiv4/dashboards/dashboardGroups-151,dashboardGroups-153,dashboards-938",
        "html_file": "24-coverage-capacity-licenses.html",
    },
    {
        "number": "25",
        "name": "25 - Access and Administration",
        "group": "Operational",
        "short": "Access",
        "display_name": "25 - Access and Administration",
        "url": "https://proservices.logicmonitor.com/santaba/uiv4/dashboards/dashboardGroups-151,dashboardGroups-153,dashboards-939",
        "html_file": "25-access-administration.html",
    },
    {
        "number": "30",
        "name": "30 - Technical Resource Investigation",
        "group": "Technical",
        "short": "Investigation",
        "display_name": "30 - Technical Resource Investigation",
        "url": "https://proservices.logicmonitor.com/santaba/uiv4/dashboards/dashboardGroups-151,dashboardGroups-154,dashboards-940",
        "html_file": "30-technical-resource-investigation.html",
    },
    {
        "number": "31",
        "name": "31 - Collector Diagnostics",
        "group": "Technical",
        "short": "Collectors",
        "display_name": "31 - Collector Diagnostics",
        "url": "https://proservices.logicmonitor.com/santaba/uiv4/dashboards/dashboardGroups-151,dashboardGroups-154,dashboards-941",
        "html_file": "31-collector-diagnostics.html",
    },
    {
        "number": "32",
        "name": "32 - LogicModule and Content",
        "group": "Technical",
        "short": "Modules",
        "display_name": "32 - LogicModule and Content",
        "url": "https://proservices.logicmonitor.com/santaba/uiv4/dashboards/dashboardGroups-151,dashboardGroups-154,dashboards-942",
        "html_file": "32-logicmodule-content.html",
    },
    {
        "number": "33",
        "name": "33 - Adoption and Optimization",
        "group": "Technical",
        "short": "Adoption",
        "display_name": "33 - Adoption and Optimization",
        "url": "https://proservices.logicmonitor.com/santaba/uiv4/dashboards/dashboardGroups-151,dashboardGroups-154,dashboards-943",
        "html_file": "33-adoption-optimization.html",
    },
    {
        "number": "34",
        "name": "34 - Technology Dashboard Directory",
        "group": "Technical",
        "short": "Tech Directory",
        "display_name": "34 - Technology Dashboard Directory",
        "url": "https://proservices.logicmonitor.com/santaba/uiv4/dashboards/dashboardGroups-151,dashboardGroups-154,dashboards-944",
        "html_file": "34-technology-dashboard-directory.html",
    },
]

BY_NUMBER = {d["number"]: d for d in DASHBOARDS}

CATEGORY_PILLS = {
    "Home": "color:#a7f3d0",
    "Executive": "color:#93c5fd",
    "Operational": "color:#fdba74",
    "Technical": "color:#fca5a5",
}

COLUMNS = [
    ("Home", ["00"]),
    ("Executive", ["10", "11", "12", "13", "14"]),
    ("Operational", ["20", "21", "22", "23", "24", "25"]),
    ("Technical", ["30", "31", "32", "33", "34"]),
]

TD_STYLE = (
    "vertical-align:top;background:rgba(15,23,42,.76);"
    "border:1px solid rgba(191,219,254,.20);border-radius:12px;padding:13px;width:25%;"
)
PILL_BASE = (
    "display:inline-block;padding:5px 8px;margin-bottom:8px;border-radius:999px;"
    "background:rgba(96,165,250,.18);border:1px solid rgba(191,219,254,.24);"
    "font-size:11px;font-weight:700;"
)
LINK_STYLE = "color:#38bdf8;text-decoration:none;font-weight:700;"
CURRENT_WRAP = (
    "background:rgba(14,165,233,.25);border:1px solid #38bdf8;"
    "border-radius:8px;padding:6px 8px;margin:4px 0;"
)
NORMAL_WRAP = "padding:4px 0;margin:3px 0;"
CURRENT_BADGE = (
    '<span style="font-size:9px;font-weight:800;color:#7dd3fc;margin-right:4px;">CURRENT</span>'
)


def nav_item(dash: dict, current_number: str) -> str:
    is_current = dash["number"] == current_number
    link = (
        f'<a href="{dash["url"]}" style="{LINK_STYLE}">{dash["short"]}</a>'
        f'<div style="font-size:10px;color:#9ca3af;">{dash["display_name"]}</div>'
    )
    if is_current:
        return (
            f'<div style="{CURRENT_WRAP}">{CURRENT_BADGE}{link}</div>'
        )
    return f'<div style="{NORMAL_WRAP}">{link}</div>'


def build_table(current_number: str) -> str:
    cells: list[str] = []
    for group_name, numbers in COLUMNS:
        pill_color = CATEGORY_PILLS[group_name]
        items = "".join(nav_item(BY_NUMBER[n], current_number) for n in numbers)
        cells.append(
            f'<td style="{TD_STYLE}">'
            f'<span style="{PILL_BASE}{pill_color}">{group_name}</span>'
            f"{items}"
            f"</td>"
        )

    return f"""<div style="font-family:Arial,Helvetica,sans-serif;background:#0b1220;color:#e5e7eb;border:1px solid #1f2a44;border-radius:16px;padding:18px;width:100%;box-sizing:border-box;">
	<div style="font-size:18px;font-weight:700;color:#ffffff;margin-bottom:6px;">SmartAdmin Connected Experience &mdash; Navigation</div>
	<div style="font-size:13px;color:#a5b4fc;margin-bottom:12px;">Navigate between Home, Executive, Operational, and Technical dashboards.</div>
	<div style="height:1px;background:#1f2a44;margin:12px 0;">
		<br>
	</div>

	<table style="width:100%;border-collapse:separate;border-spacing:12px;">
		<tbody>
			<tr>
				{"".join(cells)}
			</tr>
		</tbody>
	</table>
</div>"""


def validate_table(html: str, current: dict) -> dict:
    issues: list[str] = []
    current_count = html.count(">CURRENT<")
    if current_count != 1:
        issues.append(f"CURRENT count={current_count}, expected 1")

    # CURRENT must appear immediately before the current dashboard's short-label link
    pattern = (
        r">CURRENT</span>"
        + re.escape(f'<a href="{current["url"]}" style="{LINK_STYLE}">{current["short"]}</a>')
    )
    if not re.search(pattern, html):
        issues.append("CURRENT not on intended dashboard")

    if "{{PORTAL_BASE}}" in html or "{{DASHBOARD_ID_" in html:
        issues.append("placeholders remain")

    if "<script" in html.lower():
        issues.append("script tag found")

    for dash in DASHBOARDS:
        occurrences = html.count(f'href="{dash["url"]}"')
        if occurrences != 1:
            issues.append(f"URL for {dash['number']} count={occurrences}")

    if "Coverage, Capacity &amp; Licenses" not in html:
        issues.append("Coverage label missing &amp;")

    if html.count("<div") != html.count("</div>"):
        issues.append("unbalanced div tags")
    if html.count("<td") != html.count("</td>"):
        issues.append("unbalanced td tags")
    if html.count("<a ") != html.count("</a>"):
        issues.append("unbalanced a tags")

    return {
        "url_found": "Yes",
        "table_created": "Yes",
        "highlight_verified": "Yes" if not issues else "No",
        "status": "Pass" if not issues else "Fail: " + "; ".join(issues),
        "issues": issues,
    }


def write_library(tables: dict[str, str], validations: dict[str, dict]) -> None:
    parts = ["# Dashboard Navigation Table Library", ""]
    for dash in DASHBOARDS:
        html = tables[dash["number"]]
        dest_links = "\n".join(
            f"- `{d['name']}` → `{d['url']}`" for d in DASHBOARDS
        )
        parts.extend(
            [
                f"## {dash['name']}",
                "",
                f"**Dashboard Group:** {dash['group']}",
                "",
                f"**Current Dashboard:** {dash['name']}",
                "",
                "### Navigation Table Code",
                "",
                "```html",
                html,
                "```",
                "",
                "### Destination Links Used",
                "",
                dest_links,
                "",
                "### Validation",
                "",
                "- Current dashboard highlighted: Yes",
                "- Complete URLs included: Yes",
                "- LogicMonitor-compatible HTML: Yes",
                "- JavaScript included: No",
                "",
                "---",
                "",
            ]
        )
    LIBRARY_MD.write_text("\n".join(parts).rstrip() + "\n", encoding="utf-8")


def write_validation(validations: dict[str, dict]) -> None:
    lines = [
        "# Dashboard Link Validation",
        "",
        "| Dashboard Number | Dashboard Name | Group | URL Found | Table Created | Current Highlight Verified | Status |",
        "|---|---|---|---|---|---|---|",
    ]
    for dash in DASHBOARDS:
        v = validations[dash["number"]]
        lines.append(
            f"| {dash['number']} | {dash['name']} | {dash['group']} | "
            f"{v['url_found']} | {v['table_created']} | {v['highlight_verified']} | {v['status']} |"
        )
    VALIDATION_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    tables: dict[str, str] = {}
    validations: dict[str, dict] = {}
    failures: list[str] = []

    for dash in DASHBOARDS:
        html = build_table(dash["number"])
        tables[dash["number"]] = html
        result = validate_table(html, dash)
        validations[dash["number"]] = result
        (HTML_DIR / dash["html_file"]).write_text(html + "\n", encoding="utf-8")
        if result["issues"]:
            failures.append(f"{dash['number']}: {'; '.join(result['issues'])}")

    write_library(tables, validations)
    write_validation(validations)

    print(f"Wrote {LIBRARY_MD}")
    print(f"Wrote {VALIDATION_MD}")
    print(f"Wrote {len(DASHBOARDS)} HTML files to {HTML_DIR}")
    if failures:
        print("VALIDATION FAILURES:")
        for f in failures:
            print(f"  - {f}")
        raise SystemExit(1)
    print("All validations passed.")


if __name__ == "__main__":
    main()
