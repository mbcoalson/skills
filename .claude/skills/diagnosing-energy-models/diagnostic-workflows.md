# Diagnostic Workflows for Energy Models

Detailed step-by-step workflows for systematic OpenStudio and EnergyPlus model diagnostics. These workflows are designed to be efficient, comprehensive, and aligned with best practices.

**Key Principle**: Always validate recommendations against authoritative sources using [validation-sources.md](./validation-sources.md) before providing fixes.

---

## Workflow 1: Model Triage (5-10 minutes)

**When to Use**: Model fails to simulate, has severe warnings, or behavior is unexpected

**Goal**: Quickly identify the most critical blocking issues

### Step 1: Check Story Organization

```
1. List all Building Story objects:
   - OpenStudio → Spaces → Building Stories subtab
   - Note each story's name and Z-coordinate

2. Flag issues:
   - Multiple stories with identical Z-coordinates? → **CRITICAL: Pattern 1**
   - Number of stories doesn't match building? → **WARNING: Review needed**
   - Story names unclear (e.g., "Story 1", "Story 2")? → **MINOR: Rename for clarity**

3. Expected results:
   ✓ One story per physical floor level
   ✓ Z-coordinates increase with building height
   ✓ Story names descriptive (e.g., "Ground Floor", "Second Floor")
```

**Validation checkpoint**: If story issues found, check OpenStudio geometry documentation before recommending fixes.

### Step 2: Surface Validation

```
1. Count total surfaces:
   - OpenStudio → Surfaces tab
   - Note total count

2. Check for anomalies:
   - Surfaces with >1000 vertices? → **CRITICAL: Likely error**
   - Surfaces with 0 area? → **CRITICAL: Delete these**
   - Unmatched surfaces (red in 3D view)? → **WARNING: Run surface matching**

3. Run surface intersection test:
   - OpenStudio → Components & Measures
   - Look for "Intersect Space Geometry" measure (if available)
   - Or attempt simulation and check for intersection errors

4. Identify non-planar surfaces:
   - OpenStudio → Inspect → Surfaces → Filter warnings
   - Note surface names and locations
```

**Validation checkpoint**: Before recommending surface fixes, verify approach with OpenStudio geometry editor documentation.

### Step 3: Zone Assignment Check

```
1. List spaces without thermal zones:
   - OpenStudio → Spaces tab
   - Filter or scroll to find empty "Thermal Zone" column
   - Count unassigned spaces

2. Count thermal zones:
   - OpenStudio → Thermal Zones tab
   - Compare count to EOR equipment list (if available)
   - Flag discrepancies

3. Check for orphaned zones:
   - OpenStudio → Thermal Zones tab
   - Look for zones with 0 spaces assigned
   - Note these for potential deletion

4. Expected results:
   ✓ Every space has exactly one thermal zone
   ✓ Every zone has at least one space
   ✓ Zone count aligns with EOR equipment count
```

**Validation checkpoint**: Review OpenStudio thermal zone documentation if assignment issues found.

### Step 4: HVAC Topology Check

```
1. Verify plant loops (if water-based systems):
   - OpenStudio → HVAC Systems → Plant Loops
   - Check for heating hot water, chilled water loops as needed
   - Verify supply equipment exists (boilers, chillers)

2. Check air loop connections:
   - OpenStudio → HVAC Systems → Air Loops
   - Verify each air loop has:
     ✓ Supply fan
     ✓ Coils (if applicable)
     ✓ Connection to thermal zones

3. Confirm terminal assignments:
   - OpenStudio → Thermal Zones → HVAC Systems subtab
   - Each zone should have equipment or ideal loads
   - Verify terminal types match expected (VAV, CV, etc.)

4. Plant loop connections:
   - HVAC → Plant Loops → Connections tab
   - Verify coils connected to appropriate loops
   - Check for "not on any plant loop" components
```

**Validation checkpoint**: For HVAC issues, check both OpenStudio HVAC documentation AND Unmet Hours for validated solutions.

### Step 5: Attempt Simulation

```
1. Run simulation:
   - OpenStudio → Run Simulation
   - Wait for completion or failure

2. Parse errors (if simulation fails):
   - Open .err file (eplusout.err in run directory)
   - Identify top 5 most frequent errors
   - Categorize by type:
     - Severe: Simulation stops
     - Warning: Simulation continues but results suspect
     - Info: Informational only

3. Prioritize fixes:
   - Severe geometry errors → Fix first (blocking)
   - Missing connections → Fix second (blocking or data issues)
   - Schedule/input errors → Fix third
   - Warnings → Fix last (simulation runs)
```

### Triage Output Template

```
Model Triage Results for [Model Name]
Date: [Date]

CRITICAL ISSUES (must fix to simulate):
1. [Issue description]
   - Pattern: [Pattern number from common-error-patterns.md]
   - Recommended fix: [High-level approach]
   - Time estimate: [Hours]

WARNING ISSUES (simulation may run but results suspect):
1. [Issue description]
   ...

RECOMMENDED IMPROVEMENTS:
1. [Issue description]
   ...

NEXT STEPS:
1. [Prioritized action items]
```

---

## Workflow 2: Geometry Rebuild Decision (15-20 minutes)

**When to Use**: Considering whether to fix existing geometry or rebuild from scratch

**Goal**: Make data-driven decision on fix vs. rebuild approach

### Decision Criteria Matrix

| Factor | Fix Existing | Rebuild from Scratch |
|--------|--------------|----------------------|
| Intersecting surfaces | < 10 surfaces | > 10 surfaces |
| Story organization | Correct Z-coordinates | Multiple stories at Z=0 |
| Space assignments | Space types & zones assigned | Spaces poorly organized |
| Surface quality | Isolated issues | Systemic non-planar issues |
| HVAC systems | Well-defined | Missing or poorly structured |
| Schedules/constructions | Complete & reasonable | Missing or incorrect |

### Step 1: Quantify Issues

```
1. Count intersecting surfaces:
   - Run simulation, parse .err file
   - Search for "intersect" warnings
   - Tally unique surfaces

2. Assess story organization:
   - Count stories at same Z-coordinate
   - If >1 story at Z=0 → REBUILD indicator

3. Evaluate space organization:
   - Are spaces logically organized?
   - Do space names make sense?
   - Are space types assigned?

4. Check surface quality:
   - Count non-planar surfaces
   - If >20% of surfaces have issues → REBUILD indicator

5. Review HVAC completeness:
   - Do systems exist and appear correct?
   - Are systems connected properly?
   - If minimal or no HVAC → Neutral (rebuild doesn't lose much)
```

### Step 2: Assess Preservation Value

```
What would be lost in a rebuild?

HIGH VALUE (favor fixing):
- Complex HVAC systems properly configured
- Complete, validated schedules
- Custom constructions with specific properties
- Thermal zone assignments matching EOR specs
- Working simulation with reasonable results

LOW VALUE (favors rebuilding):
- Simple ideal loads systems
- Default schedules from templates
- Generic constructions
- Poor zone organization
- Never successfully simulated
```

### Step 3: Time Estimate Calculation

```
Fix approach time estimate:
- Simple fix (< 5 surfaces): 1-2 hours
- Medium fix (5-10 surfaces): 3-5 hours
- Complex fix (10-20 surfaces): 6-10 hours
- Very complex fix (>20 surfaces): 10-16 hours

Rebuild approach time estimate:
- Small building (< 20,000 sf, simple program): 4-8 hours
- Medium building (20,000-50,000 sf): 8-16 hours
- Large building (50,000-100,000 sf): 16-24 hours
- Very large/complex (>100,000 sf, complex HVAC): 24-40 hours

Factor in:
+ Time to extract/preserve schedules, constructions: +2-4 hours
+ Time to validate against EOR specs: +2-6 hours
+ Time to debug new issues: +20% of base estimate
```

### Step 4: Make Recommendation

```
IF (intersecting_surfaces > 10 OR multiple_stories_at_Z0):
    RECOMMEND: Rebuild from scratch
    REASON: Systemic geometry issues, fix time > rebuild time

ELIF (space_types_assigned AND hvac_well_defined AND intersecting_surfaces < 5):
    RECOMMEND: Fix existing geometry
    REASON: High preservation value, low fix complexity

ELIF (no_hvac OR simple_ideal_loads):
    RECOMMEND: Rebuild from scratch
    REASON: Low preservation value, fresh start ensures quality

ELSE:
    RECOMMEND: Hybrid approach
    REASON: Extract valuable components, rebuild geometry, reapply
    STEPS:
        1. Export schedules to CSV or library
        2. Document construction assemblies
        3. Document HVAC systems (screenshots + notes)
        4. Rebuild geometry with clean workflow
        5. Re-import schedules, constructions
        6. Recreate HVAC using documentation
```

### Decision Output Template

```
Geometry Rebuild Decision for [Model Name]
Date: [Date]

ISSUE SUMMARY:
- Intersecting surfaces: [Count]
- Story organization: [Status]
- Surface quality: [Percentage with issues]
- HVAC completeness: [Assessment]

PRESERVATION VALUE:
- Schedules: [High/Medium/Low] - [Brief reason]
- Constructions: [High/Medium/Low] - [Brief reason]
- HVAC systems: [High/Medium/Low] - [Brief reason]
- Zone assignments: [High/Medium/Low] - [Brief reason]

TIME ESTIMATES:
- Fix approach: [Hours] hours
- Rebuild approach: [Hours] hours

RECOMMENDATION: [Fix / Rebuild / Hybrid]

REASONING:
[2-3 sentences explaining the decision]

NEXT STEPS:
1. [Specific action item]
2. [Specific action item]
...
```

---

## Workflow 3: EOR Specification Mapping (30-45 minutes)

**When to Use**: Starting new model or validating thermal zone assignments against mechanical engineer's specifications

**Goal**: Create validated mapping between building spaces and EOR equipment

### Step 1: Gather Documents

```
Required documents:
□ EOR mechanical drawings (equipment schedules)
□ Architectural floor plans (space layouts with room numbers/names)
□ Basis of design narrative (system descriptions)
□ HVAC sequence of operations (if available)
□ Design load calculations (if available)

Organize in project folder:
project/
├── drawings/
│   ├── mechanical/
│   │   ├── equipment-schedule.pdf
│   │   └── hvac-plans.pdf
│   └── architectural/
│       └── floor-plans.pdf
└── specifications/
    └── basis-of-design.pdf
```

### Step 2: Create Equipment Matrix

```
Extract from EOR specifications:

Equipment Matrix Template:
| Equipment ID | Type | Spaces Served | CFM | Cooling (tons) | Heating (MBH) | Notes |
|--------------|------|---------------|-----|----------------|---------------|-------|
| HP RTU-1 | VAV w/ Elec Reheat | Library-Reading, Library-Stacks, Library-Office | 8000 | 40 | 150 | Heat pump |
| ERU-1 | DOAS | All spaces | 5000 | - | - | Ventilation only |

Key information to capture:
- Equipment ID (must match EOR exactly)
- Equipment type (VAV, CV, heat pump, etc.)
- List of spaces served (by name or number)
- Design airflow (CFM)
- Cooling capacity (tons)
- Heating capacity (MBH or kW)
- Special notes (heat pump, energy recovery, etc.)
```

### Step 3: Create Space Assignment Matrix

```
Cross-reference architectural plans with equipment schedule:

Space Assignment Matrix Template:
| Space Name | Room# | Space Type | Area (sf) | Thermal Zone | Equipment | Terminal Type | CFM |
|------------|-------|------------|-----------|--------------|-----------|---------------|-----|
| Library-Reading | 101 | Library | 5000 | Zone-RTU1-Library-Reading | HP RTU-1 | VAV Reheat | 3000 |
| Library-Stacks | 102 | Library | 3000 | Zone-RTU1-Library-Stacks | HP RTU-1 | VAV Reheat | 2000 |

Key information to capture:
- Space name (use descriptive, consistent names)
- Room number from architectural plans
- Space type (for 90.1/189.1 templates)
- Space area (from plans or model)
- Thermal zone name (create naming convention)
- Equipment serving this zone
- Terminal type (VAV reheat, CV, etc.)
- Design CFM for this zone
```

### Naming Convention Recommendations

```
Thermal zones:
Zone-[Equipment ID]-[Location/Function]

Examples:
- Zone-RTU1-Library-Reading
- Zone-RTU2-Gym-Main
- Zone-AHU1-Pool-Natatorium

Benefits:
- Clear connection to EOR equipment
- Identifies location
- Unique and descriptive
```

### Step 4: Model Validation Checklist

```
After creating matrices, validate model:

Equipment Validation:
□ All equipment from EOR specs represented in model
□ Equipment types match (VAV vs CV, heat pump vs standard, etc.)
□ Equipment capacities within 10% of design (if autosized)
□ Plant equipment matches (boilers, chillers, heat pumps)

Space Validation:
□ All spaces assigned to thermal zones
□ No orphaned thermal zones (zones without spaces)
□ Space areas in model match architectural plans (±5%)
□ Space types assigned correctly (90.1 or 189.1 templates)

Connection Validation:
□ Thermal zone names match EOR equipment naming
□ Multi-zone equipment has all intended spaces assigned
□ Terminal types match EOR specs (VAV reheat vs VAV no reheat, etc.)
□ Single-zone equipment has exactly one zone assigned

System Validation:
□ Plant loops exist for water-based systems
□ Coils connected to appropriate plant loops
□ Ventilation systems (DOAS, ERV) properly modeled
□ Service hot water systems included (if applicable)
```

### Step 5: Generate Validation Report

```
1. Export current model assignments:
   - OpenStudio → Thermal Zones → Export to CSV (if available)
   - Or manually document in spreadsheet

2. Compare model vs. matrices:
   - Use spreadsheet VLOOKUP or manual review
   - Highlight discrepancies

3. Flag issues:
   - Equipment in EOR specs but not in model
   - Equipment in model but not in EOR specs
   - Mismatched equipment types
   - Incorrect zone assignments

4. Provide fix instructions:
   - For each discrepancy, provide specific fix steps
   - Prioritize: Missing equipment → Incorrect connections → Type mismatches
```

### Validation Report Template

```
EOR Specification Mapping Report for [Project Name]
Date: [Date]
Reviewer: [Name]

DOCUMENTS REVIEWED:
- [List of EOR documents with dates]

EQUIPMENT SUMMARY:
Total equipment in EOR specs: [Count]
Total equipment in model: [Count]
Match rate: [Percentage]

DISCREPANCIES FOUND:

1. Missing from Model:
   - [Equipment ID]: [Description]
   - Recommended action: [Specific fix]

2. Not in EOR Specs:
   - [Equipment ID]: [Description]
   - Recommended action: [Verify with EOR or remove]

3. Configuration Mismatches:
   - [Equipment ID]: [What's wrong]
   - EOR spec: [Expected configuration]
   - Model config: [Current configuration]
   - Recommended action: [Specific fix]

ZONE ASSIGNMENT ISSUES:
[List of zone assignment discrepancies with fixes]

VALIDATION STATUS:
□ Complete - Model matches EOR specs
□ Pending fixes - [Number] issues to resolve
□ Major discrepancies - Recommend EOR coordination meeting

NEXT STEPS:
1. [Prioritized action items]
```

---

## Workflow 4: LEED Baseline Generation

**See [leed-compliance-procedures.md](./leed-compliance-procedures.md)** for comprehensive LEED Appendix G workflow (too detailed to include here, keeps this file focused).

Quick reference:
1. Validate proposed model (simulation runs, HVAC matches EOR)
2. Apply ASHRAE 90.1 Appendix G transformations (envelope, lighting, HVAC)
3. Create 4 rotations (0°, 90°, 180°, 270°)
4. Run all models and compare results
5. Verify ≥10% savings (or project target)
6. Generate LEED documentation

**Before baseline generation**: Check OpenStudio Standards gem documentation and Unmet Hours for ASHRAE 90.1 Appendix G best practices.

---

## Workflow 5: Systematic Error Resolution

**When to Use**: Simulation fails with multiple errors, need methodical approach to resolve

**Goal**: Efficiently resolve all errors in priority order

### Step 1: Parse and Categorize Errors

```
1. Open error file:
   - Location: [run-directory]/eplusout.err
   - Or OpenStudio → Results Summary → Errors tab

2. Extract unique errors:
   - Copy all error messages
   - Remove duplicates (same error repeated)
   - Count frequency of each unique error

3. Categorize by severity:
   SEVERE/FATAL: Simulation stops, must fix
   WARNING: Simulation runs but results questionable
   INFO: Informational only, no action needed

4. Categorize by type:
   - Geometry errors (intersecting, non-planar)
   - Connection errors (nodes, plant loops)
   - Input errors (schedules, invalid values)
   - Sizing errors (equipment, flows)
```

### Step 2: Prioritize Fixes

```
Priority 1 - Blocking issues (fix first):
- SEVERE/FATAL errors
- Geometry errors preventing simulation
- Missing required objects

Priority 2 - Data quality issues (fix second):
- Node connection errors
- Plant loop disconnections
- Schedule type mismatches

Priority 3 - Performance issues (fix third):
- Sizing warnings
- Unmet hours warnings
- Invalid input warnings (simulation continues)

Priority 4 - Informational (fix if time permits):
- INFO messages
- Suggestions for improvements
```

### Step 3: Validate Fix Approaches

```
For each error:
1. Search error message in Unmet Hours:
   site:unmethours.com "[exact error text]" openstudio

2. Check EnergyPlus I/O Reference:
   WebFetch: https://bigladdersoftware.com/epx/docs/24-2/input-output-reference/
   Prompt: "Find information about [object mentioned in error]. What are common causes of this error?"

3. Cross-reference common-error-patterns.md:
   - Does this match a known pattern?
   - Follow validated fix approach
```

### Step 4: Apply Fixes Iteratively

```
DO NOT fix all errors at once. Use iterative approach:

1. Fix top 1-3 Priority 1 errors
2. Re-run simulation
3. Check if new errors appeared (cascading fixes)
4. Parse new error file
5. Repeat until Priority 1 errors resolved

Then move to Priority 2, Priority 3, etc.

Benefits:
- Avoids cascading changes masking root cause
- Validates each fix before proceeding
- Identifies dependencies between errors
```

### Step 5: Document Fixes

```
Error Resolution Log Template:

Error: [Error message]
Category: [Geometry/Connection/Input/Sizing]
Severity: [Severe/Warning/Info]

Root Cause Analysis:
[What investigation revealed]

Sources Consulted:
□ OpenStudio documentation: [URL or section]
□ Unmet Hours: [Search query and result]
□ EnergyPlus I/O Reference: [Object or section]

Fix Applied:
[Specific steps taken]

Result:
□ Error resolved
□ Error persists (needs different approach)
□ Error changed (different error message)

Time spent: [Hours]
```

---

## General Workflow Best Practices

### Before Every Workflow

1. **Validate with authoritative sources** using [validation-sources.md](./validation-sources.md)
2. **Check for known patterns** in [common-error-patterns.md](./common-error-patterns.md)
3. **Document assumptions** (what you expect to find)

### During Every Workflow

1. **Work systematically** - Don't skip steps
2. **Document as you go** - Don't rely on memory
3. **Validate each fix** - Re-run simulation after major changes
4. **Use version control** - Save model before significant changes (Git or manual copies)

### After Every Workflow

1. **Verify results** - Does model simulate? Are results reasonable?
2. **Document completion** - What was done, what remains
3. **Update tracking** - If using work-command-center, update deliverables
4. **Capture lessons** - New patterns discovered? Document for future reference

---

**Last Updated**: 2025-11-19
**Aligned with**: OpenStudio 3.9, EnergyPlus 24.2
