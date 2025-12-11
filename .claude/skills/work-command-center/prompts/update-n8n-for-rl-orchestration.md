# Update n8n-Automation Skill for Future RL Orchestration

## Context
I've reviewed the Puppeteer paper (NeurIPS 2025) on dynamic multi-agent orchestration via reinforcement learning. The approach demonstrates superior performance and efficiency compared to static workflows through centralized, state-dependent agent routing.

**Paper location:** `C:\Users\mcoalson\Documents\WorkPath\Resources\research-papers\Puppeteer-Multi-Agent-Orchestration-NeurIPS-2025.md`

## Objective
Update the n8n-automation skill to incorporate architectural principles that will enable future evolution toward RL-based dynamic orchestration, while maintaining practical utility for current Phase 0-1 development.

## Requirements for Skill Update

### 1. Agent Design Principles
Add guidance ensuring that SkySpark agents are designed with these characteristics:

**Statelessness:**
- Agents should receive complete diagnostic context as input
- Agents should NOT maintain internal state between calls
- All necessary context passed in, new state returned out
- Enables any agent to follow any agent (routing flexibility)

**Standardized I/O Schema:**
- Define common input structure: `DiagnosticState` object containing:
  - Current alert/issue details
  - Prior agent outputs/reasoning
  - Available tools/data sources
  - Token budget remaining
  - Diagnostic confidence score
- Define common output structure: `AgentResponse` object containing:
  - Updated diagnostic state
  - Agent's findings/actions
  - Next recommended agents (even if not used yet)
  - Token cost of operation
  - Confidence update

**Role-Based Architecture:**
- Separate agent identity (role prompts) from action logic
- Enable agents to be categorized as:
  - **Tool-Use Agents:** Python execution, SkySpark queries, file reading, web search
  - **Reasoning Agents:** Planning, analysis, critique, reflection, summarization

### 2. Orchestration Layer Design
Add framework for orchestration that starts simple but can evolve:

**Phase 0-1: Static n8n Workflows**
- Current hardcoded routing is acceptable
- BUT design workflows to call centralized routing functions
- Log every routing decision with context

**Phase 2-3: Rule-Based Orchestrator**
- Create `agent_router` function that selects next agent based on:
  - Alert type/severity
  - Current diagnostic confidence
  - Prior agent sequence
  - Available tools
- Implement in Python (FastAPI endpoint)
- Rules manually tuned based on logged data

**Phase 4-5: RL-Based Orchestrator**
- Replace rule-based router with learned policy
- Use logged trajectories as training data
- Optimize for: diagnostic accuracy + token efficiency

### 3. Instrumentation Requirements
Add comprehensive logging infrastructure:

**What to Log:**
- Complete agent call sequence per diagnostic episode
- Input state for each agent call
- Output state from each agent call
- Token consumption per agent call
- Final diagnostic outcome (correct/incorrect)
- Human override/corrections
- Time to resolution

**Log Schema:**
```json
{
  "episode_id": "alert_123456_2025-12-02",
  "alert_context": {...},
  "agent_sequence": [
    {
      "timestamp": "2025-12-02T10:30:00Z",
      "agent_type": "SkySpark Query Agent",
      "input_state": {...},
      "output_state": {...},
      "tokens_used": 1500,
      "duration_ms": 3400
    },
    ...
  ],
  "final_outcome": {
    "diagnostic_correct": true,
    "resolution_actions": [...],
    "total_tokens": 8500,
    "total_duration_ms": 15200,
    "human_intervention_required": false
  }
}
```

**Storage:**
- Store in n8n database OR dedicated TimescaleDB
- Retain minimum 200 episodes per alert type for future RL training
- Enable easy export for offline analysis

### 4. Reward Function Design
Add preliminary reward function specification:

**Components:**
- **Accuracy:** Did diagnostic correctly identify root cause?
  - Validated against human review OR system resolution outcome
  - Binary (0/1) or graduated scale (0.0-1.0)
  
- **Efficiency:** Token cost relative to diagnostic complexity
  - Penalty factor λ = 0.1 (tunable)
  - Cost function: `F * log(1 + t/φ)` where t=tokens, φ=budget, F=base_cost
  
- **Timeliness:** Resolution speed relative to alert severity
  - Critical alerts: higher penalty for slow resolution
  - Informational alerts: efficiency weighted higher

**Formula:**
```
R = accuracy_score - λ × token_cost - β × time_penalty
```

Where:
- `accuracy_score ∈ [0, 1]`
- `token_cost = tokens_used / max_token_budget`
- `time_penalty = (time_to_resolve / sla_threshold) if > threshold else 0`
- `λ = 0.1` (efficiency weight, tunable)
- `β = 0.05` (timeliness weight, tunable)

### 5. Agent Categories for SkySpark
Define specific agent types aligned with Puppeteer taxonomy:

**Tool-Use Agents:**
- `SkySpark_Query_Agent`: Execute Axon queries against SkySpark database
- `Python_Analysis_Agent`: Run Python calculations, statistical analysis
- `File_Reader_Agent`: Parse CSV, JSON, equipment spec files
- `Weather_Data_Agent`: Fetch external weather data via API
- `Documentation_Agent`: Search equipment manuals, standards

**Reasoning Agents:**
- `Diagnostic_Planner_Agent`: Decompose complex issues into sub-diagnostics
- `Root_Cause_Analyzer_Agent`: Synthesize data to identify probable causes
- `Validation_Agent`: Verify diagnostic logic and calculations
- `Reflection_Agent`: Assess diagnostic trajectory, propose refinements
- `Summary_Agent`: Generate concise diagnostic reports
- `Resolution_Agent`: Recommend corrective actions
- `Modification_Agent`: Correct errors in prior reasoning

### 6. Implementation Priorities
Add phased implementation guidance:

**Phase 0 (Current - Blocked on API):**
- Design agent schemas (input/output structures)
- Document agent roles and capabilities
- Create logging infrastructure (even if not yet collecting data)
- Draft reward function specification

**Phase 1 (API Access Available):**
- Implement first 3-5 agents with standardized I/O
- Build static n8n workflows with instrumentation
- Begin logging diagnostic episodes
- Manual validation of agent outputs

**Phase 2 (After 50+ Episodes Logged):**
- Analyze logged patterns
- Implement rule-based router based on patterns
- A/B test against static workflows
- Refine agent prompts based on outcomes

**Phase 3 (After 200+ Episodes):**
- Prepare training data for RL
- Implement policy model (fine-tuned small LLM or gradient-based)
- Train orchestrator offline
- Deploy with human-in-loop validation

**Phase 4 (Production RL):**
- Online learning from production outcomes
- Continuous policy refinement
- Automated agent pruning/promotion
- Multi-objective optimization (accuracy/cost/speed)

### 7. Critical Don'ts
Add warnings about what NOT to do:

**Don't:**
- Jump to RL implementation before having logged data
- Hardcode agent sequences into prompts (keep routing external)
- Skip instrumentation "for now" (you'll never add it later)
- Design agents that assume specific predecessors
- Optimize prematurely (get working system first)
- Sacrifice debuggability for sophistication
- Forget that n8n visual workflows are a feature, not a limitation

**Do:**
- Keep current n8n approach for Phase 0-1
- Design with future RL in mind (stateless, instrumented)
- Start simple, evolve based on data
- Validate every agent output initially
- Build tooling to visualize agent sequences
- Document assumptions about reward function
- Plan for human override mechanisms

### 8. Integration with Existing SkySpark Project
Reference existing project structure:

**Related Files:**
- Project instructions: `C:\Users\mcoalson\Documents\WorkPath\Project-Specific-Instructions\SkySpark-n8n-Workflow.md`
- n8n workflows: `C:\Users\mcoalson\Documents\WorkPath\n8n\`
- Skills: `C:\Users\mcoalson\Documents\WorkPath\.claude\skills\n8n-automation\`

**Ensure Compatibility:**
- Agent design aligns with existing FastAPI tool server architecture
- Logging integrates with n8n execution data
- State schema accommodates SkySpark Haystack data model
- Reward function maps to ComEd program requirements (diagnostic accuracy)

### 9. Success Metrics
Add measurable goals for each phase:

**Phase 1 Success:**
- [ ] 5+ agents implemented with standardized I/O
- [ ] 100% of diagnostic episodes logged with schema
- [ ] Static workflow resolves 70%+ of test alerts correctly

**Phase 2 Success:**
- [ ] Rule-based router handles 80%+ of alert types
- [ ] 10% reduction in average tokens vs. static workflow
- [ ] Diagnostic accuracy maintained or improved

**Phase 3 Success:**
- [ ] RL policy trained on 200+ episodes
- [ ] RL orchestrator matches or exceeds rule-based accuracy
- [ ] 20%+ token reduction vs. static baseline
- [ ] Cyclic reasoning patterns emerge for complex diagnostics

**Phase 4 Success:**
- [ ] Online learning maintains 90%+ diagnostic accuracy
- [ ] 30%+ token reduction vs. baseline
- [ ] System handles novel alert types through adaptation
- [ ] Human intervention required <10% of cases

### 10. Open Questions to Address
Document uncertainties for future resolution:

1. **State Representation:** What specific fields belong in `DiagnosticState`?
2. **Agent Granularity:** How fine-grained should agent specialization be?
3. **Training Data Volume:** Is 200 episodes sufficient for SkySpark domain?
4. **Policy Model Size:** What size LLM needed for routing decisions?
5. **Multi-Objective Weights:** How to balance accuracy/cost/speed for different alert severities?
6. **Human Feedback Loop:** How to incorporate FM corrections into RL training?
7. **Deployment Strategy:** Blue-green deployment for policy updates?

## Action Items
When this prompt is used, Claude should:

1. **Read Current Skill:** Load `C:\Users\mcoalson\Documents\WorkPath\.claude\skills\n8n-automation\SKILL.md`

2. **Read Research Paper:** Load `C:\Users\mcoalson\Documents\WorkPath\Resources\research-papers\Puppeteer-Multi-Agent-Orchestration-NeurIPS-2025.md`

3. **Update Skill Content:** Integrate the above requirements into the n8n-automation skill, preserving existing content but adding:
   - "Agent Architecture for Future RL" section
   - "Orchestration Evolution Roadmap" section  
   - "Instrumentation & Logging Requirements" section
   - "SkySpark Agent Taxonomy" section
   - Updated examples showing stateless agent design

4. **Maintain Backward Compatibility:** Ensure updates don't invalidate current Phase 0 approach

5. **Save Updated Skill:** Write updated content back to skill file

6. **Create Summary:** Provide 3-5 sentence summary of key changes made

## Expected Outcome
The updated n8n-automation skill should enable development that:
- Works immediately with static n8n workflows (Phase 0-1)
- Requires minimal refactoring to add rule-based routing (Phase 2)
- Can evolve to RL orchestration with logged data (Phase 3-4)
- Maintains debuggability and practical utility throughout
- Aligns with cutting-edge research while staying grounded in production constraints

## Usage Instructions
Save this prompt as: `C:\Users\mcoalson\Documents\WorkPath\.claude\skills\work-command-center\prompts\update-n8n-for-rl-orchestration.md`

To execute:
```
Claude, please execute the prompt at:
C:\Users\mcoalson\Documents\WorkPath\.claude\skills\work-command-center\prompts\update-n8n-for-rl-orchestration.md
```

Claude will then read necessary files, update the n8n-automation skill, and report changes made.
