#!/usr/bin/env python3
"""
Analyze OpenStudio model (.osm) to find construction sets and constructions.
Direct text parsing - no OpenStudio SDK required.
"""

import sys
import re
from collections import defaultdict

def parse_osm_file(osm_path):
    """Parse OSM file and extract construction-related objects."""

    with open(osm_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into objects
    # OSM format: OS:ObjectType, fields...;
    objects = re.findall(r'OS:[^,]+,[^;]+;', content, re.DOTALL)

    results = {
        'construction_sets': [],
        'constructions': [],
        'schedules': []
    }

    for obj in objects:
        lines = obj.strip().split('\n')
        if not lines:
            continue

        obj_type = lines[0].strip().rstrip(',')

        # Extract object name (usually second line after handle)
        name = None
        if len(lines) > 2:
            # Look for name field (typically after handle)
            for line in lines[1:]:
                line = line.strip()
                if line and not line.startswith('{') and '!' in line:
                    # Extract value before comment
                    value = line.split('!')[0].strip().rstrip(',')
                    if value and value != '':
                        name = value
                        break

        # Categorize by object type
        if 'DefaultConstructionSet' in obj_type:
            results['construction_sets'].append({
                'type': obj_type,
                'name': name,
                'raw': obj
            })
        elif 'Construction' in obj_type and 'Set' not in obj_type:
            results['constructions'].append({
                'type': obj_type,
                'name': name
            })
        elif 'Schedule' in obj_type:
            results['schedules'].append({
                'type': obj_type,
                'name': name
            })

    return results

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze-osm-constructions.py <model.osm>")
        sys.exit(1)

    osm_path = sys.argv[1]

    print(f"\n=== Analyzing OSM File: {osm_path} ===\n")

    results = parse_osm_file(osm_path)

    # Construction Sets
    print(f"=== CONSTRUCTION SETS ({len(results['construction_sets'])}) ===")
    ashrae_2022_sets = []
    for cs in results['construction_sets']:
        name = cs['name']
        if name:
            print(f"  {name}")
            if 'ASHRAE901-2022' in name or '90.1-2022' in name:
                ashrae_2022_sets.append(name)

    print(f"\n=== ASHRAE 90.1-2022 CONSTRUCTION SETS ({len(ashrae_2022_sets)}) ===")
    for name in ashrae_2022_sets:
        print(f"  ✓ {name}")

    # Constructions
    print(f"\n=== CONSTRUCTIONS ({len(results['constructions'])}) ===")
    ashrae_2022_constructions = []
    ashrae_901_constructions = []
    ashrae_189_constructions = []

    for c in results['constructions']:
        name = c['name']
        if not name:
            continue

        if 'ASHRAE901-2022' in name or '2022' in name:
            ashrae_2022_constructions.append(name)
        elif 'ASHRAE' in name and '90.1' in name:
            ashrae_901_constructions.append(name)
        elif 'ASHRAE' in name and '189.1' in name:
            ashrae_189_constructions.append(name)

    print(f"\n90.1-2022 Constructions: {len(ashrae_2022_constructions)}")
    if ashrae_2022_constructions:
        for name in sorted(ashrae_2022_constructions)[:20]:
            print(f"  - {name}")
        if len(ashrae_2022_constructions) > 20:
            print(f"  ... and {len(ashrae_2022_constructions) - 20} more")
    else:
        print("  ❌ NONE FOUND")

    print(f"\n90.1-2010 Constructions: {len(ashrae_901_constructions)}")
    print(f"189.1-2009 Constructions: {len(ashrae_189_constructions)}")

    # Schedules
    print(f"\n=== SCHEDULES ({len(results['schedules'])}) ===")
    ashrae_2022_schedules = [s['name'] for s in results['schedules']
                             if s['name'] and ('ASHRAE901-2022' in s['name'] or '2022' in s['name'])]

    print(f"90.1-2022 Schedules: {len(ashrae_2022_schedules)}")
    if ashrae_2022_schedules:
        for name in sorted(ashrae_2022_schedules)[:20]:
            print(f"  - {name}")
        if len(ashrae_2022_schedules) > 20:
            print(f"  ... and {len(ashrae_2022_schedules) - 20} more")

    # Summary
    print("\n=== SUMMARY ===")
    print(f"✓ Construction Sets: {len(results['construction_sets'])} total, {len(ashrae_2022_sets)} are 90.1-2022")
    print(f"✓ Constructions: {len(results['constructions'])} total, {len(ashrae_2022_constructions)} are 90.1-2022")
    print(f"✓ Schedules: {len(results['schedules'])} total, {len(ashrae_2022_schedules)} are 90.1-2022")

    if ashrae_2022_sets:
        print("\n✓ READY: Model has ASHRAE 90.1-2022 construction sets loaded")
    else:
        print("\n⚠ WARNING: No ASHRAE 90.1-2022 construction sets found in model")

if __name__ == '__main__':
    main()
