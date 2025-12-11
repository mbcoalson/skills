#!/usr/bin/env python3
"""
Extract HVAC Equipment for IDAP Report
Generates equipment tables matching IDAP SD report format
"""

import sys
import os
from eppy.modeleditor import IDF

def find_idd():
    """Auto-detect Energy+.idd from common installation locations"""
    common_locations = [
        r'C:/EnergyPlusV25-1-0/Energy+.idd',
        r'C:/EnergyPlusV24-2-0/Energy+.idd',
        r'/usr/local/EnergyPlus-25-1-0/Energy+.idd',
        r'/Applications/EnergyPlus-25-1-0/Energy+.idd'
    ]
    for loc in common_locations:
        if os.path.exists(loc):
            return loc
    return None

def extract_airloops(idf):
    """Extract all AirLoopHVAC systems"""
    airloops = idf.idfobjects['AIRLOOPHVAC']
    systems = []

    for airloop in airloops:
        system = {
            'name': airloop.Name,
            'type': 'DOAS' if 'DOAS' in airloop.Name else 'RTU',
            'fans': [],
            'coils': [],
            'erv': None
        }
        systems.append(system)

    return systems

def extract_boilers(idf):
    """Extract all boilers"""
    boilers = idf.idfobjects.get('BOILER:HOTWATER', [])
    equipment = []

    for boiler in boilers:
        equipment.append({
            'name': boiler.Name,
            'type': 'Condensing Hot Water Boiler',
            'fuel': boiler.Fuel_Type if hasattr(boiler, 'Fuel_Type') else 'NaturalGas',
            'efficiency': boiler.Nominal_Thermal_Efficiency if hasattr(boiler, 'Nominal_Thermal_Efficiency') else '0.80'
        })

    return equipment

def extract_heat_pumps(idf):
    """Extract water-to-air heat pump coils"""
    cooling_coils = idf.idfobjects.get('COIL:COOLING:WATERTOAIRHEATPUMP:EQUATIONFIT', [])
    heating_coils = idf.idfobjects.get('COIL:HEATING:WATERTOAIRHEATPUMP:EQUATIONFIT', [])

    equipment = {
        'cooling': [{'name': c.Name} for c in cooling_coils],
        'heating': [{'name': h.Name} for h in heating_coils]
    }

    return equipment

def extract_pumps(idf):
    """Extract all pumps"""
    var_pumps = idf.idfobjects.get('PUMP:VARIABLESPEED', [])
    const_pumps = idf.idfobjects.get('PUMP:CONSTANTSPEED', [])

    pumps = []

    for pump in list(var_pumps) + list(const_pumps):
        pump_type = 'Variable Speed' if pump.key.upper() == 'PUMP:VARIABLESPEED' else 'Constant Speed'
        pumps.append({
            'name': pump.Name,
            'type': pump_type,
            'power': getattr(pump, 'Rated_Power_Consumption', 'Autosized'),
            'flow': getattr(pump, 'Rated_Flow_Rate', 'Autosized')
        })

    return pumps

def extract_fluid_coolers(idf):
    """Extract fluid coolers/cooling towers"""
    fluid_coolers = idf.idfobjects.get('EVAPORATIVEFLUIDCOOLER:TWOSPEED', [])

    equipment = []
    for fc in fluid_coolers:
        equipment.append({
            'name': fc.Name,
            'type': 'Two-Speed Evaporative Fluid Cooler',
            'fan_control': 'Two-Speed'
        })

    return equipment

def extract_erv(idf):
    """Extract energy recovery ventilators"""
    erv_sensible = idf.idfobjects.get('HEATEXCHANGER:AIRTOAIR:SENSIBLEANDLATENT', [])

    equipment = []
    for erv in erv_sensible:
        equipment.append({
            'name': erv.Name,
            'type': 'Air-to-Air Heat Exchanger',
            'config': 'Rotary' if 'Rotary' in erv.Name or 'Wheel' in erv.Name else 'Plate'
        })

    return equipment

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_equipment_for_report.py <path_to_model.idf>")
        sys.exit(1)

    idf_path = sys.argv[1]

    if not os.path.exists(idf_path):
        print(f"[ERROR] IDF file not found: {idf_path}")
        sys.exit(1)

    # Find and load IDD
    idd_path = find_idd()
    if not idd_path:
        print("[ERROR] Could not find Energy+.idd file")
        sys.exit(1)

    print("=" * 80)
    print("IDAP EQUIPMENT EXTRACTION")
    print("=" * 80)
    print(f"IDF: {idf_path}")
    print(f"IDD: {idd_path}\n")

    # Load IDF
    try:
        IDF.setiddname(idd_path)
        idf = IDF(idf_path)
    except Exception as e:
        print(f"[ERROR] Failed to load IDF: {e}")
        sys.exit(1)

    print("Extracting equipment...")

    # Extract all equipment
    airloops = extract_airloops(idf)
    boilers = extract_boilers(idf)
    heat_pumps = extract_heat_pumps(idf)
    pumps = extract_pumps(idf)
    fluid_coolers = extract_fluid_coolers(idf)
    ervs = extract_erv(idf)

    # Generate markdown report
    output_path = os.path.join(os.path.dirname(idf_path), "Equipment_List.md")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# SECC HVAC Equipment List\n")
        f.write("## Package C: Ground Source Heat Pump System\n\n")
        f.write("**Extracted from:** " + os.path.basename(idf_path) + "\n\n")
        f.write("---\n\n")

        # Air Systems
        f.write("## Air Systems\n\n")
        f.write(f"**Total Air Loops:** {len(airloops)}\n\n")

        for i, system in enumerate(airloops, 1):
            f.write(f"### {i}. {system['name']}\n\n")
            f.write(f"- **Type:** {system['type']}\n")
            f.write(f"- **Configuration:** Water-to-air heat pump with energy recovery\n")
            f.write(f"- **Distribution:** VAV with local zone equipment\n\n")

        # Central Plant Equipment
        f.write("## Central Plant Equipment\n\n")

        # Fluid Coolers
        if fluid_coolers:
            f.write("### Evaporative Fluid Cooler\n\n")
            for fc in fluid_coolers:
                f.write(f"- **Name:** {fc['name']}\n")
                f.write(f"- **Type:** {fc['type']}\n")
                f.write(f"- **Fan Control:** {fc['fan_control']}\n\n")

        # Boilers
        if boilers:
            f.write("### Condensing Hot Water Boilers\n\n")
            f.write(f"**Total Boilers:** {len(boilers)}\n\n")
            for i, boiler in enumerate(boilers, 1):
                f.write(f"{i}. **{boiler['name']}**\n")
                f.write(f"   - Fuel Type: {boiler['fuel']}\n")
                f.write(f"   - Efficiency: {boiler['efficiency']}\n\n")

        # Heat Pumps
        if heat_pumps:
            f.write("## Water-to-Air Heat Pump Components\n\n")
            f.write(f"**Cooling Coils:** {len(heat_pumps['cooling'])}\n\n")
            f.write(f"**Heating Coils:** {len(heat_pumps['heating'])}\n\n")

        # Energy Recovery
        if ervs:
            f.write("## Energy Recovery Ventilation\n\n")
            f.write(f"**Total ERV Units:** {len(ervs)}\n\n")
            for erv in ervs:
                f.write(f"- **{erv['name']}**\n")
                f.write(f"  - Type: {erv['type']}\n")
                f.write(f"  - Configuration: {erv['config']}\n\n")

        # Pumps
        if pumps:
            f.write("## Pumps\n\n")
            f.write(f"**Total Pumps:** {len(pumps)}\n\n")
            f.write("| Pump Name | Type | Power | Flow |\n")
            f.write("|-----------|------|------:|------:|\n")
            for pump in pumps:
                power = str(pump['power'])
                flow = str(pump['flow'])
                f.write(f"| {pump['name']} | {pump['type']} | {power} | {flow} |\n")

    print(f"\n[OK] Equipment list generated: {output_path}\n")
    print("Summary:")
    print(f"  Air Systems: {len(airloops)}")
    print(f"  Boilers: {len(boilers)}")
    print(f"  WSHP Cooling Coils: {len(heat_pumps['cooling'])}")
    print(f"  WSHP Heating Coils: {len(heat_pumps['heating'])}")
    print(f"  Fluid Coolers: {len(fluid_coolers)}")
    print(f"  ERV Units: {len(ervs)}")
    print(f"  Pumps: {len(pumps)}")

if __name__ == "__main__":
    main()
