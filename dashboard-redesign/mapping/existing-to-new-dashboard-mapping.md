# Existing → New Dashboard Mapping

| Existing dashboard / material | Proposed destination | Disposition |
|-------------------------------|----------------------|-------------|
| SmartAdmin High Level Overview | 01 Platform Value Overview (+ selective links to 02/03/04/07) | Recompose; deep metrics owned elsewhere |
| Introductive Dashboard | 00 Home / Introductory | Redesign; fix Users Resources; neutral branding; keep critical/docs link pattern as placeholders |
| SmartAdmin Alerts and DataSource Performance | 03 Alert Overview; portions to 02 and 04 | Split by concern |
| SmartAdmin Users Roles and API Tokens | 06 Access and Administration | Move largely intact |
| SmartAdmin Device Groups and Websites | 05 Websites and Services; group counts also summarized on 04 | Expand with website token |
| SmartAdmin Cloud/Local - License Counts | 04 (detail); 01 (summary) | Replace `proservices` with `{{ACCOUNT_NAME}}` |
| SmartAdmin LogicModule Status | 08 LogicModule and Content | Drop decorative headers; add noise tables from Alerts |
| Collector Health | 07 Collector Health | Canonical |
| SmartAdmin Collector Health | 07 | **Remove duplicate** |
| Design Template (PSC) | UX standard for 00/01 | Pattern only |
| _Example Exec Dashboard | Nav/landing ideas | Optional JS patterns documented |
| _DynamicDashboardGroups | — | Optional; not core |
| _FilterWidget_v7 | — | Optional; not core |
| OOTB LogicMonitor Dashboards (111) | Level-3 external targets | Link placeholders; do not clone pack |
| Root `SmartAdmin_Client_Experience_Dashboards.json` (01–07) | Reference only | Superseded by this Connected Experience v2 package for new work |
| Public logicmonitor/dashboards | Same as OOTB categories | Relationship targets |

## Functionality retained

All unique SmartAdmin portal metrics are retained somewhere in 00–09. Only exact duplicate Collector Health and decorative LogicModule headers are removed/replaced.
