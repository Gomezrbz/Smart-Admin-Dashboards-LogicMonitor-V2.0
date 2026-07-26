# Validation Results — SmartAdmin Connected Experience redesign v2

Automated checks: JSON parse, widget position overlap, missing positions, script tags in text widgets, hardcoded `proservices`, token listing, datasource scrape.

| File | Dashboard | JSON | Widgets | Status | Notes |
|------|-----------|------|---------|--------|-------|
| `dashboard-redesign/dashboards/level-1-executive/00_Home_Introductory_redesign_v2.json` | 00 - Home / Introductory | OK | 17 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/level-1-executive/01_Platform_Value_Overview_redesign_v2.json` | 01 - Platform Value Overview | OK | 22 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/level-2-operational/02_Environment_Health_redesign_v2.json` | 02 - Environment Health | OK | 20 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/level-2-operational/03_Alert_Overview_redesign_v2.json` | 03 - Alert Overview | OK | 24 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/level-2-operational/04_Coverage_Capacity_Licenses_redesign_v2.json` | 04 - Coverage, Capacity & Licenses | OK | 32 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/level-2-operational/05_Websites_and_Services_redesign_v2.json` | 05 - Websites and Services | OK | 16 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/level-2-operational/06_Access_and_Administration_redesign_v2.json` | 06 - Access and Administration | OK | 18 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/level-3-technical/07_Collector_Health_redesign_v2.json` | 07 - Collector Health | OK | 35 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/level-3-technical/08_LogicModule_and_Content_redesign_v2.json` | 08 - LogicModule and Content | OK | 18 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/level-3-technical/09_Adoption_and_Optimization_redesign_v2.json` | 09 - Adoption and Optimization | OK | 17 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/SmartAdmin_Connected_Experience_redesign_v2.json` | SmartAdmin Connected Experience | OK | 219 | **pass_with_portal_config** | Group export containing all suite dashboards. |

## Per-file details

### 00 - Home / Introductory

- **File:** `dashboard-redesign/dashboards/level-1-executive/00_Home_Introductory_redesign_v2.json`
- **JSON validation:** pass
- **Widgets reviewed:** 17
- **Widget types:** `{'text': 8, 'bigNumber': 9}`
- **Tokens:** `[('defaultResourceGroup', '*'), ('defaultResource', '*.logicmonitor.com')]`
- **Placeholders:** `['{{ACCOUNT_NAME}}', '{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_01}}', '{{DASHBOARD_ID_02}}', '{{DASHBOARD_ID_03}}', '{{DASHBOARD_ID_04}}', '{{DASHBOARD_ID_05}}', '{{DASHBOARD_ID_06}}', '{{DASHBOARD_ID_07}}', '{{DASHBOARD_ID_08}}', '{{DASHBOARD_ID_09}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** LogicMonitor_Portal_Alerts, LogicMonitor_Portal_Collectors, LogicMonitor_Portal_LicenseCounts, LogicMonitor_Portal_Resources, LogicMonitor_Portal_Users
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **Final status:** **pass_with_portal_config**

### 01 - Platform Value Overview

- **File:** `dashboard-redesign/dashboards/level-1-executive/01_Platform_Value_Overview_redesign_v2.json`
- **JSON validation:** pass
- **Widgets reviewed:** 22
- **Widget types:** `{'text': 6, 'bigNumber': 12, 'gmap': 1, 'noc': 1, 'cgraph': 2}`
- **Tokens:** `[('defaultResource', '*.logicmonitor.com'), ('defaultResourceGroup', '*')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_01}}', '{{DASHBOARD_ID_02}}', '{{DASHBOARD_ID_03}}', '{{DASHBOARD_ID_04}}', '{{DASHBOARD_ID_05}}', '{{DASHBOARD_ID_06}}', '{{DASHBOARD_ID_07}}', '{{DASHBOARD_ID_08}}', '{{DASHBOARD_ID_09}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** LogicMonitor_Portal_Alerts, LogicMonitor_Portal_Collectors, LogicMonitor_Portal_LicenseCounts, LogicMonitor_Portal_LogicModuleStatus, LogicMonitor_Portal_Resources, LogicMonitor_Portal_Users
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **Final status:** **pass_with_portal_config**

### 02 - Environment Health

- **File:** `dashboard-redesign/dashboards/level-2-operational/02_Environment_Health_redesign_v2.json`
- **JSON validation:** pass
- **Widgets reviewed:** 20
- **Widget types:** `{'text': 6, 'bigNumber': 8, 'gmap': 1, 'noc': 1, 'cgraph': 2, 'alert': 1, 'dynamicTable': 1}`
- **Tokens:** `[('defaultResource', '*.logicmonitor.com'), ('defaultResourceGroup', '*')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_01}}', '{{DASHBOARD_ID_02}}', '{{DASHBOARD_ID_03}}', '{{DASHBOARD_ID_04}}', '{{DASHBOARD_ID_05}}', '{{DASHBOARD_ID_06}}', '{{DASHBOARD_ID_07}}', '{{DASHBOARD_ID_08}}', '{{DASHBOARD_ID_09}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** HostStatus, LogicMonitor_Portal_Alerts, LogicMonitor_Portal_Collectors, LogicMonitor_Portal_MinimalMonitoring, LogicMonitor_Portal_Resources, LogicMonitor_Portal_Websites, MinimalMonitoring
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **Final status:** **pass_with_portal_config**

### 03 - Alert Overview

- **File:** `dashboard-redesign/dashboards/level-2-operational/03_Alert_Overview_redesign_v2.json`
- **JSON validation:** pass
- **Widgets reviewed:** 24
- **Widget types:** `{'text': 7, 'bigNumber': 6, 'cgraph': 3, 'alert': 2, 'dynamicTable': 6}`
- **Tokens:** `[('defaultResource', '*.logicmonitor.com'), ('defaultResourceGroup', '*')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_01}}', '{{DASHBOARD_ID_02}}', '{{DASHBOARD_ID_03}}', '{{DASHBOARD_ID_04}}', '{{DASHBOARD_ID_05}}', '{{DASHBOARD_ID_06}}', '{{DASHBOARD_ID_07}}', '{{DASHBOARD_ID_08}}', '{{DASHBOARD_ID_09}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** HostStatus, LogicMonitor_Portal_AlertRules, LogicMonitor_Portal_Alerts, LogicMonitor_Portal_DataSources, LogicMonitor_Portal_Escalationchains, LogicMonitor_Portal_Integration, LogicMonitor_Portal_Integrations_Non200Response
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **Final status:** **pass_with_portal_config**

### 04 - Coverage, Capacity & Licenses

- **File:** `dashboard-redesign/dashboards/level-2-operational/04_Coverage_Capacity_Licenses_redesign_v2.json`
- **JSON validation:** pass
- **Widgets reviewed:** 32
- **Widget types:** `{'text': 7, 'bigNumber': 22, 'dynamicTable': 1, 'cgraph': 2}`
- **Tokens:** `[('accountname', '{{ACCOUNT_NAME}}'), ('defaultResourceGroup', '*'), ('defaultResource', '*.logicmonitor.com')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_01}}', '{{DASHBOARD_ID_02}}', '{{DASHBOARD_ID_03}}', '{{DASHBOARD_ID_04}}', '{{DASHBOARD_ID_05}}', '{{DASHBOARD_ID_06}}', '{{DASHBOARD_ID_07}}', '{{DASHBOARD_ID_08}}', '{{DASHBOARD_ID_09}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** LogicMonitor_Portal_DeviceGroups, LogicMonitor_Portal_LicenseCounts, LogicMonitor_Portal_NetScanDevices_perday, LogicMonitor_Portal_Netscans, LogicMonitor_Portal_UnmonitoredDevice, LogicMonitor_Portal_WebsitesGroups, UnmonitoredDevice
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **Final status:** **pass_with_portal_config**

### 05 - Websites and Services

- **File:** `dashboard-redesign/dashboards/level-2-operational/05_Websites_and_Services_redesign_v2.json`
- **JSON validation:** pass
- **Widgets reviewed:** 16
- **Widget types:** `{'text': 8, 'bigNumber': 8}`
- **Tokens:** `[('defaultResourceGroup', '*'), ('defaultResource', '*.logicmonitor.com'), ('defaultWebsiteGroup', '*')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_01}}', '{{DASHBOARD_ID_02}}', '{{DASHBOARD_ID_03}}', '{{DASHBOARD_ID_04}}', '{{DASHBOARD_ID_05}}', '{{DASHBOARD_ID_06}}', '{{DASHBOARD_ID_07}}', '{{DASHBOARD_ID_08}}', '{{DASHBOARD_ID_09}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** LogicMonitor_Portal_DeviceGroups, LogicMonitor_Portal_Websites, LogicMonitor_Portal_WebsitesGroups
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **Final status:** **pass_with_portal_config**

### 06 - Access and Administration

- **File:** `dashboard-redesign/dashboards/level-2-operational/06_Access_and_Administration_redesign_v2.json`
- **JSON validation:** pass
- **Widgets reviewed:** 18
- **Widget types:** `{'text': 6, 'bigNumber': 12}`
- **Tokens:** `[('defaultResource', '*.logicmonitor.com'), ('defaultResourceGroup', '*')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_01}}', '{{DASHBOARD_ID_02}}', '{{DASHBOARD_ID_03}}', '{{DASHBOARD_ID_04}}', '{{DASHBOARD_ID_05}}', '{{DASHBOARD_ID_06}}', '{{DASHBOARD_ID_07}}', '{{DASHBOARD_ID_08}}', '{{DASHBOARD_ID_09}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** APITokens, LogicMonitor_Portal_APITokens, LogicMonitor_Portal_Roles, LogicMonitor_Portal_UserGroups, LogicMonitor_Portal_Users, LogicMonitor_Portal_Users_NotLogin, Users_NotLogin
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **Final status:** **pass_with_portal_config**

### 07 - Collector Health

- **File:** `dashboard-redesign/dashboards/level-3-technical/07_Collector_Health_redesign_v2.json`
- **JSON validation:** pass
- **Widgets reviewed:** 35
- **Widget types:** `{'text': 7, 'bigNumber': 11, 'dynamicTable': 3, 'alert': 1, 'cgraph': 13}`
- **Tokens:** `[('defaultResourceGroup', '*'), ('defaultResourceName', '*')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_01}}', '{{DASHBOARD_ID_02}}', '{{DASHBOARD_ID_03}}', '{{DASHBOARD_ID_04}}', '{{DASHBOARD_ID_05}}', '{{DASHBOARD_ID_06}}', '{{DASHBOARD_ID_07}}', '{{DASHBOARD_ID_08}}', '{{DASHBOARD_ID_09}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** ActiveDiscoveryTasks, DataCollectingTasks, LogicMonitor_Collector_ActiveDiscoveryTasks, LogicMonitor_Collector_DataCollectingTasks, LogicMonitor_Collector_JVMStatus
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **Final status:** **pass_with_portal_config**

### 08 - LogicModule and Content

- **File:** `dashboard-redesign/dashboards/level-3-technical/08_LogicModule_and_Content_redesign_v2.json`
- **JSON validation:** pass
- **Widgets reviewed:** 18
- **Widget types:** `{'text': 5, 'bigNumber': 8, 'dynamicTable': 5}`
- **Tokens:** `[('defaultResourceGroup', '*'), ('defaultResourceName', '*.logicmonitor.com')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_01}}', '{{DASHBOARD_ID_02}}', '{{DASHBOARD_ID_03}}', '{{DASHBOARD_ID_04}}', '{{DASHBOARD_ID_05}}', '{{DASHBOARD_ID_06}}', '{{DASHBOARD_ID_07}}', '{{DASHBOARD_ID_08}}', '{{DASHBOARD_ID_09}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** LogicMonitor_Portal_DataSources, LogicMonitor_Portal_LogicModuleStatus
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **Final status:** **pass_with_portal_config**

### 09 - Adoption and Optimization

- **File:** `dashboard-redesign/dashboards/level-3-technical/09_Adoption_and_Optimization_redesign_v2.json`
- **JSON validation:** pass
- **Widgets reviewed:** 17
- **Widget types:** `{'text': 7, 'cgraph': 6, 'bigNumber': 4}`
- **Tokens:** `[('defaultResource', '*.logicmonitor.com'), ('defaultResourceGroup', '*')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_01}}', '{{DASHBOARD_ID_02}}', '{{DASHBOARD_ID_03}}', '{{DASHBOARD_ID_04}}', '{{DASHBOARD_ID_05}}', '{{DASHBOARD_ID_06}}', '{{DASHBOARD_ID_07}}', '{{DASHBOARD_ID_08}}', '{{DASHBOARD_ID_09}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** APITokens, LogicMonitor_Portal_APITokens, LogicMonitor_Portal_Alerts, LogicMonitor_Portal_DataSources, LogicMonitor_Portal_Integrations_Non200Response, LogicMonitor_Portal_MinimalMonitoring, LogicMonitor_Portal_Resources, LogicMonitor_Portal_UnmonitoredDevice, LogicMonitor_Portal_UserGroups, LogicMonitor_Portal_Users_NotLogin, MinimalMonitoring, UnmonitoredDevice, Users_NotLogin
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **Final status:** **pass_with_portal_config**

### SmartAdmin Connected Experience

- **File:** `dashboard-redesign/dashboards/SmartAdmin_Connected_Experience_redesign_v2.json`
- **JSON validation:** pass
- **Widgets reviewed:** 219
- **Tokens:** `[('defaultResourceGroup', '*'), ('defaultResource', '*.logicmonitor.com'), ('defaultWebsiteGroup', '*'), ('accountname', '{{ACCOUNT_NAME}}')]`
- **Placeholders:** `['{{ACCOUNT_NAME}}', '{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_01}}', '{{DASHBOARD_ID_02}}', '{{DASHBOARD_ID_03}}', '{{DASHBOARD_ID_04}}', '{{DASHBOARD_ID_05}}', '{{DASHBOARD_ID_06}}', '{{DASHBOARD_ID_07}}', '{{DASHBOARD_ID_08}}', '{{DASHBOARD_ID_09}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **Final status:** **pass_with_portal_config**

## Portal testing required

- Resolve `{{PORTAL_BASE}}` and `{{DASHBOARD_ID_NN}}` after import
- Set `accountname` / `{{ACCOUNT_NAME}}` for license widgets
- Confirm portal LogicModules applied
- Optional: Dynamic Dashboard List / FilterWidget (not in core pack)
- Import OOTB tech dashboards before enabling Level-3 tech links

