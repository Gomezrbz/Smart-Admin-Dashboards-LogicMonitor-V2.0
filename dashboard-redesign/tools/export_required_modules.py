#!/usr/bin/env python3
"""Export required LogicModules (DataSources) from a LogicMonitor portal via REST API.

Reads credentials from lm_export_config.json (gitignored).
Scrapes final redesign dashboard JSON for DataSource names, matches them in the
portal, and writes XML exports under modules/datasources/.

Does not invent missing modules — documents them in modules/README.md.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import re
import time
from collections import defaultdict
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "lm_export_config.json"
DASHBOARDS = ROOT / "dashboard-redesign" / "dashboards"
MODULES = ROOT / "modules"
DS_DIR = MODULES / "datasources"

# Short names scraped from widgets that map to full DataSource names.
ALIASES = {
    "APITokens": "LogicMonitor_Portal_APITokens",
    "Users_NotLogin": "LogicMonitor_Portal_Users_NotLogin",
    "UnmonitoredDevice": "LogicMonitor_Portal_UnmonitoredDevice",
    "MinimalMonitoring": "LogicMonitor_Portal_MinimalMonitoring",
    "DataCollectingTasks": "LogicMonitor_Collector_DataCollectingTasks",
    "ActiveDiscoveryTasks": "LogicMonitor_Collector_ActiveDiscoveryTasks",
}

# Known non-exportable / non-DataSource references.
NON_DATASOURCE = {
    "LogicModule Alert over 90 days": {
        "type": "Custom monitoring content / alert table filter",
        "status": "External dependency",
        "note": "Alert-noise table filter label, not a LogicModule export.",
    },
}

EXTRA_PATTERN = re.compile(
    r"HostStatus|DataCollectingTasks|ActiveDiscoveryTasks|Users_NotLogin|"
    r"APITokens|UnmonitoredDevice|MinimalMonitoring|LogicModule Alert over 90 days"
)
LM_PATTERN = re.compile(r"LogicMonitor_[A-Za-z0-9_]+")


def load_config() -> dict:
    if not CONFIG_PATH.is_file():
        raise SystemExit(
            f"Missing {CONFIG_PATH}. Copy config/lm_export_config.example.json "
            "to lm_export_config.json and fill in credentials."
        )
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def scrape_dependencies() -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """Return (canonical_name -> dashboards, short_alias -> dashboards)."""
    by_name: dict[str, set[str]] = defaultdict(set)
    raw_refs: dict[str, set[str]] = defaultdict(set)

    for path in sorted(DASHBOARDS.rglob("*_redesign_v2.json")):
        if "level-" in path.parts:
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("type") == "dashboardgroup":
            continue
        dash = data.get("name") or path.stem
        blob = json.dumps(data)
        found = set(LM_PATTERN.findall(blob)) | set(EXTRA_PATTERN.findall(blob))
        for name in found:
            raw_refs[name].add(dash)
            canonical = ALIASES.get(name, name)
            by_name[canonical].add(dash)
            if name != canonical:
                by_name[canonical]  # already added
    return by_name, raw_refs


def _lmv1_auth(access_id: str, access_key: str, resource_path: str) -> dict[str, str]:
    epoch = str(int(time.time() * 1000))
    request_vars = "GET" + epoch + "" + resource_path
    signature = base64.b64encode(
        hmac.new(
            access_key.encode("utf-8"),
            msg=request_vars.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()
    ).decode("utf-8")
    return {
        "Authorization": f"LMv1 {access_id}:{signature}:{epoch}",
        "Content-Type": "application/json",
        "X-Version": "3",
    }


def lm_request(config: dict, resource_path: str, query: str = "") -> bytes:
    """Authenticated GET — tries LMv1, then Bearer (access_key as token)."""
    portal = config["portal"]
    access_id = config["access_id"]
    access_key = config["access_key"]
    url = f"https://{portal}.logicmonitor.com/santaba/rest{resource_path}{query}"
    attempts = [
        _lmv1_auth(access_id, access_key, resource_path),
        {
            "Authorization": f"Bearer {access_key}",
            "Content-Type": "application/json",
            "X-Version": "3",
        },
    ]
    last_err: Exception | None = None
    for headers in attempts:
        req = Request(url, headers=headers, method="GET")
        try:
            with urlopen(req, timeout=120) as resp:
                body = resp.read()
            # v1-style envelope may return HTTP 200 with auth error payload
            try:
                payload = json.loads(body.decode("utf-8"))
                status = payload.get("status")
                errmsg = (payload.get("errmsg") or payload.get("errorMessage") or "").lower()
                if status in (1400, 1401) or "authentication failed" in errmsg:
                    last_err = PermissionError(errmsg or f"auth status {status}")
                    continue
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass
            return body
        except HTTPError as e:
            last_err = e
            continue
    raise PermissionError(f"Authentication failed for portal '{portal}': {last_err}")


def list_all_datasources(config: dict) -> list[dict]:
    page_size = int(config.get("page_size") or 1000)
    offset = 0
    items: list[dict] = []
    while True:
        query = "?" + urlencode({"size": page_size, "offset": offset, "fields": "id,name,displayName,dataSourceName"})
        raw = lm_request(config, "/setting/datasources", query)
        payload = json.loads(raw.decode("utf-8"))
        batch = payload.get("items") or payload.get("data", {}).get("items") or []
        if not batch:
            # Some portals return the list at top level under "data"
            if isinstance(payload.get("data"), list):
                batch = payload["data"]
        items.extend(batch)
        total = payload.get("total")
        if total is None and isinstance(payload.get("data"), dict):
            total = payload["data"].get("total")
        offset += len(batch)
        if not batch or (total is not None and offset >= total) or len(batch) < page_size:
            break
    return items


def match_datasource(required: str, catalog: list[dict]) -> dict | None:
    """Match by name, displayName, or dataSourceName (case-insensitive)."""
    req_l = required.lower()
    for item in catalog:
        candidates = [
            item.get("name"),
            item.get("displayName"),
            item.get("dataSourceName"),
        ]
        for c in candidates:
            if c and str(c).lower() == req_l:
                return item
    # Partial: required is suffix of name (e.g. HostStatus)
    for item in catalog:
        for c in (item.get("name"), item.get("displayName"), item.get("dataSourceName")):
            if c and str(c).lower().endswith(req_l) and (
                str(c).lower() == req_l or str(c).lower().endswith("_" + req_l)
            ):
                return item
    return None


def export_xml(config: dict, ds_id: int) -> bytes:
    return lm_request(config, f"/setting/datasources/{ds_id}", "?format=xml")


def safe_filename(name: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*]', "_", name).strip()
    return cleaned or "unnamed"


def write_modules_readme(
    rows: list[dict],
    non_ds: list[dict],
    portal_notes: list[str],
) -> None:
    MODULES.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Required LogicModules",
        "",
        "LogicModules referenced by the SmartAdmin Connected Experience redesign v2 dashboards.",
        "Exports were produced from the configured LogicMonitor portal via REST API",
        "(`GET /setting/datasources/{id}?format=xml`). Module monitoring logic was not modified.",
        "",
        "## Dependency mapping",
        "",
        "| LogicModule | Type | Used By Dashboard | DataSource or Metric Reference | File Included | Status |",
        "| ----------- | ---- | ----------------- | ------------------------------ | ------------- | ------ |",
    ]
    for r in sorted(rows, key=lambda x: x["name"].lower()):
        lines.append(
            f"| {r['name']} | {r['type']} | {r['used_by']} | {r['reference']} | "
            f"{r['file']} | {r['status']} |"
        )
    for r in non_ds:
        lines.append(
            f"| {r['name']} | {r['type']} | {r['used_by']} | {r['reference']} | "
            f"{r['file']} | {r['status']} |"
        )

    lines.extend(
        [
            "",
            "## Recommended import order",
            "",
            "1. Import portal-admin DataSources (`LogicMonitor_Portal_*`).",
            "2. Import collector DataSources (`LogicMonitor_Collector_*`).",
            "3. Import / confirm native modules such as `HostStatus`.",
            "4. Validate datapoints used by dashboard widgets.",
            "5. Import Connected Experience dashboards.",
            "",
            "## Non-LogicModule portal requirements",
            "",
        ]
    )
    for note in portal_notes:
        lines.append(f"- {note}")
    lines.extend(
        [
            "",
            "## Status legend",
            "",
            "- **Included** — XML export saved under `modules/datasources/`",
            "- **Missing** — Required by dashboards but not found in the portal",
            "- **External dependency** — Not a LogicModule export (filter label, OOTB pack, etc.)",
            "- **Native LogicMonitor module** — Standard LM module; confirm in portal / Exchange",
            "- **Requires portal export** — Must be exported from a portal that has it applied",
            "- **Requires validation** — Exported or listed but needs portal smoke-test",
            "",
            "## How to re-export",
            "",
            "```bash",
            "# Ensure lm_export_config.json exists (see config/lm_export_config.example.json)",
            "python dashboard-redesign/tools/export_required_modules.py",
            "```",
            "",
        ]
    )
    (MODULES / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _row(name: str, used: str, status: str, file: str = "—", typ: str = "DataSource") -> dict:
    return {
        "name": name,
        "type": typ,
        "used_by": used,
        "reference": name,
        "file": file,
        "status": status,
    }


def document_without_export(
    by_name: dict[str, set[str]],
    raw_refs: dict[str, set[str]],
    reason: str,
    portal: str | None,
) -> None:
    """Write modules/README when portal export is unavailable — never invent XML."""
    DS_DIR.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    non_ds_rows: list[dict] = []
    for name in sorted(by_name.keys()):
        used = ", ".join(sorted(by_name[name]))
        if name in NON_DATASOURCE:
            meta = NON_DATASOURCE[name]
            non_ds_rows.append(
                _row(name, used, meta["status"], typ=meta["type"])
            )
            continue
        if name == "HostStatus":
            rows.append(_row(name, used, "Native LogicMonitor module"))
        else:
            rows.append(_row(name, used, "Requires portal export"))
    portal_notes = [
        f"Portal XML export was not completed ({reason}). Re-run after fixing `lm_export_config.json`.",
        "Dashboard tokens: `defaultResourceGroup`, `defaultResource`, `defaultWebsiteGroup`, `accountname`.",
        "After import, replace navigation URLs if targeting a portal other than proservices.",
        "OOTB technology packs for dashboard 34: https://github.com/logicmonitor/dashboards",
        "Parent dashboard group: SmartAdmin Connected Experience with Executive / Operational / Technical subgroups.",
        "Portal-assigned dashboard and subgroup IDs are not portable across portals.",
        "Do not invent LogicModule XML; export with: `python dashboard-redesign/tools/export_required_modules.py`",
    ]
    write_modules_readme(rows, non_ds_rows, portal_notes)
    summary = {
        "portal": portal,
        "export_ok": False,
        "reason": reason,
        "required_count": len(by_name),
        "included": [],
        "missing": rows,
        "non_datasource": non_ds_rows,
        "raw_refs": {k: sorted(v) for k, v in sorted(raw_refs.items())},
    }
    (MODULES / "_export_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Documented {len(rows)} modules as requiring portal export ({reason})")
    print(f"Wrote {MODULES / 'README.md'}")


def main() -> None:
    config = load_config()
    by_name, raw_refs = scrape_dependencies()
    print(f"Scraped {len(by_name)} canonical LogicModule names from dashboards")

    DS_DIR.mkdir(parents=True, exist_ok=True)

    print("Listing datasources from portal...")
    try:
        catalog = list_all_datasources(config)
    except (PermissionError, HTTPError, URLError, TimeoutError, OSError) as e:
        document_without_export(by_name, raw_refs, str(e), config.get("portal"))
        return
    print(f"Portal returned {len(catalog)} datasources")

    name_index: dict[str, dict] = {}
    for item in catalog:
        for key in ("name", "displayName", "dataSourceName"):
            val = item.get(key)
            if val:
                name_index[str(val).lower()] = item

    rows: list[dict] = []
    non_ds_rows: list[dict] = []

    for name in sorted(by_name.keys()):
        used = ", ".join(sorted(by_name[name]))
        if name in NON_DATASOURCE:
            meta = NON_DATASOURCE[name]
            non_ds_rows.append(_row(name, used, meta["status"], typ=meta["type"]))
            continue

        item = name_index.get(name.lower()) or match_datasource(name, catalog)
        if not item:
            status = "Native LogicMonitor module" if name == "HostStatus" else "Missing"
            rows.append(_row(name, used, status))
            print(f"  MISS {name}")
            continue

        ds_id = item["id"]
        fname = safe_filename(item.get("name") or name) + ".xml"
        out_path = DS_DIR / fname
        try:
            xml = export_xml(config, int(ds_id))
            text = xml.decode("utf-8", errors="replace")
            if text.lstrip().startswith("{"):
                payload = json.loads(text)
                if "data" in payload and isinstance(payload["data"], str):
                    text = payload["data"]
                else:
                    raise ValueError(f"Unexpected JSON response for {name}: keys={list(payload)[:8]}")
            out_path.write_text(text, encoding="utf-8")
            rel = f"datasources/{fname}"
            rows.append(_row(item.get("name") or name, used, "Included", file=rel))
            print(f"  OK   {name} -> {rel}")
        except (PermissionError, HTTPError, URLError, TimeoutError, OSError, ValueError) as e:
            rows.append(_row(name, used, "Requires portal export"))
            print(f"  FAIL {name}: {e}")
        time.sleep(0.15)

    portal_notes = [
        "Dashboard tokens: `defaultResourceGroup`, `defaultResource`, `defaultWebsiteGroup`, `accountname`.",
        "After import, replace navigation URLs if targeting a portal other than proservices.",
        "OOTB technology packs for dashboard 34: https://github.com/logicmonitor/dashboards",
        "Parent dashboard group: SmartAdmin Connected Experience with Executive / Operational / Technical subgroups.",
        "Portal-assigned dashboard and subgroup IDs are not portable across portals.",
    ]
    write_modules_readme(rows, non_ds_rows, portal_notes)

    summary = {
        "portal": config.get("portal"),
        "export_ok": True,
        "required_count": len(by_name),
        "included": [r for r in rows if r["status"] == "Included"],
        "missing": [r for r in rows if r["status"] != "Included"],
        "non_datasource": non_ds_rows,
        "raw_refs": {k: sorted(v) for k, v in sorted(raw_refs.items())},
    }
    (MODULES / "_export_summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    included = sum(1 for r in rows if r["status"] == "Included")
    print(f"Done. Included={included}, other={len(rows) - included}, non_ds={len(non_ds_rows)}")
    print(f"Wrote {MODULES / 'README.md'}")


if __name__ == "__main__":
    main()
