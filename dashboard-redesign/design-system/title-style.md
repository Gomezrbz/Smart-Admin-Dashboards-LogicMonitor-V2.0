# Title and Header Style (Introductive Dashboard)

**Primary reference:** `Basement/Introductive_Dashboard.json`  
**Rule:** Do not use prior proposal title styles that diverge from Introductive. Neutralize Harvard-specific branding (`#A51C30` marquee); keep typography, shells, and hierarchy.

## Tokens

| Role | Treatment |
|------|-----------|
| Font family | `Arial, Helvetica, sans-serif` |
| Panel shell | bg `#0f172a`, border `1px solid #1f2937`, radius `14px`, padding `18px`, text `#e5e7eb` |
| Panel title | `20px` / weight `700` / `#f9fafb` |
| Panel subtitle | `13px` / `#9ca3af` / margin-top `4px` |
| Column header | `15px` / weight `700` / `#f9fafb` |
| Body / link blurb | `12px` / `#9ca3af` |
| Links | `#38bdf8`, `text-decoration:none` |
| Inner card | bg `#020617`, border `#1f2937`, radius `12px`, padding `14px` |
| Nav shell | bg `#0b1220`, border `#1f2a44`, radius `16px`, padding `18px` |
| Nav title | `18px` / `700` / `#ffffff` |
| Nav subtitle | `13px` / `#a5b4fc`; links `#93c5fd` weight `700` |
| Nav section title | `14px` / `700` / white |
| Divider | `1px` `#1f2a44` |
| Theme | Widget theme `newSolidDarkBlue` |

## Section headers

**Major breaks (Home / Command Centers):** Introductive pattern — large centered white label on transparent background (`font-size:62px; font-weight:bold; height:112px`). Use sparingly.

**Dense dashboards:** Compact section bar — nav-shell colors with left accent `#38bdf8`, title `15–20px` / `700`.

## Package banner (neutralized)

Replace Harvard red marquee with gradient shell matching Introductive educational panels:

```html
<div style="font-family:Arial,Helvetica,sans-serif;background:linear-gradient(135deg,#0f172a 0%,#111827 45%,#1e3a8a 100%);color:#ffffff;border-radius:16px;padding:22px;">
  <div style="font-size:28px;font-weight:750;color:#ffffff;">SmartAdmin Connected Experience</div>
  <div style="font-size:13px;color:#dbeafe;margin-top:6px;">…</div>
</div>
```

## Builder mapping

| Helper | Uses |
|--------|------|
| `intro_panel()` | Educational shell + title/subtitle + inner columns |
| `guide_widget()` | Introductive panel with 3 question/flow/next columns |
| `section_banner()` | Compact section header |
| `section_banner_major()` | 62px Introductive section header |
| `global_nav_widget()` | Introductive nav shell + DCC-style link cards |
