#!/usr/bin/env python3
"""
IDAP Metrics Extractor - Generate Report TODAY
Extracts all key IDAP metrics from EnergyPlus HTML and SQL output
"""

import sys
import os
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

def extract_html_table(soup, table_name):
    """Extract a specific table from HTML output"""
    rows = []

    # Find the table by name
    for b_tag in soup.find_all('b'):
        if table_name.lower() in b_tag.text.lower():
            # Find the next table element
            table = b_tag.find_next('table')
            if table:
                for tr in table.find_all('tr'):
                    cells = [td.text.strip() for td in tr.find_all('td')]
                    if cells:
                        rows.append(cells)
            break

    return rows

def parse_value(value_str):
    """Parse numeric value from string"""
    try:
        # Remove commas and convert to float
        clean = value_str.replace(',', '').strip()
        return float(clean)
    except (ValueError, AttributeError):
        return 0.0

def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_idap_metrics.py <path_to_eplustbl.htm> [path_to_eplusout.sql]")
        sys.exit(1)

    htm_path = sys.argv[1]
    sql_path = sys.argv[2] if len(sys.argv) > 2 else htm_path.replace('eplustbl.htm', 'eplusout.sql')

    if not os.path.exists(htm_path):
        print(f"[ERROR] HTML file not found: {htm_path}")
        sys.exit(1)

    print("=" * 80)
    print("IDAP METRICS EXTRACTION")
    print("=" * 80)
    print(f"HTML: {htm_path}")
    print(f"SQL:  {sql_path}\n")

    # Load HTML
    with open(htm_path, 'r', encoding='latin-1') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Extract key tables
    print("Extracting data from HTML tables...")

    site_source = extract_html_table(soup, "Site and Source Energy")
    end_uses = extract_html_table(soup, "End Uses")
    building_area = extract_html_table(soup, "Building Area")

    # Parse results
    metrics = {}

    # Building area
    for row in building_area:
        if len(row) >= 2:
            if 'Total Building Area' in row[0]:
                metrics['building_area_total_sf'] = parse_value(row[1])
            elif 'Conditioned' in row[0] and 'Building Area' in row[0]:
                metrics['building_area_conditioned_sf'] = parse_value(row[1])

    # Site and Source Energy
    for row in site_source:
        if len(row) >= 3:
            metric = row[0].strip()
            if 'Total Site Energy' in metric:
                metrics['total_site_energy_mbtu'] = parse_value(row[1])
            elif 'Net Site Energy' in metric:
                metrics['net_site_energy_mbtu'] = parse_value(row[1])
            elif 'Total Source Energy' in metric:
                metrics['total_source_energy_mbtu'] = parse_value(row[1])
            elif 'Net Source Energy' in metric:
                metrics['net_source_energy_mbtu'] = parse_value(row[1])

    # End Uses by fuel
    electricity_mbtu = 0.0
    natural_gas_mbtu = 0.0

    enduse_breakdown = {}

    for row in end_uses:
        if len(row) >= 3:
            enduse = row[0].strip()
            if enduse and enduse != 'Total End Uses':
                electricity = parse_value(row[1]) if len(row) > 1 else 0
                gas = parse_value(row[2]) if len(row) > 2 else 0

                electricity_mbtu += electricity
                natural_gas_mbtu += gas

                if electricity > 0 or gas > 0:
                    enduse_breakdown[enduse] = {
                        'electricity_mbtu': electricity,
                        'natural_gas_mbtu': gas
                    }

    metrics['electricity_total_mbtu'] = electricity_mbtu
    metrics['natural_gas_total_mbtu'] = natural_gas_mbtu

    # Calculate EUI
    if metrics.get('building_area_total_sf', 0) > 0:
        metrics['site_eui_kbtu_sf'] = (metrics.get('total_site_energy_mbtu', 0) * 1000) / metrics['building_area_total_sf']

    # Get equipment sizing from SQL
    if os.path.exists(sql_path):
        print("Extracting equipment sizing from SQL...")
        conn = sqlite3.connect(sql_path)
        cursor = conn.cursor()

        # Get peak cooling
        cursor.execute("""
            SELECT Value, Units FROM ComponentSizes
            WHERE Description LIKE '%Design%Cooling%Capacity%'
               OR Description LIKE '%Design%Cooling%Load%'
            ORDER BY CAST(Value AS REAL) DESC
            LIMIT 1
        """)
        peak_cooling = cursor.fetchone()
        if peak_cooling:
            metrics['peak_cooling_load_tons'] = parse_value(str(peak_cooling[0]))
            if 'W' in str(peak_cooling[1]):  # Convert W to tons
                metrics['peak_cooling_load_tons'] = metrics['peak_cooling_load_tons'] / 12000 * 3.412

        # Get peak heating
        cursor.execute("""
            SELECT Value, Units FROM ComponentSizes
            WHERE Description LIKE '%Design%Heating%Capacity%'
               OR Description LIKE '%Design%Heating%Load%'
            ORDER BY CAST(Value AS REAL) DESC
            LIMIT 1
        """)
        peak_heating = cursor.fetchone()
        if peak_heating:
            metrics['peak_heating_load_kbtuh'] = parse_value(str(peak_heating[0]))
            if 'W' in str(peak_heating[1]):  # Convert W to kBtu/h
                metrics['peak_heating_load_kbtuh'] = metrics['peak_heating_load_kbtuh'] / 1000 * 3.412

        conn.close()

    # Generate Report
    output_path = os.path.join(os.path.dirname(htm_path), "IDAP_Metrics_Report.md")

    with open(output_path, 'w') as f:
        f.write("# IDAP Metrics Extraction Report\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"**Source:** {os.path.basename(htm_path)}\n\n")
        f.write("---\n\n")

        # Building Information
        f.write("## Building Information\n\n")
        f.write("| Metric | Value | Units |\n")
        f.write("|--------|-------:|-------|\n")
        f.write(f"| Total Building Area | {metrics.get('building_area_total_sf', 0):,.0f} | SF |\n")
        f.write(f"| Conditioned Building Area | {metrics.get('building_area_conditioned_sf', 0):,.0f} | SF |\n")
        f.write("\n")

        # Annual Energy Summary
        f.write("## Annual Energy Summary\n\n")
        f.write("| Metric | Value | Units |\n")
        f.write("|--------|-------:|-------|\n")
        f.write(f"| Total Site Energy | {metrics.get('total_site_energy_mbtu', 0):,.1f} | MBtu |\n")
        f.write(f"| Site EUI | {metrics.get('site_eui_kbtu_sf', 0):.1f} | kBtu/SF-yr |\n")
        f.write(f"| Electricity | {metrics.get('electricity_total_mbtu', 0):,.1f} | MBtu |\n")
        f.write(f"| Natural Gas | {metrics.get('natural_gas_total_mbtu', 0):,.1f} | MBtu |\n")
        f.write("\n")

        # Convert to kWh and therms
        elec_kwh = metrics.get('electricity_total_mbtu', 0) * 293.071
        gas_therms = metrics.get('natural_gas_total_mbtu', 0) * 10

        f.write("### Energy in Common Units\n\n")
        f.write("| Fuel | Value | Units |\n")
        f.write("|------|-------:|-------|\n")
        f.write(f"| Electricity | {elec_kwh:,.0f} | kWh |\n")
        f.write(f"| Natural Gas | {gas_therms:,.0f} | Therms |\n")
        f.write("\n")

        # End Use Breakdown
        f.write("## End Use Breakdown\n\n")
        f.write("| End Use | Electricity (MBtu) | Natural Gas (MBtu) | Total (MBtu) |\n")
        f.write("|---------|-------------------:|-------------------:|-------------:|\n")

        for enduse, values in sorted(enduse_breakdown.items()):
            elec = values['electricity_mbtu']
            gas = values['natural_gas_mbtu']
            total = elec + gas
            f.write(f"| {enduse} | {elec:,.1f} | {gas:,.1f} | {total:,.1f} |\n")

        f.write(f"| **TOTAL** | **{electricity_mbtu:,.1f}** | **{natural_gas_mbtu:,.1f}** | **{electricity_mbtu + natural_gas_mbtu:,.1f}** |\n")
        f.write("\n")

        # Peak Loads
        f.write("## Peak Design Loads\n\n")
        f.write("| Load Type | Value | Units |\n")
        f.write("|-----------|-------:|-------|\n")
        f.write(f"| Peak Cooling Load | {metrics.get('peak_cooling_load_tons', 0):,.0f} | Tons |\n")
        f.write(f"| Peak Heating Load | {metrics.get('peak_heating_load_kbtuh', 0):,.0f} | kBtu/h |\n")
        f.write("\n")

        # IDAP Calculations Placeholder
        f.write("## IDAP Calculations (Manual Input Required)\n\n")
        f.write("### Utility Costs\n\n")
        f.write("**Electricity Rate:** $0.131/kWh (blended)\n\n")
        f.write("**Natural Gas Rate:** $0.4466/dekatherm\n\n")
        f.write("| Fuel | Annual Use | Rate | Annual Cost |\n")
        f.write("|------|-------:|-------:|-------:|\n")

        elec_cost = elec_kwh * 0.131
        gas_cost = gas_therms * 0.4466 / 10

        f.write(f"| Electricity | {elec_kwh:,.0f} kWh | $0.131/kWh | ${elec_cost:,.2f} |\n")
        f.write(f"| Natural Gas | {gas_therms:,.0f} Therms | $0.4466/dth | ${gas_cost:,.2f} |\n")
        f.write(f"| **TOTAL** |  |  | **${elec_cost + gas_cost:,.2f}** |\n")
        f.write("\n")

        f.write("### Key IDAP Metrics (TO BE CALCULATED)\n\n")
        f.write("- **PBPm (Proposed Building Performance):** ${:,.2f}/yr\n".format(elec_cost + gas_cost))
        f.write("- **PBREC (Proposed Regulated Energy Cost):** TBD - requires regulated/unregulated classification\n")
        f.write("- **BBPCode (Baseline Building Performance):** TBD - requires baseline model\n")
        f.write("- **Percent Below Code:** TBD - requires baseline comparison\n")
        f.write("- **Construction Incentive:** TBD - 2 × (BBPCode - PBPm)\n")
        f.write("\n")

        f.write("---\n\n")
        f.write("**Next Steps:**\n")
        f.write("1. Classify end uses as regulated vs. unregulated\n")
        f.write("2. Run baseline model to get BBPCode and BBREC\n")
        f.write("3. Calculate all IDAP incentives\n")
        f.write("4. Extract equipment lists from IDF\n")
        f.write("5. Generate final IDAP SD report\n")

    print(f"\n[OK] Report generated: {output_path}\n")
    print("Key Metrics:")
    print(f"  Building Area: {metrics.get('building_area_total_sf', 0):,.0f} SF")
    print(f"  Site EUI: {metrics.get('site_eui_kbtu_sf', 0):.1f} kBtu/SF-yr")
    print(f"  Electricity: {elec_kwh:,.0f} kWh (${elec_cost:,.0f}/yr)")
    print(f"  Natural Gas: {gas_therms:,.0f} Therms (${gas_cost:,.0f}/yr)")
    print(f"  Total Annual Cost: ${elec_cost + gas_cost:,.0f}/yr")
    print(f"  Peak Cooling: {metrics.get('peak_cooling_load_tons', 0):,.0f} tons")
    print(f"  Peak Heating: {metrics.get('peak_heating_load_kbtuh', 0):,.0f} kBtu/h")

if __name__ == "__main__":
    main()
