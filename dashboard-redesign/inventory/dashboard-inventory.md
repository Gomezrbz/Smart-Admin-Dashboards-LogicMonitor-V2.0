# Dashboard Source Inventory

**Generated for:** SmartAdmin Connected Experience redesign v2 (expanded Exec/Ops/Tech)  
**Santaba release:** 242  
**Sources scanned:** Basement/, New Dashboards/, public [logicmonitor/dashboards](https://github.com/logicmonitor/dashboards)  
**Rule:** Original source files were not modified.  
**Design system:** Introductive titles (`design-system/title-style.md`) + DCC cards/tables (`design-system/table-style.md`).

---

## 1. Primary sources (Basement + New Dashboards utilities)

| Source file | Dashboard name | Purpose | Audience | Main widgets | Tokens | Filters | Dependencies | Related dashboards | Recommendation | Proposed destination |
|-------------|----------------|---------|----------|--------------|--------|---------|--------------|--------------------|----------------|----------------------|
| `Basement/SmartAdmin Dashboards.json` | SmartAdmin High Level Overview | Portal health snapshot | Admins, leads | text, bigNumber×22, alert×3, cgraph×2, gmap, noc | `defaultResource=*.logicmonitor.com`, `defaultResourceGroup=*` | Resource / group tokens | Portal Alerts, Collectors, Resources, Licenses, LogicModules, Users | Peer SmartAdmin dashboards | Recompose as executive entry KPIs; remove deep duplicates | **01 / 10 / 11 / 20** (+ signals to 02/03/07) |
| `Basement/SmartAdmin Dashboards.json` | SmartAdmin Alerts and DataSource Performance | Alert + monitoring hygiene | Admins, ops | text×2, bigNumber×18, dynamicTable×9, cgraph×7 | same portal tokens | Resource / group | Portal Alerts, AlertRules, Escalationchains, Integrations, Resources, Netscans, LogicModule 90d alerts | Overview, Collector, LogicModule | Split by concern | **03 Active Alerts**; **02 Resource Health**; **04**; also **13 / 20 / 30** |
| `Basement/SmartAdmin Dashboards.json` | SmartAdmin Users Roles and API Tokens | Access inventory | Security, portal admins | text, bigNumber×12 | portal tokens | Resource / group | Portal Users, Roles, UserGroups, APITokens, Users_NotLogin | Overview | Move largely intact | **06 Access and Administration** |
| `Basement/SmartAdmin Dashboards.json` | SmartAdmin Device Groups and Websites | Group/website hygiene | Portal admins | text, bigNumber×8 | portal tokens | Resource / group | DeviceGroups, Websites, WebsitesGroups | Overview, Coverage | Expand with website token pattern | **05 Websites and Services** (+ group hygiene on **04**) |
| `Basement/SmartAdmin Dashboards.json` | SmartAdmin LogicModule Status | Module inventory counts | Content/admins | text×8 (decorative), bigNumber×8 | `defaultResourceName=*.logicmonitor.com`, `defaultResourceGroup=*` | Resource / group | LogicModuleStatus | Alerts (noise tables) | Replace empty headers with one guide; keep counts | **08 LogicModule and Content** |
| `Basement/SmartAdmin Dashboards.json` | SmartAdmin Cloud/Local - License Counts | License consumption | Admins, capacity/FinOps | bigNumber×14 | `accountname=proservices` only | Account name | LicenseCounts | Overview | Replace hardcoded account with placeholder; detail on coverage | **04** (detail); **13 Capacity Risk**; **01** (summary) |
| `Basement/SmartAdmin Dashboards.json` | Collector Health | Collector performance | Platform engineers | text×3, bigNumber×11, cgraph×13, dynamicTable×3, alert | `defaultResourceGroup=*`, `defaultResourceName=*` | Resource / group | Collector JVM, DataCollectingTasks, ActiveDiscoveryTasks | Overview alerts | Keep as canonical technical diagnostics | **07 Collector Diagnostics** |
| `Basement/SmartAdmin Dashboards.json` | SmartAdmin Collector Health | Exact duplicate of Collector Health | Same | Same 31-widget signature | same | same | same | Collector Health | **Remove duplicate** | Merge into **07** |
| `Basement/Introductive_Dashboard.json` | Introductive Dashboard | Onboarding + portal snapshot | New users, operators | text×8, bigNumber×15, alert×2, gmap, dynamicTable, cgraph | `defaultResourceGroup=*` | Resource group | Portal Alerts, Collectors, Users, JVM | Critical client ops links (external) | Redesign as Home; title system for suite; drop Harvard branding | **00 Home / Introductory** + title design system |
| `Basement/Design_Template.json` / DCC PSC Command Center | DCC - PSC Network Health Executive Command Center | Executive network command center (client-specific) | Executives, ops | text×2, bigNumber×2, viz×2, gmap, alert, noc, dynamicTable, pieChart, cgraph | `defaultResourceGroup=PSC`, `defaultResourceName=*` | Group / resource | Client FortiGate / regional (not in SmartAdmin) | Team drill-downs | **UX + card chrome** (not PSC metrics) | **10 Exec CC**, **20 Ops CC**, **30 Investigation**, table design system |
| `New Dashboards/_Example_Exec_Dashboard.json` | _Example Exec Dashboard | Multi-dashboard exec landing with dynamic list + map | Executives | text×2 (JS), noc, deviceStatus×2 | Many map + `defaultDashboardGroup`, `DashboardsToExclude` | Dashboard group / map filters | Portal API (dynamic list), map CDN | Customer dashboard groups | Extract nav/landing pattern; JS requires portal validation | Documented optional enhancement; static HTML used in core pack |
| `New Dashboards/_DynamicDashboardGroups.json` | _DynamicDashboardGroups | Dynamic dashboard list with alert status | Admins | text×3 (ES5 JS) | `defaultDashboardGroup1/2/3`, `AlertSeveritiesToShow`, theme tokens | Dashboard group | LM REST API inside text widget | Any dashboard group | Do **not** ship as core nav | Optional / portal validation required |
| `New Dashboards/_FilterWidget_v7.json` | _FilterWidget_v7 | Resource selector wizard + sample widgets | Admins, ops | text×2 (JS), alert, bigNumber, cgraph, dynamicTable | `defaultResourceGroup`, `ResourceRegex` | Resource group / regex | Portal resources | Scoped operational views | Optional advanced filter pattern | Documented; not in core pack |

---

## 2. OOTB pack summary (`New Dashboards/LogicMonitor Dashboards.json`)

**111 dashboards** across **18 subgroups** (mirrors [logicmonitor/dashboards](https://github.com/logicmonitor/dashboards)).

| Subgroup | Dashboards | Role for redesign |
|----------|------------|-------------------|
| Capacity Management | 1 | Level-3 link target for capacity/utilization |
| Cloud | 3 | AWS/Azure/GCP overview link targets |
| Databases | 3 | Tech drill-down links |
| Environmental | 1 | Optional L3 |
| GCP | 7 | Cloud L3 |
| Hardware | 4 | Tech L3 |
| Kubernetes | 7 | Tech L3 |
| Linux | 4 | Capacity/performance L3 |
| LogicMonitor | 5 | Welcome / platform examples (html nav patterns) |
| Logs | 1 | Optional (license-dependent) |
| Microsoft | 10 | Tech L3 |
| Network | 29 | Largest tech surface; L3 links |
| SaaS | 6 | L3 |
| Storage | 7 | Capacity L3 |
| Virtualization | 6 | Capacity L3 |
| Voice | 2 | Optional L3 |
| Alerting | 6 | Complements Alert Overview |
| Applications | 9 | L3 |

**Common OOTB tokens:** `##defaultResourceGroup##`, `##defaultResourceName##`, `##defaultWebsiteGroup##`, plus product-specific tokens.  
**Disposition:** Do **not** clone the full pack. Document as **34 Technology Dashboard Directory** targets with `{{OOTB_*_ID}}` placeholders. Prefer importing OOTB packages separately, then wiring links post-import.

**Public repo notes (from README):**
- 216+ individual JSON files in the public catalog (includes cloud service dashboards beyond the grouped export).
- Importers must set `##defaultResourceGroup##` when not inherited.
- Many dashboards depend on current LogicModules and dynamic groups (`Devices by Type/...`).
- Packages/ folder may lag individual files.

---

## 3. Widget type inventory (SmartAdmin visual language)

| Type | Usage in SmartAdmin | Keep as identity |
|------|---------------------|------------------|
| `bigNumber` | KPI scorecards | Yes — primary status language |
| `cgraph` | Trends / top-N | Yes |
| `dynamicTable` | Ranked multi-column lists | Yes |
| `alert` | Live exceptions | Yes |
| `gmap` | Geographic alert concentration | Yes on L1/L2 |
| `noc` | Type-based health | Yes on L1/L2 |
| `text` | Banners / guides / nav | Yes — evolve to guides + nav (not empty headers) |

Themes observed: almost all `newSolidDarkBlue`; occasional `newSolidBlue` / `borderPurple`.

---

## 4. Confirmed datasources / LogicModules (Phase 1–5 baseline)

| Family | Examples |
|--------|----------|
| Portal alerts / rules | `LogicMonitor_Portal_Alerts`, `LogicMonitor_Portal_AlertRules`, `LogicMonitor_Portal_Escalationchains`, `LogicMonitor_Portal_Integration(s)` |
| Resources / websites | `LogicMonitor_Portal_Resources`, `LogicMonitor_Portal_Websites`, device/website groups, MinimalMonitoring, UnmonitoredDevice, netscans |
| Collectors | `LogicMonitor_Portal_Collectors`, `LogicMonitor_Collector_JVMStatus`, `DataCollectingTasks`, `ActiveDiscoveryTasks` |
| Users / access | `LogicMonitor_Portal_Users`, `Users_NotLogin`, `UserGroups`, `APITokens`, `Roles` |
| Licenses / modules | `LogicMonitor_Portal_LicenseCounts`, `LogicMonitor_Portal_LogicModuleStatus`, LogicModule alert-over-90-days |
| Misc | `HostStatus` (idle interval) |

---

## 5. Duplicates and defects

| Issue | Evidence | Action |
|-------|----------|--------|
| Twin Collector Health dashboards | 31/31 matching widget signature | Keep one → **07** |
| Repeated alert / dead / module scorecards across Overview + Alerts + Intro | Same bigNumbers on multiple pages | One owner per metric family; summaries only on 00/01 |
| LogicModule decorative text×8 | Near-identical headers | Replace with single guide |
| Introductive Users Resources copies Collectors content | Confirmed content bug | Fix in **00** |
| License `accountname=proservices` | Hardcoded | Use `{{ACCOUNT_NAME}}` / configurable token |
| Harvard branding on Introductive | Client-specific banner | Neutral SmartAdmin Connected branding |
| Sparse descriptions | Most `description` fields empty | Populate on all redesign dashboards |

---

## 6. Gap analysis (summary)

| Gap | Severity | Redesign response |
|-----|----------|-------------------|
| No unified Home entry | High | **00 Home / Introductory** |
| Weak progressive navigation | High | Global HTML menu + cards + footers |
| Admin-centric framing (weak client value story) | High | **01** + **09** value packaging |
| Environment Health vs Alerts conflated | Medium | Split **02** and **03** |
| No website-scoped token on SmartAdmin | Medium | Add `defaultWebsiteGroup` on **05** |
| No infra capacity metrics in SmartAdmin | Expected | L3 OOTB Capacity/Cloud/Network **links**, not invented metrics |
| Dynamic/filter JS nav not portable | Medium | Document as optional; static HTML core |
| Missing empty-state guidance | Medium | Guide widgets explain zero/empty |
| Client Experience suite (01–07) exists at repo root | N/A | Reference only; fresh package under `dashboard-redesign/` |

---

## 7. Visual identity (preserve)

- Theme: `newSolidDarkBlue`
- Guide HTML: slate surfaces `#0f172a` / `#0b1220`, borders `#1f2937`, text `#e5e7eb`, accent `#38bdf8`
- Typography: Arial/Helvetica hierarchy in text widgets
- Severity colors: reserved for Critical / Error / Warning status — not decorative
- Layout order: navigation → critical status → KPIs → trends → tables → diagnostics

Significant visual changes (documented):

| Change | Why |
|--------|-----|
| Remove Harvard crimson banner | Multi-client package; brand-neutral |
| Compact global menu vs full-width duplicate banners | Saves space; consistent orientation |
| Question-driven widget titles | Faster scanning for clients |
| Fewer decorative LogicModule headers | Reduces clutter |
