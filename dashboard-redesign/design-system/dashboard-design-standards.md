# Dashboard Design Standards

## Visual language

- Widget theme: `newSolidDarkBlue`
- Titles/headers: [title-style.md](title-style.md) (Introductive)
- Summary/nav tables: [table-style.md](table-style.md) (DCC)
- Font: Arial / Helvetica

## Layout sequence (every dashboard)

1. Suite navigation (Home / Executive / Operational / Technical)
2. Read-first guide (Introductive panel) or DCC intro grid on command centers
3. Critical summary KPIs
4. Supporting indicators
5. Trends / situation visuals
6. Detailed tables
7. Diagnostics or OOTB links
8. Contextual “Where next” footer

## Density

- Prefer 12-column grid; KPI strips of 3–4 bigNumbers per row
- Avoid stacking more than one full-width dense table without a section banner
- Command centers stay executive-dense; technical boards may be taller

## Naming

| Element | Convention | Example |
|---------|------------|---------|
| Dashboard | `NN - Topic` | `10 - Executive Command Center` |
| File | `NN_Topic_redesign_v2.json` | `10_Executive_Command_Center_redesign_v2.json` |
| Widget titles | Outcome language | `Critical Alerts Requiring Attention` |
| Groups | `Executive`, `Operational`, `Technical` | Nested `subGroups` |

## Severity colors

Reserve red / amber / green pills for Critical, Error, Warning, Healthy, At risk, Unavailable, Unknown, No data. Never decorative.

## Tokens

| Token | Default | Notes |
|-------|---------|-------|
| `defaultResourceGroup` | `*` | Global resource/alert scope |
| `defaultResource` | `*.logicmonitor.com` | Portal metrics |
| `defaultResourceName` | `*` or portal host | Collectors / modules |
| `defaultWebsiteGroup` | `*` | Websites |
| `accountname` | `{{ACCOUNT_NAME}}` | Licenses — configure after import |

Do not add filters widgets cannot consume.

## Navigation

- Configurable links: `{{PORTAL_BASE}}/uiv4/dashboard/{{DASHBOARD_ID_NN}}`
- Remain readable when placeholders are unresolved
- No `<script>` in core pack

## Empty states

Guides must state: empty/zero may mean healthy **or** missing tokens/LogicModules — verify before concluding.

## Dashboard groups

LM exports use structural nesting (`dashboardgroup` → `dashboards` / `subGroups`). Portal assigns IDs on import. Do not hardcode foreign portal group IDs.
