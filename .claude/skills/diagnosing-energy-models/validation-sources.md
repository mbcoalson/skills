# Validation Sources for Energy Model Diagnostics

Before providing any fix recommendations for OpenStudio or EnergyPlus models, validate your approach against these authoritative sources. Use WebFetch to access documentation on-demand.

## Validation Priority Order

1. **OpenStudio User Documentation** (Primary - ALWAYS check first for geometry and HVAC)
2. **Unmet Hours Community** (Secondary - Use with caution, prioritize well-regarded contributors)
3. **EnergyPlus I/O Reference** (Object-Level Details)

---

## 1. NREL OpenStudio User Documentation (PRIMARY SOURCE)

**Base URL**: https://nrel.github.io/OpenStudio-user-documentation/

**CRITICAL**: This documentation is version-specific. Always use docs matching the OpenStudio version in use.

**Current Project Version**: OpenStudio 3.9 (default unless specified otherwise)

### When to Use (ALWAYS for these topics)
- **Geometry issues** (surface matching, building stories, intersections)
- **HVAC system setup and connections** (air loops, plant loops, terminals)
- OpenStudio Application workflows
- Model organization best practices
- Measure development guidance

**Priority Rule**: For geometry fixes and HVAC solutions, check OpenStudio documentation FIRST before consulting any other source.

### Key Sections to Reference

**Geometry Issues:**
- https://nrel.github.io/OpenStudio-user-documentation/reference/geometry_editor/
- Topics: Surface matching, space organization, building stories

**HVAC Systems:**
- https://nrel.github.io/OpenStudio-user-documentation/reference/hvac_systems/
- Topics: Air loops, plant loops, thermal zones, terminals

**Measures:**
- https://nrel.github.io/OpenStudio-user-documentation/reference/measure_writing_guide/
- Topics: ModelMeasure development, OpenStudio SDK methods

**Troubleshooting:**
- https://nrel.github.io/OpenStudio-user-documentation/getting_started/troubleshooting/
- Topics: Common errors, simulation failures

### Version-Specific Documentation Access

**OpenStudio 3.9 Documentation** (Current):
- Main: https://nrel.github.io/OpenStudio-user-documentation/
- Use this for all current project work unless specified otherwise

**Version Compatibility Notes**:
- OpenStudio 3.9 → EnergyPlus 24.2
- Major changes between versions can affect HVAC modeling, measures, and SDK methods
- Always verify documentation matches the version in use

**If using different version**:
- Check version number in OpenStudio Application: Help → About
- Access version-specific docs if available
- Note version compatibility in recommendations

### WebFetch Pattern

```
Use WebFetch with:
- URL: https://nrel.github.io/OpenStudio-user-documentation/[section]/
- Prompt: "What are the recommended approaches for [specific issue] in OpenStudio version 3.9? Include any warnings about common mistakes and version-specific considerations."
```

### Example Usage

**Before recommending surface matching fixes:**
```
WebFetch:
  URL: https://nrel.github.io/OpenStudio-user-documentation/reference/geometry_editor/
  Prompt: "What is the correct workflow for surface matching in OpenStudio 3.9? What are common issues with intersecting surfaces?"
```

**Before recommending HVAC plant loop connections:**
```
WebFetch:
  URL: https://nrel.github.io/OpenStudio-user-documentation/reference/hvac_systems/
  Prompt: "What is the correct workflow for connecting plant loops to air loops in OpenStudio 3.9? What are common connection errors?"
```

---

## 2. Unmet Hours Community (USE WITH CAUTION)

**Base URL**: https://unmethours.com/

**IMPORTANT**: Unmet Hours is a community forum. Not all answers are equally reliable. Use as secondary validation AFTER checking OpenStudio documentation.

### When to Use (Secondary Source)
- Real-world troubleshooting scenarios not covered in official docs
- Community-validated solutions for edge cases
- Version-specific issues and workarounds
- Workflow recommendations from experienced practitioners

**When NOT to Use**:
- As primary source for geometry fixes (use OpenStudio docs first)
- As primary source for HVAC setup (use OpenStudio docs first)
- When official documentation provides clear guidance

### Search Strategy

**Use Web Search (not WebFetch) with site filter:**
```
Query: site:unmethours.com [your issue] openstudio
```

### Effective Search Queries

**Geometry Issues:**
- `site:unmethours.com non-planar surface openstudio`
- `site:unmethours.com intersecting surfaces openstudio`
- `site:unmethours.com building story organization openstudio`

**HVAC Issues:**
- `site:unmethours.com plant loop connection openstudio`
- `site:unmethours.com thermal zone assignment openstudio`
- `site:unmethours.com [equipment type] openstudio`

**Simulation Errors:**
- `site:unmethours.com "[exact error message]" openstudio`

### Validation Criteria (CRITICAL)

When evaluating Unmet Hours answers, apply these filters in order:

**1. Contributor Reputation (HIGHEST PRIORITY)**

Well-regarded contributors (prioritize answers from these users):
- **NREL Staff**: David Goldwasser, Andrew Parker, Eric Ringold
- **Big Ladder Software**: Kyle Benne, Jason Glazer
- **OpenStudio Core Team members**: Identifiable by consistent high-quality technical answers
- **Frequent Top Contributors**: Users with high karma (>1000) and many accepted answers

**Indicators of reliable contributors**:
- ✅ Multiple accepted answers on similar topics
- ✅ Detailed technical explanations with SDK references
- ✅ Mention of version-specific behavior
- ✅ Links to documentation or code examples
- ✅ High karma score (visible on user profile)

**2. Answer Quality**
- ✅ **Prioritize**: Accepted answers (green checkmark) from well-regarded contributors
- ✅ **Consider**: Answers with multiple upvotes (especially if from recognized contributors)
- ✅ **Check**: Answer date - Is solution compatible with OpenStudio 3.9?
- ⚠️ **Use cautiously**: Recent answers without upvotes (may be unvalidated)
- ❌ **Avoid**: Old answers (>3 years) without validation (may be outdated)
- ❌ **Avoid**: Unvalidated single answers with no upvotes from unknown contributors

**3. Version Compatibility**
- Check answer date and mentioned OpenStudio version
- OpenStudio 3.x answers generally compatible with 3.9
- OpenStudio 2.x answers may have significant differences
- OpenStudio 1.x answers likely outdated

**4. Cross-Validation**
- If Unmet Hours answer contradicts OpenStudio documentation → Trust documentation
- If multiple well-regarded contributors agree → High confidence
- If answer is from unknown contributor with no upvotes → Verify independently

### Example Usage

**Before recommending HVAC connection fix:**
```
WebSearch:
  Query: site:unmethours.com plant loop coil connection openstudio

Then evaluate:
- Do multiple answers suggest the same approach?
- Are there warnings about common mistakes?
- Is the solution compatible with OpenStudio 3.9?
```

---

## 3. Big Ladder Software EnergyPlus Documentation

**Base URL**: https://bigladdersoftware.com/epx/docs/24-2/

**Version**: EnergyPlus 24.2 (aligned with OpenStudio 3.9)

### When to Use
- Object-level field definitions
- EnergyPlus-specific simulation errors
- HVAC object requirements and connections
- Material and construction properties
- Schedule type requirements
- Performance curves and coefficients

### Key Documentation Sections

**Input Output Reference** (Most Common):
- https://bigladdersoftware.com/epx/docs/24-2/input-output-reference/
- All EnergyPlus object definitions, required/optional fields

**Engineering Reference**:
- https://bigladdersoftware.com/epx/docs/24-2/engineering-reference/
- Calculation methods, algorithms, equipment models

**Output Details and Examples**:
- https://bigladdersoftware.com/epx/docs/24-2/output-details-and-examples/
- Understanding simulation outputs

### WebFetch Pattern

```
Use WebFetch with:
- URL: https://bigladdersoftware.com/epx/docs/24-2/input-output-reference/
- Prompt: "Find the [ObjectType] object definition and explain the required fields, connections to other objects, and common configuration issues."
```

### Example Usage

**Before recommending water-to-air heat pump configuration:**
```
WebFetch:
  URL: https://bigladdersoftware.com/epx/docs/24-2/input-output-reference/
  Prompt: "Find the ZoneHVAC:WaterToAirHeatPump object definition. What are the required connections to plant loops? What are common configuration mistakes?"
```

**For simulation error about missing schedule:**
```
WebFetch:
  URL: https://bigladdersoftware.com/epx/docs/24-2/input-output-reference/
  Prompt: "What schedule type limits are required for [schedule usage]? What are valid schedule values?"
```

---

## Validation Workflow

For every recommendation you make, follow this protocol:

### Step 1: Identify Issue Type
- Geometry? → Check OpenStudio docs first
- HVAC? → Check OpenStudio docs, then Unmet Hours
- EnergyPlus error? → Check EnergyPlus docs, then Unmet Hours
- Workflow question? → Check OpenStudio docs, then Unmet Hours

### Step 2: Validate Approach
```
1. Use WebFetch on relevant documentation URL
2. Search Unmet Hours for community validation
3. Cross-reference EnergyPlus object requirements if needed
```

### Step 3: Synthesize Recommendation
Only provide recommendation after:
- ✅ Confirming approach aligns with official documentation
- ✅ Checking for community warnings about common mistakes
- ✅ Verifying compatibility with OpenStudio 3.9 / EnergyPlus 24.2

### Step 4: Cite Sources
Include brief citations with version and contributor reputation (when applicable):
```
✅ Good: "According to OpenStudio 3.9 geometry editor documentation, surface matching should..."
✅ Good: "Per OpenStudio 3.9 HVAC systems guide, plant loop connections require..."
✅ Good: "Per OpenStudio 3.9 docs... [This approach is validated by David Goldwasser (NREL) on Unmet Hours]"
❌ Avoid: "The Unmet Hours community recommends..." (too vague - who said it? when? verified?)
✅ Better: "Per Unmet Hours answer by [contributor name] (verified, 10+ upvotes, 2024)..."
```

**Priority in citations**:
1. Always cite OpenStudio 3.9 docs first
2. Add Unmet Hours validation only if from well-regarded contributor
3. Include version compatibility notes

---

## Common Validation Scenarios

### Scenario 1: Geometry Rebuild Decision

**Issue**: User has intersecting surfaces, considering rebuild vs. fix

**Validation Steps** (in priority order):
1. **PRIMARY**: WebFetch OpenStudio 3.9 geometry documentation for surface matching best practices
2. **SECONDARY** (if additional context needed): Search Unmet Hours: `site:unmethours.com when to rebuild geometry openstudio`
   - Evaluate contributor reputation before using advice
3. Base recommendation primarily on OpenStudio documentation, with Unmet Hours as supplementary context

### Scenario 2: HVAC Object Configuration

**Issue**: Setting up water-to-air heat pump with plant loop

**Validation Steps** (in priority order):
1. **PRIMARY**: WebFetch OpenStudio 3.9 HVAC systems guide for plant loop connections
2. **OBJECT DETAILS**: WebFetch EnergyPlus 24.2 I/O Reference for ZoneHVAC:WaterToAirHeatPump object
3. **SECONDARY** (if needed): Search Unmet Hours: `site:unmethours.com water to air heat pump plant loop openstudio`
   - Check contributor reputation (prefer NREL staff, Big Ladder Software)
   - Verify answer date and version compatibility
4. Synthesize configuration steps prioritizing OpenStudio 3.9 documentation

### Scenario 3: Simulation Error

**Issue**: EnergyPlus error about missing node connection

**Validation Steps** (in priority order):
1. **PRIMARY**: WebFetch OpenStudio 3.9 HVAC documentation for proper node connection workflow
2. **OBJECT DETAILS**: WebFetch EnergyPlus 24.2 I/O Reference for the specific object mentioned in error
3. **SECONDARY** (if needed): Search Unmet Hours: `site:unmethours.com "[exact error message]" openstudio`
   - Prioritize answers from well-regarded contributors
   - Check version compatibility
4. Provide fix that addresses root cause (per OpenStudio docs), not just symptoms

---

## Validation Checklist

Before providing any fix recommendation, confirm:

- [ ] Checked OpenStudio 3.9 documentation FIRST (mandatory for geometry/HVAC)
- [ ] If using Unmet Hours: Evaluated contributor reputation and answer quality
- [ ] If using Unmet Hours: Verified answer date and version compatibility
- [ ] Verified approach is compatible with OpenStudio 3.9 / EnergyPlus 24.2
- [ ] Considered common mistakes documented in sources
- [ ] Included citation with version: "Per OpenStudio 3.9 [section]..."
- [ ] If citing Unmet Hours: Included contributor name and validation indicators
- [ ] Provided complete, actionable steps (not partial guidance)
- [ ] If sources conflict: Prioritized OpenStudio docs over Unmet Hours

---

## When Documentation Conflicts

If sources provide conflicting guidance, follow this priority hierarchy:

1. **OpenStudio 3.9 Documentation** (HIGHEST PRIORITY)
   - Official NREL documentation always takes precedence
   - Version-specific to OpenStudio 3.9

2. **EnergyPlus 24.2 Documentation**
   - For object-level details not covered in OpenStudio docs
   - Must align with OpenStudio 3.9 compatibility

3. **Well-Regarded Unmet Hours Contributors** (LOWEST PRIORITY)
   - Only if from NREL staff, Big Ladder Software, or high-karma users
   - Recent answers (within 2 years)
   - Multiple upvotes or accepted answer

**Resolution Strategy**:
- If Unmet Hours contradicts OpenStudio docs → **Trust OpenStudio docs**
- If unsure about conflicting approaches → Present both to user with source citations
- If critical decision → Recommend creating small test model to validate approach
- Always document which source you followed and why

---

## Keeping Current

These URLs are stable, but content evolves:
- OpenStudio docs update with each release (~quarterly)
- EnergyPlus docs version-specific (use 24.2 for OpenStudio 3.9)
- Unmet Hours accumulates new solutions continuously

**Always use WebFetch to get current content** rather than relying on potentially outdated embedded information.

---

**Last Updated**: 2025-11-19
**Aligned with**: OpenStudio 3.9, EnergyPlus 24.2
