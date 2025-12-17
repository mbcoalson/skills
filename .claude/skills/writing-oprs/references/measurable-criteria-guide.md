# Writing Measurable Performance Criteria for OPRs

## Overview

The most critical aspect of an effective OPR is establishing clear, measurable performance criteria. Vague requirements lead to disputes during commissioning verification and make it impossible to objectively determine if the owner's requirements have been met.

## The SMART Framework

Performance criteria should be:
- **Specific**: Clearly defined without ambiguity
- **Measurable**: Can be verified through testing or observation
- **Achievable**: Realistic within project constraints
- **Relevant**: Directly tied to owner's goals
- **Time-bound**: Include when the requirement applies (occupied hours, design conditions, etc.)

## Examples: Vague vs. Measurable

### Temperature Control

❌ **Vague**: "The HVAC system shall maintain comfortable temperatures"
- Not measurable - what is "comfortable"?
- No acceptance criteria for testing

✅ **Measurable**: "The HVAC system shall maintain space temperatures of 72°F ± 2°F during occupied hours (6 AM - 10 PM) under design conditions"
- Specific setpoint and tolerance
- Defined time period
- Clear pass/fail criteria

### Lighting

❌ **Vague**: "Provide adequate lighting for office work"
- "Adequate" is subjective
- No way to verify compliance

✅ **Measurable**: "Provide minimum 50 footcandles maintained illuminance at desk height (30" AFF) in all office areas, measured on a 10-foot grid"
- Specific light level
- Defined measurement location and height
- Clear testing methodology

### Energy Performance

❌ **Vague**: "The building shall be energy efficient"
- No baseline for comparison
- Impossible to verify

✅ **Measurable**: "The building shall achieve a minimum ENERGY STAR score of 75, or reduce energy use by 30% compared to ASHRAE 90.1-2019 Appendix G baseline"
- Specific target with industry-standard metric
- Clear verification method
- Alternative compliance paths

### Ventilation

❌ **Vague**: "Provide fresh air to occupied spaces"
- No quantities specified
- No reference standard

✅ **Measurable**: "Provide outdoor air ventilation rates per ASHRAE 62.1-2019 for the design occupancy, with CO₂ levels maintained below 1000 ppm during occupied hours in all regularly occupied spaces"
- References specific code standard
- Includes secondary verification metric (CO₂)
- Defines when it applies

### Equipment Reliability

❌ **Vague**: "Equipment shall be reliable"
- No definition of reliability
- No verification period

✅ **Measurable**: "All HVAC equipment shall operate continuously for 30 days without unplanned shutdown or requiring service calls during the warranty period"
- Specific time period
- Clear failure criteria
- Defined verification period

## Key Components of Measurable Criteria

### 1. Quantitative Values
Include specific numbers with units:
- Temperatures: "68°F to 74°F"
- Flow rates: "400 CFM per person"
- Pressures: "0.02" to 0.05" W.C."
- Efficiency: "0.85 kW/ton at AHRI conditions"

### 2. Tolerances
Define acceptable ranges:
- "± 2°F" for temperature control
- "± 10%" for airflow measurements
- "± 5 psi" for pressure differentials

### 3. Operating Conditions
Specify when requirements apply:
- "During occupied hours (6 AM - 10 PM weekdays)"
- "At design conditions (95°F outdoor, 75°F indoor)"
- "Under full load"
- "During unoccupied setback mode"

### 4. Reference Standards
Cite applicable codes and standards:
- "Per ASHRAE 62.1-2019"
- "In accordance with IECC 2021"
- "Meeting LEED v4 EAp2 requirements"

### 5. Measurement Methodology
Describe how verification will occur:
- "Measured with calibrated light meter on 10-foot grid"
- "Verified through BAS trend data over 7-day period"
- "Confirmed by third-party air balance report"

## Common Pitfalls to Avoid

### Using Subjective Language
❌ Avoid: comfortable, adequate, sufficient, appropriate, reasonable, optimal
✅ Use: specific numbers, ranges, and reference standards

### Specifying Methods Instead of Performance
❌ "Install variable frequency drives on all pumps"
✅ "Pumping system shall consume no more than X kW at design flow conditions"
- The OPR focuses on WHAT performance is needed
- The Basis of Design (BOD) describes HOW it will be achieved

### Unmeasurable Qualitative Statements
❌ "The building shall be easy to maintain"
✅ "All mechanical equipment shall be accessible without removing permanent construction, with minimum 36" clearance for service"

### Missing Time Context
❌ "Maintain 72°F temperature"
✅ "Maintain 72°F ± 2°F during occupied hours; 65°F minimum during unoccupied hours"

## System-Specific Guidance

### HVAC Systems
Key measurable parameters:
- Temperature setpoints and tolerances
- Humidity range (if controlled)
- Outdoor air ventilation rates
- Space pressurization (critical areas)
- Equipment staging and response time
- Noise levels (NC or dBA criteria)

### Lighting Systems
Key measurable parameters:
- Illuminance levels (footcandles or lux)
- Color rendering index (CRI)
- Color temperature (Kelvin)
- Dimming range and control
- Lighting power density (W/SF)
- Emergency lighting duration

### Electrical Systems
Key measurable parameters:
- Voltage regulation (± %)
- Power quality (THD limits)
- Emergency power transfer time
- UPS runtime at design load
- Panel/circuit loading limits

### Controls Systems
Key measurable parameters:
- Control accuracy (± tolerance)
- Response time to setpoint changes
- Override time limits
- Alarm response requirements
- Data logging intervals
- System uptime requirements

## Verification Methods

For each measurable criterion, consider how it will be verified:

**Direct Measurement**
- Temperature sensors, light meters, flow meters, etc.
- Requires calibrated test equipment
- Documented during functional performance testing

**Trend Data Analysis**
- Building automation system data collection
- Minimum 7-day trending for typical operation
- Statistical analysis of performance

**Visual Inspection**
- Verification of installed equipment
- Confirmation of clearances and access
- Documentation through photos

**Document Review**
- Submittals and O&M manuals
- Test reports and certifications
- Energy models and calculations

**Demonstration**
- Sequence of operations testing
- Control system programming verification
- Operator training and demonstration

## Template Language

Use this template structure for each performance requirement:

**[System/Component] shall [perform action] to achieve [measurable target] [with tolerance] [under specified conditions] [verified by method].**

**Example**: "The variable air volume system shall modulate supply airflow to maintain space temperature at 72°F ± 2°F during occupied hours under design load conditions, verified through BAS trend analysis over 7 consecutive days."

## Checklist for Review

Before finalizing OPR performance criteria, verify:
- [ ] Each requirement includes specific numerical values
- [ ] Units are clearly specified
- [ ] Tolerances/ranges are defined
- [ ] Operating conditions are stated (when it applies)
- [ ] Reference standards are cited where applicable
- [ ] Verification method is identifiable
- [ ] Requirements are testable during commissioning
- [ ] Language is objective, not subjective
- [ ] Focus is on performance outcomes, not methods
- [ ] Requirements align with owner's stated goals
