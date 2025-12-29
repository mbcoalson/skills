# Skill Splitting Task: Energize Denver & Proposals Separation

Use the **skill-builder** skill to split energize-denver-proposals into two focused skills.

---

## TASK OVERVIEW

Split the current `energize-denver-proposals` skill into two separate, focused skills:

1. **energize-denver** - Denver Article XIV compliance reference (regulations, pathways, deadlines)
2. **proposals** - General proposal development methodology (pricing, scoping, service delivery)

## SKILL GOALS

### Skill 1: energize-denver (Regulations Handbook)

**Purpose:** Be the authoritative reference for Denver's Energize Denver Article XIV compliance

**What it should do:**
- Answer questions about Energize Denver requirements, deadlines, penalties
- Guide pathway selection (MAI production efficiency vs whole-building EUI vs prescriptive)
- Explain baseline calculations, custom metrics, timeline extensions
- Provide CASR contact info and application procedures

**What it should NOT do:**
- Price services or create proposals
- Provide general consulting methodologies
- Handle non-Denver building performance programs

**Key strength:** Like having the municipal code + program guidance in one searchable place

---

### Skill 2: proposals (Service Delivery Methodology)

**Purpose:** Be the reusable framework for pricing, scoping, and writing energy consulting proposals

**What it should do:**
- Help estimate project costs (labor hours, pricing, fixed-fee vs hourly)
- Define service types (ASHRAE audits, benchmarking, MBCx, commissioning)
- Structure scopes of work with clear deliverables
- Guide proposal writing (what to include, how to present)
- Support client engagement (discovery questions, needs assessment)

**What it should NOT do:**
- Contain Energize Denver-specific regulations
- Be limited to only Denver work (should work for ANY energy consulting proposal)

**Key strength:** Reusable for Energize Denver, ASHRAE audits, commissioning, any energy project

---

## CONTENT SEPARATION PRINCIPLE

**Simple rule:**
- Regulatory knowledge → energize-denver
- Service delivery methodology → proposals

**Example splits:**
- "What is the MAI production efficiency formula?" → energize-denver
- "How do I price an Energize Denver MAI audit?" → proposals (references energize-denver for requirements)
- "When is the Dec 31 deadline?" → energize-denver
- "How many hours for ASHRAE Level II audit?" → proposals

**Cross-references:**
- proposals can reference energize-denver for Denver-specific requirements
- energize-denver can reference proposals for service delivery options

---

## CURRENT SKILL LOCATION

`.claude/skills/energize-denver-proposals/`

**Files to review:**
- SKILL.md
- energize-denver-requirements.md (273 lines, just updated with MAI production efficiency details)
- pricing-guidelines.md
- service-types.md

## INSTRUCTIONS FOR SKILL-BUILDER

**Your task:** Review the current energize-denver-proposals skill and create two new skills following skill creation best practices.

**Use your judgment on:**
- File organization and structure (intention-revealing names, logical grouping)
- How many supporting files each skill needs
- Whether to split large files or keep them together
- SKILL.md activation triggers (clear, unambiguous)
- Cross-reference strategy between skills

**Requirements:**
1. **No content loss** - All current knowledge must go into one of the two new skills
2. **Clear separation** - User should know which skill to use for any question
3. **proposals must be reusable** - Should work for non-Energize Denver projects
4. **energize-denver must be complete** - All Article XIV compliance info in one place

**Recommended approach:**
1. Read all files in `.claude/skills/energize-denver-proposals/`
2. Apply separation principle (regulations vs methodology)
3. Create SKILL.md files with clear descriptions and activation triggers
4. Organize supporting files using intention-revealing names
5. Add cross-references where skills should work together
6. Ensure proposals skill is generalizable to non-Denver work

**Deliverables:**
- Two complete skills ready to use (energize-denver + proposals)
- Migration notes explaining what moved where and why
- Any identified gaps or improvement opportunities

**Don't overthink it:** Use your skill-building expertise to create clean, maintainable skills. Focus on making them useful and easy to activate correctly.

---

## USE CASES TO SUPPORT

After the split, these should work cleanly:

**energize-denver only:**
- "What is the MAI production efficiency baseline year?" → 2022 (or 2018-2022)
- "When is the Energize Denver Dec 31 deadline for?" → MAI ACO application
- "What are the penalty rates for MAI buildings?" → $0.15-$0.35/kBtu depending on timeline
- "How do I calculate production efficiency?" → Weather-normalized kBtu ÷ production units

**proposals only:**
- "How do I price an ASHRAE Level II audit?" → Use labor rates + complexity factors
- "What deliverables for benchmarking service?" → Portfolio Manager setup, annual submissions, etc.
- "Help me write a scope of work for commissioning" → Use service-types templates

**Both skills working together:**
- "Create Energize Denver MAI proposal for print shop" → proposals (pricing/structure) + energize-denver (requirements)
- "How much for Energize Denver compliance consulting?" → proposals (rates) + energize-denver (scope based on building type)

---

## CONTEXT FOR SKILL-BUILDER

**Current situation:**
- energize-denver-proposals conflates regulatory knowledge with service delivery methodology
- energize-denver-requirements.md is 273 lines and just got updated with comprehensive MAI production efficiency pathway details
- pricing-guidelines.md and service-types.md contain general consulting methodology that should work for ANY energy project

**Desired outcome:**
- energize-denver = regulations handbook (reference material, compliance guidance)
- proposals = consulting methodology (how to deliver services, price projects, write proposals)
- proposals should be reusable for ASHRAE audits, commissioning, benchmarking support for any program (not just Denver)

**Success criteria:**
- Clear activation (no user confusion about which skill to invoke)
- No duplicated content (DRY principle)
- Proposals skill works for non-Denver projects
- All current knowledge preserved in logical location
