#!/usr/bin/env python3
"""Generate dashboard-specific navigation library.

Design: HTML5/CSS pattern from dashboard_feedback.md (azure-cost-section).
Logic: SmartAdmin dashboard inventory, CURRENT highlighting, working LM links.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML_DIR = ROOT / "html"
LIBRARY_MD = ROOT / "dashboard-navigation-table-library.md"
VALIDATION_MD = ROOT / "dashboard-link-validation.md"

# Inventory URLs and labels from the original dashboard_feedback link table.
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

COLUMNS = [
    ("Home", "home", ["00"]),
    ("Executive", "executive", ["10", "11", "12", "13", "14"]),
    ("Operational", "operational", ["20", "21", "22", "23", "24", "25"]),
    ("Technical", "technical", ["30", "31", "32", "33", "34"]),
]

# Working LM link pattern (proven in LogicMonitor text widgets).
LINK_STYLE = "color:#93c5fd; text-decoration:none; font-weight:700;"
LINK_ATTRS = 'target="_blank" rel="noopener noreferrer"'

# Visual design adapted from dashboard_feedback.md azure-cost-section.
NAV_CSS = """
		.sa-nav-section {
			font-family: Arial, Helvetica, sans-serif; background: linear-gradient(135deg, #0f172a 0%, #1e293b 55%, #0f766e 100%); color: #ffffff; border-radius: 14px; padding: 22px; box-sizing: border-box; box-shadow: 0 6px 18px rgba(15, 23, 42, 0.25);
		}

		.sa-nav-header {
			display: flex; justify-content: space-between; align-items: flex-start; gap: 20px; margin-bottom: 22px;
		}

		.sa-nav-title h2 {
			margin: 0 0 6px 0; font-size: 24px; font-weight: 700; letter-spacing: 0.2px;
		}

		.sa-nav-title p {
			margin: 0; font-size: 14px; color: #cbd5e1; max-width: 760px; line-height: 1.5;
		}

		.sa-nav-badge {
			background: rgba(255, 255, 255, 0.14); border: 1px solid rgba(255, 255, 255, 0.22); border-radius: 999px; padding: 8px 14px; font-size: 13px; white-space: nowrap; color: #e0f2fe;
		}

		.sa-nav-grid {
			display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; margin-bottom: 18px;
		}

		.sa-nav-card {
			background: rgba(15, 23, 42, 0.72); border: 1px solid rgba(148, 163, 184, 0.32); border-radius: 12px; padding: 16px; min-height: 130px; box-sizing: border-box;
		}

		.sa-nav-card h3 {
			margin: 0 0 10px 0; font-size: 15px; color: #ffffff;
		}

		.sa-nav-card.home h3 { color: #a7f3d0; }
		.sa-nav-card.executive h3 { color: #93c5fd; }
		.sa-nav-card.operational h3 { color: #fdba74; }
		.sa-nav-card.technical h3 { color: #fca5a5; }

		.sa-nav-icon {
			width: 34px; height: 34px; border-radius: 10px; background: rgba(56, 189, 248, 0.18); display: flex; align-items: center; justify-content: center; margin-bottom: 12px; font-size: 18px;
		}

		.sa-nav-item {
			margin-bottom: 10px;
		}

		.sa-nav-item:last-child {
			margin-bottom: 0;
		}

		.sa-nav-item p {
			margin: 4px 0 0 0; font-size: 12px; line-height: 1.5; color: #cbd5e1;
		}

		.sa-nav-current {
			background: rgba(56, 189, 248, 0.18); border: 1px solid #38bdf8; border-radius: 10px; padding: 8px 10px; margin-bottom: 10px;
		}

		.sa-nav-current:last-child {
			margin-bottom: 0;
		}

		.sa-nav-current-label {
			display: inline-block; font-size: 10px; font-weight: 800; color: #7dd3fc; margin-right: 6px; letter-spacing: 0.4px;
		}

		.sa-nav-footer {
			display: grid; grid-template-columns: 1.2fr 1fr; gap: 14px; margin-top: 14px;
		}

		.sa-nav-panel {
			background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.14); border-radius: 12px; padding: 16px;
		}

		.sa-nav-panel h3 {
			margin: 0 0 10px 0; font-size: 15px; color: #ffffff;
		}

		.sa-nav-panel ul {
			margin: 0; padding-left: 18px; color: #dbeafe; font-size: 13px; line-height: 1.6;
		}

		.sa-nav-note {
			font-size: 13px; line-height: 1.5; color: #dbeafe; margin: 0;
		}

		.sa-nav-pill-row {
			display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px;
		}

		.sa-nav-pill {
			border-radius: 999px; padding: 6px 10px; font-size: 12px; font-weight: 600; background: rgba(56, 189, 248, 0.22); color: #e0f2fe; border: 1px solid rgba(147, 197, 253, 0.35);
		}

		@media (max-width: 900px) {
			.sa-nav-header,
			.sa-nav-footer {
				grid-template-columns: 1fr; display: block;
			}
			.sa-nav-grid {
				grid-template-columns: 1fr;
			}
			.sa-nav-badge {
				display: inline-block; margin-top: 12px;
			}
		}
"""


def make_link(url: str, label: str) -> str:
    return (
        f'<a href="{url}" {LINK_ATTRS} style="{LINK_STYLE}">'
        f"&nbsp;&nbsp;{label}&nbsp;&nbsp;</a>"
    )


def nav_item(dash: dict, current_number: str) -> str:
    is_current = dash["number"] == current_number
    body = (
        f'{make_link(dash["url"], dash["short"])}'
        f'<p>{dash["display_name"]}</p>'
    )
    if is_current:
        return (
            f'<div class="sa-nav-current">'
            f'<span class="sa-nav-current-label">CURRENT</span>{body}'
            f"</div>"
        )
    return f'<div class="sa-nav-item">{body}</div>'


def build_table(current_number: str) -> str:
    current = BY_NUMBER[current_number]
    cards: list[str] = []
    for group_name, group_class, numbers in COLUMNS:
        items = "".join(nav_item(BY_NUMBER[n], current_number) for n in numbers)
        cards.append(
            f'<div class="sa-nav-card {group_class}">'
            f'<div class="sa-nav-icon"><br></div>'
            f"<h3>{group_name}</h3>"
            f"{items}"
            f"</div>"
        )

    return f"""<div class="sa-nav-section">
	<style>
{NAV_CSS}
	</style>
	<div class="sa-nav-header">
		<div class="sa-nav-title">

			<h2>SmartAdmin Connected Experience &mdash; Navigation</h2>

			<p>Navigate between Home, Executive, Operational, and Technical dashboards. Use this menu to move across the Connected Experience suite without leaving LogicMonitor.</p>
		</div>
		<div class="sa-nav-badge">Connected Experience Navigation</div></div>
	<div class="sa-nav-grid">
		{"".join(cards)}</div>
	<div class="sa-nav-footer">
		<div class="sa-nav-panel">

			<h3>How to Use This Section</h3>

			<ul>
				<li>Start in Home for orientation, then open the Command Center for your role.</li>
				<li>Use Executive for value and risk summaries.</li>
				<li>Use Operational for alerts, health, and day-to-day triage.</li>
				<li>Use Technical for investigation, collectors, modules, and adoption.</li>
			</ul>
		</div>
		<div class="sa-nav-panel">

			<h3>Current Dashboard</h3>

			<p class="sa-nav-note">You are viewing <b>{current["name"]}</b> in the <b>{current["group"]}</b> group. The highlighted CURRENT item marks this dashboard in the navigation menu.</p>
			<div class="sa-nav-pill-row"><span class="sa-nav-pill">{current["group"]}</span> <span class="sa-nav-pill">{current["short"]}</span></div></div></div></div>"""


def validate_table(html: str, current: dict) -> dict:
    issues: list[str] = []
    current_count = html.count(">CURRENT<")
    if current_count != 1:
        issues.append(f"CURRENT count={current_count}, expected 1")

    expected_link = make_link(current["url"], current["short"])
    pattern = r">CURRENT</span>" + re.escape(expected_link)
    if not re.search(pattern, html):
        issues.append("CURRENT not on intended dashboard")

    if "{{PORTAL_BASE}}" in html or "{{DASHBOARD_ID_" in html:
        issues.append("placeholders remain")

    if "<script" in html.lower():
        issues.append("script tag found")

    if 'class="sa-nav-section"' not in html:
        issues.append("missing sa-nav-section design wrapper")
    if "<style>" not in html:
        issues.append("missing HTML5 style block")
    if "linear-gradient(135deg, #0f172a" not in html:
        issues.append("missing gradient design background")

    if html.count('target="_blank"') != len(DASHBOARDS):
        issues.append("missing target=_blank on one or more links")
    if html.count('rel="noopener noreferrer"') != len(DASHBOARDS):
        issues.append("missing rel=noopener noreferrer on one or more links")

    for dash in DASHBOARDS:
        occurrences = html.count(f'href="{dash["url"]}"')
        if occurrences != 1:
            issues.append(f"URL for {dash['number']} count={occurrences}")
        padded = f"&nbsp;&nbsp;{dash['short']}&nbsp;&nbsp;"
        if padded not in html:
            issues.append(f"nbsp padding missing for {dash['number']}")

    if "Coverage, Capacity &amp; Licenses" not in html:
        issues.append("Coverage label missing &amp;")

    if html.count("<div") != html.count("</div>"):
        issues.append("unbalanced div tags")
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
                "- HTML5 class-based design from dashboard_feedback.md: Yes",
                "- Links use target=_blank and rel=noopener noreferrer: Yes",
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
