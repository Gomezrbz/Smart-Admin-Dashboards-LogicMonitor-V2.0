# Dashboard Redesign Proposal

**Package:** SmartAdmin Connected Experience redesign v2 (expanded)  
**Status:** Implementation under `dashboard-redesign/`  
**Baseline:** SmartAdmin + Introductive + DCC design chrome; OOTB / public LM repo for technology directory targets. Client Experience suite at repo root is reference only.

---

## 1. Executive summary

This package delivers a **connected client experience** with three named dashboard groups (**Executive**, **Operational**, **Technical**), a Home lobby, and composed command-center / investigation dashboards beyond SmartAdmin-only sources. Titles follow the Introductive Dashboard educational-panel system. Summary and navigation tables follow DCC Executive Command Center card chrome (with a documented table adaptation for inventories). Original source JSON is unchanged.

---

## 2. Current-state assessment

| Source | Role |
|--------|------|
| `Basement/SmartAdmin Dashboards.json` | Portal-admin metrics (primary widget library) |
| `Basement/Introductive_Dashboard.json` | Title/header visual system + home KPIs |
| `Basement/DCC_-_PSC_…Command_Center (1).json` | Exec layout + card/table chrome (**not** PSC metrics) |
| `New Dashboards/LogicMonitor Dashboards.json` | OOTB technology link targets |
| Root Client Experience JSON | Superseded reference |

Gaps addressed vs prior v2: Introductive title fidelity, DCC table/card fidelity, named Exec/Ops/Tech subgroups, command centers, capacity/availability exec views, investigation hub, technology directory.

---

## 3. Design references

| Concern | Reference | Document |
|---------|-----------|----------|
| Titles / headers / nav shells | Introductive | `design-system/title-style.md` |
| Summary / nav / inventory tables | DCC | `design-system/table-style.md` |
| Spacing, density, severity, tokens | Combined | `design-system/dashboard-design-standards.md` |

Harvard red marquee branding is neutralized; typography and shell structure are retained.

---

## 4. Dashboard-group architecture

```
SmartAdmin Connected Experience (dashboardgroup)
├── dashboards: [00 Home / Introductory]
└── subGroups:
    ├── Executive → 10, 01, 11, 12, 13
    ├── Operational → 20, 03, 02, 05, 04, 06
    └── Technical → 30, 07, 08, 09, 31
```

LM exports use nested structure, not portable `groupId` fields. Post-import: verify subgroup names; record portal-assigned IDs locally.

---

## 5. Executive dashboards

| ID | Purpose |
|----|---------|
| 10 Executive Command Center | DCC flow: guide → KPI → map → exceptions → trends |
| 01 Platform Value Overview | Health, coverage, licenses, value |
| 11 Environment Health Executive | Exec-density risk concentration |
| 12 Availability and Service Health | Websites/services + severity |
| 13 Capacity and Risk Overview | Licenses, coverage gaps, OOTB capacity links |

Audience: leadership, CS leads. Avoid deep collector method tables.

---

## 6. Operational dashboards

| ID | Purpose |
|----|---------|
| 20 Operational Command Center | Daily triage hub |
| 03 Active Alerts | Severity, rules, integrations, noise |
| 02 Resource Health | Map/NOC, dead/minimal, idle |
| 05 Websites and Services | Website/group hygiene |
| 04 Coverage, Capacity & Licenses | Discovery, licenses, groups |
| 06 Access and Administration | Users, roles, tokens |

Audience: NOC, portal admins, ops.

---

## 7. Technical dashboards

| ID | Purpose |
|----|---------|
| 30 Technical Resource Investigation | Investigation checklist + paths |
| 07 Collector Diagnostics | JVM, tasks, method mix |
| 08 LogicModule and Content | Inventory + 90-day noise |
| 09 Adoption and Optimization | Improvement signals |
| 31 Technology Dashboard Directory | OOTB Network/Server/Storage/Cloud/Capacity links |

No empty Network/Server/Storage/Cloud metric dashboards.

---

## 8. Introductive / Home redesign

Home is the package lobby: group explanations, role starts, environment summary, filter instructions, technology directory, links to command centers.

---

## 9. Navigation proposal

Four-column Introductive nav shell with DCC card cells for Home / Executive / Operational / Technical. Contextual footers and DCC drill-path guides on command centers. Placeholders remain readable pre-configuration.

---

## 10. Tokens and filters

| Token | Default | Used on |
|-------|---------|---------|
| `defaultResourceGroup` | `*` | Most |
| `defaultResource` | `*.logicmonitor.com` | Portal metrics |
| `defaultResourceName` | `*` / portal host | Collectors, modules |
| `defaultWebsiteGroup` | `*` | 05, 12 |
| `accountname` | `{{ACCOUNT_NAME}}` | 04, 13, summaries |

Severity stays inside alert widgets. No unsupported property filters.

---

## 11. Implementation phases (completed)

1. Discovery / inventory  
2. Design system (Introductive + DCC)  
3. Architecture (Exec / Ops / Tech + new boards)  
4. Prototype command centers + Home  
5. Full package + nested group export  
6. Validation + documentation  

---

## 12. Dependencies and limitations

See `validation/dependencies.md`. PSC-specific FortiGate/region metrics are **not** copied. OOTB tech boards require separate import. HTML rendering and link IDs require portal testing.

---

## 13. Validation approach

`tools/validate_redesign_v2.py`: JSON parse, overlaps, scripts, proservices, subgroup names, placeholders, datasource scrape. Results in `validation/validation-results.md`.

---

## 14. Final recommendations

1. Import group JSON; wire placeholders.  
2. Import OOTB packs before enabling directory links.  
3. Set `accountname` per client.  
4. Use Home → Exec CC → Ops CC → Tech Investigation as the primary demo journey.  
5. Keep originals in `Basement/` as the rebuild source of truth.
