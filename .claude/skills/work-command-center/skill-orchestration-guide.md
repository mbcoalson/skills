# Work Command Center - Skill Orchestration Guide

This document describes when and how to delegate work to other specialized skills from the Work Command Center.

---

## Orchestration Philosophy

Work Command Center is an **orchestrator skill** - it stays focused on deliverables, priorities, and team coordination. When technical deep-dives are needed, it delegates to specialized skills and returns to Command Center view with a summary.

**Rules:**
1. **Stay in Command Center** unless technical deep-dive needed
2. **Call other skills** for specialized work
3. **Return to Command Center** after skill work completes with summary
4. **Never lose context** - always update tracking files after sessions

---

## Available Skills for Delegation

### skill-builder
**Purpose:** Creating/editing Claude Skills or converting sub-agents to skills

**When to Invoke:**
- User wants to create a new Claude Code skill
- User wants to improve an existing skill's description or structure
- User wants to convert a sub-agent to skill format
- User asks about skill best practices

**Example Queries:**
- "Help me create a skill for budget tracking"
- "Improve my energy-efficiency skill description"
- "Convert my sub-agent to a proper skill"

**Return to Command Center With:**
- Summary of skill created/edited
- File locations
- Any follow-up needed

---

### converting-markdown-to-word
**Purpose:** Convert markdown files to Word format for sharing with colleagues

**When to Invoke:**
- User needs to share meeting notes with Word users
- User needs to convert documentation from .md to .docx
- User mentions "Word" or "docx" in context of sharing files

**Example Queries:**
- "Convert my meeting notes to Word format"
- "Create a Word doc from this markdown file"
- "I need to share this with the team but they need Word"

**Return to Command Center With:**
- Location of generated .docx file
- Confirmation of conversion success

---

### energyplus-assistant
**Purpose:** EnergyPlus model QA/QC, HVAC topology analysis, parametric ECM testing

**When to Invoke:**
- User needs to validate EnergyPlus IDF file before simulation
- User wants to analyze HVAC topology in energy model
- User needs to test parametric ECM scenarios
- User mentions "QA/QC", "energy model errors", "HVAC topology"

**Example Queries:**
- "Validate my SECC energy model before simulation"
- "Analyze HVAC topology in my EnergyPlus model"
- "Test parametric ECM scenarios for lighting upgrades"
- "QA/QC check on EnergyPlus IDF file"

**Return to Command Center With:**
- Model validation status (pass/fail)
- Critical errors found
- Next actions needed (if any)

---

### energy-efficiency
**Purpose:** EnergyPlus modeling, ASHRAE standards, code compliance

**When to Invoke:**
- User needs help with ASHRAE 90.1 or other standards
- User needs energy model compliance calculations
- User asks about baseline requirements
- User needs code compliance verification

**Example Queries:**
- "Help me with ASHRAE 90.1 baseline requirements"
- "Review energy model compliance calculations"
- "What's the lighting power density for office space?"

**Return to Command Center With:**
- Standard requirements or calculations
- Compliance status
- Any deliverable impacts

---

### writing-openstudio-model-measures
**Purpose:** Write Ruby ModelMeasures for OpenStudio (targets v3.9)

**When to Invoke:**
- User needs to write a new OpenStudio measure
- User wants to modify existing measure
- User mentions "measure.rb", "OpenStudio measure", "ModelMeasure"

**Example Queries:**
- "Create a measure to add daylighting controls"
- "Write a measure to modify HVAC schedules"
- "Update my existing lighting measure"

**Return to Command Center With:**
- Measure file location
- Testing status
- Integration with current project deliverable

---

### skyspark-analysis
**Purpose:** SkySpark analytics and building automation systems

**When to Invoke:**
- User needs Axon query written
- User wants to analyze SkySpark trending data
- User needs fault detection logic
- User mentions "SkySpark", "Axon", "FIN", "Haystack"

**Example Queries:**
- "Write an Axon query to find fault conditions"
- "Analyze trending data for equipment performance"
- "Create a rule to detect simultaneous heating and cooling"

**Return to Command Center With:**
- Query or analysis results
- Impact on current deliverables
- Next actions

---

### commissioning-reports
**Purpose:** MBCx workflows and ASHRAE Guideline 0 procedures

**When to Invoke:**
- User needs MBCx implementation plan
- User needs testing protocol for equipment
- User mentions "MBCx", "commissioning", "test procedure", "ASHRAE Guideline 0"

**Example Queries:**
- "Generate MBCx implementation plan"
- "Create testing protocol for AHU system"
- "What's the NEBB procedure for balancing?"

**Return to Command Center With:**
- Document/plan location
- Timeline impact on deliverables
- Team coordination needs

---

### n8n-automation
**Purpose:** Multi-agent workflow automation

**When to Invoke:**
- User wants to set up n8n workflow
- User needs FastAPI tool server integration
- User mentions automation, webhooks, or workflow orchestration

**Example Queries:**
- "Set up n8n workflow for SkySpark alerts"
- "Create FastAPI tool server integration"
- "Automate the MBCx report generation"

**Return to Command Center With:**
- Workflow status
- Testing results
- Impact on team efficiency

---

### work-documentation
**Purpose:** Company procedures, standards, templates, best practices

**When to Invoke:**
- User asks about company procedures
- User needs to find a template
- User wants to know standard practices
- User mentions "procedure", "template", "how do we...", "company standard"

**Example Queries:**
- "Find the standard proposal template"
- "What's our procedure for MBCx kickoff meetings?"
- "How do we handle budget overruns?"

**Return to Command Center With:**
- Location of relevant documentation
- Key points from procedure
- Action items based on standards

---

## Integration Patterns

### Pattern 1: Quick Delegation (No Context Needed)

```
User: "Convert meeting-notes.md to Word"
→ Invoke: converting-markdown-to-word
→ Return: "✓ Created meeting-notes.docx in [location]"
```

### Pattern 2: Context Handoff (Pass Current Work)

```
User: "Validate my SECC energy model"
→ Invoke: energyplus-assistant
  - Pass relevant deliverable info (SECC project, deadline, status)
→ Return: "Model validation complete. Found 3 warnings, no errors.
           Updated SECC deliverable status to 'Ready for Simulation'"
```

### Pattern 3: Iterative Collaboration

```
User: "Help me write measures for the SECC model"
→ Invoke: writing-openstudio-model-measures
  - User works with skill on measure development
→ Return to Command Center
  - Update deliverable with measure status
  - Add testing as next action
  - Log time spent on measure development
```

### Pattern 4: Research/Documentation Lookup

```
User: "What's our MBCx implementation plan template?"
→ Invoke: work-documentation
→ Return: "Found template at [location]. Next: Customize for [current project]"
→ Add deliverable action: "Customize MBCx plan using template"
```

---

## When NOT to Delegate

Stay in Work Command Center for:
- Deliverable tracking updates
- Priority coaching ("What should I focus on today?")
- Team status reviews
- Daily standups
- Time logging
- Counter tracking (rescued deadlines, etc.)
- Brain dump sessions
- Deadline reviews
- Simple clarifications or questions

---

## Orchestration Checklist

Before delegating to another skill:

- [ ] Is this truly specialized technical work?
- [ ] Can Work Command Center handle this directly?
- [ ] What context does the other skill need?
- [ ] How will results integrate back into deliverables?
- [ ] Should time be logged for this technical work?

After returning from another skill:

- [ ] Update relevant deliverables with new status
- [ ] Log time spent (if billable project work)
- [ ] Update team coordination needs (if applicable)
- [ ] Confirm next action with user
- [ ] Maintain calm, organized Command Center view

---

## Future Integrations

Planned skill integrations:
- **Note-taking MCP** - Auto-populate deliverables from meeting notes
- **BD tracking** - Track new opportunities and proposals in flight
- **Internal tools development** - Track Claude skill and automation development
- **New employee onboarding coach** - Guide new team member integration

When these become available, update this guide with delegation patterns.
