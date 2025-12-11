# HVAC System Topology Report

**Model:** [Model Name]
**Date:** [YYYY-MM-DD]
**Analyst:** EnergyPlus Assistant

---

## Executive Summary

**Total HVAC Loops:** [X]
- Plant Loops: [X]
- Condenser Loops: [X]
- Air Loops: [X]
- Zone Equipment: [X]

**System Type:** [e.g., WSHP with central condenser loop, VAV with chiller/boiler, etc.]

---

## Plant Loops (Heating/Cooling Water)

### Loop 1: [Loop Name]

**Type:** [Heating / Cooling / Heat Recovery]

**Supply Side Equipment:**
1. [Equipment Name] - [Type]
   - Capacity: [X] kW or tons
   - Efficiency: [COP, EER, etc.]
2. [Equipment Name] - [Type]

**Demand Side Equipment:**
1. [Equipment Name] - [Type]
2. [Equipment Name] - [Type]

**Control Strategy:**
- Setpoint: [X]°C ([X]°F)
- Control Type: [Scheduled / Outdoor Reset / etc.]
- Operation: [Continuous / Scheduled]

**Topology Diagram:**
```
[ASCII diagram or reference to visualize_loop_diagram output]
```

---

### Loop 2: [Loop Name]

[Repeat structure for each plant loop]

---

## Condenser Loops (Heat Rejection)

### Loop 1: [Loop Name]

**Type:** [Cooling Tower / Ground Loop / Air-Cooled / Water-Cooled]

**Supply Side Equipment:**
1. [Equipment Name] - [Type]
   - Capacity: [X] kW
   - Efficiency: [X]

**Demand Side Equipment:**
1. [Connected Chillers/Heat Pumps]
2. [Other condenser-side equipment]

**Control Strategy:**
- Setpoint: [X]°C ([X]°F)
- Control Type: [Scheduled / Outdoor Reset / etc.]

**Topology Diagram:**
```
[ASCII diagram or reference to visualize_loop_diagram output]
```

---

## Air Loops (Air Distribution Systems)

### Loop 1: [Loop Name]

**Serves Zones:**
- [Zone 1]
- [Zone 2]
- [Zone 3]

**Supply Side Equipment:**
1. [Fan Type] - [Capacity CFM]
2. [Heating Coil Type] - [Capacity kW/Btu/h]
3. [Cooling Coil Type] - [Capacity kW/tons]
4. [Other equipment - HRV, ERV, etc.]

**Outdoor Air:**
- Ventilation Rate: [X] CFM or L/s
- Economizer: [Yes/No - Type]
- DCV (Demand Control Ventilation): [Yes/No]

**Control Strategy:**
- Supply Air Temp: [X]°C ([X]°F)
- Reset Schedule: [Yes/No - Type]
- Fan Control: [Constant / VAV / Cycling]

**Topology Diagram:**
```
[ASCII diagram or reference to visualize_loop_diagram output]
```

---

### Loop 2: [Loop Name]

[Repeat structure for each air loop]

---

## Zone Equipment (Direct Serving)

### Zone: [Zone Name]

**Equipment:**
1. [Equipment Type] - [Capacity]
   - Heating Capacity: [X] kW/Btu/h
   - Cooling Capacity: [X] kW/tons
   - Connected to: [Loop Name]

**Control:**
- Thermostat Setpoint: Heating [X]°C / Cooling [X]°C
- Schedule: [Schedule Name]

---

### Zone: [Zone Name]

[Repeat for each zone with direct equipment]

---

## System Interconnections

**Plant-to-Air Connections:**
- [Plant Loop Name] → [Air Loop Name] via [Coil Type]

**Condenser-to-Plant Connections:**
- [Condenser Loop Name] → [Equipment Name]

**Complex Interactions:**
- [Description of heat recovery, cascading systems, etc.]

---

## Key Findings

**Strengths:**
1. [Positive findings about system design]
2. [Well-configured controls]

**Potential Issues:**
1. [Equipment sizing concerns]
2. [Control sequence gaps]
3. [Missing equipment or connections]

**Recommendations:**
1. [Suggested improvements]
2. [Further investigation needed]

---

## For SECC Project

**Current State:**
- [Description of v3 model HVAC]

**Planned Rebuild:**
- [ ] Condenser loop: [Configuration]
- [ ] WSHP systems for major zones (4-5 systems)
- [ ] DOAS for ventilation
- [ ] Pool heating system

**Validation After Rebuild:**
- [ ] Run `discover_hvac_loops` to confirm all systems present
- [ ] Check `get_loop_topology` for each loop
- [ ] Verify equipment capacities reasonable
- [ ] Confirm all zones served

---

**Report Generated:** [YYYY-MM-DD HH:MM]
