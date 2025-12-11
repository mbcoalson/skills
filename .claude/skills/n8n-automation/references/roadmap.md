# SkySpark Multi-Agent Project Roadmap

## Current Status: Phase 0 - COMPLETE ✅
**Last Updated:** 2025-11-29

---

## Phase 0: Foundation ✅ COMPLETE
**Goal:** Basic tool server and agent interaction

### Completed
- [x] FastAPI tool server with mock data (`tool_server.py`)
- [x] Spark listing and filtering endpoints
- [x] Triage endpoint with priority scoring
- [x] Energy savings calculator (Python fallback)
- [x] Payback calculator (Python fallback)
- [x] n8n workflow setup guide
- [x] n8n workflow with AI Agent calling tools
- [x] End-to-end test: chat → agent → tool → response ✅

### Demo Achieved
Asked: "What are the top priority building issues?"
Got: Prioritized list with costs, equipment IDs, and recommended actions

---

## Phase 1: Mock Integration (NEXT)
**Goal:** Build agent logic with realistic mock data

### Tasks
- [ ] Get list of Axon functions to integrate (Monday)
- [ ] Create mock responses matching real Haystack format
- [ ] Expand mock spark scenarios (realistic buildings/equipment)
- [ ] Add more tools to n8n workflow
- [ ] Test multi-turn conversations

### Key Decision
- Mock data should mirror actual SkySpark/Haystack response format
- Agent behavior stays consistent when switching to live data

---

## Phase 2: Real SkySpark Connection
**Goal:** Live SkySpark integration via Haystack API

### Tasks
- [ ] Obtain Haystack API credentials
- [ ] Implement authentication in tool server
- [ ] Add Haystack client (read, hisRead, eval endpoints)
- [ ] Create `/axon/eval` endpoint to call vetted functions
- [ ] Replace mock sparks with live data
- [ ] Handle ZINC/JSON parsing
- [ ] Error handling for API failures

### Blocker
API credentials - Check with coding lead Monday

### Architecture Note
- Primary: Call Axon functions via Haystack `eval`
- Fallback: Python calculations when Axon unavailable

---

## Phase 3: Multi-Agent Coordination
**Goal:** Full specialist orchestration

### Tasks
- [ ] Gatekeeper routing logic
- [ ] HVAC specialist sub-workflow (calls HVAC-specific Axon functions)
- [ ] Energy calculation specialist
- [ ] Agent-to-agent communication
- [ ] Report generator

---

## Phase 4: Production Readiness
**Goal:** Reliable deployment

### Tasks
- [ ] Error handling and logging
- [ ] Human-in-the-loop approval steps
- [ ] Scheduled runs (daily spark digest)
- [ ] Email/Slack notifications
- [ ] Deployment to SkySpark server

---

## Quick Reference

### Tool Server
```bash
cd .claude/skills/n8n-automation/scripts
pip install -r requirements.txt
python tool_server.py
# http://localhost:8000/docs
```

### n8n Docker
```bash
docker ps  # Container: n8n
# http://localhost:5678
```

### Network (n8n → Tool Server)
Use `http://host.docker.internal:8000` from inside n8n

### Key Files
| File | Purpose |
|------|---------|
| `scripts/tool_server.py` | FastAPI server |
| `references/architecture.md` | System design |
| `references/n8n_workflow_setup.md` | n8n config guide |
| `references/roadmap.md` | This file |

---

## Monday Prep

### Get from Coding Lead
1. Haystack API credentials / how to create them
2. Base URL for SkySpark API

### Document from SkySpark
1. List of Axon functions to expose to agent
2. Input parameters for each function
3. Return format / sample responses
4. Any existing REST endpoints already exposed

---

## Session Log

### 2025-11-29 (Saturday Night)
- Created enhanced tool_server.py with 5 endpoints
- Set up n8n workflow with Chat Trigger → AI Agent → HTTP Request Tool
- Verified Docker networking (host.docker.internal works)
- Tested end-to-end: agent successfully triaged mock sparks
- Clarified architecture: SkySpark/Axon first, Python fallback
- Created architecture.md documenting design decisions
- **Phase 0 complete!**
