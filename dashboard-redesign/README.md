# SmartAdmin Connected Experience — Redesign v2

Expanded Connected Experience package with **Executive**, **Operational**, and **Technical** dashboard groups, Introductive title styling, and DCC card/table chrome.

**Source JSON under `Basement/` and `New Dashboards/` is not modified.**

## Import

1. Import [`dashboards/SmartAdmin_Connected_Experience_redesign_v2.json`](dashboards/SmartAdmin_Connected_Experience_redesign_v2.json) as a dashboard group.
2. Confirm nested subgroups: **Executive**, **Operational**, **Technical**. Home (`00`) sits at the package root.
3. After import, replace placeholders:
   - `{{PORTAL_BASE}}`
   - `{{DASHBOARD_ID_NN}}` (per dashboard)
   - `{{OOTB_*_ID}}` (technology directory)
   - `{{ACCOUNT_NAME}}` / `accountname` token for licenses
4. Portal assigns subgroup IDs — do **not** copy IDs from another portal.

## Suite (17 dashboards)

| ID | Dashboard | Group |
|----|-----------|-------|
| 00 | Home / Introductory | Package root |
| 10 | Executive Command Center | Executive |
| 11 | Platform Value Overview | Executive |
| 12 | Environment Health Executive | Executive |
| 13 | Availability and Service Health | Executive |
| 14 | Capacity and Risk Overview | Executive |
| 20 | Operational Command Center | Operational |
| 21 | Active Alerts | Operational |
| 22 | Resource Health | Operational |
| 23 | Websites and Services | Operational |
| 24 | Coverage, Capacity & Licenses | Operational |
| 25 | Access and Administration | Operational |
| 30 | Technical Resource Investigation | Technical |
| 31 | Collector Diagnostics | Technical |
| 32 | LogicModule and Content | Technical |
| 33 | Adoption and Optimization | Technical |
| 34 | Technology Dashboard Directory | Technical |

Network / Server / Virtualization / Storage / Cloud are **not** empty shells — they are rows in **34** linking to OOTB packs.

## Design system

- Titles / headers: [`design-system/title-style.md`](design-system/title-style.md) (Introductive)
- Tables / cards: [`design-system/table-style.md`](design-system/table-style.md) (DCC)
- Standards: [`design-system/dashboard-design-standards.md`](design-system/dashboard-design-standards.md)

## Rebuild / validate

```bash
python dashboard-redesign/tools/build_redesign_v2.py
python dashboard-redesign/tools/validate_redesign_v2.py
```

## Docs

| Doc | Path |
|-----|------|
| Proposal | [`proposal/dashboard-redesign-proposal.md`](proposal/dashboard-redesign-proposal.md) |
| Inventory | [`inventory/dashboard-inventory.md`](inventory/dashboard-inventory.md) |
| Navigation | [`navigation/navigation-design.md`](navigation/navigation-design.md) |
| Relationships | [`navigation/dashboard-relationship-map.md`](navigation/dashboard-relationship-map.md) |
| Group mapping | [`mapping/dashboard-group-mapping.md`](mapping/dashboard-group-mapping.md) |
| Existing→new | [`mapping/existing-to-new-mapping.md`](mapping/existing-to-new-mapping.md) |
| Validation | [`validation/validation-results.md`](validation/validation-results.md) |
| Dependencies | [`validation/dependencies.md`](validation/dependencies.md) |
