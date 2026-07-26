# Dependencies — SmartAdmin Connected Experience redesign v2

## Required LogicModules / datasources

These families are referenced by reused SmartAdmin widgets. Keep LogicModules current before import.

| Family | Examples | Used by dashboards |
|--------|----------|--------------------|
| Portal Alerts | `LogicMonitor_Portal_Alerts` | 00, 01, 02, 03, 09 |
| Alert routing | `LogicMonitor_Portal_AlertRules`, `LogicMonitor_Portal_Escalationchains`, Integrations | 03, 09 |
| Resources | `LogicMonitor_Portal_Resources`, MinimalMonitoring, UnmonitoredDevice, Netscans | 01, 02, 03, 04, 09 |
| Websites / groups | `LogicMonitor_Portal_Websites`, device/website groups | 02, 04, 05 |
| Collectors | `LogicMonitor_Portal_Collectors`, `LogicMonitor_Collector_JVMStatus`, `DataCollectingTasks`, `ActiveDiscoveryTasks` | 00, 01, 02, 07 |
| Users / access | `LogicMonitor_Portal_Users`, `Users_NotLogin`, `UserGroups`, `APITokens`, `Roles` | 00, 01, 06, 09 |
| Licenses | `LogicMonitor_Portal_LicenseCounts` | 01, 04 |
| LogicModules inventory | `LogicMonitor_Portal_LogicModuleStatus`, LogicModule alert-over-90-days | 01, 03, 08 |
| Host idle | `HostStatus` (idle interval table) | 02 |

## Dynamic groups

No SmartAdmin widgets in this pack hard-require `Devices by Type/...` dynamic groups.  
**OOTB Level-3 technology dashboards** (linked, not bundled) often do — see [logicmonitor/dashboards README](https://github.com/logicmonitor/dashboards).

## Dashboard tokens

| Token | Required | Notes |
|-------|----------|-------|
| `defaultResourceGroup` | Recommended | Default `*` |
| `defaultResource` / `defaultResourceName` | Recommended | Portal metrics use `*.logicmonitor.com` |
| `defaultWebsiteGroup` | Recommended on 05 | Default `*` |
| `accountname` | **Required for license widgets** | Replace `{{ACCOUNT_NAME}}` with portal account property |

## Portal-specific configuration

| Step | Detail |
|------|--------|
| 1 | Import `dashboards/SmartAdmin_Connected_Experience_redesign_v2.json` |
| 2 | Set `accountname` token |
| 3 | Optionally scope resource/website groups |
| 4 | Replace `{{PORTAL_BASE}}` and `{{DASHBOARD_ID_00}}`…`{{DASHBOARD_ID_09}}` in HTML nav widgets |
| 5 | Import desired OOTB packs; wire Technology Drill-Down Links |
| 6 | Portal-validate optional Dynamic Dashboard List / FilterWidget if adopted |

## Explicitly not required for core pack

- LM Logs live query widgets
- JavaScript Dynamic Dashboard List
- FilterWidget v7
- Better Map Widget CDN
- Client-specific FortiGate / PSC metrics from Design Template

## Known limitations

- Navigation hrefs are placeholders until dashboard IDs are known post-import.
- Host/app capacity metrics are not in SmartAdmin portal datasources; use OOTB Capacity/Cloud/Network.
- Alert widget log metadata columns (if present in source) still require LM Logs for full investigation — dashboards surface the signal only.
