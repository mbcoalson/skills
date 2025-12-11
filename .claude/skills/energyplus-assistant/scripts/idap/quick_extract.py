#!/usr/bin/env python3
"""
Quick IDAP Data Extraction - Get report metrics TODAY
Extracts key metrics from EnergyPlus SQL output for IDAP reporting
"""

import sqlite3
import sys
import os
from pathlib import Path

def get_annual_energy_by_fuel(sql_path):
    """Extract annual energy use by fuel type from SQL database"""
    conn = sqlite3.connect(sql_path)
    cursor = conn.cursor()

    # Get annual building utility performance summary
    query = """
    SELECT
        s1.Value as ReportName,
        s3.Value as TableName,
        s4.Value as RowName,
        s5.Value as ColumnName,
        s6.Value as Units,
        td.Value
    FROM TabularData td
    LEFT JOIN Strings s1 ON td.ReportNameIndex = s1.StringIndex
    LEFT JOIN Strings s3 ON td.TableNameIndex = s3.StringIndex
    LEFT JOIN Strings s4 ON td.RowNameIndex = s4.StringIndex
    LEFT JOIN Strings s5 ON td.ColumnNameIndex = s5.StringIndex
    LEFT JOIN Strings s6 ON td.UnitsIndex = s6.StringIndex
    WHERE s1.Value LIKE '%Annual Building%'
       OR s1.Value LIKE '%End Uses%'
    """

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return results

def get_end_use_summary(sql_path):
    """Extract end-use breakdown"""
    conn = sqlite3.connect(sql_path)
    cursor = conn.cursor()

    query = """
    SELECT
        s3.Value as TableName,
        s4.Value as EndUse,
        s5.Value as FuelType,
        td.Value
    FROM TabularData td
    LEFT JOIN Strings s1 ON td.ReportNameIndex = s1.StringIndex
    LEFT JOIN Strings s3 ON td.TableNameIndex = s3.StringIndex
    LEFT JOIN Strings s4 ON td.RowNameIndex = s4.StringIndex
    LEFT JOIN Strings s5 ON td.ColumnNameIndex = s5.StringIndex
    WHERE s1.Value LIKE '%Annual Building%'
      AND s3.Value = 'End Uses'
    ORDER BY s4.Value, s5.Value
    """

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return results

def get_component_sizes(sql_path):
    """Extract equipment sizing information"""
    conn = sqlite3.connect(sql_path)
    cursor = conn.cursor()

    query = """
    SELECT
        CompType,
        CompName,
        Description,
        Value,
        Units
    FROM ComponentSizes
    WHERE Description LIKE '%Design%'
       OR Description LIKE '%Capacity%'
       OR Description LIKE '%Load%'
    ORDER BY CompType, CompName
    """

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return results

def format_number(value_str):
    """Format numeric string with commas"""
    try:
        value = float(value_str)
        if value >= 1000:
            return f"{value:,.0f}"
        elif value >= 10:
            return f"{value:.1f}"
        else:
            return f"{value:.3f}"
    except (ValueError, TypeError):
        return value_str

def main():
    if len(sys.argv) < 2:
        print("Usage: python quick_extract.py <path_to_eplusout.sql>")
        sys.exit(1)

    sql_path = sys.argv[1]

    if not os.path.exists(sql_path):
        print(f"[ERROR] SQL file not found: {sql_path}")
        sys.exit(1)

    print("=" * 80)
    print("IDAP QUICK DATA EXTRACTION")
    print("=" * 80)
    print(f"SQL Database: {sql_path}\n")

    # Extract annual energy data
    print("Extracting annual energy data...")
    annual_data = get_annual_energy_by_fuel(sql_path)

    # Extract end-use data
    print("Extracting end-use breakdown...")
    enduse_data = get_end_use_summary(sql_path)

    # Extract sizing data
    print("Extracting equipment sizing...")
    sizing_data = get_component_sizes(sql_path)

    # Generate report
    output_path = os.path.join(os.path.dirname(sql_path), "IDAP_Quick_Extract.md")

    with open(output_path, 'w') as f:
        f.write("# IDAP Quick Data Extraction\n\n")
        f.write(f"**Source:** {sql_path}\n\n")
        f.write("---\n\n")

        # Annual Building Utility Performance
        f.write("## Annual Building Utility Performance\n\n")

        current_table = None
        for row in annual_data:
            report, table, rowname, colname, units, value = row

            if table != current_table:
                current_table = table
                f.write(f"\n### {table}\n\n")
                f.write("| Metric | Value | Units |\n")
                f.write("|--------|-------:|-------|\n")

            if value and value.strip():
                formatted_value = format_number(value)
                f.write(f"| {rowname} - {colname} | {formatted_value} | {units or ''} |\n")

        # End Uses
        f.write("\n## End Use Summary\n\n")
        f.write("| End Use | Fuel Type | Value |\n")
        f.write("|---------|-----------|-------:|\n")

        for row in enduse_data:
            table, enduse, fueltype, value = row
            if value and value.strip() and float(value) > 0:
                formatted_value = format_number(value)
                f.write(f"| {enduse} | {fueltype} | {formatted_value} |\n")

        # Equipment Sizing
        f.write("\n## Equipment Sizing\n\n")

        current_comp = None
        for row in sizing_data:
            comptype, compname, desc, value, units = row

            if comptype != current_comp:
                current_comp = comptype
                f.write(f"\n### {comptype}\n\n")
                f.write("| Component | Parameter | Value | Units |\n")
                f.write("|-----------|-----------|-------:|-------|\n")

            if value:
                formatted_value = format_number(str(value))
                f.write(f"| {compname} | {desc} | {formatted_value} | {units or ''} |\n")

    print(f"\n[OK] Report generated: {output_path}")
    print("\nKey sections extracted:")
    print(f"  - Annual energy data: {len(annual_data)} rows")
    print(f"  - End-use breakdown: {len(enduse_data)} rows")
    print(f"  - Equipment sizing: {len(sizing_data)} rows")

if __name__ == "__main__":
    main()
