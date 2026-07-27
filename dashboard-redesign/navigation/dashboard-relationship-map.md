# Dashboard Relationship Map

## Relationship table

| From | To | Relationship |
|------|----|--------------|
| 00 Home | 10 / 20 / 30 | Role entry to command centers / investigation |
| 00 Home | 11 / 21 / 34 | Value, triage, technology directory |
| 10 Exec CC | 11 / 12 / 13 / 14 | Executive siblings |
| 10 Exec CC | 20 / 21 | Operational drill |
| 10 Exec CC | 30 / 31 | Technical drill |
| 14 Capacity Risk | 24 | Operational license/coverage detail |
| 14 Capacity Risk | 34 | OOTB capacity / storage / compute |
| 13 Availability | 23 / 21 / 34 | Websites ops + alerts + OOTB websites |
| 12 Env Health Exec | 22 / 21 / 31 | Ops resource health, alerts, collectors |
| 20 Ops CC | 21 / 22 / 23 / 30 | Triage paths |
| 21 Active Alerts | 31 / 32 / 22 / 30 | Collector, modules, spatial, investigation |
| 22 Resource Health | 21 / 31 / 23 / 24 / 30 | Cross-ops + technical |
| 30 Investigation | 31 / 32 / 33 / 34 / 21 / 22 | Diagnostic fan-out |
| 34 Directory | OOTB IDs | Network / Server / Virt / Storage / Cloud / Capacity |
| 33 Adoption | 11 | Close the loop to platform value |

## Mermaid — hierarchy

```mermaid
flowchart TD
  Home["00 Home Introductory"]
  Home --> Exec["Executive"]
  Home --> Ops["Operational"]
  Home --> Tech["Technical"]
  Exec --> ECC["10 Exec Command Center"]
  Exec --> PV["11 Platform Value"]
  Exec --> EHE["12 Env Health Exec"]
  Exec --> ASH["13 Availability"]
  Exec --> CRO["14 Capacity Risk"]
  Ops --> OCC["20 Ops Command Center"]
  Ops --> AA["21 Active Alerts"]
  Ops --> RH["22 Resource Health"]
  Ops --> WS["23 Websites"]
  Ops --> CU["24 Coverage Licenses"]
  Ops --> ADM["25 Access"]
  Tech --> TRI["30 Investigation"]
  Tech --> CD["31 Collector Diagnostics"]
  Tech --> LM["32 LogicModules"]
  Tech --> ADO["33 Adoption"]
  Tech --> TD["34 Tech Directory"]
```

## Mermaid — primary journeys

```mermaid
flowchart LR
  J1A["00 Home"] --> J1B["10 Exec CC"] --> J1C["20 Ops CC"] --> J1D["21 Active Alerts"] --> J1E["30 Investigation"]
  J2A["14 Capacity Risk"] --> J2B["24 Coverage"] --> J2C["34 Directory"] --> J2D["OOTB Capacity Storage"]
  J3A["12 Env Health Exec"] --> J3B["22 Resource Health"] --> J3C["31 Collector Diagnostics"]
```

## User journeys

1. **Leadership review:** Home → Executive Command Center → Platform Value or Capacity Risk → Operational Command Center if action needed → Technical Investigation if root cause needed.
2. **Capacity risk:** Capacity Risk Overview → Coverage/Licenses → Technology Directory → OOTB Capacity/Storage.
3. **Environment / collector:** Env Health Exec → Resource Health → Collector Diagnostics.
4. **Service availability:** Availability Exec → Websites and Services → Active Alerts → OOTB Websites via Directory.
5. **Noise reduction:** Active Alerts → LogicModule and Content → Adoption and Optimization → Platform Value.
