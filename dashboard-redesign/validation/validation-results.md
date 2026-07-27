# Validation Results — SmartAdmin Connected Experience redesign v2

Automated checks: JSON parse, widget position overlap, missing positions, script tags in text widgets, hardcoded `proservices`, subgroup names, token listing, datasource scrape.

| File | Dashboard | Group | JSON | Widgets | Status | Notes |
|------|-----------|-------|------|---------|--------|-------|
| `dashboard-redesign/dashboards/executive/00_Home_Introductory_redesign_v2.json` | 00 - Home / Introductory | Home (package root; file under executive/) | OK | 17 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/executive/10_Executive_Command_Center_redesign_v2.json` | 10 - Executive Command Center | Executive | OK | 21 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/executive/11_Platform_Value_Overview_redesign_v2.json` | 11 - Platform Value Overview | Executive | OK | 22 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/executive/12_Environment_Health_Executive_redesign_v2.json` | 12 - Environment Health Executive | Executive | OK | 18 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/executive/13_Availability_and_Service_Health_redesign_v2.json` | 13 - Availability and Service Health | Executive | OK | 15 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/executive/14_Capacity_and_Risk_Overview_redesign_v2.json` | 14 - Capacity and Risk Overview | Executive | OK | 17 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/operational/20_Operational_Command_Center_redesign_v2.json` | 20 - Operational Command Center | Operational | OK | 18 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/operational/21_Active_Alerts_redesign_v2.json` | 21 - Active Alerts | Operational | OK | 24 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/operational/22_Resource_Health_redesign_v2.json` | 22 - Resource Health | Operational | OK | 20 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/operational/23_Websites_and_Services_redesign_v2.json` | 23 - Websites and Services | Operational | OK | 15 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/operational/24_Coverage_Capacity_Licenses_redesign_v2.json` | 24 - Coverage, Capacity & Licenses | Operational | OK | 32 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/operational/25_Access_and_Administration_redesign_v2.json` | 25 - Access and Administration | Operational | OK | 18 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/SmartAdmin_Connected_Experience_redesign_v2.json` | SmartAdmin Connected Experience | SmartAdmin Connected Experience (parent) | OK | 326 | **pass_with_portal_config** | Group export: 1 root dashboard(s), subGroups=['Executive', 'Operational', 'Technical'], 16 nested dashboards. |
| `dashboard-redesign/dashboards/technical/30_Technical_Resource_Investigation_redesign_v2.json` | 30 - Technical Resource Investigation | Technical | OK | 14 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/technical/31_Collector_Diagnostics_redesign_v2.json` | 31 - Collector Diagnostics | Technical | OK | 35 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/technical/32_LogicModule_and_Content_redesign_v2.json` | 32 - LogicModule and Content | Technical | OK | 18 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/technical/33_Adoption_and_Optimization_redesign_v2.json` | 33 - Adoption and Optimization | Technical | OK | 17 | **pass_with_portal_config** | Contains post-import placeholders (expected). |
| `dashboard-redesign/dashboards/technical/34_Technology_Dashboard_Directory_redesign_v2.json` | 34 - Technology Dashboard Directory | Technical | OK | 5 | **pass_with_portal_config** | Contains post-import placeholders (expected). |

## Per-file details

### 00 - Home / Introductory

- **File:** `dashboard-redesign/dashboards/executive/00_Home_Introductory_redesign_v2.json`
- **Dashboard group:** Home (package root; file under executive/)
- **JSON validation:** pass
- **Widgets reviewed:** 17
- **Widget types:** `{'text': 8, 'bigNumber': 9}`
- **Tokens:** `[('defaultResourceGroup', '*'), ('defaultResource', '*.logicmonitor.com')]`
- **Placeholders:** `['{{ACCOUNT_NAME}}', '{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_10}}', '{{DASHBOARD_ID_11}}', '{{DASHBOARD_ID_12}}', '{{DASHBOARD_ID_13}}', '{{DASHBOARD_ID_14}}', '{{DASHBOARD_ID_20}}', '{{DASHBOARD_ID_21}}', '{{DASHBOARD_ID_22}}', '{{DASHBOARD_ID_23}}', '{{DASHBOARD_ID_24}}', '{{DASHBOARD_ID_25}}', '{{DASHBOARD_ID_30}}', '{{DASHBOARD_ID_31}}', '{{DASHBOARD_ID_32}}', '{{DASHBOARD_ID_33}}', '{{DASHBOARD_ID_34}}', '{{DASHBOARD_ID_NN}}', '{{OOTB_ALERTING_ID}}', '{{OOTB_CAPACITY_ID}}', '{{OOTB_CLOUD_ID}}', '{{OOTB_NETWORK_ID}}', '{{OOTB_SERVER_ID}}', '{{OOTB_STORAGE_ID}}', '{{OOTB_VIRT_ID}}', '{{OOTB_WEBSITES_ID}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** LogicMonitor_Portal_Alerts, LogicMonitor_Portal_Collectors, LogicMonitor_Portal_LicenseCounts, LogicMonitor_Portal_Resources, LogicMonitor_Portal_Users
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **HTML validation:** Static HTML/CSS only (no script tags allowed in core pack)
- **Final status:** **pass_with_portal_config**

### 10 - Executive Command Center

- **File:** `dashboard-redesign/dashboards/executive/10_Executive_Command_Center_redesign_v2.json`
- **Dashboard group:** Executive
- **JSON validation:** pass
- **Widgets reviewed:** 21
- **Widget types:** `{'text': 7, 'bigNumber': 8, 'gmap': 1, 'noc': 1, 'alert': 2, 'cgraph': 2}`
- **Tokens:** `[('defaultResource', '*.logicmonitor.com'), ('defaultResourceGroup', '*')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_10}}', '{{DASHBOARD_ID_11}}', '{{DASHBOARD_ID_12}}', '{{DASHBOARD_ID_13}}', '{{DASHBOARD_ID_14}}', '{{DASHBOARD_ID_20}}', '{{DASHBOARD_ID_21}}', '{{DASHBOARD_ID_22}}', '{{DASHBOARD_ID_23}}', '{{DASHBOARD_ID_24}}', '{{DASHBOARD_ID_25}}', '{{DASHBOARD_ID_30}}', '{{DASHBOARD_ID_31}}', '{{DASHBOARD_ID_32}}', '{{DASHBOARD_ID_33}}', '{{DASHBOARD_ID_34}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** HostStatus, LogicMonitor_Portal_Alerts, LogicMonitor_Portal_Collectors, LogicMonitor_Portal_Resources, LogicMonitor_Portal_Websites
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **HTML validation:** Static HTML/CSS only (no script tags allowed in core pack)
- **Final status:** **pass_with_portal_config**

### 11 - Platform Value Overview

- **File:** `dashboard-redesign/dashboards/executive/11_Platform_Value_Overview_redesign_v2.json`
- **Dashboard group:** Executive
- **JSON validation:** pass
- **Widgets reviewed:** 22
- **Widget types:** `{'text': 6, 'bigNumber': 12, 'gmap': 1, 'noc': 1, 'cgraph': 2}`
- **Tokens:** `[('defaultResource', '*.logicmonitor.com'), ('defaultResourceGroup', '*')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_10}}', '{{DASHBOARD_ID_11}}', '{{DASHBOARD_ID_12}}', '{{DASHBOARD_ID_13}}', '{{DASHBOARD_ID_14}}', '{{DASHBOARD_ID_20}}', '{{DASHBOARD_ID_21}}', '{{DASHBOARD_ID_22}}', '{{DASHBOARD_ID_23}}', '{{DASHBOARD_ID_24}}', '{{DASHBOARD_ID_25}}', '{{DASHBOARD_ID_30}}', '{{DASHBOARD_ID_31}}', '{{DASHBOARD_ID_32}}', '{{DASHBOARD_ID_33}}', '{{DASHBOARD_ID_34}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** LogicMonitor_Portal_Alerts, LogicMonitor_Portal_Collectors, LogicMonitor_Portal_LicenseCounts, LogicMonitor_Portal_LogicModuleStatus, LogicMonitor_Portal_Resources, LogicMonitor_Portal_Users
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **HTML validation:** Static HTML/CSS only (no script tags allowed in core pack)
- **Final status:** **pass_with_portal_config**

### 12 - Environment Health Executive

- **File:** `dashboard-redesign/dashboards/executive/12_Environment_Health_Executive_redesign_v2.json`
- **Dashboard group:** Executive
- **JSON validation:** pass
- **Widgets reviewed:** 18
- **Widget types:** `{'text': 6, 'bigNumber': 8, 'gmap': 1, 'noc': 1, 'cgraph': 2}`
- **Tokens:** `[('defaultResource', '*.logicmonitor.com'), ('defaultResourceGroup', '*')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_10}}', '{{DASHBOARD_ID_11}}', '{{DASHBOARD_ID_12}}', '{{DASHBOARD_ID_13}}', '{{DASHBOARD_ID_14}}', '{{DASHBOARD_ID_20}}', '{{DASHBOARD_ID_21}}', '{{DASHBOARD_ID_22}}', '{{DASHBOARD_ID_23}}', '{{DASHBOARD_ID_24}}', '{{DASHBOARD_ID_25}}', '{{DASHBOARD_ID_30}}', '{{DASHBOARD_ID_31}}', '{{DASHBOARD_ID_32}}', '{{DASHBOARD_ID_33}}', '{{DASHBOARD_ID_34}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** LogicMonitor_Portal_Alerts, LogicMonitor_Portal_Collectors, LogicMonitor_Portal_MinimalMonitoring, LogicMonitor_Portal_Resources, LogicMonitor_Portal_Websites, MinimalMonitoring
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **HTML validation:** Static HTML/CSS only (no script tags allowed in core pack)
- **Final status:** **pass_with_portal_config**

### 13 - Availability and Service Health

- **File:** `dashboard-redesign/dashboards/executive/13_Availability_and_Service_Health_redesign_v2.json`
- **Dashboard group:** Executive
- **JSON validation:** pass
- **Widgets reviewed:** 15
- **Widget types:** `{'text': 6, 'bigNumber': 8, 'cgraph': 1}`
- **Tokens:** `[('defaultResourceGroup', '*'), ('defaultResource', '*.logicmonitor.com'), ('defaultWebsiteGroup', '*')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_10}}', '{{DASHBOARD_ID_11}}', '{{DASHBOARD_ID_12}}', '{{DASHBOARD_ID_13}}', '{{DASHBOARD_ID_14}}', '{{DASHBOARD_ID_20}}', '{{DASHBOARD_ID_21}}', '{{DASHBOARD_ID_22}}', '{{DASHBOARD_ID_23}}', '{{DASHBOARD_ID_24}}', '{{DASHBOARD_ID_25}}', '{{DASHBOARD_ID_30}}', '{{DASHBOARD_ID_31}}', '{{DASHBOARD_ID_32}}', '{{DASHBOARD_ID_33}}', '{{DASHBOARD_ID_34}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** LogicMonitor_Portal_Alerts, LogicMonitor_Portal_Websites, LogicMonitor_Portal_WebsitesGroups
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **HTML validation:** Static HTML/CSS only (no script tags allowed in core pack)
- **Final status:** **pass_with_portal_config**

### 14 - Capacity and Risk Overview

- **File:** `dashboard-redesign/dashboards/executive/14_Capacity_and_Risk_Overview_redesign_v2.json`
- **Dashboard group:** Executive
- **JSON validation:** pass
- **Widgets reviewed:** 17
- **Widget types:** `{'text': 7, 'bigNumber': 8, 'cgraph': 2}`
- **Tokens:** `[('accountname', '{{ACCOUNT_NAME}}'), ('defaultResourceGroup', '*'), ('defaultResource', '*.logicmonitor.com')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_10}}', '{{DASHBOARD_ID_11}}', '{{DASHBOARD_ID_12}}', '{{DASHBOARD_ID_13}}', '{{DASHBOARD_ID_14}}', '{{DASHBOARD_ID_20}}', '{{DASHBOARD_ID_21}}', '{{DASHBOARD_ID_22}}', '{{DASHBOARD_ID_23}}', '{{DASHBOARD_ID_24}}', '{{DASHBOARD_ID_25}}', '{{DASHBOARD_ID_30}}', '{{DASHBOARD_ID_31}}', '{{DASHBOARD_ID_32}}', '{{DASHBOARD_ID_33}}', '{{DASHBOARD_ID_34}}', '{{DASHBOARD_ID_NN}}', '{{OOTB_ALERTING_ID}}', '{{OOTB_CAPACITY_ID}}', '{{OOTB_CLOUD_ID}}', '{{OOTB_NETWORK_ID}}', '{{OOTB_SERVER_ID}}', '{{OOTB_STORAGE_ID}}', '{{OOTB_VIRT_ID}}', '{{OOTB_WEBSITES_ID}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** LogicMonitor_Portal_LicenseCounts, LogicMonitor_Portal_MinimalMonitoring, LogicMonitor_Portal_Resources, LogicMonitor_Portal_UnmonitoredDevice, MinimalMonitoring, UnmonitoredDevice
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **HTML validation:** Static HTML/CSS only (no script tags allowed in core pack)
- **Final status:** **pass_with_portal_config**

### 20 - Operational Command Center

- **File:** `dashboard-redesign/dashboards/operational/20_Operational_Command_Center_redesign_v2.json`
- **Dashboard group:** Operational
- **JSON validation:** pass
- **Widgets reviewed:** 18
- **Widget types:** `{'text': 6, 'bigNumber': 8, 'alert': 2, 'gmap': 1, 'noc': 1}`
- **Tokens:** `[('defaultResource', '*.logicmonitor.com'), ('defaultResourceGroup', '*')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_10}}', '{{DASHBOARD_ID_11}}', '{{DASHBOARD_ID_12}}', '{{DASHBOARD_ID_13}}', '{{DASHBOARD_ID_14}}', '{{DASHBOARD_ID_20}}', '{{DASHBOARD_ID_21}}', '{{DASHBOARD_ID_22}}', '{{DASHBOARD_ID_23}}', '{{DASHBOARD_ID_24}}', '{{DASHBOARD_ID_25}}', '{{DASHBOARD_ID_30}}', '{{DASHBOARD_ID_31}}', '{{DASHBOARD_ID_32}}', '{{DASHBOARD_ID_33}}', '{{DASHBOARD_ID_34}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** HostStatus, LogicMonitor_Portal_Alerts, LogicMonitor_Portal_Collectors, LogicMonitor_Portal_Resources, LogicMonitor_Portal_Websites
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **HTML validation:** Static HTML/CSS only (no script tags allowed in core pack)
- **Final status:** **pass_with_portal_config**

### 21 - Active Alerts

- **File:** `dashboard-redesign/dashboards/operational/21_Active_Alerts_redesign_v2.json`
- **Dashboard group:** Operational
- **JSON validation:** pass
- **Widgets reviewed:** 24
- **Widget types:** `{'text': 7, 'bigNumber': 6, 'cgraph': 3, 'alert': 2, 'dynamicTable': 6}`
- **Tokens:** `[('defaultResource', '*.logicmonitor.com'), ('defaultResourceGroup', '*')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_10}}', '{{DASHBOARD_ID_11}}', '{{DASHBOARD_ID_12}}', '{{DASHBOARD_ID_13}}', '{{DASHBOARD_ID_14}}', '{{DASHBOARD_ID_20}}', '{{DASHBOARD_ID_21}}', '{{DASHBOARD_ID_22}}', '{{DASHBOARD_ID_23}}', '{{DASHBOARD_ID_24}}', '{{DASHBOARD_ID_25}}', '{{DASHBOARD_ID_30}}', '{{DASHBOARD_ID_31}}', '{{DASHBOARD_ID_32}}', '{{DASHBOARD_ID_33}}', '{{DASHBOARD_ID_34}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** HostStatus, LogicMonitor_Portal_AlertRules, LogicMonitor_Portal_Alerts, LogicMonitor_Portal_DataSources, LogicMonitor_Portal_Escalationchains, LogicMonitor_Portal_Integration, LogicMonitor_Portal_Integrations_Non200Response
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **HTML validation:** Static HTML/CSS only (no script tags allowed in core pack)
- **Final status:** **pass_with_portal_config**

### 22 - Resource Health

- **File:** `dashboard-redesign/dashboards/operational/22_Resource_Health_redesign_v2.json`
- **Dashboard group:** Operational
- **JSON validation:** pass
- **Widgets reviewed:** 20
- **Widget types:** `{'text': 6, 'bigNumber': 8, 'gmap': 1, 'noc': 1, 'cgraph': 2, 'alert': 1, 'dynamicTable': 1}`
- **Tokens:** `[('defaultResource', '*.logicmonitor.com'), ('defaultResourceGroup', '*')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_10}}', '{{DASHBOARD_ID_11}}', '{{DASHBOARD_ID_12}}', '{{DASHBOARD_ID_13}}', '{{DASHBOARD_ID_14}}', '{{DASHBOARD_ID_20}}', '{{DASHBOARD_ID_21}}', '{{DASHBOARD_ID_22}}', '{{DASHBOARD_ID_23}}', '{{DASHBOARD_ID_24}}', '{{DASHBOARD_ID_25}}', '{{DASHBOARD_ID_30}}', '{{DASHBOARD_ID_31}}', '{{DASHBOARD_ID_32}}', '{{DASHBOARD_ID_33}}', '{{DASHBOARD_ID_34}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** HostStatus, LogicMonitor_Portal_Alerts, LogicMonitor_Portal_Collectors, LogicMonitor_Portal_MinimalMonitoring, LogicMonitor_Portal_Resources, LogicMonitor_Portal_Websites, MinimalMonitoring
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **HTML validation:** Static HTML/CSS only (no script tags allowed in core pack)
- **Final status:** **pass_with_portal_config**

### 23 - Websites and Services

- **File:** `dashboard-redesign/dashboards/operational/23_Websites_and_Services_redesign_v2.json`
- **Dashboard group:** Operational
- **JSON validation:** pass
- **Widgets reviewed:** 15
- **Widget types:** `{'text': 7, 'bigNumber': 8}`
- **Tokens:** `[('defaultResourceGroup', '*'), ('defaultResource', '*.logicmonitor.com'), ('defaultWebsiteGroup', '*')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_10}}', '{{DASHBOARD_ID_11}}', '{{DASHBOARD_ID_12}}', '{{DASHBOARD_ID_13}}', '{{DASHBOARD_ID_14}}', '{{DASHBOARD_ID_20}}', '{{DASHBOARD_ID_21}}', '{{DASHBOARD_ID_22}}', '{{DASHBOARD_ID_23}}', '{{DASHBOARD_ID_24}}', '{{DASHBOARD_ID_25}}', '{{DASHBOARD_ID_30}}', '{{DASHBOARD_ID_31}}', '{{DASHBOARD_ID_32}}', '{{DASHBOARD_ID_33}}', '{{DASHBOARD_ID_34}}', '{{DASHBOARD_ID_NN}}', '{{OOTB_ALERTING_ID}}', '{{OOTB_CAPACITY_ID}}', '{{OOTB_CLOUD_ID}}', '{{OOTB_NETWORK_ID}}', '{{OOTB_SERVER_ID}}', '{{OOTB_STORAGE_ID}}', '{{OOTB_VIRT_ID}}', '{{OOTB_WEBSITES_ID}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** LogicMonitor_Portal_DeviceGroups, LogicMonitor_Portal_Websites, LogicMonitor_Portal_WebsitesGroups
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **HTML validation:** Static HTML/CSS only (no script tags allowed in core pack)
- **Final status:** **pass_with_portal_config**

### 24 - Coverage, Capacity & Licenses

- **File:** `dashboard-redesign/dashboards/operational/24_Coverage_Capacity_Licenses_redesign_v2.json`
- **Dashboard group:** Operational
- **JSON validation:** pass
- **Widgets reviewed:** 32
- **Widget types:** `{'text': 7, 'bigNumber': 22, 'dynamicTable': 1, 'cgraph': 2}`
- **Tokens:** `[('accountname', '{{ACCOUNT_NAME}}'), ('defaultResourceGroup', '*'), ('defaultResource', '*.logicmonitor.com')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_10}}', '{{DASHBOARD_ID_11}}', '{{DASHBOARD_ID_12}}', '{{DASHBOARD_ID_13}}', '{{DASHBOARD_ID_14}}', '{{DASHBOARD_ID_20}}', '{{DASHBOARD_ID_21}}', '{{DASHBOARD_ID_22}}', '{{DASHBOARD_ID_23}}', '{{DASHBOARD_ID_24}}', '{{DASHBOARD_ID_25}}', '{{DASHBOARD_ID_30}}', '{{DASHBOARD_ID_31}}', '{{DASHBOARD_ID_32}}', '{{DASHBOARD_ID_33}}', '{{DASHBOARD_ID_34}}', '{{DASHBOARD_ID_NN}}', '{{OOTB_ALERTING_ID}}', '{{OOTB_CAPACITY_ID}}', '{{OOTB_CLOUD_ID}}', '{{OOTB_NETWORK_ID}}', '{{OOTB_SERVER_ID}}', '{{OOTB_STORAGE_ID}}', '{{OOTB_VIRT_ID}}', '{{OOTB_WEBSITES_ID}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** LogicMonitor_Portal_DeviceGroups, LogicMonitor_Portal_LicenseCounts, LogicMonitor_Portal_NetScanDevices_perday, LogicMonitor_Portal_Netscans, LogicMonitor_Portal_UnmonitoredDevice, LogicMonitor_Portal_WebsitesGroups, UnmonitoredDevice
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **HTML validation:** Static HTML/CSS only (no script tags allowed in core pack)
- **Final status:** **pass_with_portal_config**

### 25 - Access and Administration

- **File:** `dashboard-redesign/dashboards/operational/25_Access_and_Administration_redesign_v2.json`
- **Dashboard group:** Operational
- **JSON validation:** pass
- **Widgets reviewed:** 18
- **Widget types:** `{'text': 6, 'bigNumber': 12}`
- **Tokens:** `[('defaultResource', '*.logicmonitor.com'), ('defaultResourceGroup', '*')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_10}}', '{{DASHBOARD_ID_11}}', '{{DASHBOARD_ID_12}}', '{{DASHBOARD_ID_13}}', '{{DASHBOARD_ID_14}}', '{{DASHBOARD_ID_20}}', '{{DASHBOARD_ID_21}}', '{{DASHBOARD_ID_22}}', '{{DASHBOARD_ID_23}}', '{{DASHBOARD_ID_24}}', '{{DASHBOARD_ID_25}}', '{{DASHBOARD_ID_30}}', '{{DASHBOARD_ID_31}}', '{{DASHBOARD_ID_32}}', '{{DASHBOARD_ID_33}}', '{{DASHBOARD_ID_34}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** APITokens, LogicMonitor_Portal_APITokens, LogicMonitor_Portal_Roles, LogicMonitor_Portal_UserGroups, LogicMonitor_Portal_Users, LogicMonitor_Portal_Users_NotLogin, Users_NotLogin
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **HTML validation:** Static HTML/CSS only (no script tags allowed in core pack)
- **Final status:** **pass_with_portal_config**

### SmartAdmin Connected Experience

- **File:** `dashboard-redesign/dashboards/SmartAdmin_Connected_Experience_redesign_v2.json`
- **Dashboard group:** SmartAdmin Connected Experience (parent)
- **JSON validation:** pass
- **Widgets reviewed:** 326
- **Tokens:** `[('defaultResourceGroup', '*'), ('defaultResource', '*.logicmonitor.com'), ('defaultWebsiteGroup', '*'), ('accountname', '{{ACCOUNT_NAME}}')]`
- **Placeholders:** `['{{ACCOUNT_NAME}}', '{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_10}}', '{{DASHBOARD_ID_11}}', '{{DASHBOARD_ID_12}}', '{{DASHBOARD_ID_13}}', '{{DASHBOARD_ID_14}}', '{{DASHBOARD_ID_20}}', '{{DASHBOARD_ID_21}}', '{{DASHBOARD_ID_22}}', '{{DASHBOARD_ID_23}}', '{{DASHBOARD_ID_24}}', '{{DASHBOARD_ID_25}}', '{{DASHBOARD_ID_30}}', '{{DASHBOARD_ID_31}}', '{{DASHBOARD_ID_32}}', '{{DASHBOARD_ID_33}}', '{{DASHBOARD_ID_34}}', '{{DASHBOARD_ID_NN}}', '{{OOTB_ALERTING_ID}}', '{{OOTB_CAPACITY_ID}}', '{{OOTB_CLOUD_ID}}', '{{OOTB_NETWORK_ID}}', '{{OOTB_SERVER_ID}}', '{{OOTB_STORAGE_ID}}', '{{OOTB_VIRT_ID}}', '{{OOTB_WEBSITES_ID}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **HTML validation:** Static HTML/CSS only (no script tags allowed in core pack)
- **Final status:** **pass_with_portal_config**

### 30 - Technical Resource Investigation

- **File:** `dashboard-redesign/dashboards/technical/30_Technical_Resource_Investigation_redesign_v2.json`
- **Dashboard group:** Technical
- **JSON validation:** pass
- **Widgets reviewed:** 14
- **Widget types:** `{'text': 5, 'bigNumber': 4, 'alert': 2, 'cgraph': 2, 'dynamicTable': 1}`
- **Tokens:** `[('defaultResource', '*.logicmonitor.com'), ('defaultResourceGroup', '*')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_10}}', '{{DASHBOARD_ID_11}}', '{{DASHBOARD_ID_12}}', '{{DASHBOARD_ID_13}}', '{{DASHBOARD_ID_14}}', '{{DASHBOARD_ID_20}}', '{{DASHBOARD_ID_21}}', '{{DASHBOARD_ID_22}}', '{{DASHBOARD_ID_23}}', '{{DASHBOARD_ID_24}}', '{{DASHBOARD_ID_25}}', '{{DASHBOARD_ID_30}}', '{{DASHBOARD_ID_31}}', '{{DASHBOARD_ID_32}}', '{{DASHBOARD_ID_33}}', '{{DASHBOARD_ID_34}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** HostStatus, LogicMonitor_Portal_Alerts, LogicMonitor_Portal_Collectors, LogicMonitor_Portal_Resources
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **HTML validation:** Static HTML/CSS only (no script tags allowed in core pack)
- **Final status:** **pass_with_portal_config**

### 31 - Collector Diagnostics

- **File:** `dashboard-redesign/dashboards/technical/31_Collector_Diagnostics_redesign_v2.json`
- **Dashboard group:** Technical
- **JSON validation:** pass
- **Widgets reviewed:** 35
- **Widget types:** `{'text': 7, 'bigNumber': 11, 'dynamicTable': 3, 'alert': 1, 'cgraph': 13}`
- **Tokens:** `[('defaultResourceGroup', '*'), ('defaultResourceName', '*')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_10}}', '{{DASHBOARD_ID_11}}', '{{DASHBOARD_ID_12}}', '{{DASHBOARD_ID_13}}', '{{DASHBOARD_ID_14}}', '{{DASHBOARD_ID_20}}', '{{DASHBOARD_ID_21}}', '{{DASHBOARD_ID_22}}', '{{DASHBOARD_ID_23}}', '{{DASHBOARD_ID_24}}', '{{DASHBOARD_ID_25}}', '{{DASHBOARD_ID_30}}', '{{DASHBOARD_ID_31}}', '{{DASHBOARD_ID_32}}', '{{DASHBOARD_ID_33}}', '{{DASHBOARD_ID_34}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** ActiveDiscoveryTasks, DataCollectingTasks, LogicMonitor_Collector_ActiveDiscoveryTasks, LogicMonitor_Collector_DataCollectingTasks, LogicMonitor_Collector_JVMStatus
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **HTML validation:** Static HTML/CSS only (no script tags allowed in core pack)
- **Final status:** **pass_with_portal_config**

### 32 - LogicModule and Content

- **File:** `dashboard-redesign/dashboards/technical/32_LogicModule_and_Content_redesign_v2.json`
- **Dashboard group:** Technical
- **JSON validation:** pass
- **Widgets reviewed:** 18
- **Widget types:** `{'text': 5, 'bigNumber': 8, 'dynamicTable': 5}`
- **Tokens:** `[('defaultResourceGroup', '*'), ('defaultResourceName', '*.logicmonitor.com')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_10}}', '{{DASHBOARD_ID_11}}', '{{DASHBOARD_ID_12}}', '{{DASHBOARD_ID_13}}', '{{DASHBOARD_ID_14}}', '{{DASHBOARD_ID_20}}', '{{DASHBOARD_ID_21}}', '{{DASHBOARD_ID_22}}', '{{DASHBOARD_ID_23}}', '{{DASHBOARD_ID_24}}', '{{DASHBOARD_ID_25}}', '{{DASHBOARD_ID_30}}', '{{DASHBOARD_ID_31}}', '{{DASHBOARD_ID_32}}', '{{DASHBOARD_ID_33}}', '{{DASHBOARD_ID_34}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** LogicMonitor_Portal_DataSources, LogicMonitor_Portal_LogicModuleStatus
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **HTML validation:** Static HTML/CSS only (no script tags allowed in core pack)
- **Final status:** **pass_with_portal_config**

### 33 - Adoption and Optimization

- **File:** `dashboard-redesign/dashboards/technical/33_Adoption_and_Optimization_redesign_v2.json`
- **Dashboard group:** Technical
- **JSON validation:** pass
- **Widgets reviewed:** 17
- **Widget types:** `{'text': 7, 'cgraph': 6, 'bigNumber': 4}`
- **Tokens:** `[('defaultResource', '*.logicmonitor.com'), ('defaultResourceGroup', '*')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_10}}', '{{DASHBOARD_ID_11}}', '{{DASHBOARD_ID_12}}', '{{DASHBOARD_ID_13}}', '{{DASHBOARD_ID_14}}', '{{DASHBOARD_ID_20}}', '{{DASHBOARD_ID_21}}', '{{DASHBOARD_ID_22}}', '{{DASHBOARD_ID_23}}', '{{DASHBOARD_ID_24}}', '{{DASHBOARD_ID_25}}', '{{DASHBOARD_ID_30}}', '{{DASHBOARD_ID_31}}', '{{DASHBOARD_ID_32}}', '{{DASHBOARD_ID_33}}', '{{DASHBOARD_ID_34}}', '{{DASHBOARD_ID_NN}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Datasources detected:** APITokens, LogicMonitor_Portal_APITokens, LogicMonitor_Portal_Alerts, LogicMonitor_Portal_DataSources, LogicMonitor_Portal_Integrations_Non200Response, LogicMonitor_Portal_MinimalMonitoring, LogicMonitor_Portal_Resources, LogicMonitor_Portal_UnmonitoredDevice, LogicMonitor_Portal_UserGroups, LogicMonitor_Portal_Users_NotLogin, MinimalMonitoring, UnmonitoredDevice, Users_NotLogin
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **HTML validation:** Static HTML/CSS only (no script tags allowed in core pack)
- **Final status:** **pass_with_portal_config**

### 34 - Technology Dashboard Directory

- **File:** `dashboard-redesign/dashboards/technical/34_Technology_Dashboard_Directory_redesign_v2.json`
- **Dashboard group:** Technical
- **JSON validation:** pass
- **Widgets reviewed:** 5
- **Widget types:** `{'text': 5}`
- **Tokens:** `[('defaultResource', '*.logicmonitor.com'), ('defaultResourceGroup', '*')]`
- **Placeholders:** `['{{DASHBOARD_ID_00}}', '{{DASHBOARD_ID_10}}', '{{DASHBOARD_ID_11}}', '{{DASHBOARD_ID_12}}', '{{DASHBOARD_ID_13}}', '{{DASHBOARD_ID_14}}', '{{DASHBOARD_ID_20}}', '{{DASHBOARD_ID_21}}', '{{DASHBOARD_ID_22}}', '{{DASHBOARD_ID_23}}', '{{DASHBOARD_ID_24}}', '{{DASHBOARD_ID_25}}', '{{DASHBOARD_ID_30}}', '{{DASHBOARD_ID_31}}', '{{DASHBOARD_ID_32}}', '{{DASHBOARD_ID_33}}', '{{DASHBOARD_ID_34}}', '{{DASHBOARD_ID_NN}}', '{{OOTB_ALERTING_ID}}', '{{OOTB_CAPACITY_ID}}', '{{OOTB_CLOUD_ID}}', '{{OOTB_NETWORK_ID}}', '{{OOTB_SERVER_ID}}', '{{OOTB_STORAGE_ID}}', '{{OOTB_VIRT_ID}}', '{{OOTB_WEBSITES_ID}}', '{{PORTAL_BASE}}']`
- **Overlaps:** none
- **Script tags in text:** none
- **Link validation:** Placeholders only — **portal testing required** for live URLs
- **HTML validation:** Static HTML/CSS only (no script tags allowed in core pack)
- **Final status:** **pass_with_portal_config**

## Portal testing required

- Resolve `{{PORTAL_BASE}}` and `{{DASHBOARD_ID_NN}}` after import
- Resolve `{{OOTB_*_ID}}` after importing OOTB technology packs
- Set `accountname` / `{{ACCOUNT_NAME}}` for license widgets
- Confirm nested subgroups appear as Executive / Operational / Technical
- Portal assigns subgroup IDs — do not copy IDs from another portal
- Confirm portal LogicModules applied
- Verify Introductive title shells and DCC card HTML render in text widgets

