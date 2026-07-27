# SmartAdmin Connected Experience — redesign package

Final dashboard JSON and rebuild tools for the Connected Experience suite live here.

**Start with the root [README.md](../README.md)** for overview, import order, navigation, modules, configuration, and maintenance.

## Quick paths

| Item | Path |
|------|------|
| Import group | [`dashboards/SmartAdmin_Connected_Experience_redesign_v2.json`](dashboards/SmartAdmin_Connected_Experience_redesign_v2.json) |
| Individual boards | [`dashboards/executive/`](dashboards/executive/), [`operational/`](dashboards/operational/), [`technical/`](dashboards/technical/) |
| Design system | [`design-system/`](design-system/) |
| Package docs | [`proposal/`](proposal/), [`inventory/`](inventory/), [`mapping/`](mapping/), [`navigation/`](navigation/) |
| Dependencies | [`validation/dependencies.md`](validation/dependencies.md) |

## Rebuild / validate

```bash
python dashboard-redesign/tools/build_redesign_v2.py
python dashboard-redesign/tools/inject_navigation.py
python dashboard-redesign/tools/validate_navigation.py
python dashboard-redesign/tools/validate_redesign_v2.py
python dashboard-redesign/tools/export_required_modules.py
```

**Basement/** source JSON is not modified by these tools. Navigation HTML under **`navigation/html/`** is the source of truth for the Suite Navigation Menu.
