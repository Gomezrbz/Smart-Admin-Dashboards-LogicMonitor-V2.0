# Table and Card Style (DCC Executive Command Center)

**Primary reference:** `Basement/DCC_-_PSC_Network_Health_Executive_Command_Center (1).json`  
(identical twin: `Basement/Design_Template.json`)

## Critical finding

DCC text widgets do **not** use HTML `<table>`. Summary, how-to, and navigation “tables” are **CSS Grid card systems** (`.psc-exec-grid`, `.psc-nav-grid`) inside `<style>` blocks.

## Confirmed DCC tokens

| Token | Value |
|-------|-------|
| Font | `Arial, Helvetica, sans-serif` |
| Intro shell gradient | `#0f172a → #111827 → #1e3a8a` |
| Nav shell gradient | `#111827 → #172554` |
| Shell radius | `14–16px` |
| Shell padding | `18–22px` |
| Card fill | `rgba(15,23,42,.72–.76)` |
| Card border | `rgba(148,163,184,.34)` or `rgba(191,219,254,.20)` |
| Card radius | `12–14px` |
| Card padding | `13–16px` |
| Grid gap | `12–14px` |
| H1 | `28px` / weight `750` / white |
| Card H3 | `14–15px` / white |
| Body | `13px` / `#dbeafe` or `#cbd5e1` |
| Micro / pills | `11–12px` / weight `700–800` |
| Action pill | radius `999px`, `rgba(255,255,255,.12)` fill, `#bfdbfe` text |

### Severity / scope pills (meaningful states only)

| Class | Background | Text |
|-------|------------|------|
| Health | `rgba(22,163,74,.92)` | `#ecfdf5` |
| Alerts / Critical | `rgba(239,68,68,.92)` | `#fff7ed` |
| Region / Info | `rgba(59,130,246,.9)` | `#eff6ff` |
| Capacity / Warning | `rgba(250,204,21,.9)` | `#422006` |
| Sessions / Accent | `rgba(168,85,247,.88)` | `#faf5ff` |

Do **not** use these colors as decoration.

## Approved adaptation for inventory / navigation rows

When a true row inventory is needed (dashboard directory, risk list with links), encode the **same visual cell** as a table with `border-collapse:separate; border-spacing:12–14px` and card-styled `<td>` cells. This is the documented deviation from DCC markup (grid → table) while preserving appearance.

```html
<table style="width:100%;border-collapse:separate;border-spacing:14px;">
  <tr>
    <td style="vertical-align:top;background:rgba(15,23,42,.76);border:1px solid rgba(148,163,184,.34);border-radius:14px;padding:16px;">
      <span class="pill">START</span>
      <div style="font-size:15px;font-weight:700;color:#fff;margin:8px 0;">Title</div>
      <div style="font-size:13px;color:#cbd5e1;">Body</div>
      <a href="{{PORTAL_BASE}}/…" style="…">Action</a>
    </td>
  </tr>
</table>
```

## What is reused vs not copied

| Reuse | Do not copy |
|-------|-------------|
| Gradients, card chrome, pills, spacing, typography | PSC / FortiGate / region-specific datapoints |
| Guide → KPI → map → exceptions → NOC flow | Hardcoded `defaultResourceGroup=PSC` |
| Nav card columns (Executive / Operations / …) | Non-clickable-only nav (redesign adds real placeholders) |

## Builder mapping

| Helper | Uses |
|--------|------|
| `dcc_intro_guide()` | Exec intro card grid |
| `dcc_nav_guide()` | 4-col nav cards |
| `dcc_inventory_table()` | Adapted row inventory with links |
| `scope_pills()` | Severity/scope pill row |
