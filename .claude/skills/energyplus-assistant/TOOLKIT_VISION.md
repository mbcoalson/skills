# EnergyPlus Python Toolkit - Vision & Goals

**Philosophy:** "Let tools handle syntax, let humans handle logic"

---

## The Problem

EnergyPlus IDF files are complex, error-prone, and difficult to edit manually:

- **Syntax errors** from manual editing break simulations
- **Field shifting** causes corrupt objects
- **Missing references** (schedules, materials, nodes) cause fatal errors
- **Forgotten outputs** require re-running 3+ minute simulations
- **Repetitive ECM testing** requires hours of manual file editing
- **Results extraction** from HTML tables is tedious

**Current state:** Hours of manual work, high error rate, slow iteration

---

## The Solution

A comprehensive Python toolkit built on `eppy` that:

1. **Validates** IDF files before simulation (catch errors in < 10 seconds)
2. **Repairs** corrupt objects automatically (no manual editing)
3. **Manipulates** HVAC systems reliably (syntax-correct every time)
4. **Automates** ECM testing (parametric studies in minutes)
5. **Extracts** results directly to deliverable format (markdown, CSV, Excel, JSON)

**Future state:** Minutes of automated work, zero syntax errors, fast iteration

---

## Core Design Principles

### 1. Tool-Based Philosophy
- **eppy handles syntax** - Guarantees valid IDF format
- **Scripts handle logic** - You define what to change
- **No manual editing** - Tools ensure consistency

### 2. Fast Feedback Loops
- Validation: < 10 seconds
- Simple repairs: < 30 seconds
- Complex modifications: < 2 minutes
- **Never waste 3 minutes on a simulation that will fail**

### 3. Safe by Default
- Never overwrite input files
- Always create new output files
- Verbose logging of changes
- Dry-run mode available
- Backup originals

### 4. Composable & Modular
- Each script does one thing well
- Chain scripts for workflows
- Output of one is input of another
- Example: validate → fix → add outputs → simulate → extract

### 5. Consistent Interface
- Same command-line patterns
- Same output formatting
- Same error handling
- Same reporting structure
- Easy to learn, easy to use

---

## Toolkit Structure

### Phase 1: Foundation (CRITICAL)
**Goal:** Never run a simulation that will fail

- ✅ `qaqc-direct.py` - Fast pre-simulation QA/QC
- ✅ `fix-equipment-lists.py` - Repair corrupt equipment lists
- ⏳ `validate-idf-structure.py` - Comprehensive field validation
- ⏳ `add-standard-outputs.py` - Inject output variables
- ⏳ `extract-results.py` - Parse results for deliverables

### Phase 2: Repair Tools
**Goal:** Fix common errors automatically

- `fix-node-connections.py` - Repair HVAC node issues
- `fix-schedules.py` - Create missing schedules
- `fix-surface-geometry.py` - Repair degenerate surfaces

### Phase 3: Equipment Manipulation
**Goal:** Reliable HVAC system modifications

- `add-ideal-loads.py` - Replace HVAC with ideal loads
- `clone-hvac-system.py` - Duplicate HVAC to new zones
- `swap-hvac-type.py` - Replace system type

### Phase 4: ECM Testing
**Goal:** Fast parametric studies

- `apply-ecm-lighting.py` - LPD reduction
- `apply-ecm-envelope.py` - Insulation/window improvements
- `apply-ecm-schedules.py` - Schedule modifications
- `run-parametric.py` - Orchestrate multi-run studies

### Phase 5: Utilities
**Goal:** Workflow support

- `compare-models.py` - Diff two IDF files
- `merge-idf-objects.py` - Copy objects between files
- `clean-unused-objects.py` - Remove orphaned objects

---

## Use Case Examples

### Example 1: Quick Model Validation
```bash
# Before running 3-minute simulation, validate in 10 seconds
python validate-idf-structure.py model.idf --report validation.md

# Fix any issues found
python fix-node-connections.py model.idf --output fixed.idf
python fix-schedules.py fixed.idf --output ready.idf

# Add outputs so you don't forget
python add-standard-outputs.py ready.idf --preset leed --output final.idf

# Now run simulation (confident it will work)
energyplus -w weather.epw final.idf
```

### Example 2: ECM Testing Workflow
```bash
# Start with validated baseline
python validate-idf-structure.py baseline.idf

# Generate ECM variants
python apply-ecm-lighting.py baseline.idf --reduction 0.20 --output ecm1_lighting.idf
python apply-ecm-envelope.py baseline.idf --wall-r-value 30 --output ecm2_envelope.idf
python apply-ecm-envelope.py ecm1_lighting.idf --wall-r-value 30 --output ecm3_combined.idf

# Add outputs to all
for file in baseline.idf ecm*.idf; do
  python add-standard-outputs.py $file --preset energy --output ${file%.idf}_out.idf
done

# Run simulations
for file in *_out.idf; do
  energyplus -w weather.epw $file
done

# Extract results
python extract-results.py baseline_out/eplustbl.htm ecm1_lighting_out/eplustbl.htm --compare --output comparison_lighting.md
python extract-results.py baseline_out/eplustbl.htm ecm2_envelope_out/eplustbl.htm --compare --output comparison_envelope.md
python extract-results.py baseline_out/eplustbl.htm ecm3_combined_out/eplustbl.htm --compare --output comparison_combined.md
```

### Example 3: Deliverable Generation
```bash
# Extract all key metrics for client deliverable
python extract-results.py output/eplustbl.htm \
  --metrics eui,ghg,cost,enduse \
  --format markdown \
  --carbon-elec 0.42 \
  --carbon-gas 0.18 \
  --output client_results.md

# Also generate CSV for spreadsheet
python extract-results.py output/eplustbl.htm \
  --metrics eui,ghg,cost \
  --format csv \
  --output client_results.csv

# Generate Excel with charts
python extract-results.py output/eplustbl.htm \
  --metrics all \
  --format excel \
  --output client_results.xlsx
```

### Example 4: Rapid HVAC Testing
```bash
# Test envelope ECM without HVAC complexity
python add-ideal-loads.py proposed.idf --output baseline_ideal.idf

# Apply envelope ECM
python apply-ecm-envelope.py baseline_ideal.idf --wall-r-value 30 --output ecm_ideal.idf

# Run and compare (fast because ideal loads is simple)
energyplus -w weather.epw baseline_ideal.idf
energyplus -w weather.epw ecm_ideal.idf

python extract-results.py baseline_ideal/eplustbl.htm ecm_ideal/eplustbl.htm --compare
```

---

## Long-Term Vision: Complete Automation

### Single-Command Workflow

```bash
python energyplus-workflow.py config.yaml
```

**config.yaml:**
```yaml
input: proposed_model.idf
weather: weather.epw

workflow:
  - validate:
      checks: [fields, references, nodes, geometry]

  - fix:
      - node-connections
      - schedules
      - equipment-lists

  - outputs:
      presets: [leed, energy]

  - ecms:
      - name: lighting_20
        type: lighting
        reduction: 0.20

      - name: envelope_r30
        type: envelope
        wall_r_value: 30
        window_u: 0.25

      - name: combined
        type: multiple
        apply: [lighting_20, envelope_r30]

  - simulate:
      parallel: true

  - extract:
      metrics: [eui, ghg, cost, enduse]
      formats: [markdown, csv, excel]
      compare: baseline

output:
  directory: results/
  report: final_report.md
```

**Result:** One command generates:
- Validated and fixed IDF files
- 3 ECM variants
- All simulation results
- Comparison reports
- Deliverable-ready metrics

**Time savings:** Hours → Minutes

---

## Success Metrics

### Current State (Manual)
- Model validation: Manual inspection (30-60 min)
- Error fixing: Trial and error (1-4 hours)
- ECM testing: Manual editing (30 min per ECM)
- Results extraction: Copy/paste from HTML (15 min)
- **Total time per model:** 3-6 hours
- **Error rate:** High (syntax errors common)

### Future State (Automated Toolkit)
- Model validation: < 10 seconds
- Error fixing: < 2 minutes (automated)
- ECM testing: < 1 minute per ECM
- Results extraction: < 5 seconds
- **Total time per model:** 10-15 minutes
- **Error rate:** Zero (eppy ensures valid syntax)

### ROI Calculation
- **Time savings:** 90-95% reduction
- **Quality improvement:** Zero syntax errors
- **Iteration speed:** 20x faster ECM testing
- **Deliverable quality:** Consistent, professional output

---

## Development Status

**Completed (2 scripts):**
- ✅ qaqc-direct.py
- ✅ fix-equipment-lists.py

**In Progress (3 scripts):**
- ⏳ validate-idf-structure.py
- ⏳ add-standard-outputs.py
- ⏳ extract-results.py

**Planned (12+ scripts):**
- See [DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md) for complete roadmap

**Next Milestone:** Complete Phase 1 (5 scripts) for SECC deliverable

---

## Getting Started

### Prerequisites
```bash
pip install eppy
pip install beautifulsoup4  # For extract-results.py
pip install pandas openpyxl  # Optional, for Excel output
```

### Quick Start
```bash
# 1. Validate model
python ~/.claude/skills/energyplus-assistant/scripts/qaqc-direct.py model.idf

# 2. Fix any issues
python ~/.claude/skills/energyplus-assistant/scripts/fix-equipment-lists.py model.idf fixed.idf

# 3. Add outputs
python ~/.claude/skills/energyplus-assistant/scripts/add-standard-outputs.py fixed.idf final.idf --preset leed

# 4. Run simulation
energyplus -w weather.epw final.idf

# 5. Extract results
python ~/.claude/skills/energyplus-assistant/scripts/extract-results.py output/eplustbl.htm --format markdown
```

### Documentation
- [SKILL.md](./SKILL.md) - Main skill reference
- [DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md) - Complete development roadmap
- [scripts/README.md](./scripts/README.md) - Script usage guide

---

## Contributing to Development

Each script in the development plan includes:
- Complete specification
- Command-line interface
- Algorithm description
- Implementation notes
- Example outputs

**Ready to build:** Pick any script from [DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md) and implement following the template provided.

**Testing:** Each script should include example IDF files and expected outputs in `examples/{script_name}/`

---

## Questions?

See the full documentation:
- [SKILL.md](./SKILL.md) - How to use the skill
- [DEVELOPMENT_PLAN.md](./DEVELOPMENT_PLAN.md) - How to build scripts
- [SKILL_OPTIMIZATION_ANALYSIS.md](./SKILL_OPTIMIZATION_ANALYSIS.md) - Lessons learned

---

**Vision:** Transform EnergyPlus modeling from tedious manual editing to fast, reliable, automated workflows.

**Mission:** Make energy modeling accessible, efficient, and error-free through intelligent tooling.

**Philosophy:** "Let tools handle syntax, let humans handle logic."
