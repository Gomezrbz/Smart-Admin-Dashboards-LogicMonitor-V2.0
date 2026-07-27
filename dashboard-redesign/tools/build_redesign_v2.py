#!/usr/bin/env python3
"""Build SmartAdmin Connected Experience redesign v2 dashboard package.

Expands beyond SmartAdmin sources with Introductive + DCC-composed command
centers and technical hubs. Writes only under dashboard-redesign/.
Does not modify source JSON files.
"""

from __future__ import annotations

import copy
import json
import shutil
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PKG = ROOT / "dashboard-redesign"
OUT_DIR = PKG / "dashboards"
EXEC = OUT_DIR / "executive"
OPS = OUT_DIR / "operational"
TECH = OUT_DIR / "technical"

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

# id, short label, full name, group key — sequential within each group
NAV_ITEMS = [
    ("00", "Home", "00 - Home / Introductory", "home"),
    ("10", "Exec CC", "10 - Executive Command Center", "executive"),
    ("11", "Platform Value", "11 - Platform Value Overview", "executive"),
    ("12", "Env Health Exec", "12 - Environment Health Executive", "executive"),
    ("13", "Availability", "13 - Availability and Service Health", "executive"),
    ("14", "Capacity Risk", "14 - Capacity and Risk Overview", "executive"),
    ("20", "Ops CC", "20 - Operational Command Center", "operational"),
    ("21", "Active Alerts", "21 - Active Alerts", "operational"),
    ("22", "Resource Health", "22 - Resource Health", "operational"),
    ("23", "Websites", "23 - Websites and Services", "operational"),
    ("24", "Coverage", "24 - Coverage, Capacity & Licenses", "operational"),
    ("25", "Access", "25 - Access and Administration", "operational"),
    ("30", "Investigation", "30 - Technical Resource Investigation", "technical"),
    ("31", "Collectors", "31 - Collector Diagnostics", "technical"),
    ("32", "Modules", "32 - LogicModule and Content", "technical"),
    ("33", "Adoption", "33 - Adoption and Optimization", "technical"),
    ("34", "Tech Directory", "34 - Technology Dashboard Directory", "technical"),
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
    cfg_s = json.dumps(w["config"])
    if "proservices" in cfg_s:
        w["config"] = json.loads(cfg_s.replace("proservices", "##accountname##"))
    return w


def text_widget(
    name: str,
    content: str,
    row: int,
    col: int = 1,
    sizex: int = 12,
    sizey: int = 3,
    description: str = "",
) -> dict:
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


def href(nid: str) -> str:
    return f"{{{{PORTAL_BASE}}}}/uiv4/dashboard/{{{{DASHBOARD_ID_{nid}}}}}"


def link(nid: str, label: str, color: str = "#38bdf8") -> str:
    return f'<a href="{href(nid)}" style="color:{color};text-decoration:none;font-weight:700;">{escape(label)}</a>'


# ---------------------------------------------------------------------------
# Design-system HTML helpers (Introductive titles + DCC cards/tables)
# ---------------------------------------------------------------------------


# Approved navigation HTML (source of truth): navigation/html/*.html
NAV_HTML_DIR = ROOT / "navigation" / "html"
NAV_HTML_BY_ID = {
    "00": "00-home-introductory.html",
    "10": "10-executive-command-center.html",
    "11": "11-platform-value-overview.html",
    "12": "12-environment-health-executive.html",
    "13": "13-availability-service-health.html",
    "14": "14-capacity-risk-overview.html",
    "20": "20-operational-command-center.html",
    "21": "21-active-alerts.html",
    "22": "22-resource-health.html",
    "23": "23-websites-services.html",
    "24": "24-coverage-capacity-licenses.html",
    "25": "25-access-administration.html",
    "30": "30-technical-resource-investigation.html",
    "31": "31-collector-diagnostics.html",
    "32": "32-logicmodule-content.html",
    "33": "33-adoption-optimization.html",
    "34": "34-technology-dashboard-directory.html",
}


def global_nav_widget(current_id: str, row: int = 1, sizey: int = 4) -> dict:
    """Load approved navigation HTML for the current dashboard."""
    html_name = NAV_HTML_BY_ID.get(current_id)
    if not html_name:
        raise KeyError(f"No navigation HTML mapped for dashboard id {current_id}")
    path = NAV_HTML_DIR / html_name
    if not path.is_file():
        raise FileNotFoundError(f"Missing navigation source: {path}")
    content = path.read_text(encoding="utf-8").strip()
    return text_widget(
        "Suite Navigation Menu",
        content,
        row=row,
        sizey=sizey,
        description="Global navigation across Executive, Operational, and Technical groups.",
    )


def guide_widget(
    name: str,
    title: str,
    subtitle: str,
    questions: list[str],
    flow_steps: list[tuple[str, str]],
    next_steps: list,
    row: int,
    sizey: int = 5,
) -> dict:
    """Introductive educational panel (20px title, inner #020617 cards)."""
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
    content = f"""<div style="font-family:Arial,Helvetica,sans-serif;line-height:1.45;background:#0f172a;color:#e5e7eb;border:1px solid #1f2937;border-radius:14px;padding:18px;width:100%;box-sizing:border-box;">
<div style="margin-bottom:16px;">
<div style="font-size:20px;font-weight:700;color:#f9fafb;">{escape(title)}</div>
<div style="font-size:13px;color:#9ca3af;margin-top:4px;">{escape(subtitle)}</div>
</div>
<table style="width:100%;border-collapse:separate;border-spacing:16px;"><tr>
<td style="vertical-align:top;background:#020617;border:1px solid #1f2937;border-radius:12px;padding:14px;width:33%;">
<div style="font-size:15px;font-weight:700;margin-bottom:10px;color:#f9fafb;">Questions this dashboard answers</div>
<ul style="margin:0;padding-left:18px;font-size:12px;color:#e5e7eb;">{q_html}</ul>
</td>
<td style="vertical-align:top;background:#020617;border:1px solid #1f2937;border-radius:12px;padding:14px;width:34%;">
<div style="font-size:15px;font-weight:700;margin-bottom:10px;color:#f9fafb;">Recommended review flow</div>
<ol style="margin:0;padding-left:18px;font-size:12px;color:#e5e7eb;">{flow_html}</ol>
</td>
<td style="vertical-align:top;background:#020617;border:1px solid #1f2937;border-radius:12px;padding:14px;width:33%;">
<div style="font-size:15px;font-weight:700;margin-bottom:10px;color:#f9fafb;">Where to go next</div>
<ul style="margin:0;padding-left:18px;font-size:12px;color:#e5e7eb;">{next_html}</ul>
<div style="margin-top:14px;font-size:12px;color:#9ca3af;">Tip: Empty or zero values may mean healthy state or missing tokens/LogicModules — confirm before concluding.</div>
</td>
</tr></table>
</div>"""
    return text_widget(name, content, row=row, sizey=sizey, description="Read first guide for this dashboard.")


def section_banner(title: str, row: int, sizey: int = 2) -> dict:
    content = f"""<p>
<style type="text/css">
.html-wpsites {{
height: 72px; background-color: rgba(0, 0, 0, 0); font-family: Arial; font-size: 32px; color: #ffffff; font-weight: bold; text-align: center;
}}
</style>
</p>
<div class="html-wpsites">{escape(title)}</div>
<p>&nbsp;</p>"""
    return text_widget(title, content, row=row, sizey=sizey, description=f"Section: {title}")


def section_banner_major(title: str, row: int, sizey: int = 2) -> dict:
    content = f"""<p><style type="text/css">
.html-wpsites {{ height:112px; background-color:rgba(0,0,0,0); font-family:Arial; font-size:62px; color:#ffffff; font-weight:bold; text-align:center; }}
</style></p>
<div class="html-wpsites">{escape(title)}</div>
<p>&nbsp;</p>"""
    return text_widget(title, content, row=row, sizey=sizey, description=f"Major section: {title}")


def scope_pills(items: list[tuple[str, str]], row: int, sizey: int = 1) -> dict:
    """DCC scope pills. items: (label, css_class_role)."""
    colors = {
        "health": ("rgba(22,163,74,.92)", "#ecfdf5"),
        "alerts": ("rgba(239,68,68,.92)", "#fff7ed"),
        "region": ("rgba(59,130,246,.9)", "#eff6ff"),
        "capacity": ("rgba(250,204,21,.9)", "#422006"),
        "sites": ("rgba(14,165,233,.9)", "#082f49"),
        "sessions": ("rgba(168,85,247,.88)", "#faf5ff"),
    }
    pills = []
    for label, role in items:
        bg, fg = colors.get(role, colors["region"])
        pills.append(
            f'<span style="display:inline-block;border-radius:999px;padding:6px 10px;margin:4px 6px 4px 0;'
            f'font-size:12px;font-weight:700;border:1px solid rgba(255,255,255,.18);background:{bg};color:{fg};">'
            f"{escape(label)}</span>"
        )
    content = f"""<div style="font-family:Arial,Helvetica,sans-serif;padding:4px 0;">{"".join(pills)}</div>"""
    return text_widget("Scope Indicators", content, row=row, sizey=sizey, description="Severity/scope pills.")


def dcc_intro_guide(
    name: str,
    h1: str,
    subtitle: str,
    cards: list[tuple[str, str, str, str]],
    row: int,
    sizey: int = 6,
) -> dict:
    """DCC executive intro card grid. cards: (icon, title, body, action)."""
    card_html = []
    for icon, title, body, action in cards:
        card_html.append(
            f'<td style="vertical-align:top;background:rgba(15,23,42,.76);border:1px solid rgba(148,163,184,.34);'
            f'border-radius:14px;padding:16px;min-height:150px;width:{100 // max(len(cards), 1)}%;">'
            f'<div style="display:inline-block;width:auto;padding:6px 10px;border-radius:11px;'
            f'background:rgba(59,130,246,.22);border:1px solid rgba(255,255,255,.18);'
            f'font-size:11px;font-weight:800;color:#dbeafe;">{escape(icon)}</div>'
            f'<div style="font-size:15px;font-weight:700;color:#ffffff;margin:10px 0 6px;">{escape(title)}</div>'
            f'<div style="font-size:13px;line-height:1.48;color:#cbd5e1;">{body}</div>'
            f'<span style="display:inline-block;margin-top:12px;padding:7px 11px;border-radius:999px;'
            f'background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.18);'
            f'color:#bfdbfe;font-size:12px;font-weight:700;">{escape(action)}</span></td>'
        )
    # wrap in rows of 4
    rows = []
    for i in range(0, len(card_html), 4):
        chunk = card_html[i : i + 4]
        rows.append(f"<tr>{''.join(chunk)}</tr>")
    content = f"""<div style="font-family:Arial,Helvetica,sans-serif;background:linear-gradient(135deg,#0f172a 0%,#111827 45%,#1e3a8a 100%);color:#ffffff;border-radius:16px;padding:22px;box-shadow:0 8px 24px rgba(15,23,42,.32);width:100%;box-sizing:border-box;">
<div style="font-size:28px;font-weight:750;color:#ffffff;margin-bottom:6px;">{escape(h1)}</div>
<div style="font-size:13px;color:#dbeafe;margin-bottom:16px;max-width:960px;">{escape(subtitle)}</div>
<table style="width:100%;border-collapse:separate;border-spacing:14px;">{"".join(rows)}</table>
</div>"""
    return text_widget(name, content, row=row, sizey=sizey, description="DCC-style executive guide.")


def dcc_nav_guide(
    name: str,
    title: str,
    columns: list[tuple[str, str, list[str]]],
    row: int,
    sizey: int = 4,
) -> dict:
    """DCC 4-col nav guide. columns: (pill, heading, bullets)."""
    cells = []
    for pill, heading, bullets in columns:
        lis = "".join(f"<li>{escape(b)}</li>" for b in bullets)
        cells.append(
            f'<td style="vertical-align:top;background:rgba(15,23,42,.72);border:1px solid rgba(191,219,254,.20);'
            f'border-radius:12px;padding:13px;min-height:110px;width:25%;">'
            f'<span style="display:inline-block;padding:5px 8px;margin-bottom:8px;border-radius:999px;'
            f'background:rgba(96,165,250,.18);border:1px solid rgba(191,219,254,.24);'
            f'color:#bfdbfe;font-size:11px;font-weight:700;">{escape(pill)}</span>'
            f'<div style="font-size:14px;font-weight:700;color:#ffffff;margin-bottom:8px;">{escape(heading)}</div>'
            f'<ul style="margin:0;padding-left:16px;color:#cbd5e1;font-size:12px;line-height:1.55;">{lis}</ul></td>'
        )
    content = f"""<div style="font-family:Arial,Helvetica,sans-serif;background:linear-gradient(135deg,#111827 0%,#172554 100%);color:#ffffff;border-radius:14px;padding:18px 20px;width:100%;box-sizing:border-box;">
<div style="font-size:20px;font-weight:700;margin-bottom:12px;">{escape(title)}</div>
<table style="width:100%;border-collapse:separate;border-spacing:12px;"><tr>{"".join(cells)}</tr></table>
</div>"""
    return text_widget(name, content, row=row, sizey=sizey, description="DCC-style navigation guide.")


def dcc_inventory_table(
    name: str,
    title: str,
    subtitle: str,
    rows: list[tuple[str, str, str, str]],
    row: int,
    sizey: int = 4,
) -> dict:
    """Adapted DCC card cells in horizontal rows of 4: (status_pill, title, description, link_label_or_id)."""
    cells = []
    for status, rtitle, desc, link_id in rows:
        if link_id.startswith("http") or link_id.startswith("{{"):
            a = f'<a href="{link_id}" style="color:#93c5fd;text-decoration:none;font-weight:700;">{escape(rtitle)}</a>'
        elif link_id:
            a = link(link_id, rtitle, "#93c5fd")
        else:
            a = f'<span style="color:#ffffff;font-weight:700;">{escape(rtitle)}</span>'
        cells.append(
            f'<td style="vertical-align:top;background:rgba(15,23,42,.76);border:1px solid rgba(148,163,184,.34);'
            f'border-radius:12px;padding:12px 14px;width:25%;">'
            f'<span style="display:inline-block;padding:4px 8px;border-radius:999px;background:rgba(96,165,250,.18);'
            f'border:1px solid rgba(191,219,254,.24);color:#bfdbfe;font-size:11px;font-weight:700;margin-bottom:8px;">'
            f"{escape(status)}</span>"
            f'<div style="margin-top:8px;">{a}</div>'
            f'<div style="font-size:12px;color:#9ca3af;margin-top:6px;">{escape(desc)}</div></td>'
        )
    trs = []
    for i in range(0, len(cells), 4):
        chunk = cells[i : i + 4]
        trs.append(f"<tr>{''.join(chunk)}</tr>")
    content = f"""<div style="font-family:Arial,Helvetica,sans-serif;background:linear-gradient(135deg,#111827 0%,#172554 100%);color:#ffffff;border-radius:14px;padding:18px;width:100%;box-sizing:border-box;">
<div style="font-size:20px;font-weight:700;margin-bottom:4px;">{escape(title)}</div>
<div style="font-size:13px;color:#dbeafe;margin-bottom:12px;">{escape(subtitle)}</div>
<table style="width:100%;border-collapse:separate;border-spacing:10px;">{"".join(trs)}</table>
</div>"""
    return text_widget(name, content, row=row, sizey=sizey, description=title)


def footer_links(items: list[tuple[str, str]], row: int, sizey: int = 2) -> dict:
    lis = "".join(
        f'<li style="margin:4px 0;"><strong>{escape(label)}</strong> — {escape(dest)}</li>'
        for label, dest in items
    )
    content = f"""<div style="font-family:Arial,Helvetica,sans-serif;background:#0b1220;color:#e5e7eb;border:1px solid #1f2a44;border-radius:14px;padding:14px;">
<div style="font-size:14px;font-weight:700;color:#ffffff;margin-bottom:8px;">Where next</div>
<ul style="margin:0;padding-left:18px;font-size:12px;">{lis}</ul>
</div>"""
    return text_widget("Where Next", content, row=row, sizey=sizey, description="Contextual drill-down suggestions.")


def tech_directory_panel(row: int, sizey: int = 4) -> dict:
    rows = [
        ("Capacity", "Capacity Management", "Host / storage utilization trends", "{{PORTAL_BASE}}/uiv4/dashboard/{{OOTB_CAPACITY_ID}}"),
        ("Cloud", "Cloud — AWS / Azure / GCP", "Cloud account and service health", "{{PORTAL_BASE}}/uiv4/dashboard/{{OOTB_CLOUD_ID}}"),
        ("Network", "Network Performance", "Device and path performance", "{{PORTAL_BASE}}/uiv4/dashboard/{{OOTB_NETWORK_ID}}"),
        ("Server", "Linux / Microsoft Server", "OS performance and capacity", "{{PORTAL_BASE}}/uiv4/dashboard/{{OOTB_SERVER_ID}}"),
        ("Storage", "Storage", "Array and datastore health", "{{PORTAL_BASE}}/uiv4/dashboard/{{OOTB_STORAGE_ID}}"),
        ("Virt", "Virtualization", "Hypervisor and VM health", "{{PORTAL_BASE}}/uiv4/dashboard/{{OOTB_VIRT_ID}}"),
        ("Alerting", "Alerting (OOTB)", "Complementary alert packs", "{{PORTAL_BASE}}/uiv4/dashboard/{{OOTB_ALERTING_ID}}"),
        ("Websites", "Websites (OOTB)", "Deep website diagnostics", "{{PORTAL_BASE}}/uiv4/dashboard/{{OOTB_WEBSITES_ID}}"),
    ]
    return dcc_inventory_table(
        "Technology Drill-Down Directory",
        "Technology dashboards (OOTB)",
        "Import from LogicMonitor Dashboards / github.com/logicmonitor/dashboards, then wire IDs. Not bundled in this portal-admin pack.",
        rows,
        row=row,
        sizey=sizey,
    )


def make_dashboard(name: str, description: str, tokens: list, widgets: list) -> dict:
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
        ("10", "Executive", "Leaders", "Is the environment healthy? What needs attention?"),
        ("20", "Operational", "NOC / Ops", "Which alerts and resources need action now?"),
        ("30", "Technical", "Engineers", "Which metric or collector explains the issue?"),
        ("11", "Platform Value", "CS / Exec", "What operational value is the platform providing?"),
        ("21", "Active Alerts", "Triage", "Severity, noise, routing health."),
        ("34", "Tech Directory", "Deep dive", "Network, server, storage, cloud OOTB boards."),
    ]
    card_html = "".join(
        f'<td style="vertical-align:top;background:#020617;border:1px solid #1f2937;border-radius:12px;padding:14px;width:16%;">'
        f'<div style="font-size:11px;color:#38bdf8;font-weight:700;">{escape(role)}</div>'
        f'<div style="font-size:15px;font-weight:700;color:#f9fafb;margin:6px 0;">{link(nid, title)}</div>'
        f'<div style="font-size:12px;color:#9ca3af;">{escape(desc)}</div></td>'
        for nid, title, role, desc in cards
    )
    welcome = f"""<div style="font-family:Arial,Helvetica,sans-serif;background:linear-gradient(135deg,#0f172a 0%,#111827 45%,#1e3a8a 100%);color:#ffffff;border-radius:16px;padding:22px;box-shadow:0 8px 24px rgba(15,23,42,.32);">
<div style="font-size:28px;font-weight:750;color:#ffffff;">SmartAdmin Connected Experience</div>
<div style="font-size:13px;color:#dbeafe;margin-top:8px;max-width:960px;">Central lobby for Executive, Operational, and Technical dashboard groups. Start by role, review environment health, then drill into command centers. Use tokens to reuse this package across clients.</div>
</div>"""
    groups_lobby = dcc_nav_guide(
        "Dashboard Groups Lobby",
        "Three dashboard groups",
        [
            (
                "Executive",
                "Leadership visibility",
                [
                    "Command Center health snapshot",
                    "Platform value and coverage",
                    "Capacity and service risk",
                    "Links to Operational detail",
                ],
            ),
            (
                "Operational",
                "Daily monitoring",
                [
                    "Active alert triage",
                    "Resource and website health",
                    "Coverage and licenses",
                    "Access administration",
                ],
            ),
            (
                "Technical",
                "Investigation",
                [
                    "Resource investigation hub",
                    "Collector diagnostics",
                    "LogicModule noise",
                    "OOTB technology directory",
                ],
            ),
            (
                "How to use",
                "Filters and time",
                [
                    "Set defaultResourceGroup",
                    "Set accountname for licenses",
                    "Widget timescales are preserved",
                    "Wire dashboard IDs after import",
                ],
            ),
        ],
        row=9,
        sizey=5,
    )
    how = """<div style="font-family:Arial,Helvetica,sans-serif;line-height:1.45;background:#0f172a;color:#e5e7eb;border:1px solid #1f2937;border-radius:14px;padding:18px;">
<div style="font-size:20px;font-weight:700;color:#f9fafb;margin-bottom:4px;">Filters and time ranges</div>
<div style="font-size:13px;color:#9ca3af;margin-bottom:12px;">Configure tokens once; widgets that support them will scope automatically.</div>
<table style="width:100%;border-collapse:separate;border-spacing:10px;"><tr>
<td style="vertical-align:top;background:#020617;border:1px solid #1f2937;border-radius:12px;padding:14px;width:50%;">
<div style="font-size:15px;font-weight:700;color:#f9fafb;margin-bottom:8px;">Global tokens</div>
<ul style="margin:0;padding-left:18px;font-size:12px;">
<li><strong>defaultResourceGroup</strong> — default <code>*</code></li>
<li><strong>defaultResource</strong> — typically <code>*.logicmonitor.com</code></li>
<li><strong>defaultWebsiteGroup</strong> — Websites dashboards</li>
<li><strong>accountname</strong> — replace <code>{{ACCOUNT_NAME}}</code></li>
</ul>
</td>
<td style="vertical-align:top;background:#020617;border:1px solid #1f2937;border-radius:12px;padding:14px;width:50%;">
<div style="font-size:15px;font-weight:700;color:#f9fafb;margin-bottom:8px;">Time ranges</div>
<ul style="margin:0;padding-left:18px;font-size:12px;">
<li>Status scorecards — <code>day</code></li>
<li>Alert trends — <code>7days</code> / <code>1day</code></li>
<li>Coverage drift — <code>3month</code></li>
<li>Collector graphs — preserve source timescales</li>
</ul>
</td>
</tr></table>
</div>"""
    widgets = [
        global_nav_widget("00", row=1, sizey=5),
        text_widget("Welcome", welcome, row=6, sizey=3, description="Package lobby banner."),
        groups_lobby,
        text_widget(
            "Role-Based Starting Points",
            f'<div style="font-family:Arial,Helvetica,sans-serif;"><table style="width:100%;border-collapse:separate;border-spacing:12px;"><tr>{card_html}</tr></table></div>',
            row=14,
            sizey=4,
            description="Role-based navigation cards.",
        ),
        section_banner_major("Environment Summary", row=18),
        place(take("intro", "Critical Alerts"), 20, 1, 2, 2, name="Critical Alerts Requiring Attention"),
        place(take("intro", "Error Alerts"), 20, 3, 2, 2, name="Error Alerts"),
        place(take("intro", "Warning Alerts"), 20, 5, 2, 2, name="Warning Alerts"),
        place(take("intro", "Total Number of Alerts"), 20, 7, 3, 2, name="Total Active Alerts"),
        place(take("intro", "Dead Resources"), 20, 10, 3, 2, name="Resources Requiring Attention (Dead)"),
        place(take("intro", "Alive Collectors"), 22, 1, 3, 2, name="Alive Collectors"),
        place(take("intro", "Active Users"), 22, 4, 3, 2, name="Active Users"),
        place(take("overview", "Total Number of Dead Resources"), 22, 7, 3, 2, name="Dead Resources (Portal)"),
        place(take("overview", "Local Resource Licenses"), 22, 10, 3, 2, name="Local License Footprint"),
        text_widget("Filters and Time Ranges", how, row=24, sizey=5, col=1, sizex=12),
        tech_directory_panel(row=29, sizey=4),
        footer_links(
            [
                ("Executive Command Center", "10 — leadership snapshot"),
                ("Operational Command Center", "20 — triage hub"),
                ("Technical Resource Investigation", "30 — root cause"),
                ("Platform Value", "11 — coverage and value"),
            ],
            row=34,
        ),
    ]
    return make_dashboard(
        "00 - Home / Introductory",
        "Primary entry point: group lobby, role starts, environment summary, and suite navigation.",
        HOME_TOKENS,
        widgets,
    )


def build_10() -> dict:
    """NEW — Executive Command Center (DCC flow, portable metrics)."""
    widgets = [
        global_nav_widget("10", row=1, sizey=5),
        dcc_intro_guide(
            "Executive Command Center — Read First",
            "Executive Command Center",
            "Concise leadership view of platform health, risks, and where to drill. Portable tokens — not PSC-specific metrics.",
            [
                ("START", "Scan alert posture", "Review Critical / Error / Warning KPIs before drilling.", "Severity strip"),
                ("MAP", "Locate concentration", "Use geographic and type NOC views for blast radius.", "Map + NOC"),
                ("EXC", "Exceptions", "Open live resource and collector alerts when elevated.", "Alert list"),
                ("CAP", "Coverage risk", "Check dead/minimal resources and license pressure.", "Coverage KPIs"),
                ("COL", "Collectors", "Confirm the monitoring pipeline is alive.", "Alive vs down"),
                ("NEXT", "Drill with intent", "Move to Operational or Technical only when signaled.", "Ops / Tech links"),
            ],
            row=6,
            sizey=6,
        ),
        scope_pills(
            [
                ("Health", "health"),
                ("Alerts", "alerts"),
                ("Coverage", "capacity"),
                ("Collectors", "region"),
                ("Services", "sites"),
            ],
            row=12,
        ),
        section_banner("Critical status", row=13),
        place(take("overview", "Total Ack'd and Unack'd Critical Alerts"), 15, 1, 3, 2, name="Critical Alerts Requiring Attention"),
        place(take("overview", "Total Ack'd and Unack'd Error Alerts"), 15, 4, 3, 2, name="Error Alerts"),
        place(take("overview", "Total Ack'd and Unack'd Warning Alerts"), 15, 7, 3, 2, name="Warning Alerts"),
        place(take("overview", "Total Number of Ack'd and Unack'd Alerts"), 15, 10, 3, 2, name="Total Alerts"),
        place(take("overview", "Total Number of Alive Collectors"), 17, 1, 3, 2, name="Alive Collectors"),
        place(take("overview", "Total Number of Down Collectors"), 17, 4, 3, 2, name="Down Collectors"),
        place(take("overview", "Total Number of Dead Resources"), 17, 7, 3, 2, name="Dead Resources"),
        place(take("overview", "Total Number of Dead Websites"), 17, 10, 3, 2, name="Dead Websites"),
        section_banner("Situation awareness", row=19),
        place(take("overview", "Alert Status by Resource Location"), 21, 1, 6, 5, name="Alert Status by Resource Location"),
        place(take("overview", "Alert Status by Resource Types"), 21, 7, 6, 5, name="Alert Status by Resource Types"),
        place(take("overview", "All Resource Alerts"), 26, 1, 8, 5, name="Executive Exceptions"),
        place(take("overview", "Current Collector Alerts"), 26, 9, 4, 5, name="Collector Exceptions"),
        place(take("overview", "Alert Counts over time"), 31, 1, 6, 4, name="Alert Count Trend"),
        place(take("overview", "Top Dead Resources Over Time"), 31, 7, 6, 4, name="Dead Resources Trend"),
        dcc_nav_guide(
            "Team Navigation and Drill-Down",
            "Where leaders go next",
            [
                ("Executive", "Stay high-level", ["Platform Value (11)", "Env Health Exec (12)", "Availability (13)", "Capacity Risk (14)"]),
                ("Operations", "Triage detail", ["Ops Command Center (20)", "Active Alerts (21)", "Resource Health (22)"]),
                ("Technical", "Investigate", ["Resource Investigation (30)", "Collector Diagnostics (31)"]),
                ("Decision", "Escalate when", ["Critical rising", "Collectors down", "Dead websites", "License pressure"]),
            ],
            row=35,
            sizey=4,
        ),
        footer_links(
            [
                ("Platform Value Overview", "11"),
                ("Operational Command Center", "20"),
                ("Active Alerts", "21"),
                ("Collector Diagnostics", "31"),
            ],
            row=39,
        ),
    ]
    return make_dashboard(
        "10 - Executive Command Center",
        "Executive command center: DCC-style flow with portable SmartAdmin/Introductive health metrics.",
        PORTAL_TOKENS,
        widgets,
    )


def build_11() -> dict:
    widgets = [
        global_nav_widget("11", row=1, sizey=5),
        guide_widget(
            "Platform Value Overview — Read First",
            "Platform Value Overview",
            "Executive landing page for health, coverage, and platform value.",
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
                "Elevated alerts → 21 Active Alerts",
                "Dead/minimal → 22 Resource Health / 12 Exec",
                "License pressure → 14 / 24",
                "Down collectors → 31 Collector Diagnostics",
            ],
            row=6,
            sizey=5,
        ),
        section_banner("Critical status — alert posture", row=11),
        place(take("overview", "Total Ack'd and Unack'd Critical Alerts"), 13, 1, 3, 2, name="Critical Alerts Requiring Attention"),
        place(take("overview", "Total Ack'd and Unack'd Error Alerts"), 13, 4, 3, 2, name="Error Alerts"),
        place(take("overview", "Total Ack'd and Unack'd Warning Alerts"), 13, 7, 3, 2, name="Warning Alerts"),
        place(take("overview", "Total Number of Ack'd and Unack'd Alerts"), 13, 10, 3, 2, name="Total Alerts (Ack and Unack)"),
        section_banner("Platform coverage and collector health", row=15),
        place(take("overview", "Total Number of Alive Collectors"), 17, 1, 3, 2, name="Alive Collectors"),
        place(take("overview", "Total Number of Down Collectors"), 17, 4, 3, 2, name="Down Collectors"),
        place(take("alerts", "Total Number of Resources"), 17, 7, 3, 2, name="Monitored Resources"),
        place(take("alerts", "Total Number of Cloud Resources"), 17, 10, 3, 2, name="Cloud Resources"),
        place(take("overview", "Local Resource Licenses"), 19, 1, 3, 2, name="Local Resource Licenses"),
        place(take("overview", "Cloud Resource Licences"), 19, 4, 3, 2, name="Cloud Resource Licenses"),
        place(take("overview", "LogSources"), 19, 7, 3, 2, name="LogSources Installed"),
        place(take("overview", "Active Users"), 19, 10, 3, 2, name="Active Users"),
        section_banner("Situation awareness", row=21),
        place(take("overview", "Alert Status by Resource Location"), 23, 1, 6, 5, name="Alert Status by Resource Location"),
        place(take("overview", "Alert Status by Resource Types"), 23, 7, 6, 5, name="Alert Status by Resource Types"),
        place(take("overview", "Alert Counts over time"), 28, 1, 6, 4, name="Alert Count Trend"),
        place(take("overview", "Top Dead Resources Over Time"), 28, 7, 6, 4, name="Dead Resources Trend"),
        footer_links(
            [
                ("Executive Command Center", "10"),
                ("Resource Health", "22"),
                ("Active Alerts", "21"),
                ("Capacity and Risk", "14"),
                ("Collector Diagnostics", "31"),
            ],
            row=32,
        ),
    ]
    return make_dashboard(
        "11 - Platform Value Overview",
        "Executive view: alert posture, collectors, footprint, licenses, map/NOC, and navigation.",
        PORTAL_TOKENS,
        widgets,
    )


def build_12() -> dict:
    """NEW — Environment Health Executive (exec-density)."""
    widgets = [
        global_nav_widget("12", row=1, sizey=5),
        guide_widget(
            "Environment Health Executive — Read First",
            "Environment Health Executive Overview",
            "Leadership-density view of where risk is concentrated — without deep operational tables.",
            [
                "Where is risk concentrated geographically or by type?",
                "Are dead or minimally monitored resources rising?",
                "Are collectors and websites signaling trouble?",
            ],
            [
                ("Map + NOC", "Concentration"),
                ("Dead / minimal / websites", "Blind spots"),
                ("Collector pulse", "Trust in data"),
                ("Drill to Ops", "Resource Health / Alerts"),
            ],
            [
                "Operational Resource Health → 22",
                "Active Alerts → 21",
                "Collector Diagnostics → 31",
                "Websites → 23 / 13",
            ],
            row=6,
            sizey=5,
        ),
        scope_pills([("Health", "health"), ("Alerts", "alerts"), ("Capacity", "capacity"), ("Services", "sites")], row=11),
        section_banner("Executive risk indicators", row=12),
        place(take("alerts", "Total Number of Critical Alerts"), 14, 1, 3, 2, name="Critical Alerts"),
        place(take("alerts", "Total Number of Dead Resources"), 14, 4, 3, 2, name="Dead Resources"),
        place(take("alerts", "Total Number of Minimal Monitoring Resource"), 14, 7, 3, 2, name="Minimally Monitored Resources"),
        place(take("overview", "Total Number of Dead Websites"), 14, 10, 3, 2, name="Dead Websites"),
        place(take("overview", "Total Number of Alive Collectors"), 16, 1, 3, 2, name="Alive Collectors"),
        place(take("overview", "Total Number of Down Collectors"), 16, 4, 3, 2, name="Down Collectors"),
        place(take("alerts", "Total Number of SDT Resource"), 16, 7, 3, 2, name="Resources in SDT"),
        place(take("alerts", "Total Number of Resources"), 16, 10, 3, 2, name="Monitored Resources"),
        section_banner("Situation visuals", row=18),
        place(take("overview", "Alert Status by Resource Location"), 20, 1, 6, 5, name="Alert Status by Resource Location"),
        place(take("overview", "Alert Status by Resource Types"), 20, 7, 6, 5, name="Alert Status by Resource Types"),
        place(take("alerts", "Top Dead Resources Over Time"), 25, 1, 6, 4, name="Dead Resources Trend"),
        place(take("alerts", "Total Minimal Monitoring Resources over Time"), 25, 7, 6, 4, name="Minimal Monitoring Trend"),
        footer_links(
            [
                ("Executive Command Center", "10"),
                ("Resource Health (Operational)", "22"),
                ("Active Alerts", "21"),
                ("Collector Diagnostics", "31"),
            ],
            row=29,
        ),
    ]
    return make_dashboard(
        "12 - Environment Health Executive",
        "Executive environment health: map/NOC, dead/minimal/website/collector signals without deep ops tables.",
        PORTAL_TOKENS,
        widgets,
    )


def build_13() -> dict:
    """NEW — Availability and Service Health."""
    widgets = [
        global_nav_widget("13", row=1, sizey=5),
        guide_widget(
            "Availability and Service Health — Read First",
            "Availability and Service Health",
            "Executive view of website/service availability and related alert severity.",
            [
                "Are websites available?",
                "Are empty website groups creating blind spots?",
                "Is alert severity elevated for services?",
            ],
            [
                ("Website KPIs", "Counts and dead"),
                ("Alert severity", "Service impact signal"),
                ("Ops websites", "Deep hygiene on 23"),
            ],
            [
                "Websites and Services → 23",
                "Active Alerts → 21",
                "OOTB Websites → 34 directory",
            ],
            row=6,
            sizey=5,
        ),
        section_banner("Service availability", row=11),
        place(take("groups", "Total Number of Websites"), 13, 1, 3, 2, name="Websites Monitored"),
        place(take("groups", "Total Number of Dead Website"), 13, 4, 3, 2, name="Dead Websites"),
        place(take("groups", "Total Number of Website Groups"), 13, 7, 3, 2, name="Website Groups"),
        place(take("groups", "Total Number of Empty Website Groups"), 13, 10, 3, 2, name="Empty Website Groups"),
        section_banner("Related alert posture", row=15),
        place(take("intro", "Critical Alerts"), 17, 1, 3, 2, name="Critical Alerts"),
        place(take("intro", "Error Alerts"), 17, 4, 3, 2, name="Error Alerts"),
        place(take("intro", "Warning Alerts"), 17, 7, 3, 2, name="Warning Alerts"),
        place(take("intro", "Total Number of Alerts"), 17, 10, 3, 2, name="Total Active Alerts"),
        place(take("intro", "Alert Count over time"), 19, 1, 12, 4, name="Alert Count Trend"),
        dcc_inventory_table(
            "Service Drill-Down Links",
            "Related operational and technical views",
            "Configure IDs after import.",
            [
                ("Ops", "Websites and Services", "Group and website hygiene detail", "23"),
                ("Ops", "Active Alerts", "Live exceptions and noise", "21"),
                ("Tech", "Technology Directory", "OOTB website diagnostics", "34"),
                ("Exec", "Executive Command Center", "Return to leadership hub", "10"),
            ],
            row=23,
            sizey=4,
        ),
        footer_links(
            [
                ("Websites and Services", "23"),
                ("Executive Command Center", "10"),
                ("Operational Command Center", "20"),
            ],
            row=27,
        ),
    ]
    return make_dashboard(
        "13 - Availability and Service Health",
        "Executive availability: websites/services KPIs plus alert severity and drill-downs.",
        WEBSITE_TOKENS,
        widgets,
    )


def build_14() -> dict:
    """NEW — Capacity and Risk Overview."""
    widgets = [
        global_nav_widget("14", row=1, sizey=5),
        guide_widget(
            "Capacity and Risk Overview — Read First",
            "Capacity and Risk Overview",
            "Executive capacity, license, and coverage-risk signals. Host utilization deep-dives via OOTB Capacity.",
            [
                "Is license pressure rising?",
                "Are unmonitored or minimal resources creating risk?",
                "Where should capacity investigation continue?",
            ],
            [
                ("License strip", "Cloud and local"),
                ("Coverage gaps", "Unmonitored / minimal"),
                ("OOTB capacity", "Infra utilization"),
            ],
            [
                "Ops Coverage detail → 24",
                "Technology Directory → 34",
                "Platform Value → 11",
            ],
            row=6,
            sizey=5,
        ),
        scope_pills([("Capacity", "capacity"), ("Coverage", "region"), ("Risk", "alerts")], row=11),
        section_banner("License and footprint risk", row=12),
        place(take("licenses", "IaaS - Total"), 14, 1, 3, 2, name="IaaS Licenses Total"),
        place(take("licenses", "PaaS - Total"), 14, 4, 3, 2, name="PaaS Licenses Total"),
        place(take("licenses", "Non-Compute - Total"), 14, 7, 3, 2, name="Non-Compute Licenses Total"),
        place(take("licenses", "Local Licenses"), 14, 10, 3, 2, name="Local Licenses"),
        place(take("licenses", "Local Licenses Percents"), 16, 1, 3, 2, name="Local License Percent Used"),
        place(take("alerts", "Total Number of Resources"), 16, 4, 3, 2, name="Monitored Resources"),
        place(take("alerts", "Total Number of Dead Resources"), 16, 7, 3, 2, name="Dead Resources"),
        place(take("alerts", "Total Number of Minimal Monitoring Resource"), 16, 10, 3, 2, name="Minimally Monitored"),
        section_banner("Coverage risk trends", row=18),
        place(take("alerts", "Number of Unmonitored Devices Over 90 days"), 20, 1, 6, 4, name="Unmonitored Devices Trend (90 Days)"),
        place(take("alerts", "Total Minimal Monitoring Resources over Time"), 20, 7, 6, 4, name="Minimal Monitoring Trend"),
        tech_directory_panel(row=24, sizey=4),
        footer_links(
            [
                ("Coverage, Capacity & Licenses", "04 — operational detail"),
                ("Technology Directory", "31 — OOTB capacity"),
                ("Executive Command Center", "10"),
            ],
            row=29,
        ),
    ]
    return make_dashboard(
        "14 - Capacity and Risk Overview",
        "Executive capacity and coverage risk: licenses, gaps, and OOTB capacity links.",
        LICENSE_TOKENS,
        widgets,
    )


def build_20() -> dict:
    """NEW — Operational Command Center."""
    widgets = [
        global_nav_widget("20", row=1, sizey=5),
        dcc_intro_guide(
            "Operational Command Center — Read First",
            "Operational Command Center",
            "Daily triage hub: prioritize alerts, unhealthy resources, collector pulse, then drill.",
            [
                ("ALERT", "Triage severity", "Start with Critical and Error counts, then live lists.", "Active Alerts"),
                ("RES", "Resource health", "Dead, minimal, SDT, and map concentration.", "Resource Health"),
                ("COL", "Collector pulse", "Confirm collection before trusting gaps.", "Alive / down"),
                ("WEB", "Services", "Dead websites and empty groups.", "Websites"),
                ("NEXT", "Investigate", "Open Technical Investigation when root cause needed.", "Tech hub"),
                ("BACK", "Exec summary", "Return leaders to Command Center when stabilized.", "Exec CC"),
            ],
            row=6,
            sizey=6,
        ),
        section_banner("Triage strip", row=12),
        place(take("alerts", "Total Number of Critical Alerts"), 14, 1, 3, 2, name="Critical Alerts Requiring Attention"),
        place(take("alerts", "Total Number of Error Alerts"), 14, 4, 3, 2, name="Error Alerts"),
        place(take("alerts", "Total Number of Dead Resources"), 14, 7, 3, 2, name="Dead Resources"),
        place(take("overview", "Total Number of Down Collectors"), 14, 10, 3, 2, name="Down Collectors"),
        place(take("overview", "Total Number of Dead Websites"), 16, 1, 3, 2, name="Dead Websites"),
        place(take("alerts", "Total Number of Minimal Monitoring Resource"), 16, 4, 3, 2, name="Minimally Monitored"),
        place(take("alerts", "Total Number of SDT Resource"), 16, 7, 3, 2, name="Resources in SDT"),
        place(take("overview", "Total Number of Alive Collectors"), 16, 10, 3, 2, name="Alive Collectors"),
        section_banner("Live exceptions and concentration", row=18),
        place(take("overview", "All Resource Alerts"), 20, 1, 8, 5, name="Active Resource Alerts"),
        place(take("overview", "Current Collector Alerts"), 20, 9, 4, 5, name="Collector Alerts"),
        place(take("overview", "Alert Status by Resource Location"), 25, 1, 6, 5, name="Alert Status by Resource Location"),
        place(take("overview", "Alert Status by Resource Types"), 25, 7, 6, 5, name="Alert Status by Resource Types"),
        dcc_nav_guide(
            "Operational Drill Paths",
            "Next operational and technical steps",
            [
                ("Alerts", "Active Alerts (21)", ["Severity KPIs", "Rules / integrations", "Module noise"]),
                ("Resources", "Resource Health (22)", ["Dead / minimal trends", "Idle interval", "Collector signals"]),
                ("Services", "Websites (23)", ["Dead websites", "Empty groups", "Website token"]),
                ("Technical", "Investigation (30)", ["Metric families", "Collector diagnostics", "OOTB directory"]),
            ],
            row=30,
            sizey=4,
        ),
        footer_links(
            [
                ("Active Alerts", "21"),
                ("Resource Health", "22"),
                ("Technical Resource Investigation", "30"),
                ("Executive Command Center", "10"),
            ],
            row=34,
        ),
    ]
    return make_dashboard(
        "20 - Operational Command Center",
        "Operational triage hub: alerts, resource health, collector pulse, and drill paths.",
        PORTAL_TOKENS,
        widgets,
    )


def build_22() -> dict:
    widgets = [
        global_nav_widget("22", row=1, sizey=5),
        guide_widget(
            "Resource Health — Read First",
            "Resource Health",
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
                "Active alert triage → 21",
                "Collector diagnostics → 31",
                "Website detail → 23",
                "Coverage / discovery → 24",
                "Technical investigation → 30",
            ],
            row=6,
            sizey=5,
        ),
        section_banner("Critical status", row=11),
        place(take("alerts", "Total Number of Critical Alerts"), 13, 1, 3, 2, name="Critical Alerts"),
        place(take("alerts", "Total Number of Dead Resources"), 13, 4, 3, 2, name="Dead Resources"),
        place(take("alerts", "Total Number of Minimal Monitoring Resource"), 13, 7, 3, 2, name="Minimally Monitored Resources"),
        place(take("overview", "Total Number of Dead Websites"), 13, 10, 3, 2, name="Dead Websites"),
        place(take("overview", "Total Number of Alive Collectors"), 15, 1, 3, 2, name="Alive Collectors"),
        place(take("overview", "Total Number of Down Collectors"), 15, 4, 3, 2, name="Down Collectors"),
        place(take("alerts", "Total Number of SDT Resource"), 15, 7, 3, 2, name="Resources in SDT"),
        place(take("alerts", "Total Number of Netflow Resource"), 15, 10, 3, 2, name="Netflow Resources"),
        section_banner("Situation visuals", row=17),
        place(take("overview", "Alert Status by Resource Location"), 19, 1, 6, 5, name="Alert Status by Resource Location"),
        place(take("overview", "Alert Status by Resource Types"), 19, 7, 6, 5, name="Alert Status by Resource Types"),
        section_banner("Trends and collector signals", row=24),
        place(take("alerts", "Top Dead Resources Over Time"), 26, 1, 4, 4, name="Dead Resources Trend"),
        place(take("alerts", "Total Minimal Monitoring Resources over Time"), 26, 5, 4, 4, name="Minimal Monitoring Trend"),
        place(take("overview", "Current Collector Alerts"), 26, 9, 4, 4, name="Current Collector Alerts"),
        place(take("alerts", "Idle Interval"), 30, 1, 12, 4, name="Resources with Idle Interval Risk"),
        footer_links(
            [
                ("Operational Command Center", "20"),
                ("Active Alerts", "21"),
                ("Collector Diagnostics", "31"),
                ("Technical Investigation", "30"),
            ],
            row=34,
        ),
    ]
    return make_dashboard(
        "22 - Resource Health",
        "Operational resource health: map/NOC, dead/minimal resources, collector and website signals.",
        PORTAL_TOKENS,
        widgets,
    )


def build_21() -> dict:
    widgets = [
        global_nav_widget("21", row=1, sizey=5),
        guide_widget(
            "Active Alerts — Read First",
            "Active Alerts",
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
                "Collector-caused gaps → 31",
                "Noisy modules deep dive → 32",
                "Spatial concentration → 22",
                "Technical investigation → 30",
            ],
            row=6,
            sizey=5,
        ),
        section_banner("Severity and volume", row=11),
        place(take("alerts", "Total Number of Critical Alerts"), 13, 1, 3, 2, name="Critical Alerts Requiring Attention"),
        place(take("alerts", "Total Number of Error Alerts"), 13, 4, 3, 2, name="Error Alerts"),
        place(take("alerts", "Total Number of Warning Alerts"), 13, 7, 3, 2, name="Warning Alerts"),
        place(take("alerts", "Total Number of Alerts"), 13, 10, 3, 2, name="Total Alerts"),
        place(take("alerts", "Alert Counts over time"), 15, 1, 6, 4, name="Alert Count Trend"),
        place(take("alerts", "Top Datasources by Alerts"), 15, 7, 6, 4, name="Top Datasources by Alert Volume"),
        section_banner("Live exceptions", row=19),
        place(take("overview", "All Resource Alerts"), 21, 1, 8, 5, name="All Resource Alerts"),
        place(take("overview", "Current Collector Alerts"), 21, 9, 4, 5, name="Current Collector Alerts"),
        section_banner("Routing and integrations", row=26),
        place(take("alerts", "Alert Rules"), 28, 1, 4, 4, name="Alert Rules in Use"),
        place(take("alerts", "Escalation Chains inUse by Alert Rules"), 28, 5, 4, 4, name="Escalation Chains in Use"),
        place(take("alerts", "Total Number of Escalation Chains"), 28, 9, 3, 2, name="Escalation Chain Count"),
        place(take("alerts", "Total Number of Portal Integration"), 30, 9, 3, 2, name="Portal Integrations"),
        place(take("alerts", "Number of Integrations with Non 200 Response"), 32, 1, 6, 4, name="Integrations with Non-200 Responses"),
        section_banner("LogicModule alert noise (90 days)", row=36),
        place(take("alerts", "Datasource Alerts in last 90 days"), 38, 1, 6, 4, name="DataSource Alerts Last 90 Days"),
        place(take("alerts", "EventSource Alerts in last 90 days"), 38, 7, 6, 4, name="EventSource Alerts Last 90 Days"),
        place(take("alerts", "ConfigSource Alerts in last 90 days"), 42, 1, 6, 4, name="ConfigSource Alerts Last 90 Days"),
        place(take("alerts", "LogSource Alerts in last 90 days"), 42, 7, 6, 4, name="LogSource Alerts Last 90 Days"),
        footer_links(
            [
                ("Operational Command Center", "20"),
                ("Resource Health", "22"),
                ("Collector Diagnostics", "31"),
                ("LogicModule and Content", "32"),
            ],
            row=46,
        ),
    ]
    return make_dashboard(
        "21 - Active Alerts",
        "Operational alert cockpit: severity, trends, live alerts, rules, escalations, integrations, and module noise.",
        PORTAL_TOKENS,
        widgets,
    )


def build_24() -> dict:
    widgets = [
        global_nav_widget("24", row=1, sizey=5),
        guide_widget(
            "Coverage Capacity Licenses — Read First",
            "Coverage, Capacity & Licenses",
            "Discovery coverage, license consumption, and group hygiene. Host capacity lives in OOTB links.",
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
                "Executive Capacity Risk → 14",
                "Modules → 32",
                "Websites → 23",
                "Technology Directory → 34",
            ],
            row=6,
            sizey=5,
        ),
        section_banner("License consumption", row=11),
        place(take("licenses", "IaaS - Total"), 13, 1, 3, 2, name="IaaS Licenses Total"),
        place(take("licenses", "PaaS - Total"), 13, 4, 3, 2, name="PaaS Licenses Total"),
        place(take("licenses", "Non-Compute - Total"), 13, 7, 3, 2, name="Non-Compute Licenses Total"),
        place(take("licenses", "Local Licenses"), 13, 10, 3, 2, name="Local Licenses"),
        place(take("licenses", "AWS - IaaS"), 15, 1, 2, 2),
        place(take("licenses", "AWS - PaaS"), 15, 3, 2, 2),
        place(take("licenses", "AWS - Non-Compute"), 15, 5, 2, 2),
        place(take("licenses", "Azure - IaaS"), 15, 7, 2, 2),
        place(take("licenses", "Azure - PaaS"), 15, 9, 2, 2),
        place(take("licenses", "Azure - Non-Compute"), 15, 11, 2, 2),
        place(take("licenses", "GCP - IaaS"), 17, 1, 2, 2),
        place(take("licenses", "GCP - PaaS"), 17, 3, 2, 2),
        place(take("licenses", "GCP - Non-Compute"), 17, 5, 2, 2),
        place(take("licenses", "Local Licenses Percents"), 17, 7, 3, 2, name="Local License Percent Used"),
        section_banner("Discovery and coverage gaps", row=19),
        place(take("alerts", "Total Number of Netscans"), 21, 1, 3, 2, name="Netscans Total"),
        place(take("alerts", "Total Number of Netscans - EC2"), 21, 4, 3, 2),
        place(take("alerts", "Total Number of Netscans - Script"), 21, 7, 3, 2),
        place(take("alerts", "Total Number of Netscans - Scheduled"), 21, 10, 3, 2),
        place(take("alerts", "Netscans"), 23, 1, 12, 4, name="Netscan Inventory"),
        place(take("alerts", "Number of Unmonitored Devices Over 90 days"), 27, 1, 6, 4, name="Unmonitored Devices Trend (90 Days)"),
        place(take("alerts", "Number of Netscan Devices Added Per Day Over 90 Days"), 27, 7, 6, 4, name="Netscan Devices Added Per Day"),
        section_banner("Group hygiene", row=31),
        place(take("groups", "Total Number of Device Groups"), 33, 1, 3, 2),
        place(take("groups", "Total Number of Empty Static Groups"), 33, 4, 3, 2, name="Empty Static Device Groups"),
        place(take("groups", "Total Number of Website Groups"), 33, 7, 3, 2),
        place(take("groups", "Total Number of Empty Website Groups"), 33, 10, 3, 2, name="Empty Website Groups"),
        tech_directory_panel(row=35, sizey=4),
        footer_links(
            [
                ("Capacity and Risk Overview", "14"),
                ("LogicModule and Content", "32"),
                ("Websites and Services", "23"),
                ("Adoption", "33"),
            ],
            row=40,
        ),
    ]
    return make_dashboard(
        "24 - Coverage, Capacity & Licenses",
        "Operational coverage: licenses, netscans, unmonitored trends, group hygiene, and OOTB capacity links.",
        LICENSE_TOKENS,
        widgets,
    )


def build_23() -> dict:
    widgets = [
        global_nav_widget("23", row=1, sizey=5),
        guide_widget(
            "Websites and Services — Read First",
            "Websites and Services",
            "Website and group hygiene for service checks. Deep website performance via OOTB Website dashboards.",
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
                ("Availability Exec", "13"),
                ("Resource Health", "22"),
                ("Coverage", "24"),
                ("OOTB Websites", "34"),
            ],
            row=6,
            sizey=5,
        ),
        section_banner("Website health", row=11),
        place(take("groups", "Total Number of Websites"), 13, 1, 3, 2, name="Websites Monitored"),
        place(take("groups", "Total Number of Dead Website"), 13, 4, 3, 2, name="Dead Websites"),
        place(take("groups", "Total Number of Website Groups"), 13, 7, 3, 2, name="Website Groups"),
        place(take("groups", "Total Number of Empty Website Groups"), 13, 10, 3, 2, name="Empty Website Groups"),
        section_banner("Device group structure", row=15),
        place(take("groups", "Total Number of Device Groups"), 17, 1, 3, 2),
        place(take("groups", "Total Number of Static Device Groups"), 17, 4, 3, 2),
        place(take("groups", "Total Number of Dynamic Device Groups"), 17, 7, 3, 2),
        place(take("groups", "Total Number of Empty Static Groups"), 17, 10, 3, 2, name="Empty Static Device Groups"),
        text_widget(
            "Website Token Scope",
            """<div style="font-family:Arial,Helvetica,sans-serif;line-height:1.45;background:#0f172a;color:#e5e7eb;border:1px solid #1f2937;border-radius:14px;padding:18px;">
<div style="font-size:20px;font-weight:700;color:#f9fafb;">defaultWebsiteGroup</div>
<div style="font-size:13px;color:#9ca3af;margin-top:4px;">Set <code>##defaultWebsiteGroup##</code> to scope website views when OOTB website dashboards are linked. Default is <code>*</code>.</div>
</div>""",
            row=19,
            sizey=2,
        ),
        tech_directory_panel(row=21, sizey=4),
        footer_links(
            [
                ("Availability and Service Health", "13"),
                ("Resource Health", "22"),
                ("Active Alerts", "21"),
            ],
            row=26,
        ),
    ]
    return make_dashboard(
        "23 - Websites and Services",
        "Operational websites and group hygiene with defaultWebsiteGroup token.",
        WEBSITE_TOKENS,
        widgets,
    )


def build_25() -> dict:
    widgets = [
        global_nav_widget("25", row=1, sizey=5),
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
            row=6,
            sizey=5,
        ),
        section_banner("Users and access", row=11),
        place(take("users", "Users"), 13, 1, 3, 2, name="Total Users"),
        place(take("users", "Users with Active Status"), 13, 4, 3, 2, name="Active Users"),
        place(take("users", "API Access Users"), 13, 7, 3, 2, name="Users with API Access"),
        place(take("users", "API Only users"), 13, 10, 3, 2, name="API-Only Users"),
        section_banner("Roles and groups", row=15),
        place(take("users", "User Roles"), 17, 1, 3, 2),
        place(take("users", "Roles with no assigned Users"), 17, 4, 3, 2, name="Roles with No Assigned Users"),
        place(take("users", "User Groups"), 17, 7, 3, 2),
        place(take("users", "Empty User Groups"), 17, 10, 3, 2, name="Empty User Groups"),
        section_banner("Tokens and idle access (90 days)", row=19),
        place(take("users", "API Tokens"), 21, 1, 3, 2),
        place(take("users", "API Token not used in last 90 days"), 21, 4, 3, 2, name="Idle API Tokens (90 Days)"),
        place(take("users", "Users not logged in last 90 days"), 21, 7, 3, 2, name="Idle Users (90 Days)"),
        place(take("users", "API Only Users not logged in last 90 days"), 21, 10, 3, 2, name="Idle API-Only Users (90 Days)"),
        footer_links(
            [
                ("Adoption and Optimization", "33"),
                ("Home", "00"),
                ("Platform Value", "11"),
            ],
            row=23,
        ),
    ]
    return make_dashboard(
        "25 - Access and Administration",
        "Operational access governance: users, roles, groups, API tokens, and idle access.",
        PORTAL_TOKENS,
        widgets,
    )


def build_30() -> dict:
    """NEW — Technical Resource Investigation hub."""
    widgets = [
        global_nav_widget("30", row=1, sizey=5),
        dcc_intro_guide(
            "Technical Resource Investigation — Read First",
            "Technical Resource Investigation",
            "Start here for root-cause investigation. Confirm scope, isolate metric family, then open collector or OOTB technology boards.",
            [
                ("SCOPE", "Confirm tokens", "defaultResourceGroup / ResourceName must match the incident scope.", "Tokens"),
                ("TIME", "When did it start?", "Compare alert trend and dead-resource trend windows.", "Trends"),
                ("WHO", "Which resources?", "Use alert lists and idle/dead tables.", "Exceptions"),
                ("PIPE", "Collector involved?", "JVM, tasks, method mix on Collector Diagnostics.", "Collectors"),
                ("CONTENT", "Noisy modules?", "LogicModule 90-day alert tables.", "Modules"),
                ("TECH", "Domain board", "Network / Server / Storage / Cloud via directory.", "Directory"),
            ],
            row=6,
            sizey=6,
        ),
        section_banner("Investigation signals", row=12),
        place(take("alerts", "Total Number of Critical Alerts"), 14, 1, 3, 2, name="Critical Alerts"),
        place(take("alerts", "Total Number of Dead Resources"), 14, 4, 3, 2, name="Dead Resources"),
        place(take("overview", "Total Number of Down Collectors"), 14, 7, 3, 2, name="Down Collectors"),
        place(take("alerts", "Total Number of Minimal Monitoring Resource"), 14, 10, 3, 2, name="Minimally Monitored"),
        place(take("overview", "All Resource Alerts"), 16, 1, 8, 5, name="Scoped Resource Alerts"),
        place(take("overview", "Current Collector Alerts"), 16, 9, 4, 5, name="Collector Alerts"),
        place(take("alerts", "Alert Counts over time"), 21, 1, 6, 4, name="Alert Count Trend"),
        place(take("alerts", "Top Dead Resources Over Time"), 21, 7, 6, 4, name="Dead Resources Trend"),
        place(take("alerts", "Idle Interval"), 25, 1, 12, 4, name="Idle Interval Risk Resources"),
        dcc_inventory_table(
            "Investigation Paths",
            "Metric-family and diagnostic paths",
            "Open the matching technical board. Configure OOTB IDs on 34 after import.",
            [
                ("Collectors", "Collector Diagnostics", "JVM, tasks, method mix, collector alerts", "31"),
                ("Content", "LogicModule and Content", "Inventory and 90-day noise", "32"),
                ("Adoption", "Adoption and Optimization", "Noise and coverage improvement", "33"),
                ("Directory", "Technology Dashboard Directory", "Network / Server / Storage / Cloud / Capacity", "34"),
                ("Ops", "Active Alerts", "Rules, integrations, live triage", "21"),
                ("Ops", "Resource Health", "Map, NOC, dead/minimal", "22"),
            ],
            row=29,
            sizey=4,
        ),
        footer_links(
            [
                ("Collector Diagnostics", "31"),
                ("Technology Directory", "34"),
                ("Operational Command Center", "20"),
                ("Executive Command Center", "10"),
            ],
            row=34,
        ),
    ]
    return make_dashboard(
        "30 - Technical Resource Investigation",
        "Technical investigation hub: checklist, scoped signals, and paths to collectors/modules/OOTB tech boards.",
        PORTAL_TOKENS,
        widgets,
    )


def build_31() -> dict:
    widgets = [
        global_nav_widget("31", row=1, sizey=5),
        guide_widget(
            "Collector Diagnostics — Read First",
            "Collector Diagnostics",
            "Technical dashboard for collector availability, JVM pressure, and collection/AD task health. Canonical single copy.",
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
                ("Resource Health", "22"),
                ("Active Alerts", "21"),
                ("Technical Investigation", "30"),
            ],
            row=6,
            sizey=5,
        ),
        section_banner("Instance counts by collection method", row=11),
        place(take("collector", "Selenium Instance Count"), 13, 1, 2, 2),
        place(take("collector", "Batchscript Instance Count"), 13, 3, 2, 2),
        place(take("collector", "DNS Instance Count"), 13, 5, 2, 2),
        place(take("collector", "JMX Instance Count"), 13, 7, 2, 2),
        place(take("collector", "Ping Instance Count"), 13, 9, 2, 2),
        place(take("collector", "Script Instance Count"), 13, 11, 2, 2),
        place(take("collector", "SNMP Instance Count"), 15, 1, 2, 2),
        place(take("collector", "Webpage Instance Count"), 15, 3, 2, 2),
        place(take("collector", "WMI Instance Count"), 15, 5, 2, 2),
        place(take("collector", "Data Collection Instance Counts"), 15, 7, 3, 2),
        place(take("collector", "Total Data Collecting Instance Count"), 15, 10, 3, 2, name="Total Data Collecting Instances"),
        section_banner("Real-time collector stats", row=17),
        place(take("collector", "Collector JVM Performance (Real-time)"), 19, 1, 6, 4, name="Collector JVM Performance"),
        place(take("collector", "Collector Alert History"), 19, 7, 6, 4, name="Collector Alert History"),
        place(take("collector", "Top Collectors by Heap Utilization (Trend)"), 23, 1, 6, 4, name="Top Collectors by Heap Utilization"),
        place(take("collector", "Top Collectors by CPU Utilization (Trend)"), 23, 7, 6, 4, name="Top Collectors by CPU Utilization"),
        section_banner("Collection and Active Discovery tasks", row=27),
        place(take("collector", "Top 10 Collection Tasks by Slowest Successful Execution"), 29, 1, 4, 4, name="Slowest Successful Collection Tasks"),
        place(take("collector", "Active DiscoveryTop 10 Tasks by Failure Rate"), 29, 5, 4, 4, name="Active Discovery Tasks by Failure Rate"),
        place(take("collector", "Top Collection Tasks (Real-time)"), 29, 9, 4, 4),
        place(take("collector", "Top Active Discovery Tasks (Real-time)"), 33, 1, 6, 4),
        place(take("collector", "Collector Data Collecting Tasks-Total"), 33, 7, 6, 4, name="Data Collecting Tasks Total"),
        place(take("collector", "Collector Data Collecting Tasks-Unavailable Thread Scheduling"), 37, 1, 6, 4),
        place(take("collector", "Total Instance Counts by Collector"), 37, 7, 6, 4),
        section_banner("Individual collector methods", row=41),
        place(take("collector", "Collector Data Collecting Tasks-script"), 43, 1, 4, 3),
        place(take("collector", "Collector Data Collecting Tasks-batchscript"), 43, 5, 4, 3),
        place(take("collector", "Collector Data Collecting Tasks-WMI"), 43, 9, 4, 3),
        place(take("collector", "Collector Data Collecting Tasks-SNMP"), 46, 1, 4, 3),
        place(take("collector", "Collector Data Collecting Tasks-Ping"), 46, 5, 4, 3),
        place(take("collector", "Collector Data Collecting Tasks-JMX"), 46, 9, 4, 3),
        footer_links(
            [
                ("Technical Resource Investigation", "30"),
                ("Resource Health", "22"),
                ("Active Alerts", "21"),
                ("Home", "00"),
            ],
            row=49,
        ),
    ]
    return make_dashboard(
        "31 - Collector Diagnostics",
        "Technical collector diagnostics (single canonical dashboard; duplicate removed).",
        COLLECTOR_TOKENS,
        widgets,
    )


def build_32() -> dict:
    widgets = [
        global_nav_widget("32", row=1, sizey=5),
        guide_widget(
            "LogicModule and Content — Read First",
            "LogicModule and Content",
            "Content inventory plus noisy modules.",
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
                ("Active Alerts", "21"),
                ("Adoption", "33"),
                ("Coverage", "24"),
                ("Investigation", "30"),
            ],
            row=6,
            sizey=5,
        ),
        section_banner("LogicModule inventory", row=11),
        place(take("modules", "DataSources"), 13, 1, 3, 2),
        place(take("modules", "EventSources"), 13, 4, 3, 2),
        place(take("modules", "ConfigSources"), 13, 7, 3, 2),
        place(take("modules", "PropertySources"), 13, 10, 3, 2),
        place(take("modules", "LogSources"), 15, 1, 3, 2),
        place(take("modules", "TopologySources"), 15, 4, 3, 2),
        place(take("modules", "SNMP SYSOID Maps"), 15, 7, 3, 2),
        place(take("modules", "AppliesTo Functions"), 15, 10, 3, 2),
        section_banner("Noisy modules and instance footprint", row=17),
        place(take("alerts", "Datasource Alerts in last 90 days"), 19, 1, 6, 4, name="DataSource Alerts Last 90 Days"),
        place(take("alerts", "EventSource Alerts in last 90 days"), 19, 7, 6, 4, name="EventSource Alerts Last 90 Days"),
        place(take("alerts", "ConfigSource Alerts in last 90 days"), 23, 1, 6, 4, name="ConfigSource Alerts Last 90 Days"),
        place(take("alerts", "LogSource Alerts in last 90 days"), 23, 7, 6, 4, name="LogSource Alerts Last 90 Days"),
        place(take("alerts", "Top Datasources by Instance Count"), 27, 1, 12, 4, name="Top Datasources by Instance Count"),
        footer_links(
            [
                ("Active Alerts", "21"),
                ("Adoption", "33"),
                ("Technical Investigation", "30"),
            ],
            row=31,
        ),
    ]
    return make_dashboard(
        "32 - LogicModule and Content",
        "Technical content inventory and noisy LogicModules.",
        MODULE_TOKENS,
        widgets,
    )


def build_33() -> dict:
    widgets = [
        global_nav_widget("33", row=1, sizey=5),
        guide_widget(
            "Adoption and Optimization — Read First",
            "Adoption and Optimization",
            "Continuous improvement and platform value signals for CS and leadership.",
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
                ("Platform Value", "11 — close the loop"),
                ("Active Alerts", "21"),
                ("Access", "25"),
                ("Coverage", "24"),
            ],
            row=6,
            sizey=5,
        ),
        section_banner("Alert noise and improvement signals", row=11),
        place(take("alerts", "Alert Counts over time"), 13, 1, 6, 4, name="Alert Count Trend"),
        place(take("alerts", "Top Datasources by Alerts"), 13, 7, 6, 4, name="Top Noisy Datasources"),
        section_banner("Idle access summary", row=17),
        place(take("users", "Users not logged in last 90 days"), 19, 1, 3, 2, name="Idle Users (90 Days)"),
        place(take("users", "API Token not used in last 90 days"), 19, 4, 3, 2, name="Idle API Tokens (90 Days)"),
        place(take("users", "API Only Users not logged in last 90 days"), 19, 7, 3, 2, name="Idle API-Only Users (90 Days)"),
        place(take("users", "Empty User Groups"), 19, 10, 3, 2, name="Empty User Groups"),
        section_banner("Coverage gaps and integration health", row=21),
        place(take("alerts", "Number of Unmonitored Devices Over 90 days"), 23, 1, 6, 4, name="Unmonitored Devices Trend"),
        place(take("alerts", "Total Minimal Monitoring Resources over Time"), 23, 7, 6, 4, name="Minimal Monitoring Trend"),
        place(take("alerts", "Number of Integrations with Non 200 Response"), 27, 1, 6, 4, name="Integration Non-200 Trend"),
        place(take("alerts", "Top Dead Resources Over Time"), 27, 7, 6, 4, name="Dead Resources Trend"),
        text_widget(
            "LM Logs Adoption Note",
            """<div style="font-family:Arial,Helvetica,sans-serif;line-height:1.45;background:#0f172a;color:#e5e7eb;border:1px solid #1f2937;border-radius:14px;padding:18px;">
<div style="font-size:20px;font-weight:700;color:#f9fafb;">LM Logs (optional)</div>
<div style="font-size:13px;color:#9ca3af;margin-top:4px;">Raw log streams are intentionally excluded. LogSources inventory and alert tables appear on Modules / Alerts as health signals. Add a dedicated Logs strip only after LM Logs licensing is confirmed.</div>
</div>""",
            row=31,
            sizey=2,
        ),
        footer_links(
            [
                ("Platform Value Overview", "11"),
                ("Active Alerts", "21"),
                ("Access and Administration", "25"),
                ("Coverage", "24"),
            ],
            row=33,
        ),
    ]
    return make_dashboard(
        "33 - Adoption and Optimization",
        "Technical / value view: noise, idle access, coverage gaps, and integration health.",
        PORTAL_TOKENS,
        widgets,
    )


def build_34() -> dict:
    """NEW — Technology Dashboard Directory (OOTB hubs, no empty metric boards)."""
    widgets = [
        global_nav_widget("34", row=1, sizey=5),
        guide_widget(
            "Technology Directory — Read First",
            "Technology Dashboard Directory",
            "Single directory for Network, Server, Virtualization, Storage, Cloud, and Capacity OOTB boards. Avoids empty per-domain shells.",
            [
                "Which technology family matches the incident?",
                "Have OOTB packs been imported?",
                "Are portal dashboard IDs configured?",
            ],
            [
                ("Pick family", "Network / Server / Storage / Cloud / Capacity"),
                ("Confirm import", "LogicMonitor Dashboards pack"),
                ("Wire ID", "Replace OOTB_* placeholders"),
                ("Return", "Investigation hub when done"),
            ],
            [
                ("Technical Investigation", "30"),
                ("Collector Diagnostics", "31"),
                ("Capacity Risk Exec", "14"),
            ],
            row=6,
            sizey=5,
        ),
        tech_directory_panel(row=11, sizey=4),
        dcc_nav_guide(
            "Domain Guidance",
            "How to choose a technology board",
            [
                ("Network", "Path / device symptoms", ["Latency", "Interface errors", "Topology alerts"]),
                ("Compute", "Server / virtualization", ["CPU / memory", "Guest health", "Hypervisor"]),
                ("Data", "Storage / capacity", ["Datastore full", "IOPS", "License pressure"]),
                ("Cloud", "AWS / Azure / GCP", ["Account health", "Service quotas", "Regional impact"]),
            ],
            row=17,
            sizey=4,
        ),
        footer_links(
            [
                ("Technical Resource Investigation", "30"),
                ("Collector Diagnostics", "31"),
                ("Capacity and Risk Overview", "14"),
                ("Home", "00"),
            ],
            row=21,
        ),
    ]
    return make_dashboard(
        "34 - Technology Dashboard Directory",
        "Technical directory of OOTB technology dashboards (placeholders). No empty metric shells.",
        PORTAL_TOKENS,
        widgets,
    )


# filename, folder, builder, subgroup key
DASHBOARD_SPECS = [
    ("00_Home_Introductory_redesign_v2.json", EXEC, build_00, "home"),
    ("10_Executive_Command_Center_redesign_v2.json", EXEC, build_10, "executive"),
    ("11_Platform_Value_Overview_redesign_v2.json", EXEC, build_11, "executive"),
    ("12_Environment_Health_Executive_redesign_v2.json", EXEC, build_12, "executive"),
    ("13_Availability_and_Service_Health_redesign_v2.json", EXEC, build_13, "executive"),
    ("14_Capacity_and_Risk_Overview_redesign_v2.json", EXEC, build_14, "executive"),
    ("20_Operational_Command_Center_redesign_v2.json", OPS, build_20, "operational"),
    ("21_Active_Alerts_redesign_v2.json", OPS, build_21, "operational"),
    ("22_Resource_Health_redesign_v2.json", OPS, build_22, "operational"),
    ("23_Websites_and_Services_redesign_v2.json", OPS, build_23, "operational"),
    ("24_Coverage_Capacity_Licenses_redesign_v2.json", OPS, build_24, "operational"),
    ("25_Access_and_Administration_redesign_v2.json", OPS, build_25, "operational"),
    ("30_Technical_Resource_Investigation_redesign_v2.json", TECH, build_30, "technical"),
    ("31_Collector_Diagnostics_redesign_v2.json", TECH, build_31, "technical"),
    ("32_LogicModule_and_Content_redesign_v2.json", TECH, build_32, "technical"),
    ("33_Adoption_and_Optimization_redesign_v2.json", TECH, build_33, "technical"),
    ("34_Technology_Dashboard_Directory_redesign_v2.json", TECH, build_34, "technical"),
]


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def make_subgroup(name: str, description: str, dashboards: list) -> dict:
    return {
        "santabaRelease": 242,
        "widgetTokens": [],
        "name": name,
        "description": description,
        "type": "dashboardgroup",
        "dashboards": dashboards,
        "subGroups": [],
        "version": 2,
    }


def main() -> None:
    # Remove legacy level-* folders and stale filenames in group folders
    for legacy in ("level-1-executive", "level-2-operational", "level-3-technical"):
        p = OUT_DIR / legacy
        if p.exists():
            shutil.rmtree(p)

    keep_names = {filename for filename, _, _, _ in DASHBOARD_SPECS}
    for folder in (EXEC, OPS, TECH):
        folder.mkdir(parents=True, exist_ok=True)
        for f in folder.glob("*_redesign_v2.json"):
            if f.name not in keep_names:
                f.unlink()
                print(f"Removed stale {folder.name}/{f.name}")

    built: dict[str, list] = {"home": [], "executive": [], "operational": [], "technical": []}

    for filename, folder, builder, group_key in DASHBOARD_SPECS:
        dash = builder()
        write_json(folder / filename, dash)
        built[group_key].append(dash)
        print(f"Wrote {folder.name}/{filename} ({len(dash['widgets'])} widgets)")

    # Nested group: Home at root + three named subgroups
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
            "Connected Experience redesign v2 with Executive, Operational, and Technical subgroups. "
            "Home is the package entry point. Configure portal URL/dashboard ID placeholders and accountname after import. "
            "Portal assigns subgroup IDs — do not reuse IDs from other portals."
        ),
        "type": "dashboardgroup",
        "dashboards": built["home"],
        "subGroups": [
            make_subgroup(
                "Executive",
                "Leadership visibility: command center, platform value, environment, availability, capacity risk.",
                built["executive"],
            ),
            make_subgroup(
                "Operational",
                "Daily monitoring and triage: command center, alerts, resource health, websites, coverage, access.",
                built["operational"],
            ),
            make_subgroup(
                "Technical",
                "Investigation: resource hub, collector diagnostics, modules, adoption, OOTB technology directory.",
                built["technical"],
            ),
        ],
        "version": 2,
    }
    group_path = OUT_DIR / "SmartAdmin_Connected_Experience_redesign_v2.json"
    write_json(group_path, group)
    print(
        f"Wrote group {group_path} with {len(built['home'])} root + "
        f"{sum(len(built[k]) for k in ('executive', 'operational', 'technical'))} subgroup dashboards"
    )


if __name__ == "__main__":
    main()
