#!/usr/bin/env python3
"""
Model Comparison Report

Compare proposed vs baseline OpenStudio models for LEED documentation.
Generates detailed comparison of envelope, HVAC, lighting, and energy consumption.

Usage:
    python model_comparison_report.py <proposed.osm> <baseline.osm>

TODO: Implement model comparison logic
"""

import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: python model_comparison_report.py <proposed.osm> <baseline.osm>")
        sys.exit(1)

    proposed_model = sys.argv[1]
    baseline_model = sys.argv[2]

    print(f"Comparing models:")
    print(f"  Proposed: {proposed_model}")
    print(f"  Baseline: {baseline_model}")
    print("TODO: Implement model comparison logic")

    # Future implementation:
    # 1. Parse both OSM files
    # 2. Compare key parameters:
    #    - Building envelope (constructions, window-to-wall ratio)
    #    - HVAC systems (equipment types, efficiencies)
    #    - Lighting power densities
    #    - Service hot water
    # 3. Parse simulation results (if available)
    # 4. Calculate percent savings
    # 5. Generate comparison report for LEED documentation

if __name__ == "__main__":
    main()
