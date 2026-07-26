# Dashboard Redesign Proposal

**Package:** SmartAdmin Connected Experience redesign v2  
**Status:** Implementation package under `dashboard-redesign/`  
**Baseline:** Fresh rebuild from Basement SmartAdmin + Introductive + Design Template patterns; New Dashboards / public LM repo for navigation and Level-3 targets. Client Experience suite at repo root is reference only.

---

## 1. Executive summary

This package turns the SmartAdmin portal-administration dashboards into a **connected client experience**: Home → Platform Value → operational drill-downs → technical investigation. It preserves the SmartAdmin dark-blue visual language, reuses working portal widgets, removes the duplicate Collector Health dashboard, and adds consistent HTML navigation without unsupported core JavaScript.

---

## 2. Hierarchy and levels

### Level 1 — Executive and client value

| # | Dashboard | Answers |
|---|-----------|---------|
| 00 | Home / Introductory | What is in this package? Where do I start by role? |
| 01 | Platform Value Overview | Are we healthy? What coverage/value exists? Where next? |

### Level 2 — Operational overview

| # | Dashboard | Answers |
|---|-----------|---------|
| 02 | Environment Health | Where is risk concentrated (map/NOC/dead/minimal/collectors/websites)? |
| 03 | Alert Overview | Which alerts need action? Rules, escalations, integrations, noise? |
| 04 | Coverage, Capacity & Licenses | Discovery gaps, license mix, group hygiene; links to OOTB capacity |
| 05 | Websites and Services | Website/group health and website-scoped token |
| 06 | Access and Administration | Users, roles, tokens, idle access |

### Level 3 — Technical investigation

| # | Dashboard | Answers |
|---|-----------|---------|
| 07 | Collector Health | Collector JVM, tasks, method mix, collector alerts |
| 08 | LogicModule and Content | Inventory + noisy modules (90 days) |
| 09 | Adoption and Optimization | Improvement story: noise, idle access, coverage, integrations |

**Level-3 technology links (not bundled):** Capacity Management, Cloud (AWS/Azure/GCP), Network, Linux/Windows, Storage, Virtualization, Alerting, Websites — import from OOTB / public repo, then configure placeholders.

---

## 3. Naming conventions

| Element | Convention | Example |
|---------|------------|---------|
| Dashboard (in group) | `NN - <Topic>` | `01 - Platform Value Overview` |
| Export file | `NN_<Topic>_redesign_v2.json` | `01_Platform_Value_Overview_redesign_v2.json` |
| Group export | `SmartAdmin_Connected_Experience_redesign_v2.json` | — |
| Widget titles | Question / outcome language | `Critical Alerts Requiring Attention` |
| Section banners | Short verb phrase | `Review active exceptions` |

---

## 4. Tokens and filters

| Token | Default | Dashboards | Widgets that respond |
|-------|---------|------------|----------------------|
| `defaultResourceGroup` | `*` | All | Portal resource/alert/collector scoped widgets |
| `defaultResource` | `*.logicmonitor.com` | Portal metric dashboards | Portal datasource bigNumbers / graphs |
| `defaultResourceName` | `*.logicmonitor.com` or `*` | Modules / collectors | Resource-name scoped widgets |
| `defaultWebsiteGroup` | `*` | 05 (and website widgets) | Website group metrics when applicable |
| `accountname` | `{{ACCOUNT_NAME}}` | 04 (licenses), summary on 01 | LicenseCounts bigNumbers |

**Not added:** Arbitrary property filters (customer, location, severity as dashboard filters) unless the underlying widget config already supports them. Severity is handled inside alert widgets.

**Time ranges (standards):**

| Family | Timescale |
|--------|-----------|
| Status scorecards | `day` |
| Alert trends | `7days` / `1day` (preserve source) |
| Coverage drift | `3month` (preserve source) |
| Collector graphs | `1day` / `2days` (preserve source) |

---

## 5. Design standards

### Header (every dashboard)

1. Compact global nav strip (current section highlighted)
2. Dashboard title + short purpose (guide or header text)
3. Scope/token reminder when relevant

### Layout order

Navigation → Critical status → KPIs → Trends → Detail tables → Diagnostics / Where next

### Severity colors

Use only for Critical / Error / Warning (and equivalent risk thresholds). Do not use severity colors for decorative section chrome.

### Empty states (guide language)

| Condition | Guidance |
|-----------|----------|
| Healthy zero (0 critical) | Expected; still review Warning trend and dead resources |
| No matching resources | Check `defaultResourceGroup` / `defaultResource` |
| Missing LogicModule | Install/apply required portal/collector modules |
| Wrong license token | Set `accountname` after import |
| Permissions | Confirm view rights on portal resources |

### Significant visual changes

| Change | Reason |
|--------|--------|
| Neutral Connected branding (no Harvard red) | Portable multi-client package |
| Shared compact menu | Orientation without consuming a full viewport |
| One metric owner per family | Less cognitive duplication |
| Question-driven titles | Client-facing clarity |

---

## 6. Navigation model

See [`../navigation/navigation-design.md`](../navigation/navigation-design.md).

**Committed approach:** Global HTML menu + Home nav cards + contextual footers. Static HTML/CSS only in core pack.

---

## 7. Gap analysis (architecture response)

| Gap | Response |
|-----|----------|
| Missing Home | Dashboard 00 |
| Missing split Env vs Alerts | 02 + 03 |
| Missing website token | `defaultWebsiteGroup` on 05 |
| Missing capacity metrics in SmartAdmin | OOTB L3 links on 04/00 |
| Duplicate collectors | Single 07 |
| Hardcoded proservices | `{{ACCOUNT_NAME}}` |
| JS dynamic nav | Optional docs only |

---

## 8. Implementation phases (completed in this package)

1. Discovery / inventory  
2. Architecture docs  
3. Prototype 00–03  
4. Full 04–09 + group export  
5. Validation + dependencies  

---

## 9. Portal post-import checklist

1. Import `SmartAdmin_Connected_Experience_redesign_v2.json`.
2. Set `accountname` to the portal license account property value.
3. Optionally scope `defaultResourceGroup` / `defaultWebsiteGroup`.
4. Replace `{{PORTAL_BASE}}` and `{{DASHBOARD_ID_*}}` placeholders in HTML nav with real portal URLs/IDs.
5. Import desired OOTB tech dashboards; wire Level-3 links.
6. Portal-validate optional Dynamic Dashboard List / FilterWidget if adopted later.
