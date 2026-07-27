# Dependencies and Portal Configuration

## LogicModules / datasources (portal-admin pack)

Common dependencies reused from SmartAdmin / Introductive widgets:

- Portal Alerts / Resources / Collectors scorecards (`LogicMonitor_*` portal datasources)
- `HostStatus` / dead-resource metrics
- `DataCollectingTasks`, `ActiveDiscoveryTasks`, collector JVM metrics
- LicenseCounts (`accountname` token)
- Users / Roles / APITokens / Users_NotLogin
- DeviceGroups / Websites / WebsitesGroups
- LogicModuleStatus inventory
- Netscans / UnmonitoredDevice / MinimalMonitoring trends

Exact widget→datasource bindings are preserved from source clones. Confirm modules are applied in the target portal.

## Tokens requiring client configuration

| Token / placeholder | Required for | Action |
|---------------------|--------------|--------|
| `accountname` / `{{ACCOUNT_NAME}}` | License widgets on 04, 13, summaries | Set to client account name |
| `defaultResourceGroup` | Most resource/alert scopes | Often `*`; tighten per client |
| `defaultResource` | Portal host metrics | Typically `*.logicmonitor.com` |
| `defaultWebsiteGroup` | 05, 12 | Set if website scoping needed |
| `{{PORTAL_BASE}}` | All HTML nav links | e.g. `https://company.logicmonitor.com` |
| `{{DASHBOARD_ID_NN}}` | Suite navigation | Fill after import |
| `{{OOTB_*_ID}}` | Technology directory | Fill after OOTB import |

## Dashboard groups

Parent: **SmartAdmin Connected Experience**  
Subgroups: **Executive**, **Operational**, **Technical**  
Home dashboard is on the parent `dashboards` array.

Portal-assigned subgroup IDs are **not portable**. Record them after import for any automation; do not embed foreign IDs in this package.

## External packages

| Package | Purpose |
|---------|---------|
| OOTB LogicMonitor Dashboards / [logicmonitor/dashboards](https://github.com/logicmonitor/dashboards) | Network, Server, Storage, Virtualization, Cloud, Capacity, Alerting, Websites |
| LM Logs (optional) | Not required for core pack |

## Known limitations

- DCC uses CSS Grid cards; inventory links use an approved HTML table adaptation (documented in `design-system/table-style.md`).
- PSC FortiGate / regional metrics are intentionally omitted.
- HTML text-widget rendering can vary by LM UI version — portal test required.
- Navigation URLs do not work until placeholders are replaced; metrics still function.
- No core JavaScript widgets.

## Portal testing checklist

- [ ] Group import succeeds with three subgroups  
- [ ] Home opens as lobby  
- [ ] Introductive title panels and DCC cards render  
- [ ] No widget overlap in UI  
- [ ] Tokens scoped correctly  
- [ ] License widgets resolve after `accountname` set  
- [ ] Nav links resolve after ID fill  
- [ ] OOTB directory links resolve after OOTB import  
