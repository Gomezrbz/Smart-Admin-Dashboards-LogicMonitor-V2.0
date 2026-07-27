# Existing → New Dashboard Mapping

| Existing Dashboard | Proposed Dashboard | Group | Main Changes | Reused Components |
|--------------------|--------------------|-------|--------------|-------------------|
| Introductive Dashboard | 00 Home / Introductory | Home | Lobby + groups; neutralize Harvard branding; Introductive title system | Alert/collector/user KPIs, educational HTML patterns |
| Design Template / DCC PSC Command Center | 10 Executive Command Center (+ chrome on others) | Executive | UX + card chrome only; portable metrics; no PSC datapoints | Guide→KPI→map→exceptions flow, gradients, pills |
| SmartAdmin High Level Overview | 11 Platform Value; also feeds 10/12/20 | Executive | Recompose; Introductive guides; DCC nav | bigNumber, gmap, noc, alert, cgraph widgets |
| — (composed) | 12 Environment Health Executive | Executive | New exec-density slice | Overview/alerts map, NOC, dead/minimal KPIs |
| — (composed) | 13 Availability and Service Health | Executive | New from websites + intro alerts | Groups website KPIs, intro alert strip |
| SmartAdmin Cloud/Local License Counts + coverage KPIs | 14 Capacity and Risk Overview | Executive | New exec capacity risk | License bigNumbers, unmonitored/minimal trends |
| — (composed) | 20 Operational Command Center | Operational | New triage hub | Overview alerts, map/NOC, collector pulse |
| SmartAdmin Alerts and DataSource Performance | 21 Active Alerts | Operational | Rename; restyle; nav | Alert KPIs, tables, trends, rules, integrations |
| High Level + Alerts (env slice) | 22 Resource Health | Operational | Rename from Environment Health; restyle | Map, NOC, dead/minimal, idle |
| SmartAdmin Device Groups and Websites | 23 Websites and Services | Operational | Restyle; website token | Website/group bigNumbers |
| Licenses + Alerts netscan/coverage + Groups | 24 Coverage, Capacity & Licenses | Operational | Restyle; OOTB directory | License, netscan, group widgets |
| SmartAdmin Users Roles and API Tokens | 25 Access and Administration | Operational | Restyle | User/role/token bigNumbers |
| — (composed) | 30 Technical Resource Investigation | Technical | New investigation hub | Alert lists, trends, idle, path inventory |
| Collector Health (deduped) | 31 Collector Diagnostics | Technical | Rename; restyle; remove duplicate SmartAdmin Collector Health | Full collector widget set |
| SmartAdmin LogicModule Status + alert noise tables | 32 LogicModule and Content | Technical | Restyle | Module counts + 90d tables |
| Composite hygiene metrics | 33 Adoption and Optimization | Technical | Restyle | Alert/user/coverage/integration trends |
| OOTB LogicMonitor Dashboards (111) | 34 Technology Dashboard Directory | Technical | Link directory only; not cloned | Labels + `{{OOTB_*_ID}}` placeholders |
| Root Client Experience (01–07) | Reference only | — | Superseded by this package | — |
| _Example Exec / _DynamicDashboardGroups / _FilterWidget | Optional docs only | — | Not in core pack (JS) | — |

IDs are sequential within each group: Home `00`, Executive `10–14`, Operational `20–25`, Technical `30–34`.

## Functionality retained

All unique SmartAdmin portal metrics remain somewhere in 00–34. Duplicate Collector Health removed. PSC FortiGate/region metrics are not copied.
