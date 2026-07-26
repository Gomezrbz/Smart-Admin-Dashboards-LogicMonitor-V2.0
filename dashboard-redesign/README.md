# SmartAdmin Connected Experience — Redesign v2

Fresh Phases 1–5 redesign package. **Source JSON under `Basement/` and `New Dashboards/` is not modified.**

## Quick start

1. Read [`proposal/dashboard-redesign-proposal.md`](proposal/dashboard-redesign-proposal.md)
2. Import [`dashboards/SmartAdmin_Connected_Experience_redesign_v2.json`](dashboards/SmartAdmin_Connected_Experience_redesign_v2.json) into LogicMonitor
3. Configure tokens and nav placeholders per [`validation/dependencies.md`](validation/dependencies.md)

## Package layout

```
dashboard-redesign/
├── README.md                          ← this file
├── proposal/dashboard-redesign-proposal.md
├── source-inventory/dashboard-inventory.md
├── navigation/
│   ├── navigation-design.md
│   └── dashboard-relationship-map.md
├── mapping/existing-to-new-dashboard-mapping.md
├── dashboards/
│   ├── SmartAdmin_Connected_Experience_redesign_v2.json
│   ├── level-1-executive/     (00 Home, 01 Platform Value)
│   ├── level-2-operational/   (02–06)
│   └── level-3-technical/     (07–09)
├── validation/
│   ├── validation-results.md
│   └── dependencies.md
└── tools/
    ├── build_redesign_v2.py
    └── validate_redesign_v2.py
```

## Suite map

| Level | Dashboard |
|-------|-----------|
| L1 | 00 Home / Introductory |
| L1 | 01 Platform Value Overview |
| L2 | 02 Environment Health |
| L2 | 03 Alert Overview |
| L2 | 04 Coverage, Capacity & Licenses |
| L2 | 05 Websites and Services |
| L2 | 06 Access and Administration |
| L3 | 07 Collector Health |
| L3 | 08 LogicModule and Content |
| L3 | 09 Adoption and Optimization |

## Rebuild

From the repository root:

```bash
python dashboard-redesign/tools/build_redesign_v2.py
python dashboard-redesign/tools/validate_redesign_v2.py
```

## Design notes

- Visual language: SmartAdmin `newSolidDarkBlue` + slate HTML guides
- Navigation: static HTML global menu + Home cards + footers (no core JavaScript)
- Duplicate Collector Health removed; license account token is `{{ACCOUNT_NAME}}`
- OOTB technology dashboards are linked as Level-3 targets, not cloned

## Related references (unchanged)

- `Basement/` — original SmartAdmin / Introductive / Design Template
- `New Dashboards/` — OOTB pack and utility prototypes
- Root `DASHBOARD_EXPERIENCE_PROPOSAL.md` and Client Experience JSON — reference only
