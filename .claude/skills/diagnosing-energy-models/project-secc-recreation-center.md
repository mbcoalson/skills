# Project-Specific Context: SECC Recreation Center (Fort Collins)

This document contains project-specific context for the SECC Recreation Center energy modeling work. These details supplement the general diagnostic workflows and should be referenced when working on this project.

---

## Project Overview

**Project Name**: SECC Recreation Center
**Location**: Fort Collins, Colorado
**Climate Zone**: ASHRAE 169-2013-5B (Cool Dry)
**Building Size**: 92,000 sf (approximate)
**Building Type**: Recreation Center + Pool + Library (Mixed Assembly Use)
**Certifications**: LEED V4 + Colorado IDAP (Innovative Design Assistance Program)

### Key Dates

- **Pre-Thanksgiving 2025**: Coordination deadline
- **Ongoing**: Energy model development and HVAC rebuild

### Project Team

- **Engineer of Record (EOR)**: Clarkenersen
  - EOR specifications are CRITICAL for HVAC validation
  - Equipment list: See `11_10_2025_ZoneEquipList.pdf`
- **Energy Modeler**: Mat Coalson
- **IDAP Program**: Energy efficiency incentive program (10% below ASHRAE 90.1-2022 baseline)

---

## Project-Specific Challenges

### 1. Original Model Issues (Historical Context)

**Problem**: Original model had fundamentally broken geometry
```
Issue: 6 Building Stories with 5 at Z=0 (overlapping)
Result: Severe geometry errors, intersecting surfaces, simulation failure
Decision: Complete geometry rebuild required
Time investment: 8-12 hours for rebuild
```

**Lesson Learned**: Story organization must match physical building levels, not programmatic areas.

### 2. Complex Program Mix

The building includes three distinct program areas with different modeling requirements:

**Recreation Center (~40,000 sf)**
- Typical gym spaces, fitness areas, multipurpose rooms
- Standard HVAC: VAV systems with electric reheat
- Normal ceiling heights (10-12 ft)

**Natatorium/Pool (~15,000 sf)**
- Special modeling case: High humidity, chemical off-gassing
- Custom space requirements:
  - 30' ceiling height (requires careful space geometry)
  - Pool water surface modeled as internal mass or other object
  - Dehumidification system (critical for energy and comfort)
- HVAC: Dedicated pool dehumidification unit (not typical HVAC)

**Library (~37,000 sf)**
- Reading areas, stacks, offices, meeting rooms
- HVAC: VAV systems serving multiple zones
- Multiple thermal zones per equipment unit

### 3. HVAC System Complexity

The building has **6 different RTU/DOAS systems + central plant equipment**:

**Equipment from EOR Specifications** (Reference: `11_10_2025_ZoneEquipList.pdf`):
- Multiple HP RTU units (Heat Pump Rooftop Units)
- WAHP systems (Water-to-Air Heat Pumps with fluid cooler)
  - **Important**: Fluid cooler, NOT cooling tower
  - Impacts equipment selection and connections in OpenStudio
- DOAS units (Dedicated Outdoor Air Systems)
- Pool dehumidification unit (special case)

**Validation Protocol**:
- Every HVAC component must match EOR specifications EXACTLY
- Cross-reference `11_10_2025_ZoneEquipList.pdf` for equipment list
- Verify against `IDAP-SD-report-SECC_9-30-2025.docx` for IDAP compliance

---

## IDAP Program Requirements

### Energy Targets

**IDAP Baseline**: 10% below ASHRAE 90.1-2022 baseline
- More stringent than standard LEED (typically 10% for 3 points)
- IDAP provides design assistance and construction incentives

**Energy Cost Gap**: $20k/yr to close (as of project documents)
- Requires optimization of envelope, HVAC, lighting
- May need ECM analysis to identify cost-effective measures

### Construction Incentives

**Available Incentives**: $55k+ (construction phase)
- Incentives based on verified energy savings
- Must demonstrate savings through modeling and commissioning
- Requires careful documentation of ECMs

### IDAP-Specific Deliverables

Reference: `IDAP-SD-report-SECC_9-30-2025.docx`
- Energy model matching IDAP requirements
- ECM analysis with cost-effectiveness
- Coordination with utility incentive programs

---

## Special Modeling Considerations

### Pool/Natatorium Modeling

**Key Challenges**:
1. **High Ceiling Space**: 30 ft ceiling height
   - Create space with accurate geometry
   - Impacts stratification, heating/cooling loads

2. **Pool Water Surface**:
   - Evaporation loads (major latent heat source)
   - Options for modeling:
     - Internal Mass with custom properties
     - OtherEquipment with latent fraction
     - Detailed pool water heat balance (advanced)

3. **Dehumidification System**:
   - NOT a standard HVAC system
   - Typically modeled as:
     - ZoneHVAC:EnergyRecoveryVentilator (if heat recovery)
     - Custom system using ZoneHVAC components
     - Or simplified as standard unit with adjusted performance
   - Must validate approach with manufacturer data

4. **Chemical Off-Gassing**:
   - Requires higher ventilation rates than typical spaces
   - Minimum outdoor air per codes and pool design standards
   - Impacts dehumidification load and energy consumption

**Before modeling pool**:
- Check OpenStudio documentation for natatorium modeling
- Search Unmet Hours: `site:unmethours.com pool natatorium openstudio`
- Review manufacturer data for dehumidification unit

### WAHP Systems (Water-to-Air Heat Pumps)

**Equipment Details**:
- Water-source heat pumps with fluid cooler
- **NOT cooling tower** - Different modeling approach:
  - Cooling tower: Evaporative cooling (water loss, higher efficiency)
  - Fluid cooler: Dry cooling (no water loss, lower efficiency)
  - In OpenStudio: Use FluidCooler object, NOT CoolingTower

**Modeling Approach**:
1. Create condenser water loop (plant loop)
2. Add WAHP equipment to zones (ZoneHVAC:WaterToAirHeatPump)
3. Connect to condenser loop (demand side)
4. Add fluid cooler to condenser loop (supply side)
5. Verify connections in Plant Loops → Connections tab

**Validation**:
- Check EnergyPlus I/O Reference for FluidCooler object
- Search Unmet Hours: `site:unmethours.com water to air heat pump fluid cooler`

### Multiple RTU Systems

**Challenge**: Coordinating multiple RTU systems serving different zones

**EOR Equipment List Structure** (from `11_10_2025_ZoneEquipList.pdf`):
- Equipment ID (e.g., HP RTU-1, HP RTU-2)
- Spaces served by each unit
- CFM, cooling tons, heating MBH

**Modeling Workflow**:
1. Create equipment matrix (see [diagnostic-workflows.md](./diagnostic-workflows.md) Workflow 3)
2. Assign thermal zones by equipment
3. Create air loop for each RTU
4. Connect zones to appropriate air loops
5. Verify against EOR list

**Common Mistake**: Assigning wrong zones to wrong RTU
- Prevention: Use zone naming convention: "Zone-[RTU ID]-[Space Name]"

---

## HVAC Rebuild Plan

Reference open file: `SECC_HVAC_Rebuild_Plan.md` (in work tracking folder)

**Current Status**: [Check document for latest status]

**Key Steps** (as documented):
1. Validate geometry (ensure rebuild resolved story organization)
2. Create thermal zone assignments per EOR
3. Build HVAC systems matching EOR specs
4. Model pool dehumidification
5. Verify plant loop connections (especially WAHP fluid cooler)
6. Run simulation and resolve errors
7. Validate against IDAP targets

**When working on SECC HVAC rebuild**:
- Always cross-reference EOR documents
- Document assumptions and decisions
- Validate against authoritative sources before implementing
- Update HVAC rebuild plan document with progress

---

## Key Reference Documents

Located in project folders (paths may vary):

**EOR Specifications**:
- `11_10_2025_ZoneEquipList.pdf` - Equipment schedule (CRITICAL)
- Mechanical drawings (HVAC plans, equipment details)
- Sequences of operations (if available)

**IDAP Program**:
- `IDAP-SD-report-SECC_9-30-2025.docx` - IDAP schematic design report
- IDAP design assistance meeting notes
- ECM analysis documentation

**Model Development**:
- `SECC_HVAC_Rebuild_Plan.md` - Current rebuild plan and status
- Previous model files (for reference only - NOT to be used directly)
- Geometry files (SketchUp, OSM)

**Project Tracking**:
- Work tracking folder: `User-Files/work-tracking/secc-fort-collins/energy-model/`

---

## Budget and Time Constraints

### Energy Cost Gap

**Current Gap**: $20k/yr between proposed design and IDAP target
- Requires ECM analysis to close gap
- Options to consider:
  - Enhanced envelope (better insulation, windows)
  - High-efficiency HVAC (beyond code minimum)
  - Advanced controls (occupancy sensors, CO2 DCV)
  - Heat recovery (DOAS, pool dehumidification)

**Modeling Approach**:
1. Baseline model (ASHRAE 90.1-2022 Appendix G)
2. Code-minimum proposed model (90.1-2022 prescriptive)
3. IDAP target (10% below baseline)
4. Current proposed design
5. Identify gap and ECMs to close it

### Construction Incentives

**Available**: $55k+ from IDAP program
- Tied to verified energy savings
- Requires accurate modeling and commissioning
- Document ECMs with energy savings and costs

**Cost-Effectiveness Analysis**:
- Simple payback < 10 years (typical threshold)
- Consider utility incentives in payback calculation
- Prioritize ECMs with best cost-effectiveness

---

## Quality Assurance for SECC Project

In addition to standard QA checks, verify:

### EOR Compliance
```
□ All equipment from 11_10_2025_ZoneEquipList.pdf in model
□ Equipment types match exactly (HP RTU, WAHP, DOAS, etc.)
□ Thermal zones match EOR space assignments
□ CFM, capacities within 10% of EOR design (if autosized)
□ Fluid cooler (not cooling tower) used for WAHP systems
```

### Pool/Natatorium
```
□ 30' ceiling height modeled correctly
□ Pool water surface evaporation loads included
□ Dehumidification system modeled (validated approach)
□ Higher ventilation rates for pool space
□ Reasonable latent loads and humidity levels
```

### IDAP Requirements
```
□ Baseline model per ASHRAE 90.1-2022 Appendix G
□ Proposed model matches current design
□ Energy cost savings calculated correctly
□ ECMs documented with savings and costs
□ Construction incentive calculations accurate
```

### Documentation
```
□ HVAC rebuild plan updated with current status
□ Assumptions documented (especially for pool)
□ EOR coordination documented (meetings, RFIs, clarifications)
□ IDAP deliverables prepared or in progress
```

---

## When Working on SECC Project

1. **Before making HVAC recommendations**:
   - Reference `11_10_2025_ZoneEquipList.pdf`
   - Verify against EOR specs (equipment type, capacity)
   - Check OpenStudio/EnergyPlus docs for proper modeling approach
   - Search Unmet Hours for similar systems

2. **For pool/natatorium issues**:
   - Consult pool dehumidification manufacturer data
   - Validate modeling approach with multiple sources
   - Document assumptions clearly (high uncertainty area)

3. **For IDAP compliance**:
   - Reference `IDAP-SD-report-SECC_9-30-2025.docx`
   - Calculate energy cost savings, not just energy savings
   - Consider construction incentives in ECM analysis

4. **For geometry issues**:
   - Remember historical issue (story organization)
   - Verify story Z-coordinates before any major changes
   - Don't let programmatic organization drive story structure

5. **Update tracking**:
   - Update `SECC_HVAC_Rebuild_Plan.md` with progress
   - Document decisions and rationale
   - Note any deviations from EOR specs (with justification)

---

## Lessons Learned (Ongoing)

As work progresses, document lessons learned here:

**2025-11 (Historical)**:
- Story organization at Z=0 caused complete model failure → Always validate story structure first
- Pool modeling requires special attention → Research manufacturer data and precedent models

**[Add new lessons as discovered]**

---

**Last Updated**: 2025-11-19
**Project Phase**: HVAC Rebuild (Ongoing)
**Next Major Milestone**: Pre-Thanksgiving 2025 Coordination
