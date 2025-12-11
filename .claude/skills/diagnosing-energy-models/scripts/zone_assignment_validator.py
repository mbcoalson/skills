#!/usr/bin/env python3
"""
Zone Assignment Validator

Compare thermal zone assignments in OpenStudio model against Engineer of Record
(EOR) specifications to identify discrepancies.

Usage:
    python zone_assignment_validator.py <osm_file> <eor_equipment_matrix.csv>

TODO: Implement zone validation logic
"""

import sys
import csv

def main():
    if len(sys.argv) < 3:
        print("Usage: python zone_assignment_validator.py <osm_file> <eor_equipment_matrix.csv>")
        sys.exit(1)

    osm_file = sys.argv[1]
    eor_matrix = sys.argv[2]

    print(f"Validating zone assignments:")
    print(f"  Model: {osm_file}")
    print(f"  EOR Spec: {eor_matrix}")
    print("TODO: Implement zone validation logic")

    # Future implementation:
    # 1. Parse OSM to extract:
    #    - All Space objects with names and thermal zone assignments
    #    - All ThermalZone objects
    #    - HVAC equipment assignments
    # 2. Parse EOR equipment matrix CSV:
    #    - Equipment ID | Type | Spaces Served | CFM | Cooling | Heating
    # 3. Create comparison matrix
    # 4. Flag discrepancies:
    #    - Spaces without thermal zones
    #    - Thermal zones not matching EOR specs
    #    - Equipment type mismatches
    # 5. Generate validation report with fix instructions

if __name__ == "__main__":
    main()
