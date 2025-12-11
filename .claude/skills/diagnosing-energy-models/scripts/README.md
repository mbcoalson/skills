# EnergyPlus Analysis Scripts

Python tools for analyzing OpenStudio and EnergyPlus simulation outputs.

## analyze_energyplus_results.py

**Purpose**: Extract and structure all metrics from EnergyPlus simulation outputs for LLM interpretation and graphing tools.

### Quick Start

```bash
# Imperial units (default), JSON output
python analyze_energyplus_results.py --input-dir "C:/path/to/run/" --units imperial --format json

# Metric units, Markdown summary
python analyze_energyplus_results.py --input-dir "C:/path/to/run/" --units metric --format markdown

# Save to file
python analyze_energyplus_results.py --input-dir "C:/path/to/run/" --units imperial --format json --output results.json
```

### Features

- **Auto-detects** available EnergyPlus outputs (SQL, JSON, HTML)
- **Priority system**: Uses `eplusout.sql` first (most complete), supplements with `results.json` if available, falls back to HTML
- **Unit conversion**: Switch between Imperial (kBtu/sf/yr) and Metric (MJ/m²/yr) units
- **Comprehensive metrics**: Site energy, source energy, EUI, end uses, unmet hours, peak demand
- **Multiple formats**: JSON (for programmatic use) or Markdown (for human readability)

### Input Files (Priority Order)

1. **eplusout.sql** - SQLite database (Primary - most complete)
2. **results.json** - OpenStudio Results measure output (Secondary - supplemental, optional)
3. **eplustbl.htm** - HTML table output (Fallback)

### Output Metrics

**Building Information:**
- Total and conditioned areas (m², sf)

**Energy Performance:**
- Site energy (GJ, kWh, kBtu, MBtu)
- Source energy (GJ, kWh, kBtu, MBtu)
- Site EUI (MJ/m², kWh/m², kBtu/sf/yr)
- Source EUI (MJ/m², kWh/m², kBtu/sf/yr)

**End Uses:**
- By category (Heating, Cooling, Lighting, Equipment, Fans, Pumps, etc.)
- By fuel type (Electricity, Natural Gas, District Heating/Cooling, etc.)
- Percentages of total energy

**Performance:**
- Unmet hours (heating, cooling, occupied heating, occupied cooling)
- Peak electric demand (kW)

**Costs (if available):**
- Total utility cost
- Cost by fuel type

### Output Formats

**JSON**: Structured data for downstream analysis
```json
{
  "model_name": "Building 1",
  "site_energy_MBtu": 5255.8,
  "eui_kBtu_sf": 58.5,
  "end_uses_by_category": {
    "heating": 2732.1,
    "cooling": 522.8,
    ...
  },
  "unmet_hours_heating": 29.0,
  ...
}
```

**Markdown**: Human-readable summary with tables
```markdown
# EnergyPlus Results Summary

**Site Energy**: 5,255.8 MBtu (1,540,318 kWh)
**Site EUI**: 58.5 kBtu/sf/yr

## End Uses by Category
- **Heating**: 2732.1 MBtu (52.0%)
- **Interior Equipment**: 1031.5 MBtu (19.6%)
...
```

### Command Line Options

```
--input-dir PATH     Path to OpenStudio/EnergyPlus run directory (required)
--units {imperial|metric}  Output units (default: imperial)
--format {json|markdown}   Output format (default: json)
--output PATH        Output file path (optional, defaults to stdout)
```

### Examples

```bash
# Analyze SECC model with Imperial units
python analyze_energyplus_results.py \
  --input-dir "C:/Projects/SECC/run/" \
  --units imperial \
  --format json \
  --output secc-results.json

# Generate Markdown summary in metric units
python analyze_energyplus_results.py \
  --input-dir "C:/Projects/SECC/run/" \
  --units metric \
  --format markdown \
  --output secc-summary.md

# Quick analysis to stdout
python analyze_energyplus_results.py --input-dir "./run/" --units imperial --format markdown
```

### Integration with Other Tools

**Designed for use with:**
- LLM interpretation (Claude, GPT, etc.)
- Graphing libraries (Plotly, D3.js, Chart.js)
- Future GHG emissions calculator
- Future utility cost calculator
- Reporting workflows

### Requirements

- Python 3.7+
- Standard library only (no external dependencies)

### Future Enhancements

- [ ] Parse additional tabular reports (Equipment Sizing, Monthly Energy, etc.)
- [ ] Support for model comparison (Proposed vs Baseline)
- [ ] HTML parsing implementation (current Priority 3 fallback not yet implemented)
- [ ] Extract timeseries data from SQLite for detailed analysis

### Author

Matt Coalson
Part of: diagnosing-energy-models skill
Created: 2025-11-20
