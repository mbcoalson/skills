# EnergyPlus Model QA/QC Checklist

**Model:** [Model Name]
**Date:** [YYYY-MM-DD]
**Reviewer:** EnergyPlus Assistant

---

## 1. File Validation

- [ ] IDF syntax valid (no parsing errors)
- [ ] Model loads successfully
- [ ] File size reasonable (< 50 MB)

**Findings:**
```
[Results from validate_idf]
```

---

## 2. Simulation Settings

- [ ] Run period set correctly (annual vs design day)
- [ ] Timestep appropriate (4-6 steps/hour typical)
- [ ] Output variables requested match deliverable needs
- [ ] Output meters configured for utility analysis

**Current Settings:**
```
Run Period: [Start Date] to [End Date]
Timestep: [X] steps/hour
Design Day Simulations: [Yes/No]
Annual Simulation: [Yes/No]
```

**Issues:**
```
[Any issues found]
```

---

## 3. Building Geometry

- [ ] Zones defined (count: ___)
- [ ] Surfaces valid (no non-planar surfaces)
- [ ] Materials defined for all constructions
- [ ] Windows/doors properly defined
- [ ] Building orientation correct

**Zone Summary:**
```
Total Zones: [X]
Zone Names: [List]
Total Floor Area: [X] m² ([X] ft²)
```

**Surface Issues:**
```
[Any geometry errors]
```

---

## 4. Schedules

- [ ] All referenced schedules exist
- [ ] Schedule values reasonable (0-1 for fractions)
- [ ] Occupancy schedules match building type
- [ ] HVAC availability schedules logical

**Schedule Check:**
```
Total Schedules: [X]
Missing References: [List or "None"]
Warnings: [Any warnings]
```

---

## 5. Internal Loads

### People
- [ ] Occupancy density reasonable for building type
- [ ] Activity level appropriate
- [ ] Schedules assigned

**People Summary:**
```
[Results from inspect_people]
```

### Lighting
- [ ] LPD (Lighting Power Density) reasonable
- [ ] Schedules assigned
- [ ] Return air fraction set if applicable

**Lighting Summary:**
```
[Results from inspect_lights]
Average LPD: [X] W/m² ([X] W/ft²)
```

### Electric Equipment
- [ ] EPD (Equipment Power Density) reasonable
- [ ] Schedules assigned
- [ ] Radiant/convective fractions reasonable

**Equipment Summary:**
```
[Results from inspect_electric_equipment]
Average EPD: [X] W/m² ([X] W/ft²)
```

---

## 6. HVAC Systems

- [ ] All HVAC loops discovered
- [ ] Equipment properly connected
- [ ] Sizing parameters set
- [ ] Control sequences defined

**HVAC Summary:**
```
[Results from discover_hvac_loops]

Plant Loops: [X]
Condenser Loops: [X]
Air Loops: [X]
Zone Equipment: [X]
```

**Topology Issues:**
```
[Any connection or configuration issues]
```

---

## 7. Output Variables & Meters

- [ ] Key output variables added for deliverables
- [ ] Meters configured for utility tracking
- [ ] Output frequency appropriate (hourly/monthly/annual)

**Required for SECC Deliverables:**
- [ ] Total Site Energy (for EUI calculation)
- [ ] Electricity consumption (for GHG/cost)
- [ ] Natural Gas consumption (for GHG/cost)
- [ ] District Heating/Cooling (if applicable)

**Current Output Configuration:**
```
[Results from get_output_variables and get_output_meters]
```

---

## 8. Pre-Simulation Readiness

**Overall Status:** [READY / NOT READY / NEEDS REVIEW]

**Critical Issues (Must Fix):**
1. [Issue 1]
2. [Issue 2]

**Warnings (Review Recommended):**
1. [Warning 1]
2. [Warning 2]

**Recommended Actions:**
1. [Action 1]
2. [Action 2]

---

## Next Steps

Based on QA/QC results:

- [ ] Fix critical issues before simulation
- [ ] Review warnings and address if needed
- [ ] Add missing output variables
- [ ] Run test simulation (design day)
- [ ] If test passes, proceed to annual simulation
- [ ] If test fails, review error logs and troubleshoot

---

**QA/QC Complete:** [YYYY-MM-DD HH:MM]
