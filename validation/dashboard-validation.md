# Dashboard Validation

Static validation of final Connected Experience redesign v2 dashboards.
Portal UI rendering and live datapoint checks are **not** claimed here.

| Dashboard | Group | JSON Valid | Navigation Valid | Modules Mapped | Links Valid | Portal Testing Required | Status |
| --------- | ----- | ---------- | ---------------- | -------------- | ----------- | ----------------------- | ------ |
| 00 - Home / Introductory | Home | Yes | Yes | Yes | Yes | Yes | pass_static |
| 10 - Executive Command Center | Executive | Yes | Yes | Yes | Yes | Yes | pass_static |
| 11 - Platform Value Overview | Executive | Yes | Yes | Yes | Yes | Yes | pass_static |
| 12 - Environment Health Executive | Executive | Yes | Yes | Yes | Yes | Yes | pass_static |
| 13 - Availability and Service Health | Executive | Yes | Yes | Yes | Yes | Yes | pass_static |
| 14 - Capacity and Risk Overview | Executive | Yes | Yes | Yes | Yes | Yes | pass_static |
| 20 - Operational Command Center | Operational | Yes | Yes | Yes | Yes | Yes | pass_static |
| 21 - Active Alerts | Operational | Yes | Yes | Yes | Yes | Yes | pass_static |
| 22 - Resource Health | Operational | Yes | Yes | Yes | Yes | Yes | pass_static |
| 23 - Websites and Services | Operational | Yes | Yes | Yes | Yes | Yes | pass_static |
| 24 - Coverage, Capacity & Licenses | Operational | Yes | Yes | Yes | Yes | Yes | pass_static |
| 25 - Access and Administration | Operational | Yes | Yes | Yes | Yes | Yes | pass_static |
| 30 - Technical Resource Investigation | Technical | Yes | Yes | Yes | Yes | Yes | pass_static |
| 31 - Collector Diagnostics | Technical | Yes | Yes | Yes | Yes | Yes | pass_static |
| 32 - LogicModule and Content | Technical | Yes | Yes | Yes | Yes | Yes | pass_static |
| 33 - Adoption and Optimization | Technical | Yes | Yes | Yes | Yes | Yes | pass_static |
| 34 - Technology Dashboard Directory | Technical | Yes | Yes | Yes | Yes | Yes | pass_static |

## Group package

| File | JSON Valid | Notes | Portal Testing Required |
| ---- | ---------- | ----- | ----------------------- |
| `SmartAdmin_Connected_Experience_redesign_v2.json` | Yes | subGroups=['Executive', 'Operational', 'Technical'] | Yes |

## Checks performed

- JSON parse
- Navigation widget present and matches `navigation/html/`
- Exactly one CURRENT navigation indicator
- Hyperlinks match navigation sources (no placeholders in nav HTML)
- Datasource names scraped and recorded against `modules/` mapping

## Checks requiring a LogicMonitor portal

- Widget rendering and HTML theme compatibility
- Datapoint / instance availability
- Token and filter scopes
- Resource / website group membership
- Time ranges and alert windows
- Dashboard permissions and sharing
- Empty or missing data diagnosis

