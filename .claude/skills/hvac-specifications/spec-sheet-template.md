# HVAC Equipment Specification Sheet Template

This template guides specification extraction from manufacturer data sheets, submittal documents, and technical literature. Use this structure to present findings consistently.

## Universal Output Format

```
[BRAND] [MODEL NUMBER] Specifications

Equipment Type: [AHU/VAV/Chiller/Boiler/Pump/Fan/etc.]

CAPACITY
- [Specification]: [Value with units]

EFFICIENCY
- [Specification]: [Value with units]

ELECTRICAL REQUIREMENTS
- [Specification]: [Value with units]

PHYSICAL DIMENSIONS
- [Specification]: [Value with units]

OPERATING CONDITIONS
- [Specification]: [Value with units]

ADDITIONAL SPECIFICATIONS
- [Any other relevant specs]

---
📄 SOURCES:
- [Source Name](actual-url)
- [Source Name](actual-url)

⚠️ VERIFICATION REQUIRED: Please verify source URLs are legitimate before using specifications for design or procurement.
```

---

## Equipment-Specific Extraction Patterns

### Air Handling Units (AHU)

**CAPACITY**
- Airflow: [CFM] at [static pressure]
- Cooling Capacity: [tons or MBH]
- Heating Capacity: [MBH or kW]
- External Static Pressure: [in. w.g.]

**EFFICIENCY**
- Fan Motor Efficiency: [%]
- Total Unit Efficiency: [if available]

**ELECTRICAL REQUIREMENTS**
- Voltage: [V]
- Phase: [1 or 3]
- Frequency: [Hz]
- Supply Fan Motor: [HP]
- Full Load Amps (FLA): [A]
- Minimum Circuit Ampacity (MCA): [A]
- Maximum Overcurrent Protection (MOCP): [A]

**PHYSICAL DIMENSIONS**
- Length: [in or mm]
- Width: [in or mm]
- Height: [in or mm]
- Weight (Operating): [lbs or kg]
- Weight (Shipping): [lbs or kg]

**OPERATING CONDITIONS**
- Design Airflow: [CFM]
- Entering Air Temperature: [°F or °C]
- Supply Air Temperature: [°F or °C]

**ADDITIONAL SPECIFICATIONS**
- Coil Type: [DX, Chilled Water, Hot Water, Steam]
- Filter Type and Size: [type, MERV rating]
- Sound Rating: [dBA or sones]
- Cabinet Construction: [material]
- Insulation: [type, R-value]

---

### Chillers

**CAPACITY**
- Cooling Capacity: [tons] at [conditions]
- Capacity (kW): [kW]
- Operating Range: [min - max tons]

**EFFICIENCY**
- Full Load Efficiency: [kW/ton or COP or EER]
- IPLV (Integrated Part Load Value): [kW/ton or COP]
- Part Load Efficiencies:
  - 100% Load: [kW/ton]
  - 75% Load: [kW/ton]
  - 50% Load: [kW/ton]
  - 25% Load: [kW/ton]
- SEER (if applicable): [value]

**ELECTRICAL REQUIREMENTS**
- Voltage: [V]
- Phase: [3]
- Frequency: [Hz]
- Rated Load Amps (RLA): [A]
- Full Load Amps (FLA): [A]
- Minimum Circuit Ampacity (MCA): [A]
- Maximum Overcurrent Protection (MOCP): [A]
- Starting Method: [VFD, soft start, etc.]

**PHYSICAL DIMENSIONS**
- Length: [in or mm]
- Width: [in or mm]
- Height: [in or mm]
- Operating Weight: [lbs or kg]
- Shipping Weight: [lbs or kg]
- Rigging Weight: [lbs or kg]

**OPERATING CONDITIONS**
- Refrigerant Type: [R-410A, R-134a, R-513A, etc.]
- Refrigerant Charge: [lbs]
- Evaporator Water Flow: [GPM]
- Evaporator Pressure Drop: [ft or PSI]
- Condenser Water Flow: [GPM]
- Condenser Pressure Drop: [ft or PSI]
- Entering/Leaving Water Temps: [°F]
- Operating Ambient Range: [min - max °F]

**ADDITIONAL SPECIFICATIONS**
- Compressor Type: [scroll, screw, centrifugal]
- Number of Compressors: [count]
- Sound Rating: [dBA at distance]
- Control System: [manufacturer/model]
- Communication Protocol: [BACnet, Modbus, etc.]

---

### Boilers

**CAPACITY**
- Heating Input: [MBH input]
- Heating Output: [MBH output or kW]
- Steam Capacity: [lbs/hr] (if steam boiler)

**EFFICIENCY**
- AFUE (Annual Fuel Utilization Efficiency): [%]
- Thermal Efficiency: [%]
- Combustion Efficiency: [%]

**ELECTRICAL REQUIREMENTS**
- Voltage: [V]
- Phase: [1 or 3]
- Frequency: [Hz]
- Full Load Amps: [A]
- Control Circuit: [V]

**PHYSICAL DIMENSIONS**
- Length: [in or mm]
- Width: [in or mm]
- Height: [in or mm]
- Weight (Dry): [lbs or kg]
- Weight (Operating): [lbs or kg]

**OPERATING CONDITIONS**
- Fuel Type: [Natural Gas, Propane, Oil, Electric]
- Gas Connection Size: [in]
- Water Connection Size: [in]
- Operating Pressure: [PSI]
- Maximum Operating Temperature: [°F]
- Water Flow Rate: [GPM]
- Pressure Drop: [ft or PSI]

**ADDITIONAL SPECIFICATIONS**
- Turndown Ratio: [ratio, e.g., 5:1]
- Modulation Type: [full modulating, staged, on/off]
- Venting Type: [direct vent, power vent, etc.]
- Flue Size: [in]
- Burner Type: [description]
- Control System: [description]

---

### VAV Boxes

**CAPACITY**
- Maximum Airflow: [CFM]
- Minimum Airflow: [CFM]
- Turndown Ratio: [ratio]

**ELECTRICAL REQUIREMENTS**
- Control Voltage: [VAC]
- Actuator Power: [VA or W]

**PHYSICAL DIMENSIONS**
- Inlet Size: [in diameter or rectangular dimensions]
- Length: [in]
- Width: [in]
- Height: [in]
- Weight: [lbs]

**OPERATING CONDITIONS**
- Maximum Static Pressure: [in. w.g.]
- Inlet Velocity: [FPM]

**ADDITIONAL SPECIFICATIONS**
- Damper Type: [single blade, opposed blade, parallel blade]
- Actuator Type: [pneumatic, electric, DDC]
- Reheat Coil (if applicable):
  - Type: [hot water, electric]
  - Capacity: [MBH or kW]
  - Valve Size: [in]
- Sound Rating: [NC or sones]
- Leakage Class: [class rating]
- Control Options: [pressure independent, pressure dependent]

---

### Pumps

**CAPACITY**
- Flow Rate: [GPM]
- Head (Total Dynamic): [feet or PSI]
- Operating Point: [GPM @ feet]

**EFFICIENCY**
- Pump Efficiency: [%] at [GPM]
- Motor Efficiency: [%]
- Wire-to-Water Efficiency: [%]

**ELECTRICAL REQUIREMENTS**
- Voltage: [V]
- Phase: [1 or 3]
- Frequency: [Hz]
- Motor Horsepower: [HP]
- Full Load Amps (FLA): [A]
- Service Factor: [value]
- Motor Type: [TEFC, ODP, etc.]
- VFD Compatible: [Yes/No]

**PHYSICAL DIMENSIONS**
- Length: [in]
- Width: [in]
- Height: [in]
- Weight: [lbs]

**OPERATING CONDITIONS**
- Pump Type: [end suction, inline, split case, etc.]
- Impeller Diameter: [in]
- Speed: [RPM]
- Maximum Fluid Temperature: [°F]
- Maximum Working Pressure: [PSI]
- Connection Size (Suction): [in]
- Connection Size (Discharge): [in]

**ADDITIONAL SPECIFICATIONS**
- Materials of Construction:
  - Casing: [material]
  - Impeller: [material]
  - Shaft: [material]
  - Seal: [type]
- NPSHr (Net Positive Suction Head Required): [feet]
- Sound Rating: [dBA]

---

### Fans

**CAPACITY**
- Airflow: [CFM]
- Static Pressure: [in. w.g.]
- Operating Point: [CFM @ static pressure]

**EFFICIENCY**
- Fan Efficiency: [%]
- Motor Efficiency: [%]

**ELECTRICAL REQUIREMENTS**
- Voltage: [V]
- Phase: [1 or 3]
- Frequency: [Hz]
- Motor Horsepower: [HP or kW]
- Full Load Amps (FLA): [A]
- Motor Type: [TEFC, ODP, etc.]
- VFD Compatible: [Yes/No]

**PHYSICAL DIMENSIONS**
- Fan Diameter: [in]
- Length: [in]
- Width: [in]
- Height: [in]
- Weight: [lbs]

**OPERATING CONDITIONS**
- Fan Type: [centrifugal, axial, plug, etc.]
- Wheel Type: [forward curved, backward inclined, airfoil, etc.]
- Speed: [RPM]
- Maximum Ambient Temperature: [°F]
- Class and Arrangement: [AMCA class]

**ADDITIONAL SPECIFICATIONS**
- Sound Rating: [sones or dBA]
- Inlet Size: [in]
- Outlet Size: [in]
- Drive Type: [direct drive, belt drive]
- Materials of Construction: [description]

---

## Common Unit Conversions (for Reference)

### Capacity
- 1 ton (cooling) = 12,000 BTU/h = 3.517 kW
- 1 MBH = 1,000 BTU/h

### Temperature
- °F to °C: (°F - 32) × 5/9
- °C to °F: (°C × 9/5) + 32

### Pressure
- 1 PSI = 2.31 feet of head
- 1 in. w.g. = 0.0361 PSI = 0.0833 feet of head

### Flow
- 1 GPM = 8.33 lbs/min (water at 60°F)
- 1 GPM = 0.227 m³/h

### Power
- 1 HP = 0.746 kW = 2,544 BTU/h

---

## Handling Missing Data

When specifications are not found:
```
CAPACITY
- Airflow: NOT FOUND IN SOURCE
- Cooling Capacity: 5 tons
```

Always note what is missing so user knows what additional research is needed.

---

## Notes for Iteration

**This template will evolve.** As you use this skill, you may discover:
- Additional specification categories needed
- Different naming conventions from manufacturers
- Equipment-specific details not covered here

Update this template as patterns emerge to improve future lookups.
