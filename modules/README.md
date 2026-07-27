# Required LogicModules

LogicModules referenced by the SmartAdmin Connected Experience redesign v2 dashboards.
When portal authentication succeeds, exports are written via REST API
(`GET /setting/datasources/{id}?format=xml`). Module monitoring logic is never modified.

## Dependency mapping

| LogicModule | Type | Used By Dashboard | DataSource or Metric Reference | File Included | Status |
| ----------- | ---- | ----------------- | ------------------------------ | ------------- | ------ |
| HostStatus | DataSource | 10 - Executive Command Center, 20 - Operational Command Center, 21 - Active Alerts, 22 - Resource Health, 30 - Technical Resource Investigation | HostStatus | — | Native LogicMonitor module |
| LogicMonitor_Collector_ActiveDiscoveryTasks | DataSource | 31 - Collector Diagnostics | LogicMonitor_Collector_ActiveDiscoveryTasks | — | Requires portal export |
| LogicMonitor_Collector_DataCollectingTasks | DataSource | 31 - Collector Diagnostics | LogicMonitor_Collector_DataCollectingTasks | — | Requires portal export |
| LogicMonitor_Collector_JVMStatus | DataSource | 31 - Collector Diagnostics | LogicMonitor_Collector_JVMStatus | — | Requires portal export |
| LogicMonitor_Portal_AlertRules | DataSource | 21 - Active Alerts | LogicMonitor_Portal_AlertRules | — | Requires portal export |
| LogicMonitor_Portal_Alerts | DataSource | 00 - Home / Introductory, 10 - Executive Command Center, 11 - Platform Value Overview, 12 - Environment Health Executive, 13 - Availability and Service Health, 20 - Operational Command Center, 21 - Active Alerts, 22 - Resource Health, 30 - Technical Resource Investigation, 33 - Adoption and Optimization | LogicMonitor_Portal_Alerts | — | Requires portal export |
| LogicMonitor_Portal_APITokens | DataSource | 25 - Access and Administration, 33 - Adoption and Optimization | LogicMonitor_Portal_APITokens | — | Requires portal export |
| LogicMonitor_Portal_Collectors | DataSource | 00 - Home / Introductory, 10 - Executive Command Center, 11 - Platform Value Overview, 12 - Environment Health Executive, 20 - Operational Command Center, 22 - Resource Health, 30 - Technical Resource Investigation | LogicMonitor_Portal_Collectors | — | Requires portal export |
| LogicMonitor_Portal_DataSources | DataSource | 21 - Active Alerts, 32 - LogicModule and Content, 33 - Adoption and Optimization | LogicMonitor_Portal_DataSources | — | Requires portal export |
| LogicMonitor_Portal_DeviceGroups | DataSource | 23 - Websites and Services, 24 - Coverage, Capacity & Licenses | LogicMonitor_Portal_DeviceGroups | — | Requires portal export |
| LogicMonitor_Portal_Escalationchains | DataSource | 21 - Active Alerts | LogicMonitor_Portal_Escalationchains | — | Requires portal export |
| LogicMonitor_Portal_Integration | DataSource | 21 - Active Alerts | LogicMonitor_Portal_Integration | — | Requires portal export |
| LogicMonitor_Portal_Integrations_Non200Response | DataSource | 21 - Active Alerts, 33 - Adoption and Optimization | LogicMonitor_Portal_Integrations_Non200Response | — | Requires portal export |
| LogicMonitor_Portal_LicenseCounts | DataSource | 00 - Home / Introductory, 11 - Platform Value Overview, 14 - Capacity and Risk Overview, 24 - Coverage, Capacity & Licenses | LogicMonitor_Portal_LicenseCounts | — | Requires portal export |
| LogicMonitor_Portal_LogicModuleStatus | DataSource | 11 - Platform Value Overview, 32 - LogicModule and Content | LogicMonitor_Portal_LogicModuleStatus | — | Requires portal export |
| LogicMonitor_Portal_MinimalMonitoring | DataSource | 12 - Environment Health Executive, 14 - Capacity and Risk Overview, 22 - Resource Health, 33 - Adoption and Optimization | LogicMonitor_Portal_MinimalMonitoring | — | Requires portal export |
| LogicMonitor_Portal_NetScanDevices_perday | DataSource | 24 - Coverage, Capacity & Licenses | LogicMonitor_Portal_NetScanDevices_perday | — | Requires portal export |
| LogicMonitor_Portal_Netscans | DataSource | 24 - Coverage, Capacity & Licenses | LogicMonitor_Portal_Netscans | — | Requires portal export |
| LogicMonitor_Portal_Resources | DataSource | 00 - Home / Introductory, 10 - Executive Command Center, 11 - Platform Value Overview, 12 - Environment Health Executive, 14 - Capacity and Risk Overview, 20 - Operational Command Center, 22 - Resource Health, 30 - Technical Resource Investigation, 33 - Adoption and Optimization | LogicMonitor_Portal_Resources | — | Requires portal export |
| LogicMonitor_Portal_Roles | DataSource | 25 - Access and Administration | LogicMonitor_Portal_Roles | — | Requires portal export |
| LogicMonitor_Portal_UnmonitoredDevice | DataSource | 14 - Capacity and Risk Overview, 24 - Coverage, Capacity & Licenses, 33 - Adoption and Optimization | LogicMonitor_Portal_UnmonitoredDevice | — | Requires portal export |
| LogicMonitor_Portal_UserGroups | DataSource | 25 - Access and Administration, 33 - Adoption and Optimization | LogicMonitor_Portal_UserGroups | — | Requires portal export |
| LogicMonitor_Portal_Users | DataSource | 00 - Home / Introductory, 11 - Platform Value Overview, 25 - Access and Administration | LogicMonitor_Portal_Users | — | Requires portal export |
| LogicMonitor_Portal_Users_NotLogin | DataSource | 25 - Access and Administration, 33 - Adoption and Optimization | LogicMonitor_Portal_Users_NotLogin | — | Requires portal export |
| LogicMonitor_Portal_Websites | DataSource | 10 - Executive Command Center, 12 - Environment Health Executive, 13 - Availability and Service Health, 20 - Operational Command Center, 22 - Resource Health, 23 - Websites and Services | LogicMonitor_Portal_Websites | — | Requires portal export |
| LogicMonitor_Portal_WebsitesGroups | DataSource | 13 - Availability and Service Health, 23 - Websites and Services, 24 - Coverage, Capacity & Licenses | LogicMonitor_Portal_WebsitesGroups | — | Requires portal export |
| LogicModule Alert over 90 days | Custom monitoring content / alert table filter | 21 - Active Alerts, 32 - LogicModule and Content | LogicModule Alert over 90 days | — | External dependency |

## Recommended import order

1. Import portal-admin DataSources (`LogicMonitor_Portal_*`).
2. Import collector DataSources (`LogicMonitor_Collector_*`).
3. Import / confirm native modules such as `HostStatus`.
4. Validate datapoints used by dashboard widgets.
5. Import Connected Experience dashboards.

## Non-LogicModule portal requirements

- Portal XML export was not completed (Authentication failed for portal 'proservices': HTTP Error 401: Unauthorized). Re-run after fixing `lm_export_config.json`.
- Dashboard tokens: `defaultResourceGroup`, `defaultResource`, `defaultWebsiteGroup`, `accountname`.
- After import, replace navigation URLs if targeting a portal other than proservices.
- OOTB technology packs for dashboard 34: https://github.com/logicmonitor/dashboards
- Parent dashboard group: SmartAdmin Connected Experience with Executive / Operational / Technical subgroups.
- Portal-assigned dashboard and subgroup IDs are not portable across portals.
- Do not invent LogicModule XML; export with: `python dashboard-redesign/tools/export_required_modules.py`

## Status legend

- **Included** — XML export saved under `modules/datasources/`
- **Missing** — Required by dashboards but not found in the portal
- **External dependency** — Not a LogicModule export (filter label, OOTB pack, etc.)
- **Native LogicMonitor module** — Standard LM module; confirm in portal / Exchange
- **Requires portal export** — Must be exported from a portal that has it applied
- **Requires validation** — Exported or listed but needs portal smoke-test

## How to re-export

```bash
# Ensure lm_export_config.json exists (see config/lm_export_config.example.json)
python dashboard-redesign/tools/export_required_modules.py
```

