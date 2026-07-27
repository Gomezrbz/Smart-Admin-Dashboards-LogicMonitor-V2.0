# Dependency Validation

LogicModule and portal dependency status for the Connected Experience package.

- Portal configured for export: `proservices`
- Export completed: `False`
- Reason (if not completed): Authentication failed for portal 'proservices': HTTP Error 401: Unauthorized
- Required canonical modules: 27
- Included XML files: 0

## Module status summary

| LogicModule | Status |
| ----------- | ------ |
| HostStatus | Native LogicMonitor module |
| LogicMonitor_Collector_ActiveDiscoveryTasks | Requires portal export |
| LogicMonitor_Collector_DataCollectingTasks | Requires portal export |
| LogicMonitor_Collector_JVMStatus | Requires portal export |
| LogicMonitor_Portal_AlertRules | Requires portal export |
| LogicMonitor_Portal_Alerts | Requires portal export |
| LogicMonitor_Portal_APITokens | Requires portal export |
| LogicMonitor_Portal_Collectors | Requires portal export |
| LogicMonitor_Portal_DataSources | Requires portal export |
| LogicMonitor_Portal_DeviceGroups | Requires portal export |
| LogicMonitor_Portal_Escalationchains | Requires portal export |
| LogicMonitor_Portal_Integration | Requires portal export |
| LogicMonitor_Portal_Integrations_Non200Response | Requires portal export |
| LogicMonitor_Portal_LicenseCounts | Requires portal export |
| LogicMonitor_Portal_LogicModuleStatus | Requires portal export |
| LogicMonitor_Portal_MinimalMonitoring | Requires portal export |
| LogicMonitor_Portal_NetScanDevices_perday | Requires portal export |
| LogicMonitor_Portal_Netscans | Requires portal export |
| LogicMonitor_Portal_Resources | Requires portal export |
| LogicMonitor_Portal_Roles | Requires portal export |
| LogicMonitor_Portal_UnmonitoredDevice | Requires portal export |
| LogicMonitor_Portal_UserGroups | Requires portal export |
| LogicMonitor_Portal_Users | Requires portal export |
| LogicMonitor_Portal_Users_NotLogin | Requires portal export |
| LogicMonitor_Portal_Websites | Requires portal export |
| LogicMonitor_Portal_WebsitesGroups | Requires portal export |
| LogicModule Alert over 90 days | External dependency |

## Non-module configuration

- Tokens: `defaultResourceGroup`, `defaultResource`, `defaultWebsiteGroup`, `accountname`
- Navigation URLs: proservices portal IDs (update for other portals)
- OOTB packs: https://github.com/logicmonitor/dashboards
- Full mapping: [`modules/README.md`](../modules/README.md)
- Package dependency notes: [`dashboard-redesign/validation/dependencies.md`](../dashboard-redesign/validation/dependencies.md)

## Validation verdict

Dependencies are **identified and documented**. XML exports are **not included** until `lm_export_config.json` authenticates successfully. No fake module files were created.

