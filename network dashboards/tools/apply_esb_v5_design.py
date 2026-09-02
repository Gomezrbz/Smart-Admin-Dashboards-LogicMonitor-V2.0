#!/usr/bin/env python3
"""Add SmartAdmin-style intro, section headers, and layout polish to ESB V5 dashboard."""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DASH = ROOT / "network dashboards" / "ESB_Network_Devices_V5.json"
MAIN = ROOT / "network dashboards" / "ESB_Network_Devices.json"

INTRO_ROWS = 4
SECTION_ROWS = 2
INTRO_OFFSET = INTRO_ROWS + SECTION_ROWS  # first content block starts after intro + section1 header


def section_header(title: str, description: str) -> dict:
    content = (
        '<p><style type="text/css">\n'
        ".html-wpsites { height: 72px; background-color: rgba(0, 0, 0, 0); "
        "font-family: Arial; font-size: 32px; color: #ffffff; font-weight: bold; "
        "text-align: center; }\n"
        "</style></p>\n"
        f'<div class="html-wpsites">{title}</div>\n'
        "<p>&nbsp;</p>"
    )
    return {
        "displaySettings": {},
        "isSupportCustomProperty": False,
        "supportCustomProperty": False,
        "name": title,
        "description": description,
        "theme": "newSolidDarkBlue",
        "interval": 15,
        "type": "text",
        "timescale": "day",
        "version": 2,
        "content": content,
    }


def intro_banner() -> dict:
    content = (
        '<div style="font-family:Arial,Helvetica,sans-serif;background:linear-gradient(135deg,#0f172a 0%,#111827 45%,#1e3a8a 100%);'
        'color:#ffffff;border-radius:16px;padding:22px;box-shadow:0 8px 24px rgba(15,23,42,.32);width:100%;box-sizing:border-box;">'
        '<div style="font-size:28px;font-weight:750;color:#ffffff;margin-bottom:6px;">ESB Network Devices</div>'
        '<div style="font-size:13px;color:#dbeafe;margin-bottom:16px;max-width:960px;">'
        "Operations dashboard for resources in <b>Devices by Application/ESB</b>. "
        "Use dashboard tokens to drill from the full ESB group down to a single device or interface. "
        "Netflow widgets at the bottom monitor collector platform health (not individual ESB devices)."
        "</div>"
        '<table style="width:100%;border-collapse:separate;border-spacing:14px;"><tr>'
        '<td style="vertical-align:top;background:rgba(15,23,42,.76);border:1px solid rgba(148,163,184,.34);'
        'border-radius:14px;padding:16px;width:25%;">'
        '<div style="display:inline-block;padding:6px 10px;border-radius:11px;background:rgba(59,130,246,.22);'
        'border:1px solid rgba(255,255,255,.18);font-size:11px;font-weight:800;color:#dbeafe;">SCOPE</div>'
        '<div style="font-size:15px;font-weight:700;color:#ffffff;margin:10px 0 6px;">Resource group</div>'
        '<div style="font-size:13px;line-height:1.48;color:#cbd5e1;">'
        "Token <b>defaultResourceGroup</b> = Devices by Application/ESB"
        "</div></td>"
        '<td style="vertical-align:top;background:rgba(15,23,42,.76);border:1px solid rgba(148,163,184,.34);'
        'border-radius:14px;padding:16px;width:25%;">'
        '<div style="display:inline-block;padding:6px 10px;border-radius:11px;background:rgba(59,130,246,.22);'
        'border:1px solid rgba(255,255,255,.18);font-size:11px;font-weight:800;color:#dbeafe;">DRILL-DOWN</div>'
        '<div style="font-size:15px;font-weight:700;color:#ffffff;margin:10px 0 6px;">Single device</div>'
        '<div style="font-size:13px;line-height:1.48;color:#cbd5e1;">'
        "Set <b>defaultResourceName</b> to one hostname (e.g. len-sc01.qdx.com) to narrow interface widgets."
        "</div></td>"
        '<td style="vertical-align:top;background:rgba(15,23,42,.76);border:1px solid rgba(148,163,184,.34);'
        'border-radius:14px;padding:16px;width:25%;">'
        '<div style="display:inline-block;padding:6px 10px;border-radius:11px;background:rgba(59,130,246,.22);'
        'border:1px solid rgba(255,255,255,.18);font-size:11px;font-weight:800;color:#dbeafe;">PATH</div>'
        '<div style="font-size:15px;font-weight:700;color:#ffffff;margin:10px 0 6px;">Investigation flow</div>'
        '<div style="font-size:13px;line-height:1.48;color:#cbd5e1;">'
        "ESB group &rarr; device health &rarr; interfaces &rarr; netflow collectors"
        "</div></td>"
        '<td style="vertical-align:top;background:rgba(15,23,42,.76);border:1px solid rgba(148,163,184,.34);'
        'border-radius:14px;padding:16px;width:25%;">'
        '<div style="display:inline-block;padding:6px 10px;border-radius:11px;background:rgba(59,130,246,.22);'
        'border:1px solid rgba(255,255,255,.18);font-size:11px;font-weight:800;color:#dbeafe;">MIXED</div>'
        '<div style="font-size:15px;font-weight:700;color:#ffffff;margin:10px 0 6px;">Vendor split</div>'
        '<div style="font-size:13px;line-height:1.48;color:#cbd5e1;">'
        "Cisco switches (sc/sd/sf) and F5 BIG-IP (l5/l7) share this board; CPU widgets are vendor-specific."
        "</div></td>"
        "</tr></table></div>"
    )
    return {
        "displaySettings": {},
        "isSupportCustomProperty": False,
        "supportCustomProperty": False,
        "name": "ESB Dashboard Guide",
        "description": "Intro banner: scope, tokens, and investigation path for ESB network devices.",
        "theme": "newSolidDarkBlue",
        "interval": 15,
        "type": "text",
        "timescale": "day",
        "version": 2,
        "content": content,
    }


def text_widget(row: int, sizey: int, config: dict) -> dict:
    return {
        "position": {"col": 1, "row": row, "sizex": 12, "sizey": sizey},
        "config": config,
    }


def shift_widget(widget: dict, row_delta: int) -> dict:
    w = deepcopy(widget)
    w["position"]["row"] = w["position"]["row"] + row_delta
    return w


def cpu_widgets_from_main() -> list[dict]:
    data = json.loads(MAIN.read_text(encoding="utf-8"))
    names = {"Cisco Switch CPU Utilization", "F5 BIG-IP CPU Utilization"}
    out = []
    for widget in data.get("widgets", []):
        if widget.get("config", {}).get("name") in names:
            out.append(deepcopy(widget))
    return out


def main() -> None:
    dash = json.loads(DASH.read_text(encoding="utf-8"))
    original = dash["widgets"]

    cpu = cpu_widgets_from_main()
    for w in cpu:
        w["position"]["row"] = 14
        if w["config"]["name"] == "Cisco Switch CPU Utilization":
            w["position"].update({"col": 1, "sizex": 4, "sizey": 4})
        else:
            w["position"].update({"col": 5, "sizex": 4, "sizey": 4})

    netflow_layout = {
        "Netflow Collector Health": {"col": 1, "row": 0, "sizex": 5, "sizey": 4},
        "Netflow Collector Statistics": {"col": 6, "row": 0, "sizex": 7, "sizey": 4},
        "Collectors by Flows per Second": {"col": 1, "row": 4, "sizex": 5, "sizey": 5},
        "Flow Success vs. Failure (Trend)": {"col": 6, "row": 4, "sizex": 4, "sizey": 5},
        "Netflow Failure vs. Success": {"col": 10, "row": 4, "sizex": 3, "sizey": 5},
    }
    netflow_base_row = 28 + SECTION_ROWS
    repacked_netflow = []
    for w in original:
        name = w["config"]["name"]
        if name not in netflow_layout:
            continue
        w = deepcopy(w)
        layout = netflow_layout[name]
        w["position"] = {
            "col": layout["col"],
            "row": netflow_base_row + layout["row"],
            "sizex": layout["sizex"],
            "sizey": layout["sizey"],
        }
        repacked_netflow.append(w)

    block1_out = []
    block2_out = []
    for w in original:
        name = w["config"]["name"]
        w = deepcopy(w)
        if name in {
            "Network Device Availability",
            "Network Device Alert Summary",
            "Top Network Devices Requiring Attention",
        }:
            w["position"]["row"] = INTRO_OFFSET
            block1_out.append(w)
        elif name == "Network Device Health Trend":
            w["position"].update({"col": 1, "sizex": 12, "row": INTRO_OFFSET + 3, "sizey": 4})
            block1_out.append(w)
        elif name == "Interface Errors and Discards":
            w["position"].update({"col": 1, "sizex": 12, "row": 19, "sizey": 5})
            block2_out.append(w)
        elif name == "Top Interfaces by Utilization":
            w["position"].update({"col": 1, "sizex": 4, "row": 24, "sizey": 4})
            block2_out.append(w)

    widgets: list[dict] = [
        text_widget(1, INTRO_ROWS, intro_banner()),
        text_widget(5, SECTION_ROWS, section_header(
            "Device Health &amp; Availability",
            "Section: Device health, alerts, and ping latency for ESB resources",
        )),
        *block1_out,
        *cpu,
        text_widget(18, SECTION_ROWS, section_header(
            "Interface Performance",
            "Section: Interface errors, discards, and utilization within ESB scope",
        )),
        *block2_out,
        text_widget(28, SECTION_ROWS, section_header(
            "Netflow Collector Platform",
            "Section: Collector-scoped netflow health (Devices by Type/Collectors)",
        )),
        *repacked_netflow,
    ]

    dash["widgets"] = widgets
    dash["description"] = (
        "ESB network operations dashboard with guided sections. "
        "Defaults to Devices by Application/ESB; supports drill-down via defaultResourceName. "
        "Intro and section headers explain scope and troubleshooting path."
    )
    DASH.write_text(json.dumps(dash, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {DASH} with {len(widgets)} widgets")


if __name__ == "__main__":
    main()
