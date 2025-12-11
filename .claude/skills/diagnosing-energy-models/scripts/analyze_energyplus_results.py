#!/usr/bin/env python3
"""
EnergyPlus Results Analysis Tool

Extracts, calculates, and structures key metrics from EnergyPlus simulation outputs.
Designed to distill E+ results for LLM interpretation and graphing tools.

Author: Matt Coalson
Created: 2025-11-20
Part of: diagnosing-energy-models skill

Usage:
    python analyze_energyplus_results.py --input-dir "path/to/run/" --units imperial --format json
    python analyze_energyplus_results.py --input-dir "path/to/run/" --units metric --format markdown --output summary.md
"""

import sqlite3
import json
import argparse
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass, asdict


@dataclass
class BuildingMetrics:
    """Container for all building energy metrics"""
    model_name: str
    location: str
    timestamp: str

    # Building areas
    total_area_m2: float
    conditioned_area_m2: float
    total_area_sf: float
    conditioned_area_sf: float

    # Site energy
    site_energy_GJ: float
    site_energy_kWh: float
    site_energy_kBtu: float
    site_energy_MBtu: float

    # EUI calculations
    eui_MJ_m2: float
    eui_kWh_m2: float
    eui_kBtu_sf: float

    # Source energy
    source_energy_GJ: float
    source_energy_kWh: float
    source_energy_kBtu: float
    source_energy_MBtu: float
    source_eui_MJ_m2: float
    source_eui_kWh_m2: float
    source_eui_kBtu_sf: float

    # End uses by category (in GJ)
    end_uses_by_category: Dict[str, float]

    # End uses by fuel type (in GJ)
    end_uses_by_fuel: Dict[str, float]

    # Percentages
    end_use_percentages: Dict[str, float]
    fuel_percentages: Dict[str, float]

    # Unmet hours
    unmet_hours_heating: float
    unmet_hours_cooling: float
    unmet_hours_occupied_heating: float
    unmet_hours_occupied_cooling: float

    # Peak demand
    peak_electric_demand_kW: Optional[float] = None

    # Utility costs (if available)
    total_utility_cost: Optional[float] = None
    utility_cost_by_fuel: Optional[Dict[str, float]] = None


class EnergyPlusResultsAnalyzer:
    """Analyzes EnergyPlus simulation results from multiple input formats"""

    # Unit conversion constants
    GJ_TO_KWH = 277.778
    GJ_TO_KBTU = 947.817
    M2_TO_SF = 10.7639
    MJ_M2_TO_KBTU_SF = 0.0881250

    def __init__(self, input_dir: Path, units: str = 'imperial'):
        """
        Initialize analyzer

        Args:
            input_dir: Path to OpenStudio/EnergyPlus run directory
            units: 'imperial' or 'metric' for output units
        """
        self.input_dir = Path(input_dir)
        self.units = units.lower()

        if self.units not in ['imperial', 'metric']:
            raise ValueError(f"Units must be 'imperial' or 'metric', got: {units}")

        # Detect available input files
        self.sql_path = self.input_dir / 'eplusout.sql'
        self.results_json_path = self.input_dir / 'results.json'
        self.html_path = self.input_dir / 'eplustbl.htm'

        # Check what's available
        self.has_sql = self.sql_path.exists()
        self.has_results_json = self.results_json_path.exists()
        self.has_html = self.html_path.exists()

        if not any([self.has_sql, self.has_results_json, self.has_html]):
            raise FileNotFoundError(
                f"No valid EnergyPlus output files found in {input_dir}\n"
                f"Looking for: eplusout.sql, results.json, or eplustbl.htm"
            )

    def analyze(self) -> BuildingMetrics:
        """
        Extract and analyze all metrics

        Returns:
            BuildingMetrics object with all calculated values
        """
        # Priority 1: Extract from SQL
        if self.has_sql:
            print(f"✓ Using eplusout.sql (Priority 1)", file=sys.stderr)
            metrics = self._extract_from_sql()

        # Priority 2: Supplement with results.json if available
        if self.has_results_json:
            print(f"✓ Supplementing with results.json (Priority 2)", file=sys.stderr)
            self._supplement_with_results_json(metrics)

        # Priority 3: Fallback to HTML (if SQL not available)
        elif self.has_html and not self.has_sql:
            print(f"⚠ Falling back to eplustbl.htm parsing (Priority 3)", file=sys.stderr)
            metrics = self._extract_from_html()

        return metrics

    def _extract_from_sql(self) -> BuildingMetrics:
        """Extract metrics from eplusout.sql database"""
        conn = sqlite3.connect(str(self.sql_path))
        cursor = conn.cursor()

        # Get model metadata
        model_name, location, timestamp = self._get_model_metadata(cursor)

        # Get building areas
        area_data = self._get_building_areas(cursor)

        # Get site and source energy
        site_source_data = self._get_site_source_energy(cursor)

        # Get end uses
        end_uses_by_category = self._get_end_uses_by_category(cursor)
        end_uses_by_fuel = self._get_end_uses_by_fuel(cursor)

        # Calculate percentages
        total_site_energy = site_source_data['site_energy_GJ']
        end_use_percentages = {k: (v / total_site_energy * 100) if total_site_energy > 0 else 0
                               for k, v in end_uses_by_category.items()}
        fuel_percentages = {k: (v / total_site_energy * 100) if total_site_energy > 0 else 0
                           for k, v in end_uses_by_fuel.items()}

        # Get unmet hours
        unmet_hours = self._get_unmet_hours(cursor)

        # Get peak demand
        peak_demand = self._get_peak_demand(cursor)

        conn.close()

        # Build metrics object
        metrics = BuildingMetrics(
            model_name=model_name,
            location=location,
            timestamp=timestamp,

            # Areas
            total_area_m2=area_data['total_m2'],
            conditioned_area_m2=area_data['conditioned_m2'],
            total_area_sf=area_data['total_m2'] * self.M2_TO_SF,
            conditioned_area_sf=area_data['conditioned_m2'] * self.M2_TO_SF,

            # Site energy
            site_energy_GJ=site_source_data['site_energy_GJ'],
            site_energy_kWh=site_source_data['site_energy_GJ'] * self.GJ_TO_KWH,
            site_energy_kBtu=site_source_data['site_energy_GJ'] * self.GJ_TO_KBTU,
            site_energy_MBtu=site_source_data['site_energy_GJ'] * self.GJ_TO_KBTU / 1000,

            # Site EUI
            eui_MJ_m2=site_source_data['site_eui_MJ_m2'],
            eui_kWh_m2=site_source_data['site_eui_MJ_m2'] / 3.6,
            eui_kBtu_sf=site_source_data['site_eui_MJ_m2'] * self.MJ_M2_TO_KBTU_SF,

            # Source energy
            source_energy_GJ=site_source_data['source_energy_GJ'],
            source_energy_kWh=site_source_data['source_energy_GJ'] * self.GJ_TO_KWH,
            source_energy_kBtu=site_source_data['source_energy_GJ'] * self.GJ_TO_KBTU,
            source_energy_MBtu=site_source_data['source_energy_GJ'] * self.GJ_TO_KBTU / 1000,

            # Source EUI
            source_eui_MJ_m2=site_source_data['source_eui_MJ_m2'],
            source_eui_kWh_m2=site_source_data['source_eui_MJ_m2'] / 3.6,
            source_eui_kBtu_sf=site_source_data['source_eui_MJ_m2'] * self.MJ_M2_TO_KBTU_SF,

            # End uses
            end_uses_by_category=end_uses_by_category,
            end_uses_by_fuel=end_uses_by_fuel,

            # Percentages
            end_use_percentages=end_use_percentages,
            fuel_percentages=fuel_percentages,

            # Unmet hours
            unmet_hours_heating=unmet_hours['heating'],
            unmet_hours_cooling=unmet_hours['cooling'],
            unmet_hours_occupied_heating=unmet_hours['occupied_heating'],
            unmet_hours_occupied_cooling=unmet_hours['occupied_cooling'],

            # Peak demand
            peak_electric_demand_kW=peak_demand
        )

        return metrics

    def _get_model_metadata(self, cursor: sqlite3.Cursor) -> Tuple[str, str, str]:
        """Extract model name, location, and timestamp"""
        # Get environment period info
        query = """
        SELECT EnvironmentName, EnvironmentType
        FROM EnvironmentPeriods
        WHERE EnvironmentType = 1
        LIMIT 1
        """
        result = cursor.execute(query).fetchone()

        if result:
            env_name = result[0]
            # Parse location from environment name (e.g., "RUN PERIOD 1 ** Fort Collins...")
            location = env_name.split('**')[1].strip() if '**' in env_name else 'Unknown'
        else:
            location = 'Unknown'

        # Get simulation timestamp from Simulations table
        query = "SELECT TimeStamp FROM Simulations LIMIT 1"
        result = cursor.execute(query).fetchone()
        timestamp = result[0] if result else 'Unknown'

        # Model name - try to get from building name, otherwise use default
        model_name = "Building 1"  # EnergyPlus default

        return model_name, location, timestamp

    def _get_building_areas(self, cursor: sqlite3.Cursor) -> Dict[str, float]:
        """Extract building areas from TabularData"""
        query = """
        SELECT s_row.Value as RowName, td.Value
        FROM TabularData td
        JOIN Strings s_report ON td.ReportNameIndex = s_report.StringIndex
        JOIN Strings s_table ON td.TableNameIndex = s_table.StringIndex
        JOIN Strings s_row ON td.RowNameIndex = s_row.StringIndex
        WHERE s_report.Value = 'AnnualBuildingUtilityPerformanceSummary'
        AND s_table.Value = 'Building Area'
        """

        results = cursor.execute(query).fetchall()

        area_data = {
            'total_m2': 0.0,
            'conditioned_m2': 0.0
        }

        for row_name, value in results:
            try:
                val = float(value)
                if 'Total Building Area' in row_name:
                    area_data['total_m2'] = val
                elif 'Net Conditioned Building Area' in row_name:
                    area_data['conditioned_m2'] = val
            except (ValueError, TypeError):
                continue

        return area_data

    def _get_site_source_energy(self, cursor: sqlite3.Cursor) -> Dict[str, float]:
        """Extract site and source energy from TabularData"""
        query = """
        SELECT s_row.Value as RowName, s_col.Value as ColumnName, td.Value
        FROM TabularData td
        JOIN Strings s_report ON td.ReportNameIndex = s_report.StringIndex
        JOIN Strings s_table ON td.TableNameIndex = s_table.StringIndex
        JOIN Strings s_row ON td.RowNameIndex = s_row.StringIndex
        JOIN Strings s_col ON td.ColumnNameIndex = s_col.StringIndex
        WHERE s_report.Value = 'AnnualBuildingUtilityPerformanceSummary'
        AND s_table.Value = 'Site and Source Energy'
        """

        results = cursor.execute(query).fetchall()

        energy_data = {
            'site_energy_GJ': 0.0,
            'site_eui_MJ_m2': 0.0,
            'source_energy_GJ': 0.0,
            'source_eui_MJ_m2': 0.0
        }

        for row_name, col_name, value in results:
            try:
                val = float(value)
                if 'Total Site Energy' in row_name and 'Total Energy' in col_name:
                    energy_data['site_energy_GJ'] = val
                elif 'Total Site Energy' in row_name and 'Energy Per Conditioned Building Area' in col_name:
                    energy_data['site_eui_MJ_m2'] = val
                elif 'Total Source Energy' in row_name and 'Total Energy' in col_name:
                    energy_data['source_energy_GJ'] = val
                elif 'Total Source Energy' in row_name and 'Energy Per Conditioned Building Area' in col_name:
                    energy_data['source_eui_MJ_m2'] = val
            except (ValueError, TypeError):
                continue

        return energy_data

    def _get_end_uses_by_category(self, cursor: sqlite3.Cursor) -> Dict[str, float]:
        """Extract end use breakdown by category"""
        query = """
        SELECT s_row.Value as Category, SUM(CAST(td.Value AS REAL)) as Total_GJ
        FROM TabularData td
        JOIN Strings s_report ON td.ReportNameIndex = s_report.StringIndex
        JOIN Strings s_table ON td.TableNameIndex = s_table.StringIndex
        JOIN Strings s_row ON td.RowNameIndex = s_row.StringIndex
        WHERE s_report.Value = 'AnnualBuildingUtilityPerformanceSummary'
        AND s_table.Value = 'End Uses'
        AND s_row.Value != 'Total End Uses'
        GROUP BY s_row.Value
        """

        results = cursor.execute(query).fetchall()

        end_uses = {}
        for category, total in results:
            if category and total:
                # Clean up category names
                clean_name = category.lower().replace(' ', '_')
                end_uses[clean_name] = float(total)

        return end_uses

    def _get_end_uses_by_fuel(self, cursor: sqlite3.Cursor) -> Dict[str, float]:
        """Extract end use breakdown by fuel type"""
        query = """
        SELECT s_col.Value as FuelType, CAST(td.Value AS REAL) as Value
        FROM TabularData td
        JOIN Strings s_report ON td.ReportNameIndex = s_report.StringIndex
        JOIN Strings s_table ON td.TableNameIndex = s_table.StringIndex
        JOIN Strings s_row ON td.RowNameIndex = s_row.StringIndex
        JOIN Strings s_col ON td.ColumnNameIndex = s_col.StringIndex
        WHERE s_report.Value = 'AnnualBuildingUtilityPerformanceSummary'
        AND s_table.Value = 'End Uses'
        AND s_row.Value = 'Total End Uses'
        """

        results = cursor.execute(query).fetchall()

        fuels = {}
        for fuel_type, value in results:
            if fuel_type and value:
                # Clean up fuel names
                clean_name = fuel_type.replace(' [GJ]', '').replace(' [m3]', '').lower().replace(' ', '_')
                if clean_name != 'water' and float(value) > 0:
                    fuels[clean_name] = float(value)

        return fuels

    def _get_unmet_hours(self, cursor: sqlite3.Cursor) -> Dict[str, float]:
        """Extract unmet hours from SystemSummary"""
        query = """
        SELECT s_col.Value as Metric, td.Value
        FROM TabularData td
        JOIN Strings s_report ON td.ReportNameIndex = s_report.StringIndex
        JOIN Strings s_row ON td.RowNameIndex = s_row.StringIndex
        JOIN Strings s_col ON td.ColumnNameIndex = s_col.StringIndex
        WHERE s_report.Value = 'SystemSummary'
        AND s_row.Value = 'Facility'
        """

        results = cursor.execute(query).fetchall()

        unmet_hours = {
            'heating': 0.0,
            'cooling': 0.0,
            'occupied_heating': 0.0,
            'occupied_cooling': 0.0
        }

        for metric, value in results:
            try:
                val = float(value)
                if 'During Heating' in metric:
                    unmet_hours['heating'] = val
                elif 'During Cooling' in metric:
                    unmet_hours['cooling'] = val
                elif 'During Occupied Heating' in metric:
                    unmet_hours['occupied_heating'] = val
                elif 'During Occupied Cooling' in metric:
                    unmet_hours['occupied_cooling'] = val
            except (ValueError, TypeError):
                continue

        return unmet_hours

    def _get_peak_demand(self, cursor: sqlite3.Cursor) -> Optional[float]:
        """Extract peak electric demand (if available)"""
        # Try to get from results that might include demand
        # This is a simplified version - actual implementation may need more sophisticated queries
        return None  # Will be populated from results.json if available

    def _supplement_with_results_json(self, metrics: BuildingMetrics) -> None:
        """Supplement metrics with data from results.json (if available)"""
        if not self.has_results_json:
            return

        try:
            with open(self.results_json_path, 'r') as f:
                results_data = json.load(f)

            # Get OpenStudio Results section
            os_results = results_data.get('OpenStudio Results', {})

            # Extract peak demand if available
            if 'annual_peak_electric_demand' in os_results:
                metrics.peak_electric_demand_kW = os_results['annual_peak_electric_demand']

            # Extract utility costs if available
            if 'annual_utility_cost' in os_results:
                metrics.total_utility_cost = os_results['annual_utility_cost']

        except Exception as e:
            print(f"⚠ Warning: Could not parse results.json: {e}", file=sys.stderr)

    def _extract_from_html(self) -> BuildingMetrics:
        """Extract metrics from eplustbl.htm (fallback method)"""
        # HTML parsing implementation - placeholder for now
        raise NotImplementedError(
            "HTML parsing not yet implemented. Please ensure eplusout.sql is available."
        )

    def format_output(self, metrics: BuildingMetrics, format_type: str) -> str:
        """
        Format metrics for output

        Args:
            metrics: BuildingMetrics object
            format_type: 'json' or 'markdown'

        Returns:
            Formatted string
        """
        if format_type == 'json':
            return self._format_json(metrics)
        elif format_type == 'markdown':
            return self._format_markdown(metrics)
        else:
            raise ValueError(f"Unknown format: {format_type}")

    def _format_json(self, metrics: BuildingMetrics) -> str:
        """Format as JSON"""
        data = asdict(metrics)

        # Convert units if imperial requested
        if self.units == 'imperial':
            data = self._convert_to_imperial_json(data)

        return json.dumps(data, indent=2)

    def _convert_to_imperial_json(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert metric values to imperial for JSON output"""
        # Keep both unit systems in JSON output for flexibility
        # Primary values reflect requested units, but include conversions

        imperial_data = data.copy()
        imperial_data['units'] = 'imperial'

        # Add imperial-preferred top-level metrics
        imperial_data['site_energy_primary'] = data['site_energy_MBtu']
        imperial_data['site_energy_primary_units'] = 'MBtu'
        imperial_data['eui_primary'] = data['eui_kBtu_sf']
        imperial_data['eui_primary_units'] = 'kBtu/sf/yr'
        imperial_data['area_primary'] = data['total_area_sf']
        imperial_data['area_primary_units'] = 'sf'

        # Convert end uses to MBtu
        for category, gj_value in data['end_uses_by_category'].items():
            imperial_data['end_uses_by_category'][category] = gj_value * self.GJ_TO_KBTU / 1000

        for fuel, gj_value in data['end_uses_by_fuel'].items():
            imperial_data['end_uses_by_fuel'][fuel] = gj_value * self.GJ_TO_KBTU / 1000

        return imperial_data

    def _format_markdown(self, metrics: BuildingMetrics) -> str:
        """Format as Markdown summary"""
        if self.units == 'imperial':
            return self._format_markdown_imperial(metrics)
        else:
            return self._format_markdown_metric(metrics)

    def _format_markdown_imperial(self, metrics: BuildingMetrics) -> str:
        """Format markdown in imperial units"""
        md = f"""# EnergyPlus Results Summary

**Model**: {metrics.model_name}
**Location**: {metrics.location}
**Timestamp**: {metrics.timestamp}
**Units**: Imperial

## Building Information
- **Total Area**: {metrics.total_area_sf:,.0f} sf
- **Conditioned Area**: {metrics.conditioned_area_sf:,.0f} sf

## Energy Performance
- **Site Energy**: {metrics.site_energy_MBtu:,.1f} MBtu ({metrics.site_energy_kWh:,.0f} kWh)
- **Site EUI**: {metrics.eui_kBtu_sf:.1f} kBtu/sf/yr
- **Source Energy**: {metrics.source_energy_MBtu:,.1f} MBtu
- **Source EUI**: {metrics.source_eui_kBtu_sf:.1f} kBtu/sf/yr

## End Uses by Category
"""
        for category, gj_value in sorted(metrics.end_uses_by_category.items(), key=lambda x: -x[1]):
            mbtu = gj_value * self.GJ_TO_KBTU / 1000
            pct = metrics.end_use_percentages.get(category, 0)
            md += f"- **{category.replace('_', ' ').title()}**: {mbtu:.1f} MBtu ({pct:.1f}%)\n"

        md += "\n## End Uses by Fuel Type\n"
        for fuel, gj_value in sorted(metrics.end_uses_by_fuel.items(), key=lambda x: -x[1]):
            mbtu = gj_value * self.GJ_TO_KBTU / 1000
            pct = metrics.fuel_percentages.get(fuel, 0)
            md += f"- **{fuel.replace('_', ' ').title()}**: {mbtu:.1f} MBtu ({pct:.1f}%)\n"

        md += f"""
## Unmet Hours
- **Heating**: {metrics.unmet_hours_heating:.1f} hours
- **Cooling**: {metrics.unmet_hours_cooling:.1f} hours
- **Occupied Heating**: {metrics.unmet_hours_occupied_heating:.1f} hours
- **Occupied Cooling**: {metrics.unmet_hours_occupied_cooling:.1f} hours
"""

        if metrics.peak_electric_demand_kW:
            md += f"\n## Peak Demand\n- **Electric**: {metrics.peak_electric_demand_kW:.1f} kW\n"

        if metrics.total_utility_cost:
            md += f"\n## Utility Costs\n- **Total Annual Cost**: ${metrics.total_utility_cost:,.2f}\n"

        return md

    def _format_markdown_metric(self, metrics: BuildingMetrics) -> str:
        """Format markdown in metric units"""
        md = f"""# EnergyPlus Results Summary

**Model**: {metrics.model_name}
**Location**: {metrics.location}
**Timestamp**: {metrics.timestamp}
**Units**: Metric

## Building Information
- **Total Area**: {metrics.total_area_m2:,.1f} m²
- **Conditioned Area**: {metrics.conditioned_area_m2:,.1f} m²

## Energy Performance
- **Site Energy**: {metrics.site_energy_GJ:,.1f} GJ ({metrics.site_energy_kWh:,.0f} kWh)
- **Site EUI**: {metrics.eui_MJ_m2:.1f} MJ/m²/yr ({metrics.eui_kWh_m2:.1f} kWh/m²/yr)
- **Source Energy**: {metrics.source_energy_GJ:,.1f} GJ
- **Source EUI**: {metrics.source_eui_MJ_m2:.1f} MJ/m²/yr

## End Uses by Category
"""
        for category, gj_value in sorted(metrics.end_uses_by_category.items(), key=lambda x: -x[1]):
            pct = metrics.end_use_percentages.get(category, 0)
            md += f"- **{category.replace('_', ' ').title()}**: {gj_value:.1f} GJ ({pct:.1f}%)\n"

        md += "\n## End Uses by Fuel Type\n"
        for fuel, gj_value in sorted(metrics.end_uses_by_fuel.items(), key=lambda x: -x[1]):
            pct = metrics.fuel_percentages.get(fuel, 0)
            md += f"- **{fuel.replace('_', ' ').title()}**: {gj_value:.1f} GJ ({pct:.1f}%)\n"

        md += f"""
## Unmet Hours
- **Heating**: {metrics.unmet_hours_heating:.1f} hours
- **Cooling**: {metrics.unmet_hours_cooling:.1f} hours
- **Occupied Heating**: {metrics.unmet_hours_occupied_heating:.1f} hours
- **Occupied Cooling**: {metrics.unmet_hours_occupied_cooling:.1f} hours
"""

        if metrics.peak_electric_demand_kW:
            md += f"\n## Peak Demand\n- **Electric**: {metrics.peak_electric_demand_kW:.1f} kW\n"

        if metrics.total_utility_cost:
            md += f"\n## Utility Costs\n- **Total Annual Cost**: ${metrics.total_utility_cost:,.2f}\n"

        return md


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Analyze EnergyPlus simulation results',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze_energyplus_results.py --input-dir ./run --units imperial --format json
  python analyze_energyplus_results.py --input-dir ./run --units metric --format markdown
  python analyze_energyplus_results.py --input-dir ./run --units imperial --format json --output results.json
        """
    )

    parser.add_argument(
        '--input-dir',
        type=str,
        required=True,
        help='Path to OpenStudio/EnergyPlus run directory'
    )

    parser.add_argument(
        '--units',
        type=str,
        choices=['imperial', 'metric'],
        default='imperial',
        help='Output units (default: imperial)'
    )

    parser.add_argument(
        '--format',
        type=str,
        choices=['json', 'markdown'],
        default='json',
        help='Output format (default: json)'
    )

    parser.add_argument(
        '--output',
        type=str,
        help='Output file path (default: stdout)'
    )

    args = parser.parse_args()

    try:
        # Create analyzer
        analyzer = EnergyPlusResultsAnalyzer(
            input_dir=args.input_dir,
            units=args.units
        )

        # Analyze results
        metrics = analyzer.analyze()

        # Format output
        output = analyzer.format_output(metrics, args.format)

        # Write output
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"✓ Results written to: {args.output}", file=sys.stderr)
        else:
            print(output)

        return 0

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
