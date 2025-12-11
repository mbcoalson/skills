# SkySpark Multi-Agent System - Architecture

## Overview

Multi-agent automation system using n8n to triage and analyze SkySpark alerts, reducing manual review time for energy engineers.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         n8n Workflow                            │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │  Chat    │───▶│    AI    │───▶│   HTTP   │───▶│ Response │  │
│  │ Trigger  │    │  Agent   │    │ Request  │    │          │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FastAPI Tool Server                          │
│                  (Translation Layer)                            │
│                                                                 │
│  • Authentication handling                                      │
│  • Query translation (agent intent → API calls)                 │
│  • Response formatting (API responses → agent-friendly)         │
│  • Fallback logic (SkySpark vs Python)                         │
└─────────────────────────┬───────────────────────────────────────┘
                          │
            ┌─────────────┴─────────────┐
            ▼                           ▼
┌───────────────────────┐   ┌───────────────────────┐
│   Haystack REST API   │   │   Python Calculations │
│     (PREFERRED)       │   │     (FALLBACK)        │
│                       │   │                       │
│ • Project Haystack    │   │ • Energy savings      │
│   protocol            │   │ • Payback calcs       │
│ • eval endpoint for   │   │ • Simple conversions  │
│   Axon functions      │   │ • Utilities           │
│ • Sparks, trends,     │   │                       │
│   equipment data      │   │ Use when:             │
└───────────┬───────────┘   │ • SkySpark offline    │
            │               │ • Function not in Axon│
            ▼               │ • Quick prototyping   │
┌───────────────────────┐   └───────────────────────┘
│      SkySpark         │
│                       │
│ • Vetted Axon funcs   │
│ • Energy calculations │
│ • Equipment analysis  │
│ • All math happens    │
│   HERE when possible  │
└───────────────────────┘
```

## Design Principles

### 1. SkySpark-First Calculations
All energy calculations and analysis should use vetted Axon functions when available. Python calculations are fallback only.

**Why:**
- Axon functions are already vetted and trusted
- Keeps calculation logic in one place
- Leverages SkySpark's building data directly
- Easier to maintain and audit

### 2. Tool Server as Thin Wrapper
The FastAPI server's job is translation, not computation:
- Translate agent requests into Haystack API calls - (Python tool for consistent formatting, agent just has to specify input variable of )
- Handle authentication
- Format responses for agent consumption
- Route to Python fallback when needed

### 3. Mock Data Mirrors Reality
During development (Phases 0-1), mock data should match actual Haystack response formats so agent behavior stays consistent when switching to live data.

## Endpoint Strategy

### Phase 0-1 (Mock Data)
| Endpoint | Source | Purpose |
|----------|--------|---------|
| `/sparks/list` | Mock JSON | List active sparks |
| `/sparks/triage` | Python scoring | Prioritize sparks |
| `/sparks/{id}` | Mock JSON | Spark details |
| `/calculate/energy-savings` | Python | Estimate savings |
| `/calculate/payback` | Python | ROI calculation |

### Phase 2+ (Live SkySpark)
| Endpoint | Source | Purpose |
|----------|--------|---------|
| `/sparks/list` | Haystack API | Live sparks from SkySpark |
| `/sparks/triage` | Axon function | Prioritization logic in SkySpark |
| `/sparks/{id}` | Haystack API | Live spark details |
| `/axon/eval` | Haystack eval | Run any vetted Axon function |
| `/calculate/energy-savings` | Python (fallback) | Use if no Axon equivalent |
| `/calculate/payback` | Python (fallback) | Use if no Axon equivalent |

## Haystack API Integration

### Authentication
TBD - Waiting on API credentials from coding lead

### Key Endpoints
- `read` - Query records by filter
- `hisRead` - Get trend/history data  
- `eval` - Execute Axon expressions/functions
- `nav` - Navigate site structure

### Data Formats
- ZINC (legacy) - Text-based Haystack format
- JSON (preferred) - Standard JSON with Haystack type markers

## Axon Function Integration

### Pattern for Calling Axon
```python
# Tool server endpoint
@app.post("/axon/eval")
async def eval_axon(function_name: str, params: dict):
    # 1. Build Axon expression
    # 2. Call Haystack eval endpoint
    # 3. Parse response
    # 4. Return formatted result
```

### Functions to Integrate (TBD Monday)
- [ ] List to be provided
- [ ] Document inputs/outputs for each
- [ ] Create mock responses matching real format

## Multi-Agent Pattern (Phase 3+)

```
User Request → Gatekeeper Agent (routes by intent)
                        ↓
        ┌───────────────┼───────────────┬──────────────┐
        ↓               ↓               ↓              ↓
    Triage          HVAC            Energy         Report
    Agent           Specialist      Calc Agent     Generator
        ↓               ↓               ↓              ↓
        └───────────────┴───────────────┴──────────────┘
                        ↓
                Synthesized Response
```

Each specialist can call different Axon functions relevant to their domain.

---

Last Updated: 2025-11-29
