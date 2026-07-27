# Navigation Design

## Model

Every dashboard includes **Suite Navigation Menu** — Introductive nav shell (`#0b1220` / `#1f2a44` / radius 16) with four DCC-style columns:

1. Home  
2. Executive  
3. Operational  
4. Technical  

Current dashboard is highlighted with a cyan CURRENT badge.

Links use:

```text
{{PORTAL_BASE}}/uiv4/dashboard/{{DASHBOARD_ID_NN}}
```

Unresolved placeholders remain readable.

## Contextual navigation

| Pattern | Where |
|---------|--------|
| DCC intro card grid | 10, 20, 30 |
| DCC nav guide (4 columns) | 00, 10, 20, 31 |
| DCC inventory table (adapted rows) | 12, 30, 31 |
| Where Next footer | All dashboards |
| Technology directory | 00, 04, 05, 13, 31 |

## Label standards

| Use | Label |
|-----|-------|
| Home | Home |
| Exec hub | Exec CC / Executive Command Center |
| Ops hub | Ops CC / Operational Command Center |
| Tech hub | Investigation / Technical Resource Investigation |
| Alerts | Active Alerts |
| Resources | Resource Health |
| Collectors | Collector Diagnostics |

## Space budget

Nav widget uses ~5 grid rows. Guides use Introductive 20px titles (not decorative empty headers). Major 62px section headers only on Home environment summary.

## Unsupported

No JavaScript navigation widgets in the core pack (`_DynamicDashboardGroups`, `_FilterWidget_v7` remain optional/docs-only).
