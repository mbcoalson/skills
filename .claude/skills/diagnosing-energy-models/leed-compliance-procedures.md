# LEED Compliance Procedures for Energy Modeling

Comprehensive procedures for LEED v4/v4.1 Energy & Atmosphere credit compliance using ASHRAE 90.1 Appendix G. This document focuses on baseline generation, percent savings calculations, and documentation requirements.

**Key Reference**: ASHRAE 90.1 Appendix G (version must match project submission requirements)

---

## Overview

LEED Energy & Atmosphere credits require:
- Proposed design model matching EOR specifications
- Baseline model per ASHRAE 90.1 Appendix G
- Building rotation analysis (4 orientations)
- Percent energy cost savings calculation
- Unmet hours < 300 for both proposed and baseline
- Documentation of energy conservation measures (ECMs)

---

## Prerequisites

Before starting baseline generation, verify proposed model:

### Proposed Model Checklist

```
Geometry & Organization:
□ Model simulates successfully without severe errors
□ All spaces assigned to thermal zones
□ Surface matching complete (no red surfaces)
□ Building stories properly organized
□ Space areas match architectural plans (±5%)

HVAC Systems:
□ All systems match EOR specifications exactly
□ Equipment types correct (VAV, CV, heat pump, etc.)
□ Plant loops properly connected
□ Terminal types match EOR specs
□ Controls match EOR sequences

Envelope:
□ Construction assemblies assigned to all surfaces
□ Window properties match specifications
□ Door assemblies defined
□ Infiltration rates reasonable (per ASHRAE 62.1 or project specs)

Internal Loads:
□ Space types assigned (90.1 or 189.1 templates)
□ Occupancy schedules defined and reasonable
□ Lighting power densities match design
□ Equipment loads defined
□ Service hot water included (if applicable)

Schedules:
□ HVAC availability schedules defined
□ Heating/cooling setpoints reasonable (typically 70°F/75°F)
□ Thermostat setback schedules (if applicable)
□ Operating schedules match building type

Simulation Results:
□ Simulation completes successfully
□ Unmet hours < 300
□ Energy consumption reasonable for building type (compare EUI to benchmarks)
□ Peak demands reasonable
□ No severe warnings in error file
```

**If any items unchecked**: Resolve before proceeding with baseline generation.

---

## ASHRAE 90.1 Appendix G Baseline Transformation Rules

These rules transform the proposed model into the baseline model. Rules vary slightly by 90.1 version (2019, 2022, etc.) - verify correct version for your project.

### Envelope Transformations

**Opaque Surfaces (Walls, Roofs, Floors):**
```
- Replace all constructions with Appendix G baseline assemblies
- Baseline U-factors from Table G3.1.5 (based on climate zone)
- Construction details (specific materials) don't matter, only overall U-factor
- Mass vs. non-mass designation affects assembly type
```

**Windows:**
```
- Window-to-wall ratio (WWR):
  - IF proposed WWR ≤ 40%: Baseline uses proposed WWR
  - IF proposed WWR > 40%: Baseline uses 40% WWR (reduce proportionally)
- Vertical fenestration properties from Table G3.1.5:
  - U-factor by climate zone
  - SHGC (Solar Heat Gain Coefficient) by climate zone
  - Use simple window model (no detailed angular properties)
- Window distribution:
  - Maintain proportional distribution by orientation
  - If reducing WWR, scale all windows proportionally
```

**Doors:**
```
- Opaque door area must match proposed
- Baseline U-factors from Table G3.1.5
- Glazed doors follow fenestration rules
```

**Skylights:**
```
- Skylight area:
  - IF proposed ≤ 3% of roof: Baseline uses proposed skylight area
  - IF proposed > 3%: Baseline uses 3% of roof area
- Skylight properties from Table G3.1.5 (U-factor, SHGC)
- Distribution: Maintain proportional distribution across roof surfaces
```

**Infiltration:**
```
- Per Section G3.1.1.4:
- Peak: 0.6 cfm/sf of above-grade envelope at 0.3 in. H₂O
- Adjusted for climate using coefficients
- Modeled as constant or scheduled based on HVAC operation
```

**Validation before applying**: Check latest ASHRAE 90.1 Appendix G tables for climate zone values.

### Lighting Transformations

**Interior Lighting:**
```
- Use building area method from Table G3.1.6:
  - Lighting power density (LPD) by space type
  - Or whole building LPD if detailed space types unavailable
- Apply to all spaces based on their function
- Maintain proposed space categorization

- Controls (per G3.1.2.4):
  - Automatic shutoff controls required:
    - Occupancy sensors OR
    - Scheduled automatic shutoff
  - Model as schedule or occupancy-based control
```

**Exterior Lighting:**
```
- Use proposed design exterior lighting power
- Baseline cannot exceed proposed
- Controls per Section 9.4.1.3 (automatic shutoff, daylight controls)
```

**Validation**: Verify space type assignments against Table G3.1.6, confirm all spaces have appropriate LPD.

### HVAC System Transformations

HVAC baseline is the most complex transformation. System type depends on building characteristics.

**System Selection Logic (Table G3.1.1-1 through G3.1.1-4):**

```
Determine baseline system based on:
1. Building type (residential vs. non-residential)
2. Number of floors (≤3, 4-5, >5)
3. Conditioned floor area
4. Heating source (electric, fossil fuel, purchased)

Common baseline systems:
- System 1: PTAC (Packaged Terminal Air Conditioner)
- System 2: PTHP (Packaged Terminal Heat Pump)
- System 3: PSZ-AC (Packaged Single Zone - Air Conditioner)
- System 4: PSZ-HP (Packaged Single Zone - Heat Pump)
- System 5: Packaged VAV with reheat
- System 6: Packaged VAV with PFP boxes
- System 7: VAV with reheat
- System 8: VAV with PFP boxes
- System 9: Heating and ventilation (heated only)
- System 10: Heating and ventilation (heated only)
- System 11: Single Zone VAV
- System 12: Single Zone VAV (heating and ventilation)
- System 13: Single Zone VAV (cooling and ventilation)
```

**Example: Recreation Center (Non-Residential, Assembly)**
```
- Typically System 7 (VAV with reheat) or System 5 (Packaged VAV with reheat)
- Selection based on:
  - Conditioned floor area > 25,000 sf → System 7 or 8
  - Heating: Electric → System 8, Fossil → System 7
  - Number of floors considered
```

**Fan Power (G3.1.2.9):**
```
- Calculate allowable fan power using formula:
  Pfan = CFMs × 0.0013 + A

  Where:
  - CFMs = Supply airflow in cfm
  - A = Adjustment factors for:
    - Exhaust systems
    - Economizers
    - Heat recovery
    - Filtration
    - Etc.

- Model as constant or variable volume depending on system type
```

**Equipment Efficiencies:**
```
- From Tables 6.8.1-1 through 6.8.1-19:
  - Cooling efficiency (EER, COP) by equipment type and capacity
  - Heating efficiency by equipment type and capacity
  - Part-load performance curves (use defaults if not specified)

- Autosizing:
  - Baseline equipment sized based on baseline model loads
  - Not copied from proposed model
```

**Economizers:**
```
- Required by climate zone (Table G3.1.2.6):
  - Climate zone 2B, 3B, 3C, 4C, 5-8: Economizer required
  - Climate zone 1, 2A, 3A, 4A, 4B: Check specific requirements
- Type: Dry bulb or enthalpy (climate zone dependent)
- High limit: Per Table G3.1.2.6
```

**Controls:**
```
- Setpoints:
  - Cooling: 75°F
  - Heating: 70°F
  - Dead band: 5°F (implied by setpoints)

- Schedules:
  - Match proposed HVAC availability schedule
  - Setback: 5°F heating setback during unoccupied hours (if applicable)

- Demand control ventilation:
  - Required for systems >5000 cfm AND >40 people/1000 sf
  - Model as CO2-based control
```

**Validation before applying**:
- Check Table G3.1.1-1 for correct system type
- Verify efficiency tables for equipment capacities
- Confirm economizer requirements for climate zone

### Service Hot Water Transformations

```
- Equipment type from Table G3.1.1-2:
  - Electric or fuel-fired storage water heater (typical)
  - Efficiency from applicable standard (10 CFR 430, etc.)

- Energy use:
  - Baseline = 50% of proposed service hot water energy
  - If no service hot water in proposed: None in baseline

- Distribution losses:
  - Model pipe losses if significant
  - Use Table G3.1.3.13 for insulation requirements
```

---

## Building Rotation Analysis

LEED requires simulating baseline model at 4 orientations to account for site-specific advantages.

### Rotation Requirements

```
Required orientations:
- 0° (North as designed)
- 90° (North rotated 90° clockwise)
- 180° (North rotated 180°)
- 270° (North rotated 270° clockwise)

Which models to rotate:
- ONLY baseline model is rotated (4 baseline simulations)
- Proposed model stays as-designed (1 simulation)

Why:
- Removes site-specific orientation advantage from proposed design
- Ensures savings aren't solely from favorable orientation
```

### Creating Rotations in OpenStudio

**Method 1: Manual Rotation (Simple)**
```
1. Save baseline.osm as baseline_000.osm
2. Duplicate: baseline_090.osm, baseline_180.osm, baseline_270.osm
3. For each rotated model:
   - OpenStudio → Geometry → Select all surfaces
   - Geometry → Rotate → Apply rotation angle
   - OR modify "Building" object "North Axis" field

4. Run all 4 simulations
```

**Method 2: Measure-Based Rotation (Recommended)**
```
Use OpenStudio Measure to automate rotation:
- "Rotate Building" measure (may need to create or find)
- Apply measure with rotation angle as argument
- Run parametric analysis with 0, 90, 180, 270 as parameters

Benefits:
- Automated, less error-prone
- Easy to re-run if baseline changes
```

**Best Practice**: Use "North Axis" field rather than rotating geometry:
```
- OpenStudio → Site tab → Building → North Axis
- Set to: 0, 90, 180, 270 for each model
- Preserves geometry coordinates (easier to compare models)
```

### Averaging Results

```
Per ASHRAE 90.1 Appendix G:
- Average the 4 baseline rotation results
- Use average baseline energy for percent savings calculation

Calculation:
Baseline_avg = (Baseline_000 + Baseline_090 + Baseline_180 + Baseline_270) / 4

Percent Savings = (Baseline_avg - Proposed) / Baseline_avg × 100%
```

---

## Percent Savings Calculation

### Energy Cost Budget (ECB) Method

```
1. Calculate baseline energy costs:
   - For each rotation: Sum all energy costs (electric, gas, etc.)
   - Average the 4 baseline costs: ECB = Σ(Baseline_costs) / 4

2. Calculate proposed energy costs:
   - Sum all energy costs from proposed model

3. Calculate percent savings:
   Savings (%) = (ECB - Proposed_cost) / ECB × 100%

4. LEED points:
   - v4 BD+C: Optimized Energy Performance (EA Credit)
     - 6% savings: 2 points
     - 10% savings: 3 points
     - Each additional 2%: +1 point
     - Up to 50% savings: 18 points
   - Check specific rating system for exact thresholds
```

### Energy Rates

```
Use actual utility rates from project location:
- Electric: $/kWh (may have demand charges, time-of-use rates)
- Natural gas: $/therm or $/ccf
- Other fuels: appropriate unit costs

Sources for rates:
- Utility bills from similar facilities
- Local utility rate schedules (residential, commercial, industrial)
- State energy office resources
- EIA (Energy Information Administration) average rates

Important:
- Use same rates for proposed AND baseline
- Document rate sources
- Model demand charges if significant
```

### Unmet Hours Verification

```
Both proposed and baseline must meet unmet hours limit:
- Limit: < 300 hours per year
- Count both heating and cooling unmet hours

OpenStudio reporting:
- Results → ABUPS report → Unmet Hours section
- Or parse eplusout.csv for zone unmet hours

If unmet hours exceed 300:
1. Check equipment sizing (may be undersized)
2. Review control setpoints (too tight?)
3. Verify schedules (HVAC availability adequate?)
4. Check for geometry issues (missing surfaces, infiltration too high)
5. Consider increasing equipment capacities (baseline may need larger equipment than proposed)
```

---

## Documentation Requirements

### Models

```
Required deliverables:
□ Proposed model (.osm file)
□ Baseline model - 0° rotation (.osm file)
□ Baseline model - 90° rotation (.osm file)
□ Baseline model - 180° rotation (.osm file)
□ Baseline model - 270° rotation (.osm file)

Naming convention:
- [ProjectName]_Proposed.osm
- [ProjectName]_Baseline_000.osm
- [ProjectName]_Baseline_090.osm
- [ProjectName]_Baseline_180.osm
- [ProjectName]_Baseline_270.osm
```

### Simulation Results

```
For each model, save:
□ eplusout.html (summary report)
□ eplusout.err (error file - verify no severe errors)
□ eplustbl.htm (tabular results)
□ eplusout.sql (for detailed queries if needed)

Organize in folders:
results/
├── proposed/
│   ├── eplusout.html
│   ├── eplustbl.htm
│   └── eplusout.err
└── baseline/
    ├── 000/
    ├── 090/
    ├── 180/
    └── 270/
```

### Compliance Forms

```
LEED EA forms typically require:
- Building characteristics summary
- Envelope assembly descriptions (U-factors, SHGC)
- HVAC system descriptions
- Interior lighting power densities
- Energy cost budget calculation
- Percent savings calculation
- Energy conservation measures (ECMs) list with descriptions

May use:
- LEED Online forms (web-based)
- Or narrative report format
- Include simulation outputs as appendices
```

### Narrative Report Outline

```
1. Executive Summary
   - Project overview
   - Percent savings achieved
   - LEED points expected

2. Modeling Methodology
   - Software used (OpenStudio X.X.X, EnergyPlus X.X)
   - Standards applied (ASHRAE 90.1-20XX Appendix G)
   - Weather file source

3. Proposed Design Description
   - Envelope (walls, windows, roof)
   - HVAC systems (match EOR)
   - Lighting systems
   - Internal loads assumptions
   - Schedules

4. Baseline Design Description
   - Envelope transformations applied
   - HVAC systems (per Appendix G)
   - Lighting transformations
   - Rotation analysis approach

5. Energy Analysis Results
   - Proposed energy consumption (by end use)
   - Baseline energy consumption (4 rotations, averaged)
   - Energy cost budget calculation
   - Percent savings achieved
   - Unmet hours verification

6. Energy Conservation Measures
   - List of ECMs implemented
   - Energy/cost impact of each (if analyzed separately)

7. Appendices
   - Simulation summary reports
   - Model inputs summary
   - Utility rate schedules
   - Appendix G transformations checklist
```

---

## Quality Assurance Checks

Before submitting for LEED review:

### Model Integrity

```
Proposed Model:
□ Simulation completes without severe errors
□ Unmet hours < 300
□ HVAC systems match EOR specifications exactly
□ Equipment capacities reasonable (compare to rules of thumb)
□ Envelope constructions match specifications
□ Lighting power densities match design

Baseline Model:
□ All 4 rotations simulate successfully
□ Unmet hours < 300 for each rotation
□ HVAC system type correct per Table G3.1.1-1
□ Equipment efficiencies match Table 6.8.1-X
□ Envelope assemblies match Table G3.1.5
□ Lighting power densities match Table G3.1.6
□ Fan power within Appendix G limits
```

### Results Reasonableness

```
Energy Consumption:
□ EUI (kBtu/sf/yr) within expected range for building type
□ Baseline EUI > Proposed EUI (if savings claimed)
□ End use breakdown reasonable (HVAC ~50%, Lighting ~20%, typical ratios)
□ Peak demands reasonable for building size

Rotation Analysis:
□ Four baseline rotations have similar (±10%) energy use
□ If one rotation is outlier, investigate cause
□ Averaged baseline is representative

Percent Savings:
□ Calculation method correct (ECB basis)
□ Savings percentage meets LEED target
□ Energy rates documented and reasonable
□ Same rates used for proposed and baseline
```

### Documentation Completeness

```
□ All required models saved and organized
□ Simulation results for all runs saved
□ Compliance forms completed
□ Narrative report written (if required)
□ ECMs documented
□ Utility rates documented
□ EOR coordination documented (proposed model matches specs)
□ Appendix G exceptions documented (if any)
```

---

## Common Issues and Solutions

### Issue 1: Baseline Unmet Hours > 300

**Cause**: Baseline equipment undersized or controls too restrictive

**Solution**:
```
1. Check equipment sizing:
   - OpenStudio → HVAC Systems → View autosized capacities
   - Compare to proposed model capacities
   - If significantly smaller, investigate cause

2. Review load calculations:
   - Are baseline internal loads correct?
   - Is baseline envelope more conductive (higher loads)?

3. Adjust sizing factors if needed:
   - Increase sizing factors slightly (1.1x, 1.2x)
   - Re-run autosizing
   - Verify compliance reviewer accepts this approach

4. Check setpoints and schedules:
   - Baseline setpoints: 70°F heat / 75°F cool
   - HVAC availability matches proposed
```

### Issue 2: Proposed Better Performance Seems Unrealistic

**Cause**: Proposed model may have overly optimistic inputs

**Solution**:
```
1. Verify proposed model inputs:
   - HVAC equipment efficiencies (match manufacturer data?)
   - Lighting power densities (match design?)
   - Occupancy/plug loads (reasonable for building type?)
   - Envelope properties (match specifications?)

2. Compare to benchmarks:
   - CBECS (Commercial Buildings Energy Consumption Survey)
   - ENERGY STAR Portfolio Manager typical EUI
   - Similar LEED projects

3. Coordinate with design team:
   - Confirm optimistic inputs are actually specified
   - Verify controls and sequences will be commissioned
```

### Issue 3: Rotation Results Vary Widely

**Cause**: Asymmetric building or unusual window distribution

**Solution**:
```
1. Verify rotations were applied correctly:
   - Check "North Axis" field for each model
   - Confirm rotations are 90° increments

2. Investigate building characteristics:
   - Is building highly asymmetric (long rectangle)?
   - Does one side have much higher WWR?
   - Are there large skylights on one side?

3. If legitimate:
   - Document why rotations vary
   - Average still appropriate per Appendix G
   - Explain in narrative report

4. If error:
   - Check for modeling mistakes (HVAC assigned to wrong zones in some rotations)
   - Re-create baseline model carefully
```

---

## Using OpenStudio Standards Gem

The OpenStudio Standards gem automates many Appendix G transformations.

### Installation

```bash
# OpenStudio 3.9 includes Standards gem
# Verify version:
openstudio gem list | grep openstudio-standards
```

### Creating Baseline Measure

```ruby
# Example measure using OpenStudio Standards gem
require 'openstudio-standards'

# Create standard object
standard = Standard.build('90.1-2019')  # Or 2022, etc.

# Create baseline model
baseline_model = standard.model_create_prototype_model(
  building_type: 'Assembly',  # Or other type
  climate_zone: 'ASHRAE 169-2013-5B',
  epw_file: 'path/to/weather.epw',
  template: '90.1-2019',
  modify_wkdy_op_hrs: false,
  modify_wknd_op_hrs: false
)
```

### Applying Transformations

```ruby
# Apply Appendix G transformations to existing model
model = translator.loadModel('proposed_model.osm').get

# Create baseline from proposed
standard.model_apply_appendix_g_baseline(model, building_type: 'Assembly')

# Adjustments
standard.model_apply_hvac_efficiency_standard(model, climate_zone)
```

**Note**: Standards gem is powerful but may require customization for project-specific needs. Always validate automated results.

---

## Before Providing LEED Guidance

Always validate approach:

1. **Check ASHRAE 90.1 version** required for project
2. **WebFetch current Appendix G requirements** (editions change)
3. **Search Unmet Hours** for LEED compliance best practices:
   ```
   site:unmethours.com appendix g baseline openstudio
   site:unmethours.com leed rotation analysis
   ```
4. **Verify climate zone** and corresponding requirements
5. **Confirm building type** for correct baseline system selection

---

**Last Updated**: 2025-11-19
**Aligned with**: ASHRAE 90.1-2019/2022 Appendix G, LEED v4/v4.1, OpenStudio 3.9
