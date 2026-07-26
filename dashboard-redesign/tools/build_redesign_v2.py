#!/usr/bin/env python3
"""Build SmartAdmin Connected Experience redesign v2 dashboard package.

Fresh rebuild from Basement SmartAdmin + Introductive exports.
Writes only under dashboard-redesign/. Does not modify source JSON files.
"""

from __future__ import annotations

import copy
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PKG = ROOT / "dashboard-redesign"
OUT_DIR = PKG / "dashboards"
L1 = OUT_DIR / "level-1-executive"
L2 = OUT_DIR / "level-2-operational"
L3 = OUT_DIR / "level-3-technical"

SA = json.loads((ROOT / "Basement" / "SmartAdmin Dashboards.json").read_text(encoding="utf-8"))
INTRO = json.loads((ROOT / "Basement" / "Introductive_Dashboard.json").read_text(encoding="utf-8"))
BY_NAME = {d["name"]: d for d in SA["dashboards"]}


def index_widgets(dashboard: dict) -> dict[str, list]:
    idx: dict[str, list] = {}
    for w in dashboard.get("widgets", []):
        idx.setdefault(w["config"]["name"], []).append(w)
    return idx


W = {
    "overview": index_widgets(BY_NAME["SmartAdmin High Level Overview"]),
    "alerts": index_widgets(BY_NAME["SmartAdmin Alerts and DataSource Performance"]),
    "users": index_widgets(BY_NAME["SmartAdmin Users Roles and API Tokens"]),
    "groups": index_widgets(BY_NAME["SmartAdmin Device Groups and Websites"]),
    "modules": index_widgets(BY_NAME["SmartAdmin LogicModule Status"]),
    "licenses": index_widgets(BY_NAME["SmartAdmin Cloud/Local - License Counts"]),
    "collector": index_widgets(BY_NAME["Collector Health"]),
    "intro": index_widgets(INTRO),
}

NAV_ITEMS = [
    ("00", "Home", "00 - Home / Introductory"),
    ("01", "Platform Value", "01 - Platform Value Overview"),
    ("02", "Environment", "02 - Environment Health"),
    ("03", "Alerts", "03 - Alert Overview"),
    ("04", "Coverage", "04 - Coverage, Capacity & Licenses"),
    ("05", "Websites", "05 - Websites and Services"),
    ("06", "Admin", "06 - Access and Administration"),
    ("07", "Collectors", "07 - Collector Health"),
    ("08", "Modules", "08 - LogicModule and Content"),
    ("09", "Adoption", "09 - Adoption and Optimization"),
]

PORTAL_TOKENS = [
    {"name": "defaultResource", "value": "*.logicmonitor.com"},
    {"name": "defaultResourceGroup", "value": "*"},
]
COLLECTOR_TOKENS = [
    {"name": "defaultResourceGroup", "value": "*"},
    {"name": "defaultResourceName", "value": "*"},
]
LICENSE_TOKENS = [
    {"name": "accountname", "value": "{{ACCOUNT_NAME}}"},
    {"name": "defaultResourceGroup", "value": "*"},
    {"name": "defaultResource", "value": "*.logicmonitor.com"},
]
WEBSITE_TOKENS = [
    {"name": "defaultResourceGroup", "value": "*"},
    {"name": "defaultResource", "value": "*.logicmonitor.com"},
    {"name": "defaultWebsiteGroup", "value": "*"},
]
MODULE_TOKENS = [
    {"name": "defaultResourceGroup", "value": "*"},
    {"name": "defaultResourceName", "value": "*.logicmonitor.com"},
]
HOME_TOKENS = [
    {"name": "defaultResourceGroup", "value": "*"},
    {"name": "defaultResource", "value": "*.logicmonitor.com"},
]


def take(src: str, name: str, occur: int = 0) -> dict:
    lst = W[src].get(name)
    if not lst:
        raise KeyError(f"Missing widget: {src} / {name}")
    if occur >= len(lst):
        raise KeyError(f"Occurrence {occur} missing: {src} / {name}")
    return copy.deepcopy(lst[occur])


def place(
    widget: dict,
    row: int,
    col: int,
    sizex: int | None = None,
    sizey: int | None = None,
    name: str | None = None,
    description: str | None = None,
) -> dict:
    w = widget
    w["position"] = {
        "row": row,
        "col": col,
        "sizex": sizex if sizex is not None else w["position"].get("sizex", 3),
        "sizey": sizey if sizey is not None else w["position"].get("sizey", 2),
    }
    if name:
        w["config"]["name"] = name
    if description is not None:
        w["config"]["description"] = description
    # Replace hardcoded proservices in license widgets
    cfg_s = json.dumps(w["config"])
    if "proservices" in cfg_s:
        w["config"] = json.loads(cfg_s.replace("proservices", "##accountname##"))
    return w


def text_widget(name: str, content: str, row: int, col: int = 1, sizex: int = 12, sizey: int = 3, description: str = "") -> dict:
    return {
        "position": {"col": col, "sizex": sizex, "row": row, "sizey": sizey},
        "config": {
            "displaySettings": {},
            "isSupportCustomProperty": False,
            "supportCustomProperty": False,
            "name": name,
            "description": description or name,
            "theme": "newSolidDarkBlue",
            "interval": 15,
            "type": "text",
            "timescale": "day",
            "version": 2,
            "content": content,
        },
    }


def global_nav_widget(current_id: str, row: int = 1, sizey: int = 2) -> dict:
    cells = []
    for nid, label, full in NAV_ITEMS:
        is_cur = nid == current_id
        bg = "#0ea5e9" if is_cur else "#020617"
        border = "#38bdf8" if is_cur else "#1f2937"
        color = "#0b1220" if is_cur else "#e5e7eb"
        badge = '<div style="font-size:10px;font-weight:700;letter-spacing:0.04em;margin-bottom:4px;">CURRENT</div>' if is_cur else ""
        href = f"{{{{PORTAL_BASE}}}}/uiv4/dashboard/{{{{DASHBOARD_ID_{nid}}}}}"
        cells.append(
            f'<td style="vertical-align:top;background:{bg};border:1px solid {border};border-radius:10px;padding:8px 10px;">'
            f'{badge}<a href="{href}" style="color:{color};text-decoration:none;font-size:12px;font-weight:700;">{escape(label)}</a>'
            f'<div style="font-size:10px;color:#94a3b8;margin-top:4px;">{escape(full)}</div></td>'
        )
    # two rows of 5
    row1 = "".join(cells[:5])
    row2 = "".join(cells[5:])
    content = f"""<div style="font-family:Arial,Helvetica,sans-serif;background:#0b1220;color:#e5e7eb;border:1px solid #1f2937;border-radius:12px;padding:10px 12px;width:100%;box-sizing:border-box;">
<div style="font-size:13px;font-weight:700;margin-bottom:8px;color:#f8fafc;">SmartAdmin Connected Experience — Navigation</div>
<table style="width:100%;border-collapse:separate;border-spacing:6px;"><tr>{row1}</tr><tr>{row2}</tr></table>
<div style="font-size:11px;color:#94a3b8;margin-top:6px;">After import, replace {{{{PORTAL_BASE}}}} and {{{{DASHBOARD_ID_NN}}}} placeholders. Metrics work even before links are configured.</div>
</div>"""
    return text_widget(
        "Suite Navigation Menu",
        content,
        row=row,
        sizey=sizey,
        description="Global navigation across the Connected Experience suite.",
    )


def guide_widget(
    name: str,
    title: str,
    subtitle: str,
    questions: list[str],
    flow_steps: list[tuple[str, str]],
    next_steps: list[str],
    row: int,
    sizey: int = 5,
) -> dict:
    q_html = "".join(f'<li style="margin:5px 0;">{escape(q)}</li>' for q in questions)
    flow_html = "".join(
        f'<li style="margin:5px 0;"><strong>{escape(s[0])}</strong> — {escape(s[1])}</li>'
        for s in flow_steps
    )
    def _as_text(n) -> str:
        if isinstance(n, (tuple, list)):
            return " — ".join(str(x) for x in n)
        return str(n)

    next_html = "".join(f'<li style="margin:5px 0;">{escape(_as_text(n))}</li>' for n in next_steps)
    content = f"""<div style="font-family:Arial,Helvetica,sans-serif;line-height:1.45;background:#0f172a;color:#e5e7eb;border:1px solid #1f2937;border-radius:14px;padding:16px;width:100%;box-sizing:border-box;">
<div style="font-size:18px;font-weight:700;color:#f9fafb;margin-bottom:4px;">{escape(title)}</div>
<div style="font-size:13px;color:#9ca3af;margin-bottom:12px;">{escape(subtitle)}</div>
<table style="width:100%;border-collapse:separate;border-spacing:10px;"><tr>
<td style="vertical-align:top;background:#020617;border:1px solid #1f2937;border-radius:12px;padding:12px;width:33%;">
<div style="font-size:13px;font-weight:700;margin-bottom:8px;">Questions this dashboard answers</div>
<ul style="margin:0;padding-left:18px;font-size:12px;">{q_html}</ul>
</td>
<td style="vertical-align:top;background:#020617;border:1px solid #1f2937;border-radius:12px;padding:12px;width:34%;">
<div style="font-size:13px;font-weight:700;margin-bottom:8px;">Recommended review flow</div>
<ol style="margin:0;padding-left:18px;font-size:12px;">{flow_html}</ol>
</td>
<td style="vertical-align:top;background:#020617;border:1px solid #1f2937;border-radius:12px;padding:12px;width:33%;">
<div style="font-size:13px;font-weight:700;margin-bottom:8px;">Where to go next</div>
<ul style="margin:0;padding-left:18px;font-size:12px;">{next_html}</ul>
<div style="margin-top:10px;font-size:11px;color:#94a3b8;">Empty / zero: confirm tokens and LogicModules. Healthy zero critical alerts still warrants Warning and dead-resource checks.</div>
</td>
</tr></table>
</div>"""
    return text_widget(name, content, row=row, sizey=sizey, description="Read first guide for this dashboard.")


def section_banner(title: str, row: int, sizey: int = 1) -> dict:
    content = f"""<div style="font-family:Arial,Helvetica,sans-serif;background:#0b1220;color:#f8fafc;border-left:4px solid #38bdf8;padding:8px 14px;border-radius:8px;">
<div style="font-size:15px;font-weight:700;">{escape(title)}</div>
</div>"""
    return text_widget(title, content, row=row, sizey=sizey, description=f"Section: {title}")


def footer_links(items: list[tuple[str, str]], row: int, sizey: int = 2) -> dict:
    lis = "".join(
        f'<li style="margin:4px 0;"><strong>{escape(label)}</strong> — {escape(dest)}</li>'
        for label, dest in items
    )
    content = f"""<div style="font-family:Arial,Helvetica,sans-serif;background:#0b1220;color:#e5e7eb;border:1px solid #1f2937;border-radius:12px;padding:12px;">
<div style="font-size:14px;font-weight:700;margin-bottom:6px;">Where next</div>
<ul style="margin:0;padding-left:18px;font-size:12px;">{lis}</ul>
</div>"""
    return text_widget("Where Next", content, row=row, sizey=sizey, description="Contextual drill-down suggestions.")


def tech_links_panel(row: int, sizey: int = 3) -> dict:
    cats = [
        ("Capacity Management", "Host / storage utilization trends"),
        ("Cloud — AWS / Azure / GCP", "Cloud account and service health"),
        ("Network", "Device and path performance"),
        ("Linux / Microsoft", "OS performance and capacity"),
        ("Storage / Virtualization", "Datastore and hypervisor health"),
        ("Alerting / Websites", "OOTB alert and website packs"),
    ]
    cards = "".join(
        f'<td style="vertical-align:top;background:#020617;border:1px solid #1f2937;border-radius:10px;padding:10px;width:16%;">'
        f'<div style="font-weight:700;font-size:12px;color:#38bdf8;">{escape(t)}</div>'
        f'<div style="font-size:11px;color:#94a3b8;margin-top:4px;">{escape(d)}</div>'
        f'<div style="font-size:10px;color:#64748b;margin-top:6px;">Link: {{{{PORTAL_BASE}}}}/… (configure after OOTB import)</div></td>'
        for t, d in cats
    )
    content = f"""<div style="font-family:Arial,Helvetica,sans-serif;background:#0b1220;color:#e5e7eb;border:1px solid #1f2937;border-radius:12px;padding:12px;">
<div style="font-size:14px;font-weight:700;margin-bottom:8px;">Level-3 technology dashboards (OOTB)</div>
<div style="font-size:12px;color:#94a3b8;margin-bottom:10px;">Import from LogicMonitor Dashboards / github.com/logicmonitor/dashboards, then wire URLs. Not bundled in this portal-admin pack.</div>
<table style="width:100%;border-collapse:separate;border-spacing:8px;"><tr>{cards}</tr></table>
</div>"""
    return text_widget(
        "Technology Drill-Down Links",
        content,
        row=row,
        sizey=sizey,
        description="Placeholders for OOTB Level-3 technology dashboards.",
    )


def make_dashboard(name: str, description: str, tokens: list, widgets: list) -> dict:
    # Ensure no overlapping positions by simple validation later; clear None positions already fixed via place()
    return {
        "santabaRelease": 242,
        "defaultDashboardFilters": {"defaultDashboardFilterDetails": []},
        "widgetTokens": tokens,
        "name": name,
        "description": description,
        "overwriteGroupFields": False,
        "widgetsConfigVersion": 2,
        "type": "dashboard",
        "version": 2,
        "widgets": widgets,
    }


# ---------------------------------------------------------------------------
# Dashboard builders
# ---------------------------------------------------------------------------


def build_00() -> dict:
    cards = [
        ("Executive health", "Leadership", "01 - Platform Value Overview", "Are we healthy? What value is the platform providing?"),
        ("Triage alerts", "NOC / Ops", "03 - Alert Overview", "Which alerts require action now?"),
        ("Environment risk", "Ops", "02 - Environment Health", "Where is risk concentrated?"),
        ("Coverage & licenses", "Admins / FinOps", "04 - Coverage, Capacity & Licenses", "Are there blind spots or license pressure?"),
        ("Access hygiene", "Security", "06 - Access and Administration", "Idle users, tokens, empty roles?"),
        ("Collector pipeline", "Platform engineers", "07 - Collector Health", "Is monitoring data still flowing?"),
    ]
    card_html = "".join(
        f'<td style="vertical-align:top;background:#020617;border:1px solid #1f2937;border-radius:12px;padding:12px;width:16%;">'
        f'<div style="font-size:11px;color:#38bdf8;font-weight:700;">{escape(role)}</div>'
        f'<div style="font-size:14px;font-weight:700;margin:6px 0;">{escape(title)}</div>'
        f'<div style="font-size:11px;color:#94a3b8;">{escape(desc)}</div>'
        f'<div style="font-size:11px;margin-top:8px;color:#e5e7eb;">Open <strong>{escape(dest)}</strong></div></td>'
        for title, role, dest, desc in cards
    )
    welcome = f"""<div style="font-family:Arial,Helvetica,sans-serif;background:linear-gradient(135deg,#0f172a,#1e3a8a);color:#e5e7eb;border-radius:14px;padding:18px;">
<div style="font-size:22px;font-weight:700;color:#f8fafc;">SmartAdmin Connected Experience</div>
<div style="font-size:13px;color:#cbd5e1;margin-top:6px;max-width:900px;">Portal administration and platform-value dashboards for client reviews. Start from this Home page, then drill into operational and technical views. Use dashboard tokens to reuse the package across environments.</div>
</div>"""
    how = """<div style="font-family:Arial,Helvetica,sans-serif;background:#0b1220;color:#e5e7eb;border:1px solid #1f2937;border-radius:12px;padding:14px;">
<div style="font-size:14px;font-weight:700;margin-bottom:8px;">How filters and time ranges work</div>
<ul style="margin:0;padding-left:18px;font-size:12px;line-height:1.5;">
<li><strong>defaultResourceGroup</strong> — scopes resource/alert widgets (default <code>*</code>).</li>
<li><strong>defaultResource</strong> — typically <code>*.logicmonitor.com</code> for portal metrics.</li>
<li><strong>defaultWebsiteGroup</strong> — used on Websites dashboard.</li>
<li><strong>accountname</strong> — set after import for license widgets (replace <code>{{ACCOUNT_NAME}}</code>).</li>
<li>Each widget keeps its own timescale (day, 7days, 3month, etc.).</li>
</ul>
</div>"""
    learn = """<div style="font-family:Arial,Helvetica,sans-serif;background:#0b1220;color:#e5e7eb;border:1px solid #1f2937;border-radius:12px;padding:14px;">
<div style="font-size:14px;font-weight:700;margin-bottom:8px;">Learn &amp; support</div>
<ul style="margin:0;padding-left:18px;font-size:12px;">
<li>LogicMonitor Support documentation (configure portal doc links after import).</li>
<li>OOTB technology dashboards: Capacity, Cloud, Network — see Technology Drill-Down Links.</li>
<li>Users / roles training: see <strong>06 Access and Administration</strong> (corrected content — not collector training).</li>
</ul>
</div>"""
    widgets = [
        global_nav_widget("00", row=1, sizey=3),
        text_widget("Welcome", welcome, row=4, sizey=3, description="Platform value statement and package orientation."),
        text_widget(
            "Role-Based Starting Points",
            f'<div style="font-family:Arial,Helvetica,sans-serif;"><table style="width:100%;border-collapse:separate;border-spacing:8px;"><tr>{card_html}</tr></table></div>',
            row=7,
            sizey=4,
            description="Role-based navigation cards.",
        ),
        section_banner("Environment summary — alerts and collectors", row=11),
        place(take("intro", "Critical Alerts"), 12, 1, 2, 2, name="Critical Alerts Requiring Attention"),
        place(take("intro", "Error Alerts"), 12, 3, 2, 2, name="Error Alerts"),
        place(take("intro", "Warning Alerts"), 12, 5, 2, 2, name="Warning Alerts"),
        place(take("intro", "Total Number of Alerts"), 12, 7, 3, 2, name="Total Active Alerts"),
        place(take("intro", "Dead Resources"), 12, 10, 3, 2, name="Resources Requiring Attention (Dead)"),
        place(take("intro", "Alive Collectors"), 14, 1, 3, 2, name="Alive Collectors"),
        place(take("intro", "Active Users"), 14, 4, 3, 2, name="Active Users"),
        place(take("overview", "Total Number of Dead Resources"), 14, 7, 3, 2, name="Dead Resources (Portal)"),
        place(take("overview", "Local Resource Licenses"), 14, 10, 3, 2, name="Local License Footprint"),
        text_widget("Filters and Time Ranges", how, row=16, sizey=3, col=1, sizex=6),
        text_widget("Learn and Support", learn, row=16, sizey=3, col=7, sizex=6),
        tech_links_panel(row=19, sizey=3),
        footer_links(
            [
                ("Platform Value", "01 — executive KPIs"),
                ("Alert Overview", "03 — triage"),
                ("Environment Health", "02 — map/NOC/dead"),
                ("Adoption", "09 — improvement story"),
            ],
            row=22,
        ),
    ]
    return make_dashboard(
        "00 - Home / Introductory",
        "Primary entry point for SmartAdmin Connected Experience. Role-based starts, environment summary, and suite navigation.",
        HOME_TOKENS,
        widgets,
    )


def build_01() -> dict:
    widgets = [
        global_nav_widget("01", row=1, sizey=3),
        guide_widget(
            "Platform Value Overview — Read First",
            "Platform Value Overview",
            "Executive landing page. Confirm health, coverage, and where to drill.",
            [
                "Are we healthy right now (alert posture)?",
                "Are collectors alive?",
                "What is our monitoring footprint and license mix?",
                "Where should we drill next?",
            ],
            [
                ("Scan severity KPIs", "Critical / Error / Warning"),
                ("Check collectors", "Alive vs down"),
                ("Review map and NOC", "Concentration of risk"),
                ("Drill only when signaled", "Alerts, Coverage, Collectors"),
            ],
            [
                "Elevated alerts → 03 Alert Overview",
                "Dead/minimal resources → 02 Environment Health",
                "License pressure → 04 Coverage",
                "Down collectors → 07 Collector Health",
            ],
            row=4,
            sizey=5,
        ),
        section_banner("Critical status — alert posture", row=9),
        place(take("overview", "Total Ack'd and Unack'd Critical Alerts"), 10, 1, 3, 2, name="Critical Alerts Requiring Attention"),
        place(take("overview", "Total Ack'd and Unack'd Error Alerts"), 10, 4, 3, 2, name="Error Alerts"),
        place(take("overview", "Total Ack'd and Unack'd Warning Alerts"), 10, 7, 3, 2, name="Warning Alerts"),
        place(take("overview", "Total Number of Ack'd and Unack'd Alerts"), 10, 10, 3, 2, name="Total Alerts (Ack and Unack)"),
        section_banner("Platform coverage and collector health", row=12),
        place(take("overview", "Total Number of Alive Collectors"), 13, 1, 3, 2, name="Alive Collectors"),
        place(take("overview", "Total Number of Down Collectors"), 13, 4, 3, 2, name="Down Collectors"),
        place(take("alerts", "Total Number of Resources"), 13, 7, 3, 2, name="Monitored Resources"),
        place(take("alerts", "Total Number of Cloud Resources"), 13, 10, 3, 2, name="Cloud Resources"),
        place(take("overview", "Local Resource Licenses"), 15, 1, 3, 2, name="Local Resource Licenses"),
        place(take("overview", "Cloud Resource Licences"), 15, 4, 3, 2, name="Cloud Resource Licenses"),
        place(take("overview", "LogSources"), 15, 7, 3, 2, name="LogSources Installed"),
        place(take("overview", "Active Users"), 15, 10, 3, 2, name="Active Users"),
        section_banner("Situation awareness", row=17),
        place(take("overview", "Alert Status by Resource Location"), 18, 1, 6, 5, name="Alert Status by Resource Location"),
        place(take("overview", "Alert Status by Resource Types"), 18, 7, 6, 5, name="Alert Status by Resource Types"),
        place(take("overview", "Alert Counts over time"), 23, 1, 6, 4, name="Alert Count Trend"),
        place(take("overview", "Top Dead Resources Over Time"), 23, 7, 6, 4, name="Dead Resources Trend"),
        footer_links(
            [
                ("Environment Health", "02"),
                ("Alert Overview", "03"),
                ("Coverage & Licenses", "04"),
                ("Collector Health", "07"),
                ("Adoption", "09"),
            ],
            row=27,
        ),
    ]
    return make_dashboard(
        "01 - Platform Value Overview",
        "Level-1 executive view: alert posture, collectors, footprint, licenses, map/NOC, and navigation.",
        PORTAL_TOKENS,
        widgets,
    )


def build_02() -> dict:
    widgets = [
        global_nav_widget("02", row=1, sizey=3),
        guide_widget(
            "Environment Health — Read First",
            "Environment Health",
            "Operational view of where risk is concentrated across resources, collectors, and websites.",
            [
                "Where are alerts concentrated geographically or by type?",
                "Which resources are dead or minimally monitored?",
                "Are collectors healthy enough to trust the data?",
                "Are websites failing?",
            ],
            [
                ("Map + NOC", "Find concentration"),
                ("Dead / minimal KPIs", "Blind spots"),
                ("Collector alerts", "Data pipeline"),
                ("Website dead count", "Service checks"),
            ],
            [
                "Active alert triage → 03",
                "Collector diagnostics → 07",
                "Website detail → 05",
                "Coverage / discovery → 04",
            ],
            row=4,
            sizey=5,
        ),
        section_banner("Critical status", row=9),
        place(take("alerts", "Total Number of Critical Alerts"), 10, 1, 3, 2, name="Critical Alerts"),
        place(take("alerts", "Total Number of Dead Resources"), 10, 4, 3, 2, name="Dead Resources"),
        place(take("alerts", "Total Number of Minimal Monitoring Resource"), 10, 7, 3, 2, name="Minimally Monitored Resources"),
        place(take("overview", "Total Number of Dead Websites"), 10, 10, 3, 2, name="Dead Websites"),
        place(take("overview", "Total Number of Alive Collectors"), 12, 1, 3, 2, name="Alive Collectors"),
        place(take("overview", "Total Number of Down Collectors"), 12, 4, 3, 2, name="Down Collectors"),
        place(take("alerts", "Total Number of SDT Resource"), 12, 7, 3, 2, name="Resources in SDT"),
        place(take("alerts", "Total Number of Netflow Resource"), 12, 10, 3, 2, name="Netflow Resources"),
        section_banner("Situation visuals", row=14),
        place(take("overview", "Alert Status by Resource Location"), 15, 1, 6, 5, name="Alert Status by Resource Location"),
        place(take("overview", "Alert Status by Resource Types"), 15, 7, 6, 5, name="Alert Status by Resource Types"),
        section_banner("Trends and collector signals", row=20),
        place(take("alerts", "Top Dead Resources Over Time"), 21, 1, 4, 4, name="Dead Resources Trend"),
        place(take("alerts", "Total Minimal Monitoring Resources over Time"), 21, 5, 4, 4, name="Minimal Monitoring Trend"),
        place(take("overview", "Current Collector Alerts"), 21, 9, 4, 4, name="Current Collector Alerts"),
        place(take("alerts", "Idle Interval"), 25, 1, 12, 4, name="Resources with Idle Interval Risk"),
        footer_links(
            [
                ("Alert Overview", "03"),
                ("Collector Health", "07"),
                ("Websites and Services", "05"),
                ("Coverage", "04"),
            ],
            row=29,
        ),
    ]
    return make_dashboard(
        "02 - Environment Health",
        "Level-2 operational view: map/NOC, dead/minimal resources, collector and website health signals.",
        PORTAL_TOKENS,
        widgets,
    )


def build_03() -> dict:
    widgets = [
        global_nav_widget("03", row=1, sizey=3),
        guide_widget(
            "Alert Overview — Read First",
            "Alert Overview",
            "Operational cockpit for severity, trends, rules, integrations, and LogicModule noise.",
            [
                "What is alerting by severity?",
                "Are rules and escalations healthy?",
                "Which datasources generate the most noise?",
                "Are integrations failing?",
            ],
            [
                ("Severity KPIs", "Critical / Error / Warning / Total"),
                ("Alert list", "Live exceptions"),
                ("Trends + top datasources", "Noise"),
                ("Rules / escalations / integrations", "Routing health"),
                ("90-day module tables", "Content noise"),
            ],
            [
                "Collector-caused gaps → 07",
                "Noisy modules deep dive → 08",
                "Spatial concentration → 02",
            ],
            row=4,
            sizey=5,
        ),
        section_banner("Severity and volume", row=9),
        place(take("alerts", "Total Number of Critical Alerts"), 10, 1, 3, 2, name="Critical Alerts Requiring Attention"),
        place(take("alerts", "Total Number of Error Alerts"), 10, 4, 3, 2, name="Error Alerts"),
        place(take("alerts", "Total Number of Warning Alerts"), 10, 7, 3, 2, name="Warning Alerts"),
        place(take("alerts", "Total Number of Alerts"), 10, 10, 3, 2, name="Total Alerts"),
        place(take("alerts", "Alert Counts over time"), 12, 1, 6, 4, name="Alert Count Trend"),
        place(take("alerts", "Top Datasources by Alerts"), 12, 7, 6, 4, name="Top Datasources by Alert Volume"),
        section_banner("Live exceptions", row=16),
        place(take("overview", "All Resource Alerts"), 17, 1, 8, 5, name="All Resource Alerts"),
        place(take("overview", "Current Collector Alerts"), 17, 9, 4, 5, name="Current Collector Alerts"),
        section_banner("Routing and integrations", row=22),
        place(take("alerts", "Alert Rules"), 23, 1, 4, 4, name="Alert Rules in Use"),
        place(take("alerts", "Escalation Chains inUse by Alert Rules"), 23, 5, 4, 4, name="Escalation Chains in Use"),
        place(take("alerts", "Total Number of Escalation Chains"), 23, 9, 3, 2, name="Escalation Chain Count"),
        place(take("alerts", "Total Number of Portal Integration"), 25, 9, 3, 2, name="Portal Integrations"),
        place(take("alerts", "Number of Integrations with Non 200 Response"), 27, 1, 6, 4, name="Integrations with Non-200 Responses"),
        section_banner("LogicModule alert noise (90 days)", row=31),
        place(take("alerts", "Datasource Alerts in last 90 days"), 32, 1, 6, 4, name="DataSource Alerts Last 90 Days"),
        place(take("alerts", "EventSource Alerts in last 90 days"), 32, 7, 6, 4, name="EventSource Alerts Last 90 Days"),
        place(take("alerts", "ConfigSource Alerts in last 90 days"), 36, 1, 6, 4, name="ConfigSource Alerts Last 90 Days"),
        place(take("alerts", "LogSource Alerts in last 90 days"), 36, 7, 6, 4, name="LogSource Alerts Last 90 Days"),
        footer_links(
            [
                ("Environment Health", "02"),
                ("Collector Health", "07"),
                ("LogicModule and Content", "08"),
                ("Adoption", "09"),
            ],
            row=40,
        ),
    ]
    return make_dashboard(
        "03 - Alert Overview",
        "Level-2 alert cockpit: severity, trends, live alerts, rules, escalations, integrations, and module noise.",
        PORTAL_TOKENS,
        widgets,
    )


def build_04() -> dict:
    widgets = [
        global_nav_widget("04", row=1, sizey=3),
        guide_widget(
            "Coverage Capacity Licenses — Read First",
            "Coverage, Capacity & Licenses",
            "Discovery coverage, license consumption, and group hygiene. Host capacity lives in OOTB Level-3 links.",
            [
                "Are we discovering devices?",
                "Unmonitored or minimal gaps?",
                "Cloud vs local license mix?",
                "Empty groups / dead websites?",
            ],
            [
                ("License strip", "Cloud and local"),
                ("Netscan KPIs + table", "Discovery"),
                ("Unmonitored / netscan trends", "Gaps"),
                ("Group hygiene", "Empty groups"),
                ("OOTB capacity links", "Infra utilization"),
            ],
            [
                "Modules → 08",
                "Websites → 05",
                "Platform Value → 01",
            ],
            row=4,
            sizey=5,
        ),
        section_banner("License consumption", row=9),
        place(take("licenses", "IaaS - Total"), 10, 1, 3, 2, name="IaaS Licenses Total"),
        place(take("licenses", "PaaS - Total"), 10, 4, 3, 2, name="PaaS Licenses Total"),
        place(take("licenses", "Non-Compute - Total"), 10, 7, 3, 2, name="Non-Compute Licenses Total"),
        place(take("licenses", "Local Licenses"), 10, 10, 3, 2, name="Local Licenses"),
        place(take("licenses", "AWS - IaaS"), 12, 1, 2, 2),
        place(take("licenses", "AWS - PaaS"), 12, 3, 2, 2),
        place(take("licenses", "AWS - Non-Compute"), 12, 5, 2, 2),
        place(take("licenses", "Azure - IaaS"), 12, 7, 2, 2),
        place(take("licenses", "Azure - PaaS"), 12, 9, 2, 2),
        place(take("licenses", "Azure - Non-Compute"), 12, 11, 2, 2),
        place(take("licenses", "GCP - IaaS"), 14, 1, 2, 2),
        place(take("licenses", "GCP - PaaS"), 14, 3, 2, 2),
        place(take("licenses", "GCP - Non-Compute"), 14, 5, 2, 2),
        place(take("licenses", "Local Licenses Percents"), 14, 7, 3, 2, name="Local License Percent Used"),
        section_banner("Discovery and coverage gaps", row=16),
        place(take("alerts", "Total Number of Netscans"), 17, 1, 3, 2, name="Netscans Total"),
        place(take("alerts", "Total Number of Netscans - EC2"), 17, 4, 3, 2),
        place(take("alerts", "Total Number of Netscans - Script"), 17, 7, 3, 2),
        place(take("alerts", "Total Number of Netscans - Scheduled"), 17, 10, 3, 2),
        place(take("alerts", "Netscans"), 19, 1, 12, 4, name="Netscan Inventory"),
        place(take("alerts", "Number of Unmonitored Devices Over 90 days"), 23, 1, 6, 4, name="Unmonitored Devices Trend (90 Days)"),
        place(take("alerts", "Number of Netscan Devices Added Per Day Over 90 Days"), 23, 7, 6, 4, name="Netscan Devices Added Per Day"),
        section_banner("Group hygiene", row=27),
        place(take("groups", "Total Number of Device Groups"), 28, 1, 3, 2),
        place(take("groups", "Total Number of Empty Static Groups"), 28, 4, 3, 2, name="Empty Static Device Groups"),
        place(take("groups", "Total Number of Website Groups"), 28, 7, 3, 2),
        place(take("groups", "Total Number of Empty Website Groups"), 28, 10, 3, 2, name="Empty Website Groups"),
        tech_links_panel(row=30, sizey=3),
        footer_links(
            [
                ("LogicModule and Content", "08"),
                ("Websites and Services", "05"),
                ("Platform Value", "01"),
                ("Adoption", "09"),
            ],
            row=33,
        ),
    ]
    return make_dashboard(
        "04 - Coverage, Capacity & Licenses",
        "Level-2 coverage: licenses, netscans, unmonitored trends, group hygiene, and OOTB capacity links.",
        LICENSE_TOKENS,
        widgets,
    )


def build_05() -> dict:
    widgets = [
        global_nav_widget("05", row=1, sizey=3),
        guide_widget(
            "Websites and Services — Read First",
            "Websites and Services",
            "Website and group hygiene for service checks. Deep website performance is via OOTB Website dashboards.",
            [
                "How many websites and website groups exist?",
                "Are there dead websites or empty groups?",
                "How do device groups compare?",
            ],
            [
                ("Website KPIs", "Counts and dead"),
                ("Device group KPIs", "Static/dynamic/empty"),
                ("OOTB Website links", "Performance deep dive"),
            ],
            [
                ("Environment Health", "02"),
                ("Coverage", "04"),
                ("OOTB Websites pack", "configure after import"),
            ],
            row=4,
            sizey=5,
        ),
        section_banner("Website health", row=9),
        place(take("groups", "Total Number of Websites"), 10, 1, 3, 2, name="Websites Monitored"),
        place(take("groups", "Total Number of Dead Website"), 10, 4, 3, 2, name="Dead Websites"),
        place(take("groups", "Total Number of Website Groups"), 10, 7, 3, 2, name="Website Groups"),
        place(take("groups", "Total Number of Empty Website Groups"), 10, 10, 3, 2, name="Empty Website Groups"),
        section_banner("Device group structure", row=12),
        place(take("groups", "Total Number of Device Groups"), 13, 1, 3, 2),
        place(take("groups", "Total Number of Static Device Groups"), 13, 4, 3, 2),
        place(take("groups", "Total Number of Dynamic Device Groups"), 13, 7, 3, 2),
        place(take("groups", "Total Number of Empty Static Groups"), 13, 10, 3, 2, name="Empty Static Device Groups"),
        section_banner("Token reminder", row=15),
        text_widget(
            "Website Token Scope",
            """<div style="font-family:Arial,Helvetica,sans-serif;background:#0b1220;color:#e5e7eb;border:1px solid #1f2937;border-radius:12px;padding:12px;">
<div style="font-size:13px;font-weight:700;margin-bottom:6px;">defaultWebsiteGroup</div>
<div style="font-size:12px;color:#94a3b8;">Set <code>##defaultWebsiteGroup##</code> to scope website views when OOTB website dashboards are linked. Default is <code>*</code>.</div>
</div>""",
            row=16,
            sizey=2,
        ),
        tech_links_panel(row=18, sizey=3),
        footer_links(
            [
                ("Environment Health", "02"),
                ("Coverage", "04"),
                ("Alert Overview", "03"),
            ],
            row=21,
        ),
    ]
    return make_dashboard(
        "05 - Websites and Services",
        "Level-2 websites and group hygiene with defaultWebsiteGroup token for reusable scoping.",
        WEBSITE_TOKENS,
        widgets,
    )


def build_06() -> dict:
    widgets = [
        global_nav_widget("06", row=1, sizey=3),
        guide_widget(
            "Access and Administration — Read First",
            "Access and Administration",
            "Users, roles, groups, and API token hygiene for security and portal administration.",
            [
                "How many active vs idle users/tokens?",
                "Unused roles or empty groups?",
                "API-only sprawl?",
            ],
            [
                ("User KPIs", "Active / API"),
                ("Roles and groups", "Empty / unused"),
                ("Token idle metrics", "90-day hygiene"),
            ],
            [
                ("Adoption", "09 — idle access trends"),
                ("Home", "00"),
            ],
            row=4,
            sizey=5,
        ),
        section_banner("Users and access", row=9),
        place(take("users", "Users"), 10, 1, 3, 2, name="Total Users"),
        place(take("users", "Users with Active Status"), 10, 4, 3, 2, name="Active Users"),
        place(take("users", "API Access Users"), 10, 7, 3, 2, name="Users with API Access"),
        place(take("users", "API Only users"), 10, 10, 3, 2, name="API-Only Users"),
        section_banner("Roles and groups", row=12),
        place(take("users", "User Roles"), 13, 1, 3, 2),
        place(take("users", "Roles with no assigned Users"), 13, 4, 3, 2, name="Roles with No Assigned Users"),
        place(take("users", "User Groups"), 13, 7, 3, 2),
        place(take("users", "Empty User Groups"), 13, 10, 3, 2, name="Empty User Groups"),
        section_banner("Tokens and idle access (90 days)", row=15),
        place(take("users", "API Tokens"), 16, 1, 3, 2),
        place(take("users", "API Token not used in last 90 days"), 16, 4, 3, 2, name="Idle API Tokens (90 Days)"),
        place(take("users", "Users not logged in last 90 days"), 16, 7, 3, 2, name="Idle Users (90 Days)"),
        place(take("users", "API Only Users not logged in last 90 days"), 16, 10, 3, 2, name="Idle API-Only Users (90 Days)"),
        footer_links(
            [
                ("Adoption and Optimization", "09"),
                ("Home", "00"),
                ("Platform Value", "01"),
            ],
            row=18,
        ),
    ]
    return make_dashboard(
        "06 - Access and Administration",
        "Level-2 access governance: users, roles, groups, API tokens, and idle access.",
        PORTAL_TOKENS,
        widgets,
    )


def build_07() -> dict:
    """Single collector dashboard (deduped)."""
    widgets = [
        global_nav_widget("07", row=1, sizey=3),
        guide_widget(
            "Collector Health — Read First",
            "Collector Health",
            "Technical dashboard for collector availability, JVM pressure, and collection/AD task health. Canonical single copy (duplicate removed).",
            [
                "Alive instance method mix?",
                "JVM / CPU / heap pressure?",
                "Slow or failing collection / AD tasks?",
            ],
            [
                ("Instance counts", "Method mix"),
                ("JVM table + trends", "Pressure"),
                ("Task graphs/tables", "Slow / failing"),
                ("Collector alerts", "Exceptions"),
            ],
            [
                ("Environment Health", "02"),
                ("Alert Overview", "03"),
            ],
            row=4,
            sizey=5,
        ),
        section_banner("Instance counts by collection method", row=9),
        place(take("collector", "Selenium Instance Count"), 10, 1, 2, 2),
        place(take("collector", "Batchscript Instance Count"), 10, 3, 2, 2),
        place(take("collector", "DNS Instance Count"), 10, 5, 2, 2),
        place(take("collector", "JMX Instance Count"), 10, 7, 2, 2),
        place(take("collector", "Ping Instance Count"), 10, 9, 2, 2),
        place(take("collector", "Script Instance Count"), 10, 11, 2, 2),
        place(take("collector", "SNMP Instance Count"), 12, 1, 2, 2),
        place(take("collector", "Webpage Instance Count"), 12, 3, 2, 2),
        place(take("collector", "WMI Instance Count"), 12, 5, 2, 2),
        place(take("collector", "Data Collection Instance Counts"), 12, 7, 3, 2),
        place(take("collector", "Total Data Collecting Instance Count"), 12, 10, 3, 2, name="Total Data Collecting Instances"),
        section_banner("Real-time collector stats", row=14),
        place(take("collector", "Collector JVM Performance (Real-time)"), 15, 1, 6, 4, name="Collector JVM Performance"),
        place(take("collector", "Collector Alert History"), 15, 7, 6, 4, name="Collector Alert History"),
        place(take("collector", "Top Collectors by Heap Utilization (Trend)"), 19, 1, 6, 4, name="Top Collectors by Heap Utilization"),
        place(take("collector", "Top Collectors by CPU Utilization (Trend)"), 19, 7, 6, 4, name="Top Collectors by CPU Utilization"),
        section_banner("Collection and Active Discovery tasks", row=23),
        place(take("collector", "Top 10 Collection Tasks by Slowest Successful Execution"), 24, 1, 4, 4, name="Slowest Successful Collection Tasks"),
        place(take("collector", "Active DiscoveryTop 10 Tasks by Failure Rate"), 24, 5, 4, 4, name="Active Discovery Tasks by Failure Rate"),
        place(take("collector", "Top Collection Tasks (Real-time)"), 24, 9, 4, 4),
        place(take("collector", "Top Active Discovery Tasks (Real-time)"), 28, 1, 6, 4),
        place(take("collector", "Collector Data Collecting Tasks-Total"), 28, 7, 6, 4, name="Data Collecting Tasks Total"),
        place(take("collector", "Collector Data Collecting Tasks-Unavailable Thread Scheduling"), 32, 1, 6, 4),
        place(take("collector", "Total Instance Counts by Collector"), 32, 7, 6, 4),
        section_banner("Individual collector methods", row=36),
        place(take("collector", "Collector Data Collecting Tasks-script"), 37, 1, 4, 3),
        place(take("collector", "Collector Data Collecting Tasks-batchscript"), 37, 5, 4, 3),
        place(take("collector", "Collector Data Collecting Tasks-WMI"), 37, 9, 4, 3),
        place(take("collector", "Collector Data Collecting Tasks-SNMP"), 40, 1, 4, 3),
        place(take("collector", "Collector Data Collecting Tasks-Ping"), 40, 5, 4, 3),
        place(take("collector", "Collector Data Collecting Tasks-JMX"), 40, 9, 4, 3),
        footer_links(
            [
                ("Environment Health", "02"),
                ("Alert Overview", "03"),
                ("Home", "00"),
            ],
            row=43,
        ),
    ]
    return make_dashboard(
        "07 - Collector Health",
        "Level-3 collector diagnostics (single canonical dashboard; duplicate SmartAdmin Collector Health removed).",
        COLLECTOR_TOKENS,
        widgets,
    )


def build_08() -> dict:
    widgets = [
        global_nav_widget("08", row=1, sizey=3),
        guide_widget(
            "LogicModule and Content — Read First",
            "LogicModule and Content",
            "Content inventory plus noisy modules. Decorative duplicate headers from the source pack were replaced by this guide.",
            [
                "What LogicModules are installed by type?",
                "Which modules alert most over 90 days?",
                "Which datasources have the most instances?",
            ],
            [
                ("Inventory scorecards", "Counts by type"),
                ("90-day alert tables", "Noise"),
                ("Instance count table", "Footprint"),
            ],
            [
                ("Alert Overview", "03"),
                ("Adoption", "09"),
                ("Coverage", "04"),
            ],
            row=4,
            sizey=5,
        ),
        section_banner("LogicModule inventory", row=9),
        place(take("modules", "DataSources"), 10, 1, 3, 2),
        place(take("modules", "EventSources"), 10, 4, 3, 2),
        place(take("modules", "ConfigSources"), 10, 7, 3, 2),
        place(take("modules", "PropertySources"), 10, 10, 3, 2),
        place(take("modules", "LogSources"), 12, 1, 3, 2),
        place(take("modules", "TopologySources"), 12, 4, 3, 2),
        place(take("modules", "SNMP SYSOID Maps"), 12, 7, 3, 2),
        place(take("modules", "AppliesTo Functions"), 12, 10, 3, 2),
        section_banner("Noisy modules and instance footprint", row=14),
        place(take("alerts", "Datasource Alerts in last 90 days"), 15, 1, 6, 4, name="DataSource Alerts Last 90 Days"),
        place(take("alerts", "EventSource Alerts in last 90 days"), 15, 7, 6, 4, name="EventSource Alerts Last 90 Days"),
        place(take("alerts", "ConfigSource Alerts in last 90 days"), 19, 1, 6, 4, name="ConfigSource Alerts Last 90 Days"),
        place(take("alerts", "LogSource Alerts in last 90 days"), 19, 7, 6, 4, name="LogSource Alerts Last 90 Days"),
        place(take("alerts", "Top Datasources by Instance Count"), 23, 1, 12, 4, name="Top Datasources by Instance Count"),
        footer_links(
            [
                ("Alert Overview", "03"),
                ("Adoption", "09"),
                ("Coverage", "04"),
            ],
            row=27,
        ),
    ]
    return make_dashboard(
        "08 - LogicModule and Content",
        "Level-3 content inventory and noisy LogicModules (including LogSources as health signals).",
        MODULE_TOKENS,
        widgets,
    )


def build_09() -> dict:
    widgets = [
        global_nav_widget("09", row=1, sizey=3),
        guide_widget(
            "Adoption and Optimization — Read First",
            "Adoption and Optimization",
            "Packages hygiene metrics as continuous improvement and platform value for CS and leadership.",
            [
                "Is alert noise declining?",
                "Are idle identities cleaned up?",
                "Are coverage gaps closing?",
                "Are integrations healthy?",
            ],
            [
                ("Alert trend + top datasources", "Noise"),
                ("Idle access KPIs", "Identity hygiene"),
                ("Coverage gap trends", "Blind spots"),
                ("Integration failures", "Routing health"),
            ],
            [
                ("Platform Value", "01 — close the loop"),
                ("Alert Overview", "03"),
                ("Access", "06"),
                ("Coverage", "04"),
            ],
            row=4,
            sizey=5,
        ),
        section_banner("Alert noise and improvement signals", row=9),
        place(take("alerts", "Alert Counts over time"), 10, 1, 6, 4, name="Alert Count Trend"),
        place(take("alerts", "Top Datasources by Alerts"), 10, 7, 6, 4, name="Top Noisy Datasources"),
        section_banner("Idle access summary", row=14),
        place(take("users", "Users not logged in last 90 days"), 15, 1, 3, 2, name="Idle Users (90 Days)"),
        place(take("users", "API Token not used in last 90 days"), 15, 4, 3, 2, name="Idle API Tokens (90 Days)"),
        place(take("users", "API Only Users not logged in last 90 days"), 15, 7, 3, 2, name="Idle API-Only Users (90 Days)"),
        place(take("users", "Empty User Groups"), 15, 10, 3, 2, name="Empty User Groups"),
        section_banner("Coverage gaps and integration health", row=17),
        place(take("alerts", "Number of Unmonitored Devices Over 90 days"), 18, 1, 6, 4, name="Unmonitored Devices Trend"),
        place(take("alerts", "Total Minimal Monitoring Resources over Time"), 18, 7, 6, 4, name="Minimal Monitoring Trend"),
        place(take("alerts", "Number of Integrations with Non 200 Response"), 22, 1, 6, 4, name="Integration Non-200 Trend"),
        place(take("alerts", "Top Dead Resources Over Time"), 22, 7, 6, 4, name="Dead Resources Trend"),
        text_widget(
            "LM Logs Adoption Note",
            """<div style="font-family:Arial,Helvetica,sans-serif;background:#0b1220;color:#e5e7eb;border:1px solid #1f2937;border-radius:12px;padding:12px;">
<div style="font-size:13px;font-weight:700;margin-bottom:6px;">LM Logs (optional)</div>
<div style="font-size:12px;color:#94a3b8;">Raw log streams are intentionally excluded from this overview. LogSources inventory and LogSource alert tables appear on Modules / Alerts as health signals. Add a dedicated Logs strip only after LM Logs licensing and metrics are confirmed in the portal.</div>
</div>""",
            row=26,
            sizey=2,
        ),
        footer_links(
            [
                ("Platform Value Overview", "01"),
                ("Alert Overview", "03"),
                ("Access and Administration", "06"),
                ("Coverage", "04"),
            ],
            row=28,
        ),
    ]
    return make_dashboard(
        "09 - Adoption and Optimization",
        "Level-3 / value view: noise, idle access, coverage gaps, and integration health as improvement signals.",
        PORTAL_TOKENS,
        widgets,
    )


DASHBOARD_SPECS = [
    ("00_Home_Introductory_redesign_v2.json", L1, build_00),
    ("01_Platform_Value_Overview_redesign_v2.json", L1, build_01),
    ("02_Environment_Health_redesign_v2.json", L2, build_02),
    ("03_Alert_Overview_redesign_v2.json", L2, build_03),
    ("04_Coverage_Capacity_Licenses_redesign_v2.json", L2, build_04),
    ("05_Websites_and_Services_redesign_v2.json", L2, build_05),
    ("06_Access_and_Administration_redesign_v2.json", L2, build_06),
    ("07_Collector_Health_redesign_v2.json", L3, build_07),
    ("08_LogicModule_and_Content_redesign_v2.json", L3, build_08),
    ("09_Adoption_and_Optimization_redesign_v2.json", L3, build_09),
]


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    dashboards = []
    for filename, folder, builder in DASHBOARD_SPECS:
        dash = builder()
        write_json(folder / filename, dash)
        dashboards.append(dash)
        print(f"Wrote {folder.name}/{filename} ({len(dash['widgets'])} widgets)")

    group = {
        "santabaRelease": 242,
        "widgetTokens": [
            {"name": "defaultResourceGroup", "value": "*"},
            {"name": "defaultResource", "value": "*.logicmonitor.com"},
            {"name": "defaultWebsiteGroup", "value": "*"},
            {"name": "accountname", "value": "{{ACCOUNT_NAME}}"},
        ],
        "name": "SmartAdmin Connected Experience",
        "description": (
            "Connected SmartAdmin redesign v2: Home → Platform Value → operational → technical. "
            "Import this group, then configure portal URL/dashboard ID placeholders and accountname."
        ),
        "type": "dashboardgroup",
        "dashboards": dashboards,
        "subGroups": [],
        "version": 2,
    }
    group_path = OUT_DIR / "SmartAdmin_Connected_Experience_redesign_v2.json"
    write_json(group_path, group)
    print(f"Wrote group {group_path} with {len(dashboards)} dashboards")


if __name__ == "__main__":
    main()
