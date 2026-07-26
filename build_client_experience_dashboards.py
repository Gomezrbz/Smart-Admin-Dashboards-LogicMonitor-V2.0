#!/usr/bin/env python3
"""Assemble SmartAdmin Client Experience dashboard group JSON for LogicMonitor import.

Reuses widgets from existing SmartAdmin / Introductive exports per
DASHBOARD_EXPERIENCE_PROPOSAL.md. Does not modify production source exports.
"""

from __future__ import annotations

import copy
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "SmartAdmin_Client_Experience_Dashboards.json"

SA = json.loads((ROOT / "SmartAdmin Dashboards.json").read_text(encoding="utf-8"))
INTRO = json.loads((ROOT / "Introductive_Dashboard.json").read_text(encoding="utf-8"))

BY_NAME = {d["name"]: d for d in SA["dashboards"]}


def index_widgets(dashboard: dict) -> dict:
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
    "collector": index_widgets(BY_NAME["SmartAdmin Collector Health"]),
    "intro": index_widgets(INTRO),
}


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
    return w


def guide_widget(
    name: str,
    title: str,
    subtitle: str,
    questions: list[str],
    flow_steps: list[tuple[str, str]],
    next_steps: list[str],
    row: int,
    sizey: int = 6,
) -> dict:
    q_html = "".join(f'<li style="margin:6px 0;">{escape(q)}</li>' for q in questions)
    flow_html = "".join(
        f'<li style="margin:6px 0;"><strong>{escape(s[0])}</strong> — {escape(s[1])}</li>'
        for s in flow_steps
    )
    next_html = "".join(f'<li style="margin:6px 0;">{escape(n)}</li>' for n in next_steps)
    content = f"""<div style="font-family:Arial,Helvetica,sans-serif;line-height:1.45;background:#0f172a;color:#e5e7eb;border:1px solid #1f2937;border-radius:14px;padding:18px;width:100%;box-sizing:border-box;">
<div style="font-size:20px;font-weight:700;color:#f9fafb;margin-bottom:4px;">{escape(title)}</div>
<div style="font-size:13px;color:#9ca3af;margin-bottom:14px;">{escape(subtitle)}</div>
<table style="width:100%;border-collapse:separate;border-spacing:12px;"><tr>
<td style="vertical-align:top;background:#020617;border:1px solid #1f2937;border-radius:12px;padding:14px;width:33%;">
<div style="font-size:14px;font-weight:700;margin-bottom:8px;color:#f9fafb;">Questions this dashboard answers</div>
<ul style="margin:0;padding-left:18px;">{q_html}</ul>
</td>
<td style="vertical-align:top;background:#020617;border:1px solid #1f2937;border-radius:12px;padding:14px;width:34%;">
<div style="font-size:14px;font-weight:700;margin-bottom:8px;color:#f9fafb;">Recommended review flow</div>
<ol style="margin:0;padding-left:18px;">{flow_html}</ol>
</td>
<td style="vertical-align:top;background:#020617;border:1px solid #1f2937;border-radius:12px;padding:14px;width:33%;">
<div style="font-size:14px;font-weight:700;margin-bottom:8px;color:#f9fafb;">Where to go next</div>
<ul style="margin:0;padding-left:18px;">{next_html}</ul>
<div style="margin-top:12px;font-size:12px;color:#94a3b8;">If a section shows zero or no data, confirm tokens (defaultResource / defaultResourceGroup) and that related LogicModules are applied.</div>
</td>
</tr></table>
</div>"""
    return {
        "position": {"col": 1, "sizex": 12, "row": row, "sizey": sizey},
        "config": {
            "displaySettings": {},
            "isSupportCustomProperty": False,
            "supportCustomProperty": False,
            "name": name,
            "description": "Read this guide first. It explains the purpose of the dashboard and where to drill down.",
            "theme": "newSolidDarkBlue",
            "interval": 15,
            "type": "text",
            "timescale": "day",
            "version": 2,
            "content": content,
        },
    }


def section_banner(title: str, row: int, sizey: int = 2) -> dict:
    content = (
        '<p><style type="text/css">\n'
        "\t\t.html-wpsites {\n"
        "\t\t\theight: 72px; background-color: rgba(0, 0, 0, 0); font-family: Arial; "
        "font-size: 32px; color: #ffffff; font-weight: bold; text-align: center;\n"
        "\t\t}\n\n\t</style></p>"
        f'<div class="html-wpsites">{escape(title)}</div><p>&nbsp;</p>'
    )
    return {
        "position": {"col": 1, "sizex": 12, "row": row, "sizey": sizey},
        "config": {
            "displaySettings": {},
            "isSupportCustomProperty": False,
            "supportCustomProperty": False,
            "name": title,
            "description": "",
            "theme": "newSolidDarkBlue",
            "interval": 15,
            "type": "text",
            "timescale": "day",
            "version": 2,
            "content": content,
        },
    }


def nav_widget(row: int, sizey: int = 5) -> dict:
    content = """<div style="font-family:Arial,Helvetica,sans-serif;line-height:1.45;background:#0b1220;color:#e5e7eb;border:1px solid #1f2a44;border-radius:16px;padding:18px;width:100%;box-sizing:border-box;">
<div style="font-size:18px;font-weight:700;color:#ffffff;margin-bottom:6px;">SmartAdmin Client Experience — Navigation</div>
<div style="font-size:13px;color:#a5b4fc;margin-bottom:14px;">Use the dashboard group menu to open each view. Drill down only when a KPI, map, NOC, or alert signal requires action.</div>
<table style="width:100%;border-collapse:separate;border-spacing:10px;"><tr>
<td style="vertical-align:top;background:#020617;border:1px solid #1f2937;border-radius:12px;padding:12px;width:25%;">
<div style="font-weight:700;margin-bottom:8px;">Tier 1 — Start here</div>
<ul style="margin:0;padding-left:18px;font-size:13px;">
<li><strong>01 Platform Value Overview</strong> — health, coverage, where next</li>
<li><strong>02 Environment and Alert Health</strong> — triage active problems</li>
<li><strong>05 Collector Health</strong> — monitoring pipeline integrity</li>
</ul></td>
<td style="vertical-align:top;background:#020617;border:1px solid #1f2937;border-radius:12px;padding:12px;width:25%;">
<div style="font-weight:700;margin-bottom:8px;">Tier 2 — Admin hygiene</div>
<ul style="margin:0;padding-left:18px;font-size:13px;">
<li><strong>03 Monitoring Coverage and Licenses</strong></li>
<li><strong>04 Access and Governance</strong></li>
<li><strong>06 LogicModule and Content</strong></li>
</ul></td>
<td style="vertical-align:top;background:#020617;border:1px solid #1f2937;border-radius:12px;padding:12px;width:25%;">
<div style="font-weight:700;margin-bottom:8px;">Tier 3 — Value</div>
<ul style="margin:0;padding-left:18px;font-size:13px;">
<li><strong>07 Adoption and Optimization</strong> — noise, idle access, coverage gaps, integrations</li>
</ul></td>
<td style="vertical-align:top;background:#020617;border:1px solid #1f2937;border-radius:12px;padding:12px;width:25%;">
<div style="font-weight:700;margin-bottom:8px;">Client ops (optional)</div>
<div style="font-size:12px;color:#94a3b8;">Link your environment-specific service health dashboards here (for example Service Health, network, cloud). Those views are outside this portal-admin pack.</div>
</td>
</tr></table>
</div>"""
    return {
        "position": {"col": 1, "sizex": 12, "row": row, "sizey": sizey},
        "config": {
            "displaySettings": {},
            "isSupportCustomProperty": False,
            "supportCustomProperty": False,
            "name": "Suite Navigation Guide",
            "description": "Navigation across the SmartAdmin Client Experience dashboard group.",
            "theme": "newSolidDarkBlue",
            "interval": 15,
            "type": "text",
            "timescale": "day",
            "version": 2,
            "content": content,
        },
    }


PORTAL_TOKENS = [
    {"name": "defaultResource", "value": "*.logicmonitor.com"},
    {"name": "defaultResourceGroup", "value": "*"},
]
COLLECTOR_TOKENS = [
    {"name": "defaultResourceGroup", "value": "*"},
    {"name": "defaultResourceName", "value": "*"},
]
LICENSE_TOKENS = [
    {"name": "accountname", "value": "proservices"},
    {"name": "defaultResourceGroup", "value": "*"},
    {"name": "defaultResource", "value": "*.logicmonitor.com"},
]
MODULE_TOKENS = [
    {"name": "defaultResourceGroup", "value": "*"},
    {"name": "defaultResourceName", "value": "*.logicmonitor.com"},
]


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


def build_01() -> dict:
    widgets = [
        guide_widget(
            "Platform Value Overview — Read First",
            "Platform Value Overview",
            "Executive landing page for SmartAdmin Client Experience. Confirm health, coverage, and where to drill.",
            [
                "Are we healthy right now (alert posture)?",
                "Are collectors alive and monitoring continuous?",
                "What is our monitored footprint and license summary?",
                "Where should I go next for investigation?",
            ],
            [
                ("KPI strip", "Review alert, collector, resource, and license scorecards"),
                ("Map / NOC", "Check geographic and resource-type concentration"),
                ("Navigate", "Open 02 for alerts, 05 for collectors, 03 for coverage/licenses"),
            ],
            [
                "Elevated Critical/Error → 02 Environment and Alert Health",
                "Collector down or collector alerts → 05 Collector Health",
                "Coverage or license questions → 03 Monitoring Coverage and Licenses",
                "Idle access concerns → 04 Access and Governance",
                "Module noise → 06 LogicModule and Content",
            ],
            row=1,
            sizey=6,
        ),
        place(
            take("overview", "Total Ack'd and Unack'd Warning Alerts"),
            8,
            1,
            3,
            2,
            name="Warning alerts (ack'd and unack'd)",
            description="Current warning alert volume including acknowledged and unacknowledged.",
        ),
        place(
            take("overview", "Total Ack'd and Unack'd Error Alerts"),
            8,
            4,
            3,
            2,
            name="Error alerts (ack'd and unack'd)",
            description="Current error alert volume including acknowledged and unacknowledged.",
        ),
        place(
            take("overview", "Total Ack'd and Unack'd Critical Alerts"),
            8,
            7,
            3,
            2,
            name="Critical alerts (ack'd and unack'd)",
            description="Current critical alert volume including acknowledged and unacknowledged.",
        ),
        place(
            take("overview", "Total Number of Ack'd and Unack'd Alerts"),
            8,
            10,
            3,
            2,
            name="Total alerts (ack'd and unack'd)",
            description="Combined alert volume across severities.",
        ),
        place(
            take("overview", "Total Number of Alive Collectors"),
            11,
            1,
            3,
            2,
            name="Alive collectors",
            description="Collectors currently reporting as alive.",
        ),
        place(
            take("overview", "Total Number of Down Collectors"),
            11,
            4,
            3,
            2,
            name="Down collectors",
            description="Collectors currently down — drill to 05 if elevated.",
        ),
        place(
            take("alerts", "Total Number of Resources"),
            11,
            7,
            3,
            2,
            name="Total resources",
            description="Monitored resource footprint.",
        ),
        place(
            take("alerts", "Total Number of Cloud Resources"),
            11,
            10,
            3,
            2,
            name="Cloud resources",
            description="Cloud resource footprint.",
        ),
        place(
            take("overview", "Local Resource Licenses"),
            14,
            1,
            3,
            2,
            name="Local resource licenses",
            description="Local license summary — see 03 for cloud breakdown.",
        ),
        place(
            take("overview", "Cloud Resource Licences"),
            14,
            4,
            3,
            2,
            name="Cloud resource licenses",
            description="Cloud license summary — see 03 for provider detail.",
        ),
        place(
            take("overview", "LogSources"),
            14,
            7,
            3,
            2,
            name="LogSources (coverage)",
            description="LogSource inventory count (coverage signal, not log volume).",
        ),
        place(
            take("overview", "Active Users"),
            14,
            10,
            3,
            2,
            name="Active users",
            description="Active portal users — see 04 for access hygiene.",
        ),
        place(
            take("overview", "Alert Status by Resource Location"),
            17,
            1,
            6,
            5,
            description="Geographic concentration of alert status.",
        ),
        place(
            take("overview", "Alert Status by Resource Types"),
            17,
            7,
            6,
            5,
            description="Alert status by resource type (NOC).",
        ),
        place(
            take("overview", "Alert Counts over time"),
            23,
            1,
            12,
            4,
            name="Alert counts over time",
            description="Short-term alert trend for executive awareness.",
        ),
        nav_widget(28, sizey=5),
        place(
            take("intro", "Alerts Resources"),
            34,
            1,
            12,
            5,
            name="Learn — Alerts in LogicMonitor",
            description="Training and documentation links for alert management.",
        ),
        place(
            take("intro", "Collectors Resources"),
            40,
            1,
            12,
            5,
            name="Learn — Collectors in LogicMonitor",
            description="Training and documentation links for collectors.",
        ),
    ]
    return make_dashboard(
        "01 - Platform Value Overview",
        "Executive entry dashboard: platform health, coverage, licenses summary, navigation, and learning links. Start here.",
        PORTAL_TOKENS,
        widgets,
    )


def build_02() -> dict:
    widgets = [
        guide_widget(
            "Environment and Alert Health — Read First",
            "Environment and Alert Health",
            "Operational cockpit for severity, active exceptions, resource health, and alert routing.",
            [
                "What is alerting, and at which severity?",
                "Where is impact concentrated (map / type)?",
                "Which resources are dead or minimally monitored?",
                "Are integrations and escalation paths healthy?",
            ],
            [
                ("Severity KPIs", "Confirm Critical/Error/Warning volume"),
                ("Alert list", "Identify affected resources and context"),
                ("Hygiene", "Review dead/minimal resources and noise summary"),
                ("Collectors", "If collector alerts appear, open 05"),
            ],
            [
                "Collector alerts → 05 Collector Health",
                "Discovery / unmonitored gaps → 03",
                "Noisy modules detail → 06 LogicModule and Content",
                "Zero alerts — still review Warning trend and dead resources",
            ],
            row=1,
            sizey=6,
        ),
        place(
            take("alerts", "Total Number of Warning Alerts"),
            8,
            1,
            3,
            2,
            name="Warning alerts",
            description="Current warning alert count.",
        ),
        place(
            take("alerts", "Total Number of Error Alerts"),
            8,
            4,
            3,
            2,
            name="Error alerts",
            description="Current error alert count.",
        ),
        place(
            take("alerts", "Total Number of Critical Alerts"),
            8,
            7,
            3,
            2,
            name="Critical alerts",
            description="Current critical alert count.",
        ),
        place(
            take("alerts", "Total Number of Alerts"),
            8,
            10,
            3,
            2,
            name="Total alerts",
            description="Total alert count across severities.",
        ),
        place(
            take("alerts", "Alert Counts over time"),
            11,
            1,
            6,
            4,
            name="Alert counts over time (ops)",
            description="Operational alert trend.",
        ),
        place(
            take("alerts", "Top Datasources by Alerts"),
            11,
            7,
            6,
            4,
            description="Top datasources contributing alerts.",
        ),
        place(
            take("overview", "All Resource Alerts"),
            16,
            1,
            6,
            6,
            description="Active resource alerts. Use Log Metadata / Logs Partition columns when present, then continue in native LM workflows.",
        ),
        place(
            take("overview", "Current Collector Alerts"),
            16,
            7,
            6,
            6,
            description="Collector-related alerts — drill to 05 Collector Health.",
        ),
        place(
            take("overview", "Alert Status by Resource Location"),
            23,
            1,
            6,
            5,
            name="Alert status by resource location (ops)",
            description="Geographic concentration for triage.",
        ),
        place(
            take("overview", "Alert Status by Resource Types"),
            23,
            7,
            6,
            5,
            name="Alert status by resource types (ops)",
            description="NOC view by resource type.",
        ),
        section_banner("Alert routing and integrations", 29),
        place(
            take("alerts", "Alert Rules"),
            32,
            1,
            4,
            4,
            description="Configured alert rules.",
        ),
        place(
            take("alerts", "Escalation Chains inUse by Alert Rules"),
            32,
            5,
            4,
            4,
            description="Escalation chains in use by alert rules.",
        ),
        place(
            take("alerts", "Total Number of Escalation Chains"),
            32,
            9,
            2,
            2,
            name="Escalation chains",
            description="Total escalation chains.",
        ),
        place(
            take("alerts", "Total Number of Portal Integration"),
            34,
            9,
            2,
            2,
            name="Portal integrations",
            description="Total portal integrations.",
        ),
        place(
            take("alerts", "Number of Integrations with Non 200 Response"),
            37,
            1,
            12,
            4,
            description="Integration delivery health (non-200 responses).",
        ),
        section_banner("Resources needing attention", 42),
        place(
            take("alerts", "Total Number of Dead Resources"),
            45,
            1,
            3,
            2,
            name="Dead resources",
            description="Resources currently dead.",
        ),
        place(
            take("alerts", "Total Number of Minimal Monitoring Resource"),
            45,
            4,
            3,
            2,
            name="Minimal monitoring resources",
            description="Resources under minimal monitoring.",
        ),
        place(
            take("alerts", "Total Number of SDT Resource"),
            45,
            7,
            3,
            2,
            name="Resources in SDT",
            description="Resources currently in scheduled downtime.",
        ),
        place(
            take("alerts", "Total Number of Netflow Resource"),
            45,
            10,
            3,
            2,
            name="Netflow resources",
            description="Resources with Netflow enabled.",
        ),
        place(
            take("alerts", "Top Dead Resources Over Time"),
            48,
            1,
            6,
            4,
            description="Dead resource trend.",
        ),
        place(
            take("alerts", "Total Minimal Monitoring Resources over Time"),
            48,
            7,
            6,
            4,
            description="Minimal monitoring trend.",
        ),
        place(
            take("alerts", "Idle Interval"),
            53,
            1,
            12,
            4,
            description="Idle interval table for host attention.",
        ),
        section_banner("LogicModule alert noise (summary) — detail on 06", 58),
        place(
            take("alerts", "Datasource Alerts in last 90 days"),
            61,
            1,
            6,
            4,
            name="DataSource alerts (90 days) — summary",
            description="Summary table. Content owners should tune from 06 LogicModule and Content.",
        ),
        place(
            take("alerts", "LogSource Alerts in last 90 days"),
            61,
            7,
            6,
            4,
            name="LogSource alerts (90 days) — summary",
            description="LogSource alert noise as a health signal (not a log stream).",
        ),
    ]
    return make_dashboard(
        "02 - Environment and Alert Health",
        "Operational alert cockpit: severity, active alerts, resource hygiene, integrations, and LogicModule noise summary including LogSources.",
        PORTAL_TOKENS,
        widgets,
    )


def build_03() -> dict:
    widgets = [
        guide_widget(
            "Monitoring Coverage and Licenses — Read First",
            "Monitoring Coverage and Licenses",
            "Discovery coverage, unmonitored gaps, website/group hygiene, and full license breakdown.",
            [
                "Are netscans discovering devices?",
                "Are unmonitored or minimal-monitoring gaps growing?",
                "Is group/website structure healthy?",
                "How are local and cloud licenses consumed?",
            ],
            [
                ("Discovery", "Review netscan totals and unmonitored trends"),
                ("Hygiene", "Check empty groups and dead websites"),
                ("Licenses", "Review provider and local license scorecards"),
            ],
            [
                "Alert impact of gaps → 02",
                "Module coverage questions → 06",
                "Confirm accountname token if license widgets are empty",
            ],
            row=1,
            sizey=6,
        ),
        section_banner("Discovery and coverage", 8),
        place(take("alerts", "Total Number of Netscans"), 11, 1, 3, 2, name="Netscans (total)"),
        place(take("alerts", "Total Number of Netscans - Scheduled"), 11, 4, 3, 2, name="Netscans — scheduled"),
        place(take("alerts", "Total Number of Netscans - Script"), 11, 7, 3, 2, name="Netscans — script"),
        place(take("alerts", "Total Number of Netscans - Nmap"), 11, 10, 3, 2, name="Netscans — nmap"),
        place(take("alerts", "Total Number of Netscans - EC2"), 14, 1, 3, 2, name="Netscans — EC2"),
        place(
            take("alerts", "Total Number of Netscans - Enhanced Script"),
            14,
            4,
            3,
            2,
            name="Netscans — enhanced script",
        ),
        place(
            take("alerts", "Total Number of Minimal Monitoring Resource"),
            14,
            7,
            3,
            2,
            name="Minimal monitoring resources",
            description="Coverage gap indicator.",
        ),
        place(
            take("alerts", "Total Number of Dead Resources"),
            14,
            10,
            3,
            2,
            name="Dead resources",
            description="Availability/coverage concern.",
        ),
        place(take("alerts", "Netscans"), 17, 1, 6, 4, name="Netscans table", description="Netscan inventory table."),
        # There are two widgets named Netscans (banner text + table). Prefer dynamicTable.
        place(
            take("alerts", "Number of Unmonitored Devices Over 90 days"),
            17,
            7,
            6,
            4,
            description="Unmonitored device trend over 90 days.",
        ),
        place(
            take("alerts", "Number of Netscan Devices Added Per Day Over 90 Days"),
            22,
            1,
            6,
            4,
            description="Discovery throughput trend.",
        ),
        place(
            take("alerts", "Total Minimal Monitoring Resources over Time"),
            22,
            7,
            6,
            4,
            name="Minimal monitoring over time",
            description="Minimal monitoring drift.",
        ),
        section_banner("Device groups and websites", 27),
        place(take("groups", "Total Number of Device Groups"), 30, 1, 3, 2, name="Device groups"),
        place(take("groups", "Total Number of Static Device Groups"), 30, 4, 3, 2, name="Static device groups"),
        place(take("groups", "Total Number of Empty Static Groups"), 30, 7, 3, 2, name="Empty static groups"),
        place(take("groups", "Total Number of Dynamic Device Groups"), 30, 10, 3, 2, name="Dynamic device groups"),
        place(take("groups", "Total Number of Website Groups"), 33, 1, 3, 2, name="Website groups"),
        place(take("groups", "Total Number of Websites"), 33, 4, 3, 2, name="Websites"),
        place(take("groups", "Total Number of Empty Website Groups"), 33, 7, 3, 2, name="Empty website groups"),
        place(take("groups", "Total Number of Dead Website"), 33, 10, 3, 2, name="Dead websites"),
        section_banner("License consumption", 36),
        place(take("licenses", "Local Licenses"), 39, 1, 3, 2),
        place(take("licenses", "Local Licenses Percents"), 39, 4, 3, 2),
        place(take("licenses", "IaaS - Total"), 39, 7, 3, 2, name="IaaS — total"),
        place(take("licenses", "PaaS - Total"), 39, 10, 3, 2, name="PaaS — total"),
        place(take("licenses", "Non-Compute - Total"), 42, 1, 3, 2, name="Non-compute — total"),
        place(take("licenses", "AWS - IaaS"), 42, 4, 3, 2, name="AWS — IaaS"),
        place(take("licenses", "AWS - PaaS"), 42, 7, 3, 2, name="AWS — PaaS"),
        place(take("licenses", "AWS - Non-Compute"), 42, 10, 3, 2, name="AWS — non-compute"),
        place(take("licenses", "Azure - IaaS"), 45, 1, 3, 2, name="Azure — IaaS"),
        place(take("licenses", "Azure - PaaS"), 45, 4, 3, 2, name="Azure — PaaS"),
        place(take("licenses", "Azure - Non-Compute"), 45, 7, 3, 2, name="Azure — non-compute"),
        place(take("licenses", "GCP - IaaS"), 48, 1, 3, 2, name="GCP — IaaS"),
        place(take("licenses", "GCP - PaaS"), 48, 4, 3, 2, name="GCP — PaaS"),
        place(take("licenses", "GCP - Non-Compute"), 48, 7, 3, 2, name="GCP — non-compute"),
    ]
    # Fix Netscans table: pick dynamicTable occurrence if banner grabbed first
    for i, w in enumerate(widgets):
        if w["config"].get("name") == "Netscans table" and w["config"].get("type") != "dynamicTable":
            # replace with dynamicTable occurrence
            for occ, cand in enumerate(W["alerts"]["Netscans"]):
                if cand["config"]["type"] == "dynamicTable":
                    widgets[i] = place(
                        take("alerts", "Netscans", occur=occ),
                        17,
                        1,
                        6,
                        4,
                        name="Netscans table",
                        description="Netscan inventory table.",
                    )
                    break
    return make_dashboard(
        "03 - Monitoring Coverage and Licenses",
        "Discovery coverage (netscans/unmonitored), device/website group hygiene, and full cloud/local license breakdown. Confirm accountname token per portal.",
        LICENSE_TOKENS,
        widgets,
    )


def build_04() -> dict:
    widgets = [
        guide_widget(
            "Access and Governance — Read First",
            "Access and Governance",
            "User, role, group, and API token hygiene for portal security posture.",
            [
                "How many active vs idle users and tokens?",
                "Are there unused roles or empty groups?",
                "Is API-only access sprawling?",
            ],
            [
                ("Inventory", "Review user/role/group/token counts"),
                ("Idle access", "Prioritize 90-day idle users and tokens"),
                ("Cleanup", "Coordinate with security owners"),
            ],
            [
                "Platform value narrative → 07 Adoption and Optimization",
                "Return to 01 after cleanup to confirm Active users KPI",
            ],
            row=1,
            sizey=5,
        ),
        place(take("users", "Users"), 7, 1, 3, 2, name="Users", description="Total users."),
        place(take("users", "Users with Active Status"), 7, 4, 3, 2, name="Users with active status"),
        place(take("users", "API Access Users"), 7, 7, 3, 2, name="API access users"),
        place(take("users", "API Only users"), 7, 10, 3, 2, name="API-only users"),
        place(take("users", "User Groups"), 10, 1, 3, 2, name="User groups"),
        place(take("users", "Empty User Groups"), 10, 4, 3, 2, name="Empty user groups"),
        place(take("users", "User Roles"), 10, 7, 3, 2, name="User roles"),
        place(take("users", "Roles with no assigned Users"), 10, 10, 3, 2, name="Roles with no assigned users"),
        place(take("users", "API Tokens"), 13, 1, 3, 2, name="API tokens"),
        place(
            take("users", "API Token not used in last 90 days"),
            13,
            4,
            3,
            2,
            name="API tokens unused (90 days)",
        ),
        place(
            take("users", "Users not logged in last 90 days"),
            13,
            7,
            3,
            2,
            name="Users not logged in (90 days)",
        ),
        place(
            take("users", "API Only Users not logged in last 90 days"),
            13,
            10,
            3,
            2,
            name="API-only users not logged in (90 days)",
        ),
    ]
    return make_dashboard(
        "04 - Access and Governance",
        "Portal access hygiene: users, roles, groups, API tokens, and idle access over 90 days.",
        PORTAL_TOKENS,
        widgets,
    )


def build_05() -> dict:
    """Single collector health dashboard — clone SmartAdmin Collector Health with guide prepended."""
    src_widgets = copy.deepcopy(BY_NAME["SmartAdmin Collector Health"]["widgets"])
    # Find min row among positioned widgets; many have null rows in export — keep relative layout
    # Shift all numeric rows down by guide height
    guide_rows = 6
    for w in src_widgets:
        pos = w.get("position") or {}
        row = pos.get("row")
        if isinstance(row, int):
            pos["row"] = row + guide_rows
            w["position"] = pos
        # Improve a few descriptions
        cname = w["config"].get("name", "")
        if cname == "Collector Alert History":
            w["config"]["description"] = "Collector alert history for pipeline troubleshooting."
        if cname == "Collector JVM Performance (Real-time)":
            w["config"]["description"] = "Real-time collector JVM performance."

    guide = guide_widget(
        "Collector Health — Read First",
        "Collector Health",
        "Single technical dashboard for collector availability and collection performance. Duplicate collector dashboards from the old pack are intentionally collapsed here.",
        [
            "Are collectors under JVM/CPU/heap pressure?",
            "Which collection or Active Discovery tasks are slow or failing?",
            "Is the method mix (SNMP/WMI/script/etc.) balanced?",
        ],
        [
            ("Instance counts", "Confirm collection method distribution"),
            ("JVM / trends", "Check heap and CPU leaders"),
            ("Tasks", "Inspect slow collection and AD failure tables/graphs"),
        ],
        [
            "Alert impact → 02 Environment and Alert Health",
            "Return to 01 after remediation to confirm Alive/Down collectors",
        ],
        row=1,
        sizey=5,
    )
    widgets = [guide] + src_widgets
    return make_dashboard(
        "05 - Collector Health",
        "Canonical collector health dashboard (merged from previously duplicated Collector Health views): instance counts, JVM, tasks, and collector alerts.",
        COLLECTOR_TOKENS,
        widgets,
    )


def build_06() -> dict:
    widgets = [
        guide_widget(
            "LogicModule and Content — Read First",
            "LogicModule and Content",
            "Content inventory and alert-noise tables for module owners. LogSources appear as coverage and noise signals, not log streams.",
            [
                "What LogicModules are installed (including LogSources)?",
                "Which modules generate the most alerts over 90 days?",
                "Which datasources have the largest instance counts?",
            ],
            [
                ("Inventory", "Review module type scorecards"),
                ("Noise", "Tune top DataSource/EventSource/ConfigSource/LogSource alert tables"),
                ("Scale", "Review top datasources by instance count"),
            ],
            [
                "Ops triage of active alerts → 02",
                "Adoption / noise reduction narrative → 07",
            ],
            row=1,
            sizey=5,
        ),
        place(take("modules", "DataSources"), 7, 1, 3, 2, name="DataSources"),
        place(take("modules", "EventSources"), 7, 4, 3, 2, name="EventSources"),
        place(take("modules", "ConfigSources"), 7, 7, 3, 2, name="ConfigSources"),
        place(take("modules", "PropertySources"), 7, 10, 3, 2, name="PropertySources"),
        place(take("modules", "LogSources"), 10, 1, 3, 2, name="LogSources", description="LogSource inventory (coverage)."),
        place(take("modules", "TopologySources"), 10, 4, 3, 2, name="TopologySources"),
        place(take("modules", "SNMP SYSOID Maps"), 10, 7, 3, 2, name="SNMP SYSOID maps"),
        place(take("modules", "AppliesTo Functions"), 10, 10, 3, 2, name="AppliesTo functions"),
        section_banner("Alert noise by LogicModule type (90 days)", 13),
        place(
            take("alerts", "Datasource Alerts in last 90 days"),
            16,
            1,
            6,
            4,
            name="DataSource alerts (90 days)",
            description="Primary tuning list for content owners.",
        ),
        place(
            take("alerts", "EventSource Alerts in last 90 days"),
            16,
            7,
            6,
            4,
            name="EventSource alerts (90 days)",
        ),
        place(
            take("alerts", "ConfigSource Alerts in last 90 days"),
            21,
            1,
            6,
            4,
            name="ConfigSource alerts (90 days)",
        ),
        place(
            take("alerts", "LogSource Alerts in last 90 days"),
            21,
            7,
            6,
            4,
            name="LogSource alerts (90 days)",
            description="LogSource alert noise signal for content tuning.",
        ),
        place(
            take("alerts", "Top Datasources by Instance Count"),
            26,
            1,
            12,
            4,
            description="Largest datasources by instance count.",
        ),
        place(
            take("alerts", "Top Datasources by Alerts"),
            31,
            1,
            12,
            4,
            name="Top datasources by alerts (content)",
            description="Alert contribution by datasource for content owners.",
        ),
    ]
    return make_dashboard(
        "06 - LogicModule and Content",
        "LogicModule inventory and alert-noise tables (DataSource/EventSource/ConfigSource/LogSource) for content governance.",
        MODULE_TOKENS,
        widgets,
    )


def build_07() -> dict:
    widgets = [
        guide_widget(
            "Adoption and Optimization — Read First",
            "Adoption and Optimization",
            "Platform value and continuous improvement: alert noise, idle access, coverage gaps, and integration health. Optional LM Logs adoption metrics are deferred until licensing is confirmed.",
            [
                "Is alert noise concentrated in a few datasources?",
                "Are idle identities being cleaned up?",
                "Are coverage gaps (unmonitored/minimal/dead) improving?",
                "Are integrations delivering successfully?",
            ],
            [
                ("Noise", "Review alert trend and top noisy datasources"),
                ("Access", "Check idle users and tokens"),
                ("Coverage", "Review unmonitored/minimal/dead signals"),
                ("Integrations", "Inspect non-200 integration responses"),
            ],
            [
                "Deep alert triage → 02",
                "Access cleanup → 04",
                "Coverage remediation → 03",
                "Module tuning → 06",
            ],
            row=1,
            sizey=6,
        ),
        section_banner("Alert noise and trends", 8),
        place(
            take("overview", "Alert Counts over time"),
            11,
            1,
            6,
            4,
            name="Alert counts over time (value)",
            description="Alert volume trend for adoption storytelling.",
        ),
        place(
            take("alerts", "Top Datasources by Alerts"),
            11,
            7,
            6,
            4,
            name="Top datasources by alerts (value)",
            description="Concentration of alert noise.",
        ),
        section_banner("Idle access", 16),
        place(
            take("users", "Users not logged in last 90 days"),
            19,
            1,
            3,
            2,
            name="Users not logged in (90 days)",
        ),
        place(
            take("users", "API Only Users not logged in last 90 days"),
            19,
            4,
            3,
            2,
            name="API-only users not logged in (90 days)",
        ),
        place(
            take("users", "API Token not used in last 90 days"),
            19,
            7,
            3,
            2,
            name="API tokens unused (90 days)",
        ),
        place(take("users", "API Tokens"), 19, 10, 3, 2, name="API tokens (inventory)"),
        section_banner("Coverage gaps", 22),
        place(
            take("alerts", "Total Number of Dead Resources"),
            25,
            1,
            3,
            2,
            name="Dead resources",
        ),
        place(
            take("alerts", "Total Number of Minimal Monitoring Resource"),
            25,
            4,
            3,
            2,
            name="Minimal monitoring resources",
        ),
        place(
            take("alerts", "Number of Unmonitored Devices Over 90 days"),
            25,
            7,
            6,
            4,
            name="Unmonitored devices over 90 days",
        ),
        place(
            take("alerts", "Top Dead Resources Over Time"),
            30,
            1,
            6,
            4,
            name="Dead resources over time (value)",
        ),
        place(
            take("alerts", "Total Minimal Monitoring Resources over Time"),
            30,
            7,
            6,
            4,
            name="Minimal monitoring over time (value)",
        ),
        section_banner("Integration health", 35),
        place(
            take("alerts", "Total Number of Portal Integration"),
            38,
            1,
            3,
            2,
            name="Portal integrations",
        ),
        place(
            take("alerts", "Number of Integrations with Non 200 Response"),
            38,
            4,
            9,
            4,
            name="Integrations with non-200 responses",
            description="Integration delivery failures requiring remediation.",
        ),
        section_banner("Logs adoption (deferred)", 43, sizey=3),
    ]
    # Deferred LM Logs note as text widget
    deferred = {
        "position": {"col": 1, "sizex": 12, "row": 47, "sizey": 3},
        "config": {
            "displaySettings": {},
            "isSupportCustomProperty": False,
            "supportCustomProperty": False,
            "name": "LM Logs adoption — deferred pending license confirmation",
            "description": "Placeholder guidance only. Do not invent log analytics widgets without confirmed datasources.",
            "theme": "newSolidDarkBlue",
            "interval": 15,
            "type": "text",
            "timescale": "day",
            "version": 2,
            "content": """<div style="font-family:Arial,Helvetica,sans-serif;background:#0f172a;color:#e5e7eb;border:1px solid #1f2937;border-radius:12px;padding:16px;">
<div style="font-size:16px;font-weight:700;margin-bottom:8px;">LM Logs adoption strip — not included yet</div>
<div style="font-size:13px;color:#94a3b8;">Per the proposal, raw log streams and LM Logs analytics are excluded until licensing and available datasources/widgets are confirmed. LogSource inventory and LogSource alert tables remain on dashboards 01, 02, and 06 as coverage/noise signals.</div>
</div>""",
        },
    }
    widgets.append(deferred)
    return make_dashboard(
        "07 - Adoption and Optimization",
        "Platform value view: alert noise, idle access, coverage gaps, and integration health. LM Logs adoption deferred pending confirmation.",
        PORTAL_TOKENS,
        widgets,
    )


def main() -> None:
    dashboards = [
        build_01(),
        build_02(),
        build_03(),
        build_04(),
        build_05(),
        build_06(),
        build_07(),
    ]
    group = {
        "santabaRelease": 242,
        "widgetTokens": [],
        "name": "SmartAdmin Client Experience",
        "subGroups": [],
        "description": (
            "Progressive SmartAdmin Client Experience suite (01–07) aligned to "
            "DASHBOARD_EXPERIENCE_PROPOSAL.md. Reuses portal/collector widgets from "
            "SmartAdmin and Introductive exports. Import as a dashboard group. "
            "Confirm license accountname token and collector/resource tokens per portal."
        ),
        "type": "dashboardgroup",
        "version": 1,
        "dashboards": dashboards,
    }

    # Validation
    names = [d["name"] for d in dashboards]
    assert names == [
        "01 - Platform Value Overview",
        "02 - Environment and Alert Health",
        "03 - Monitoring Coverage and Licenses",
        "04 - Access and Governance",
        "05 - Collector Health",
        "06 - LogicModule and Content",
        "07 - Adoption and Optimization",
    ], names
    for d in dashboards:
        assert d["widgets"], d["name"]
        for w in d["widgets"]:
            assert "config" in w and "position" in w
            assert w["config"].get("type")
            assert w["config"].get("name")

    OUT.write_text(json.dumps(group, indent=2), encoding="utf-8")
    counts = {d["name"]: len(d["widgets"]) for d in dashboards}
    print(f"Wrote {OUT}")
    print("Widget counts:")
    for k, v in counts.items():
        print(f"  {k}: {v}")
    print(f"Total widgets: {sum(counts.values())}")


if __name__ == "__main__":
    main()
