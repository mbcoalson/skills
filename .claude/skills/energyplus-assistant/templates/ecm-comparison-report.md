# ECM Parametric Analysis Report

**Project:** [Project Name]
**Baseline Model:** [Model Name]
**Date:** [YYYY-MM-DD]
**Analyst:** EnergyPlus Assistant

---

## Baseline Performance

**Model:** [Baseline IDF filename]
**Weather File:** [Location]
**Simulation Period:** [Start] to [End]

### Energy Use Summary

| Metric | Value | Units |
|--------|-------|-------|
| Total Site Energy | [X] | kWh/year |
| Electricity | [X] | kWh/year |
| Natural Gas | [X] | therms/year |
| EUI (Energy Use Intensity) | [X] | kBtu/ft²/year |
| Peak Electric Demand | [X] | kW |

### Cost Summary

| Utility | Consumption | Rate | Annual Cost |
|---------|-------------|------|-------------|
| Electricity | [X] kWh | $[X]/kWh | $[X] |
| Natural Gas | [X] therms | $[X]/therm | $[X] |
| Demand Charges | [X] kW | $[X]/kW-month | $[X] |
| **Total Annual Cost** | - | - | **$[X]** |

### GHG Emissions

| Fuel | Consumption | Carbon Intensity | Emissions |
|------|-------------|------------------|-----------|
| Electricity | [X] kWh | [X] lb CO2e/kWh | [X] metric tons CO2e |
| Natural Gas | [X] therms | [X] lb CO2e/therm | [X] metric tons CO2e |
| **Total GHG** | - | - | **[X] metric tons CO2e** |

---

## ECM Scenarios Tested

### ECM 1: [ECM Name]

**Description:** [Brief description of measure]

**Modifications Made:**
- Parameter 1: Changed from [X] to [Y]
- Parameter 2: Changed from [X] to [Y]

**MCP Tools Used:**
- `modify_lights` / `modify_electric_equipment` / `modify_people` / etc.

**Results:**

| Metric | Baseline | ECM 1 | Change | % Savings |
|--------|----------|-------|--------|-----------|
| Total Site Energy (kWh) | [X] | [Y] | [Δ] | [%] |
| Electricity (kWh) | [X] | [Y] | [Δ] | [%] |
| Natural Gas (therms) | [X] | [Y] | [Δ] | [%] |
| Annual Cost ($) | [X] | [Y] | [Δ] | [%] |
| GHG (metric tons CO2e) | [X] | [Y] | [Δ] | [%] |

**Financial Analysis:**
- Annual Energy Savings: $[X]
- Estimated Implementation Cost: $[X]
- Simple Payback: [X] years
- 20-Year NPV (@[X]% discount): $[X]

---

### ECM 2: [ECM Name]

[Repeat structure for each ECM]

---

### ECM 3: Combined Measures

**Description:** [ECMs combined together]

**Interactions Considered:**
- [How measures interact - additive, synergistic, cannibalistic]

**Results:**

| Metric | Baseline | Combined ECMs | Change | % Savings |
|--------|----------|---------------|--------|-----------|
| Total Site Energy (kWh) | [X] | [Y] | [Δ] | [%] |
| Electricity (kWh) | [X] | [Y] | [Δ] | [%] |
| Natural Gas (therms) | [X] | [Y] | [Δ] | [%] |
| Annual Cost ($) | [X] | [Y] | [Δ] | [%] |
| GHG (metric tons CO2e) | [X] | [Y] | [Δ] | [%] |

---

## ECM Comparison Summary

| ECM | Energy Savings (%) | Cost Savings ($/yr) | GHG Reduction (tons CO2e) | Simple Payback (years) | Ranking |
|-----|-------------------|---------------------|---------------------------|------------------------|---------|
| Baseline | - | - | - | - | - |
| ECM 1 | [%] | $[X] | [X] | [X] | [Rank] |
| ECM 2 | [%] | $[X] | [X] | [X] | [Rank] |
| ECM 3 | [%] | $[X] | [X] | [X] | [Rank] |
| Combined | [%] | $[X] | [X] | [X] | [Rank] |

**Ranking Criteria:** [Cost-effectiveness / GHG reduction / Energy savings / Client priority]

---

## Recommendations

### Top Priority ECMs
1. **[ECM Name]** - [Brief justification]
   - Savings: $[X]/year, [X]% energy reduction
   - Payback: [X] years

2. **[ECM Name]** - [Brief justification]
   - Savings: $[X]/year, [X]% energy reduction
   - Payback: [X] years

### Bundle Recommendations
- **Phase 1:** [ECMs with shortest payback]
- **Phase 2:** [ECMs requiring capital investment]
- **Phase 3:** [Long-term improvements]

### Additional Analysis Needed
- [ ] [Further investigation item 1]
- [ ] [Further investigation item 2]

---

## Methodology Notes

**Simulation Settings:**
- EnergyPlus Version: [X.X.X]
- Weather File: [Location/Source]
- Run Period: [Annual / Custom]
- Timestep: [X] steps/hour

**Utility Rates:**
- Electricity: $[X]/kWh (Source: [Utility company])
- Demand: $[X]/kW-month (Source: [Utility company])
- Natural Gas: $[X]/therm (Source: [Utility company])
- Carbon Intensity: [X] lb CO2e/kWh (Source: EPA eGRID [Year])

**Assumptions:**
- [Key assumption 1]
- [Key assumption 2]
- [Key assumption 3]

**Limitations:**
- [Limitation 1]
- [Limitation 2]

---

## Appendix: Detailed Results

### Energy End-Use Breakdown (Baseline)

| End Use | Electricity (kWh) | % of Total | Natural Gas (therms) | % of Total |
|---------|-------------------|------------|----------------------|------------|
| Heating | [X] | [%] | [X] | [%] |
| Cooling | [X] | [%] | [X] | [%] |
| Interior Lighting | [X] | [%] | - | - |
| Exterior Lighting | [X] | [%] | - | - |
| Interior Equipment | [X] | [%] | - | - |
| Fans | [X] | [%] | - | - |
| Pumps | [X] | [%] | - | - |
| Heat Rejection | [X] | [%] | - | - |
| DHW | [X] | [%] | [X] | [%] |
| **Total** | **[X]** | **100%** | **[X]** | **100%** |

### Monthly Energy Use Profiles

[Reference to interactive plots created with `create_interactive_plot`]

---

**Report Generated:** [YYYY-MM-DD HH:MM]
