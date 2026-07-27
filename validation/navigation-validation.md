# Navigation Validation

Source of truth: `navigation/html/*.html`. Injected into final redesign dashboards under `dashboard-redesign/dashboards/`.

| Dashboard | Navigation File Found | Navigation Updated | Current Dashboard Correct | Links Validated | JSON Valid |
| --------- | --------------------- | ------------------ | ------------------------- | --------------- | ---------- |
| 00 — 00 - Home / Introductory | Yes | Yes | Yes | Yes | Yes |
| 10 — 10 - Executive Command Center | Yes | Yes | Yes | Yes | Yes |
| 11 — 11 - Platform Value Overview | Yes | Yes | Yes | Yes | Yes |
| 12 — 12 - Environment Health Executive | Yes | Yes | Yes | Yes | Yes |
| 13 — 13 - Availability and Service Health | Yes | Yes | Yes | Yes | Yes |
| 14 — 14 - Capacity and Risk Overview | Yes | Yes | Yes | Yes | Yes |
| 20 — 20 - Operational Command Center | Yes | Yes | Yes | Yes | Yes |
| 21 — 21 - Active Alerts | Yes | Yes | Yes | Yes | Yes |
| 22 — 22 - Resource Health | Yes | Yes | Yes | Yes | Yes |
| 23 — 23 - Websites and Services | Yes | Yes | Yes | Yes | Yes |
| 24 — 24 - Coverage, Capacity & Licenses | Yes | Yes | Yes | Yes | Yes |
| 25 — 25 - Access and Administration | Yes | Yes | Yes | Yes | Yes |
| 30 — 30 - Technical Resource Investigation | Yes | Yes | Yes | Yes | Yes |
| 31 — 31 - Collector Diagnostics | Yes | Yes | Yes | Yes | Yes |
| 32 — 32 - LogicModule and Content | Yes | Yes | Yes | Yes | Yes |
| 33 — 33 - Adoption and Optimization | Yes | Yes | Yes | Yes | Yes |
| 34 — 34 - Technology Dashboard Directory | Yes | Yes | Yes | Yes | Yes |

## Notes

All 17 dashboards passed navigation validation.

## Method

1. Locate the Suite Navigation Menu text widget.
2. Compare widget HTML to the matching file under `navigation/html/`.
3. Confirm exactly one `sa-nav-current` block.
4. Confirm all hrefs match the navigation source (no `{{...}}` placeholders).
5. Confirm JSON parses.

Portal UI rendering was **not** tested in this pass.

