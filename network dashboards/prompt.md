# Dashboard Scope and Filtering

This dashboard is specifically for ESB network devices.

The LogicMonitor Resource Group that defines the scope of the dashboard is:

`Devices by Application/ESB`

This group contains the resources associated with:

`application = ESB`

## Primary dashboard scope

Use the Resource Group:

`Devices by Application/ESB`

as the primary scope for all network-device widgets.

Do NOT independently recreate the `application=ESB` property filtering inside every widget if the Resource Group already provides the correct population of resources.

The Resource Group should be treated as the source of truth for the dashboard scope.

## Dashboard token

Follow the filtering pattern used by the supplied `Interface Bandwidth Investigation.json`.

Use:

`defaultResourceGroup`

with the default value:

`Devices by Application/ESB`

Widgets should reference the token using:

`##defaultResourceGroup##`

where supported by the LogicMonitor widget schema.

This should allow the dashboard to default to ESB while keeping the dashboard design reusable if the Resource Group token is changed later.

## Resource selection

Within the ESB Resource Group, allow the operator to narrow the investigation to an individual network device where supported.

The intended troubleshooting hierarchy is:

`Devices by Application/ESB`
→ Network Device
→ Interface
→ Interface utilization/errors
→ NetFlow investigation

## Widget filtering

Apply `##defaultResourceGroup##` consistently to:

* Network Device Alert Summary
* Network Device Availability
* Top Network Devices Requiring Attention
* CPU Utilization
* Memory Utilization
* Interface Errors and Discards
* Top Interfaces by Utilization
* Interface Utilization Trend
* Network Device Health Trend

Collector-health widgets may use a broader scope if restricting them to `Devices by Application/ESB` would exclude the Collectors responsible for monitoring those resources.

## Important

Use the supplied `Interface Bandwidth Investigation.json` as the source of truth for the exact LogicMonitor JSON implementation of `defaultResourceGroup`.

Do not invent a different filtering mechanism when the supplied dashboard already demonstrates the required structure.

The finished dashboard should open by default showing only resources under:

`Devices by Application/ESB`
