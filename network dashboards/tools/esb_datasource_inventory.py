#!/usr/bin/env python3
"""Inventory datasources for Devices by Application/ESB via LogicMonitor API."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import sys
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "lm_export_config_questdiag.json"
GROUP = "Devices by Application/ESB"
KEY_MODULES = {"Cisco_CPU_SNMP", "Cisco_NTP", "F5_BigIP_System", "HostStatus", "Ping"}


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def auth(access_id: str, access_key: str, path: str) -> dict[str, str]:
    epoch = str(int(time.time() * 1000))
    msg = f"GET{epoch}{path}"
    signature = base64.b64encode(
        hmac.new(access_key.encode(), msg=msg.encode(), digestmod=hashlib.sha256).digest()
    ).decode()
    return {
        "Authorization": f"LMv1 {access_id}:{signature}:{epoch}",
        "Content-Type": "application/json",
        "X-Version": "3",
    }


def get(config: dict, path: str, query: str = "") -> dict:
    portal = config["portal"]
    access_id = config["access_id"]
    access_key = config["access_key"]
    url = f"https://{portal}.logicmonitor.com/santaba/rest{path}{query}"
    attempts = [
        auth(access_id, access_key, path),
        {
            "Authorization": f"Bearer {access_key}",
            "Content-Type": "application/json",
            "X-Version": "3",
        },
    ]
    last_err: Exception | None = None
    for headers in attempts:
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                body = json.loads(resp.read().decode())
            status = body.get("status")
            errmsg = (body.get("errmsg") or body.get("errorMessage") or "").lower()
            if status in (1400, 1401) or "authentication failed" in errmsg:
                last_err = PermissionError(errmsg or f"auth status {status}")
                continue
            return body
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            continue
    raise PermissionError(f"Authentication failed: {last_err}")


def paginate(config: dict, path: str, params: dict | None = None) -> list[dict]:
    items: list[dict] = []
    offset = 0
    base_params = dict(params or {})
    while True:
        page_params = {**base_params, "size": 300, "offset": offset}
        query = "?" + urllib.parse.urlencode(page_params, quote_via=urllib.parse.quote)
        data = get(config, path, query)
        batch = data.get("items", [])
        items.extend(batch)
        if len(batch) < 300:
            break
        offset += 300
    return items


def main() -> int:
    config = load_config()
    devices = paginate(
        config,
        "/device/devices",
        {"filter": f'systemProperties.fullPath~"{GROUP}"'},
    )
    print(f"DEVICES ({len(devices)}):")
    for device in sorted(devices, key=lambda d: d.get("displayName", "")):
        print(
            f"  {device['id']:>6}  {device.get('displayName')}  "
            f"type={device.get('deviceType')}"
        )

    all_ds: dict[str, set[str]] = defaultdict(set)
    datapoints: dict[str, set[str]] = defaultdict(set)

    for device in devices:
        did = device["id"]
        dname = device.get("displayName", str(did))
        dss = paginate(config, f"/device/devices/{did}/devicedatasources")
        for ds in dss:
            sn = ds.get("dataSourceName") or ""
            if sn:
                all_ds[sn].add(dname)
            if sn not in KEY_MODULES:
                continue
            dsid = ds["id"]
            instances = paginate(
                config,
                f"/device/devices/{did}/devicedatasources/{dsid}/instances",
            )
            for inst in instances:
                for dp in inst.get("dataPoints") or []:
                    name = dp.get("dataPointName") or dp.get("name")
                    if name:
                        datapoints[f"{dname}|{sn}"].add(name)

    print("\nDATASOURCE MATRIX:")
    for sn in sorted(all_ds):
        devs = ", ".join(sorted(all_ds[sn]))
        print(f"  {sn} ({len(all_ds[sn])}): {devs}")

    print("\nKEY DATAPOINTS:")
    for key in sorted(datapoints):
        print(f"  {key}: {sorted(datapoints[key])}")

    out = ROOT / "network dashboards" / "validation" / "esb_datasource_matrix.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(
            {
                "group": GROUP,
                "devices": [
                    {"id": d["id"], "name": d.get("displayName"), "type": d.get("deviceType")}
                    for d in sorted(devices, key=lambda x: x.get("displayName", ""))
                ],
                "datasources": {k: sorted(v) for k, v in sorted(all_ds.items())},
                "key_datapoints": {k: sorted(v) for k, v in sorted(datapoints.items())},
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\nWrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
