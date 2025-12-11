#!/usr/bin/env python3
"""
IDAP Metrics Calculator - Calculate all IDAP formulas
Classifies regulated/unregulated and calculates BBPCode, PBPm, incentives
"""

import sys

# IDAP Constants (Fort Collins Utilities)
BPF_CODE = 0.57  # ASHRAE 90.1-2019
BPF_IDAP = 0.513  # 10% below code
DESIGN_INCENTIVE_BASE = 5000  # $
DESIGN_INCENTIVE_PER_SF = 0.10  # $/SF
CONSTRUCTION_INCENTIVE_MULTIPLIER = 2

# Regulated end uses (count toward code compliance)
REGULATED_ENDUSES = [
    'Heating',
    'Cooling',
    'Fans',
    'Pumps',
    'Interior Lighting',
    'Heat Rejection',
    'Humidification',
    'Heat Recovery',
    'Water Systems'  # DHW
]

# Unregulated end uses (excluded from compliance)
UNREGULATED_ENDUSES = [
    'Exterior Lighting',
    'Interior Equipment',  # Plugs, IT, office equipment
    'Refrigeration',
    'Elevators',
    'Generators'
]

def classify_enduse(enduse_name):
    """Classify end use as regulated or unregulated"""
    for reg in REGULATED_ENDUSES:
        if reg.lower() in enduse_name.lower():
            return 'regulated'

    for unreg in UNREGULATED_ENDUSES:
        if unreg.lower() in enduse_name.lower():
            return 'unregulated'

    # Default to regulated if uncertain (conservative)
    print(f"[WARNING] Unknown end use '{enduse_name}' - defaulting to REGULATED")
    return 'regulated'

def calculate_idap_metrics(enduse_data, utility_rates, building_sf, is_baseline=False):
    """
    Calculate IDAP metrics from end-use data

    Args:
        enduse_data: dict of {enduse_name: {electricity_mbtu, natural_gas_mbtu}}
        utility_rates: dict with {electricity_$/kwh, natural_gas_$/dekatherm}
        building_sf: building square footage
        is_baseline: True if this is baseline model, False if proposed

    Returns:
        dict with all IDAP metrics
    """

    # Convert MBtu to common units and calculate costs
    regulated_elec_cost = 0.0
    regulated_gas_cost = 0.0
    unregulated_elec_cost = 0.0
    unregulated_gas_cost = 0.0

    regulated_enduses = []
    unregulated_enduses = []

    elec_rate = utility_rates['electricity_$/kwh']
    gas_rate = utility_rates['natural_gas_$/dekatherm']

    for enduse, values in enduse_data.items():
        elec_mbtu = values['electricity_mbtu']
        gas_mbtu = values['natural_gas_mbtu']

        # Convert to common units
        elec_kwh = elec_mbtu * 293.071  # MBtu to kWh
        gas_dekatherm = gas_mbtu * 10  # MBtu to dekatherms

        # Calculate costs
        elec_cost = elec_kwh * elec_rate
        gas_cost = gas_dekatherm * gas_rate

        # Classify
        classification = classify_enduse(enduse)

        if classification == 'regulated':
            regulated_elec_cost += elec_cost
            regulated_gas_cost += gas_cost
            regulated_enduses.append({
                'name': enduse,
                'electricity_kwh': elec_kwh,
                'natural_gas_dekatherm': gas_dekatherm,
                'electricity_cost': elec_cost,
                'natural_gas_cost': gas_cost,
                'total_cost': elec_cost + gas_cost
            })
        else:
            unregulated_elec_cost += elec_cost
            unregulated_gas_cost += gas_cost
            unregulated_enduses.append({
                'name': enduse,
                'electricity_kwh': elec_kwh,
                'natural_gas_dekatherm': gas_dekatherm,
                'electricity_cost': elec_cost,
                'natural_gas_cost': gas_cost,
                'total_cost': elec_cost + gas_cost
            })

    # IDAP Formulas
    BBREC_or_PBREC = regulated_elec_cost + regulated_gas_cost  # Regulated energy cost
    BBUEC = unregulated_elec_cost + unregulated_gas_cost  # Unregulated energy cost

    if is_baseline:
        # Baseline Building Performance (BBPCode)
        # BBPCode = BBUEC + (BPFCode × BBREC)
        BBPCode = BBUEC + (BPF_CODE * BBREC_or_PBREC)

        metrics = {
            'BBREC': BBREC_or_PBREC,
            'BBUEC': BBUEC,
            'BBPCode': BBPCode,
            'total_annual_cost': BBUEC + BBREC_or_PBREC,
            'regulated_cost': BBREC_or_PBREC,
            'unregulated_cost': BBUEC,
            'regulated_enduses': regulated_enduses,
            'unregulated_enduses': unregulated_enduses
        }
    else:
        # Proposed Building Performance
        PBREC = BBREC_or_PBREC  # Proposed regulated energy cost
        PBPm = BBUEC + PBREC  # Proposed building performance (modeled)

        # Proposed Building Performance Target
        # PBPt = BBUEC + (BPFIDAP × BBREC)
        # Note: BBREC here should come from baseline, but we'll calculate it for reference
        PBPt_estimate = BBUEC + (BPF_IDAP * PBREC)  # Estimate (needs actual baseline BBREC)

        metrics = {
            'PBREC': PBREC,
            'BBUEC': BBUEC,
            'PBPm': PBPm,
            'PBPt_estimate': PBPt_estimate,
            'total_annual_cost': PBPm,
            'regulated_cost': PBREC,
            'unregulated_cost': BBUEC,
            'regulated_enduses': regulated_enduses,
            'unregulated_enduses': unregulated_enduses
        }

    return metrics

def main():
    print("=" * 80)
    print("IDAP METRICS CALCULATOR")
    print("=" * 80)
    print()

    # Example data from SECC model
    enduse_data = {
        'Cooling': {'electricity_mbtu': 60.5, 'natural_gas_mbtu': 0.0},
        'Fans': {'electricity_mbtu': 416.6, 'natural_gas_mbtu': 0.0},
        'Heat Rejection': {'electricity_mbtu': 3.3, 'natural_gas_mbtu': 0.0},
        'Heating': {'electricity_mbtu': 736.1, 'natural_gas_mbtu': 3505.6},
        'Interior Equipment': {'electricity_mbtu': 1088.2, 'natural_gas_mbtu': 0.0},
        'Interior Lighting': {'electricity_mbtu': 1022.8, 'natural_gas_mbtu': 0.0},
        'Pumps': {'electricity_mbtu': 85.5, 'natural_gas_mbtu': 0.0},
    }

    utility_rates = {
        'electricity_$/kwh': 0.131,
        'natural_gas_$/dekatherm': 0.4466
    }

    building_sf = 8351

    # Calculate proposed metrics
    print("Calculating PROPOSED building metrics...\n")
    proposed = calculate_idap_metrics(enduse_data, utility_rates, building_sf, is_baseline=False)

    print("PROPOSED BUILDING PERFORMANCE")
    print("-" * 80)
    print(f"  PBPm (Total Annual Cost):        ${proposed['PBPm']:,.2f}/yr")
    print(f"  PBREC (Regulated Energy Cost):   ${proposed['PBREC']:,.2f}/yr")
    print(f"  BBUEC (Unregulated Energy Cost): ${proposed['BBUEC']:,.2f}/yr")
    print()

    print("REGULATED END USES:")
    for enduse in proposed['regulated_enduses']:
        print(f"  {enduse['name']:25s} ${enduse['total_cost']:>10,.2f}/yr")
    print(f"  {'TOTAL REGULATED':25s} ${proposed['regulated_cost']:>10,.2f}/yr")
    print()

    print("UNREGULATED END USES:")
    for enduse in proposed['unregulated_enduses']:
        print(f"  {enduse['name']:25s} ${enduse['total_cost']:>10,.2f}/yr")
    print(f"  {'TOTAL UNREGULATED':25s} ${proposed['unregulated_cost']:>10,.2f}/yr")
    print()

    # Calculate design incentive
    design_incentive = DESIGN_INCENTIVE_BASE + (DESIGN_INCENTIVE_PER_SF * building_sf)
    print("INCENTIVES")
    print("-" * 80)
    print(f"  Design Incentive:                ${design_incentive:,.2f}")
    print(f"    (Base: ${DESIGN_INCENTIVE_BASE:,.2f} + ${DESIGN_INCENTIVE_PER_SF:.2f}/SF × {building_sf:,.0f} SF)")
    print()
    print("  Construction Incentive:          TBD - requires baseline model")
    print("    Formula: 2 × (BBPCode - PBPm)")
    print("    Need baseline BBPCode to calculate")
    print()
    print("  Performance Incentive:           TBD - requires baseline model")
    print("    Formula: (BPFCode × BBREC) - Actual Regulated Cost")
    print("    Need baseline BBREC to calculate")
    print()

    # Show what we need from baseline
    print("WHAT'S NEEDED FROM BASELINE MODEL:")
    print("-" * 80)
    print("  1. BBREC (Baseline Regulated Energy Cost)")
    print("  2. BBPCode = BBUEC + (0.57 × BBREC)")
    print()
    print("  Then calculate:")
    print(f"  - PBPt = ${proposed['BBUEC']:,.2f} + (0.513 × BBREC)")
    print(f"  - Construction Incentive = 2 × (BBPCode - ${proposed['PBPm']:,.2f})")
    print(f"  - Performance Incentive = (0.57 × BBREC) - ${proposed['PBREC']:,.2f}")
    print(f"  - Percent Below Code = 1 - (${proposed['PBREC']:,.2f} / (0.57 × BBREC))")
    print()

if __name__ == "__main__":
    main()
