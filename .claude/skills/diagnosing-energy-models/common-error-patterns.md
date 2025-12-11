# Common Error Patterns in OpenStudio/EnergyPlus Models

This document catalogs frequently encountered error patterns with their symptoms, root causes, fixes, and prevention strategies. These patterns are validated against real-world troubleshooting experience and community knowledge.

---

## Pattern 1: Overlapping Building Stories

### Symptom
- Multiple "Building Story" objects with identical Z-coordinates
- EnergyPlus reports intersecting surfaces during simulation
- Simulation fails with geometry errors
- OpenStudio surface inspector shows red (unmatched) surfaces

### Root Cause
User organized program areas as separate "stories" rather than spaces on the same floor.

**Common Mistake**: Creating separate Building Story objects for different functional areas (Pool, Library, Gym) that are actually on the same physical floor level (all at Z=0).

**Why This Happens**: Misunderstanding that Building Story represents physical floor elevation, not programmatic organization.

### Fix Strategy

**Before making recommendations, validate against:**
- OpenStudio geometry editor documentation (surface matching, story organization)
- Unmet Hours: `site:unmethours.com building story organization openstudio`

**Step-by-step fix:**
```
1. List all Building Story objects and their Z-coordinates
2. Identify true floor elevations:
   - Ground floor: typically Z=0
   - Second floor: Z=12' to 16' (depending on floor-to-floor height)
   - Third floor: Z=24' to 32', etc.
3. Consolidate spaces onto proper stories based on actual building levels
4. Delete duplicate story objects (keep only stories representing physical floors)
5. Reassign spaces to correct stories
6. Re-run surface matching (OpenStudio → Components & Measures → Surface Matching)
7. Verify all surfaces are matched (no red surfaces in 3D view)
```

### Prevention
- Use "Building Story" ONLY for actual vertical building levels
- Organize different program areas as separate spaces WITHIN a story
- Verify story Z-coordinates before adding spaces to stories
- Name stories by physical level: "Ground Floor", "Second Floor", not by program

### Validation Before Recommending
- [ ] Check OpenStudio docs for surface matching requirements
- [ ] Search Unmet Hours for story organization best practices
- [ ] Verify fix won't create new issues (e.g., losing space assignments)

---

## Pattern 2: Non-Planar Surfaces from SketchUp

### Symptom
- EnergyPlus warning: "Surface has vertices that are not coplanar"
- Simulation fails or produces unrealistic results
- Surface area calculations are incorrect
- Surfaces appear correct visually but fail geometric tests

### Root Cause
SketchUp's loose geometric tolerances combined with manual vertex editing create surfaces where vertices don't lie in a single plane.

**Common Sources**:
- SketchUp's native drawing tools (not OpenStudio plugin)
- Manual vertex adjustments after face creation
- Importing complex curved surfaces
- Copy-paste operations from non-orthogonal geometry

### Fix Strategy

**Before making recommendations, validate against:**
- OpenStudio geometry editor documentation
- Unmet Hours: `site:unmethours.com non-planar surface openstudio`

**Step-by-step fix:**
```
1. Identify non-planar surfaces:
   - OpenStudio Application: Inspect → Surfaces → Filter "Non-Planar" warnings
   - Note surface names and locations

2. For each problematic surface:
   a. Document the space it belongs to
   b. Note adjacent surfaces (for surface matching later)
   c. Delete the problematic surface in OpenStudio Application

3. Recreate geometry in SketchUp:
   a. Use ONLY the OpenStudio plugin drawing tools
   b. Draw simple rectangular geometry (avoid complex shapes)
   c. Use orthogonal (90°) angles only
   d. Avoid manual vertex adjustments

4. Re-import to OpenStudio Application

5. Re-run surface matching

6. Verify fix:
   - No non-planar warnings
   - Surface area matches expected value
   - Adjacent surfaces properly matched
```

### Prevention
- Use OpenStudio SketchUp plugin from the FIRST drawing session
- Draw ONLY orthogonal (90°) geometry for energy models
- Avoid SketchUp's native drawing tools for thermal envelope surfaces
- Use space separation guidelines: simple rectangular boxes, no complex shapes
- Don't manually adjust vertices after face creation
- Use "New Space from Diagram" feature in OpenStudio plugin (creates clean geometry)

### Alternative: Simplification Approach
For complex existing geometry:
```
1. Approximate curved/angled surfaces with rectangular segments
2. Use multiple simple surfaces instead of one complex surface
3. Accept minor area differences for geometric validity
```

### Validation Before Recommending
- [ ] Check OpenStudio docs for geometry creation best practices
- [ ] Search Unmet Hours for non-planar surface solutions
- [ ] Consider impact on surface matching and adjacent spaces

---

## Pattern 3: Unassigned or Duplicate Thermal Zones

### Symptom
- Spaces exist without thermal zone assignments
- Multiple spaces incorrectly assigned to the same zone
- HVAC equipment serving wrong areas
- Simulation error: "Zone not found" or "Zone has no equipment"
- Thermal zone exists but has no spaces assigned (orphaned zone)

### Root Cause
Manual thermal zone creation without proper space assignments, often due to:
- Creating zones before assigning them to spaces
- Copy-paste errors during zone setup
- Misunderstanding EOR equipment list organization
- Deleting spaces without cleaning up zone assignments

### Fix Strategy

**Before making recommendations, validate against:**
- OpenStudio HVAC systems documentation (thermal zone requirements)
- Unmet Hours: `site:unmethours.com thermal zone assignment openstudio`
- EnergyPlus I/O Reference: `ThermalZone` object requirements

**Step-by-step fix:**
```
1. Audit current state:
   a. Export list of all spaces (OpenStudio → Spaces tab)
   b. Export list of all thermal zones (OpenStudio → Thermal Zones tab)
   c. Identify spaces without zones
   d. Identify orphaned zones (zones with no spaces)

2. Gather EOR specifications:
   a. Review mechanical drawings for equipment schedule
   b. Note which spaces each piece of equipment serves
   c. Create zone assignment matrix (see template below)

3. Create zone assignment matrix:
   ```
   Space Name | Space Type | Area (sf) | Thermal Zone | Equipment | Terminal Type
   Library-Reading | Library | 5000 | Zone-RTU1-Library | HP RTU-1 | VAV Reheat
   Library-Stacks | Library | 3000 | Zone-RTU1-Library | HP RTU-1 | VAV Reheat
   ```

4. Assign thermal zones in OpenStudio:
   a. Select space in Spaces tab
   b. Choose thermal zone from dropdown in right panel
   c. Verify assignment in Thermal Zones tab

5. Clean up orphaned zones:
   a. Delete zones with no spaces assigned
   b. Verify HVAC equipment reassignment if needed

6. Validate assignment:
   a. Every space has exactly one thermal zone
   b. Each zone has at least one space
   c. Zone names match EOR equipment naming
   d. Multi-zone equipment has all intended spaces assigned
```

### Zone Assignment Matrix Template
```
Equipment ID | Type | Spaces Served | CFM | Cooling (tons) | Heating (MBH)
HP RTU-1 | VAV w/ Elec Reheat | Library-Reading, Library-Stacks, Library-Office | 8000 | 40 | 150
```

### Prevention
- ALWAYS assign thermal zones during space creation workflow
- Follow consistent naming convention: "Zone - [Equipment ID]"
- Create zone assignment matrix BEFORE modeling
- Use OpenStudio Measures for bulk zone assignment (when >20 zones)
- Never delete spaces without checking thermal zone orphaning

### Validation Before Recommending
- [ ] Check OpenStudio docs for thermal zone workflow
- [ ] Verify EOR specifications are correctly interpreted
- [ ] Ensure one-to-one or many-to-one space:zone mapping (never one-to-many)

---

## Pattern 4: Missing or Incorrect HVAC Connections

### Symptom
- Plant equipment exists but not connected to air loops
- Coils exist without water loop connections
- Simulation error: "Component not on any plant loop"
- Simulation error: "Node connection mismatch"
- HVAC system renders in topology view but fails in simulation

### Root Cause
Manual component addition without following proper connection workflow:
- Adding components in wrong order
- Deleting components breaks downstream connections
- Misunderstanding OpenStudio HVAC object hierarchy
- Manual node editing (should never be done)

### Fix Strategy

**Before making recommendations, validate against:**
- OpenStudio HVAC systems documentation (plant loop connections)
- Unmet Hours: `site:unmethours.com plant loop connection openstudio`
- EnergyPlus I/O Reference: Specific component object requirements

**Step-by-step fix for disconnected coils:**
```
1. Identify the disconnected component:
   - Check simulation error message for component name
   - Note which air loop or zone equipment it belongs to

2. Check current connections:
   - OpenStudio → HVAC Systems → Select air loop or zone equipment
   - HVAC → Plant Loops → Check Connections tab
   - Verify Supply Equipment → Demand Equipment flow

3. For disconnected heating/cooling coil:
   a. Delete coil from air loop (or zone equipment)
   b. Verify required plant loop exists (heating hot water, chilled water, etc.)
   c. Add coil back using proper workflow:
      - Drag coil from library onto air loop diagram
      - OpenStudio automatically prompts for plant loop connection
      - Select appropriate plant loop
   d. Verify connection in Plant Loops → Connections tab

4. For missing plant loops:
   a. Create plant loop first (HVAC → Add Plant Loop)
   b. Add supply equipment (boiler, chiller, etc.)
   c. Then add demand components (coils)
   d. OpenStudio creates connections automatically
```

**Step-by-step fix for node connection errors:**
```
1. Do NOT manually edit nodes
2. Delete the problematic component entirely
3. Re-add using OpenStudio Application workflow (drag-and-drop)
4. Let OpenStudio handle node creation automatically
```

### HVAC Addition Order (Critical)
```
Correct order:
1. Create Plant Loops (if needed for heating/cooling)
2. Add supply equipment to plant loops (boilers, chillers)
3. Create Air Loops
4. Add air-side equipment to air loops (fans, coils)
5. OpenStudio prompts for plant loop connections
6. Add terminals to thermal zones
7. Connect terminals to air loops
```

### Prevention
- Use OpenStudio Application built-in HVAC workflows (drag-and-drop)
- Add components in correct order: Plant → Air Loop → Terminals
- NEVER manually edit node connections
- Use HVAC templates when available (speeds setup and ensures connections)
- Check Plant Loop Connections tab after every addition

### Common Mistakes to Avoid
- ❌ Creating air loop before plant loops (for water-based systems)
- ❌ Copy-pasting HVAC components between loops
- ❌ Deleting plant loops without removing demand components first
- ❌ Manual IDF editing for node connections (use OpenStudio Application)

### Validation Before Recommending
- [ ] Check OpenStudio HVAC documentation for proper workflow
- [ ] Search Unmet Hours for component-specific connection issues
- [ ] Verify EnergyPlus object requirements from I/O Reference
- [ ] Confirm plant loop type matches coil requirements

---

## Pattern 5: Surface Matching Failures

### Symptom
- Red (unmatched) surfaces in OpenStudio 3D view
- Warning: "Surface not matched with adjacent surface"
- Incorrect heat transfer between spaces
- Higher than expected energy consumption

### Root Cause
- Adjacent surfaces not within tolerance (0.01 ft default)
- Spaces on different building stories when they should share surfaces
- Manual surface creation without using matching algorithm
- Floating point precision errors from SketchUp imports

### Fix Strategy

**Before making recommendations, validate against:**
- OpenStudio geometry editor documentation (surface matching algorithm)
- Unmet Hours: `site:unmethours.com surface matching openstudio`

**Step-by-step fix:**
```
1. Run surface matching:
   - OpenStudio → Components & Measures → Surface Matching
   - Set tolerance: 0.01 ft (default) or increase if needed

2. If matching fails:
   a. Check story organization (see Pattern 1)
   b. Verify adjacent spaces are on correct stories
   c. Inspect surface geometry for alignment issues

3. For persistent failures:
   a. Identify unmatched surface pairs
   b. Check vertex coordinates (should align within tolerance)
   c. Consider rebuilding problematic surfaces
```

### Prevention
- Always run surface matching after geometry changes
- Maintain proper story organization
- Use SketchUp OpenStudio plugin for clean geometry
- Avoid manual surface vertex editing

---

## Pattern 6: Schedule Type Mismatches

### Symptom
- Simulation error: "Schedule type mismatch"
- Error mentions specific object and schedule field
- Model fails despite all schedules being defined

### Root Cause
EnergyPlus schedule types have specific type limits (e.g., on/off, fractional, temperature) and assigning wrong type to an object field causes errors.

### Fix Strategy

**Before making recommendations, validate against:**
- EnergyPlus I/O Reference: Schedule type limit definitions
- Unmet Hours: `site:unmethours.com schedule type limits energyplus`

**Step-by-step fix:**
```
1. Identify the problematic schedule from error message
2. Check EnergyPlus I/O Reference for required schedule type
3. Verify schedule type limits in OpenStudio:
   - Schedules tab → Select schedule → Check "Schedule Type Limits"
4. Create new schedule with correct type or modify existing
```

### Common Schedule Types
- **On/Off**: Binary (0 or 1), used for availability
- **Fractional**: 0.0 to 1.0, used for loads/occupancy
- **Temperature**: °C, used for setpoints
- **Activity**: W/person, used for occupant activity levels

---

## Using These Patterns

When diagnosing a model:

1. **Match symptoms** to patterns above
2. **Validate fix approach** using sources in [validation-sources.md](./validation-sources.md)
3. **Follow step-by-step fix** procedures
4. **Verify fix** before moving to next issue
5. **Document** any new patterns discovered

**Always validate against authoritative sources before recommending fixes.**

---

**Last Updated**: 2025-11-19
**Aligned with**: OpenStudio 3.9, EnergyPlus 24.2
