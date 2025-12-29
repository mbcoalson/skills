# validate-idf-structure.py Examples

## Test Case 1: Commercial Building Model Validation

**File:** Example commercial building model (provide path to your own IDF file)
`path/to/your/model.idf`

**Command:**
```bash
python validate-idf-structure.py model.idf --report validation_report.md
```

**Expected Results:**
```
================================================================================
VALIDATE IDF STRUCTURE
================================================================================

Input: model.idf
IDD Version: 25.1.0
IDF Version: 25.1

[INFO] Building object reference maps...

Running validation checks...

[INFO] Validating field types...
  [OK] Field type validation (IDF loaded successfully)

[INFO] Validating required fields...
  [OK] Required fields check

[INFO] Validating object references...
  [WARNING] Object reference validation (995 issues found)

[INFO] Validating node connections...
  [INFO] Found 172 inlet nodes and 167 outlet nodes
  [OK] Node connection validation

[INFO] Validating surface geometry...
  [OK] Surface geometry validation (295 surfaces checked)

================================================================================
VALIDATION SUMMARY
================================================================================
  Total Objects: 1,560
  Errors: 0
  Warnings: 995
  Info: 0

RECOMMENDATION: Review warnings - may cause simulation issues

See detailed report: validation_report.md
[OK] Report saved to validation_report.md
```

**Issues Found:**
- 995 warnings related to schedule references (schedules like "Always On" referenced but may use different naming)
- All surfaces validated successfully
- All node connections valid
- No critical errors found

**Usage:**
This test case demonstrates validation of a real-world commercial building model. The warnings are primarily schedule reference issues that don't prevent simulation from running successfully.

## Test Case 2: Specific Validation Categories

**Command:**
```bash
python validate-idf-structure.py model.idf --check fields,references
```

**Description:**
Validates only field types and object references, skipping node connections and geometry checks. Useful when you only need to check specific aspects of the model.

## Test Case 3: Severity Filtering

**Command:**
```bash
python validate-idf-structure.py model.idf --severity error
```

**Description:**
Only reports errors and fatals, filtering out warnings and info messages. Useful when you want to focus on critical issues that will prevent simulation from running.

## Test Case 4: Quiet Mode with Report

**Command:**
```bash
python validate-idf-structure.py model.idf --quiet --report validation.md
```

**Description:**
Suppresses all console output while still generating a detailed markdown report. Useful for automated workflows or CI/CD pipelines.

## Test Case 5: Error Handling

**Command:**
```bash
python validate-idf-structure.py nonexistent.idf
```

**Expected Result:**
```
[ERROR] Input file not found: nonexistent.idf
```

**Exit Code:** 3 (file not found)

**Description:**
Demonstrates graceful error handling when input file doesn't exist.

## Performance Benchmarks

**Example Commercial Building Model (1,560 objects, 295 surfaces):**
- Validation time: < 5 seconds
- IDF file size: ~1.2 MB
- Memory usage: < 100 MB

**Comparison to EnergyPlus Simulation:**
- Validation: < 10 seconds
- Full simulation: 3-5 minutes
- **Speedup: 18-30x faster for catching errors**

## Integration with Workflow

**Recommended workflow:**
```bash
# 1. Quick QA/QC
python qaqc-direct.py model.idf

# 2. Structural validation
python validate-idf-structure.py model.idf --report validation.md

# 3. Fix issues if found
# (use fix-* scripts as needed)

# 4. Run simulation
energyplus -w weather.epw -d output model.idf
```

## Tips

1. **Use --report for documentation:** Always generate markdown reports for project documentation
2. **Focus on errors first:** Use `--severity error` to see only critical issues
3. **Validate after every edit:** Run validation after manual IDF edits to catch issues early
4. **Automate in CI/CD:** Use `--quiet` mode in automated workflows

## Known Limitations

1. **Schedule references:** May report false positives for EnergyPlus built-in schedules (e.g., "Always On")
2. **IDD version:** Validation quality depends on IDD version - always use matching version
3. **Geometry complexity:** Advanced geometry checks (planarity, surface normal) not yet implemented
4. **Performance:** Large models (10,000+ objects) may take 15-20 seconds

## Troubleshooting

**Q: Getting too many schedule reference warnings?**
A: These are often false positives for built-in EnergyPlus schedules. Use `--severity error` to filter them out.

**Q: Validation passes but simulation fails?**
A: This tool checks structural issues, not physics/logic. EnergyPlus may still catch runtime issues like:
- Invalid physics (e.g., negative heat capacity)
- Convergence failures
- Unmet loads
- Node temperature out of bounds

**Q: How to fix issues found by validation?**
A: See related scripts:
- `fix-equipment-lists.py` - Fix ZoneHVAC equipment lists
- `fix-node-connections.py` - Fix HVAC node connections (coming soon)
- `fix-schedules.py` - Fix schedule references (coming soon)
