# n8n Workflow Setup Guide - Phase 0

This guide walks through setting up the AI Agent workflow in n8n to call your tool server.

## Prerequisites

- n8n running in Docker
- Tool server running (`python tool_server.py`)
- OpenAI API key (or Anthropic key if you prefer Claude)

## Step 1: Start the Tool Server

Open a terminal and run:

```bash
cd C:\Users\mcoalson\Documents\WorkPath\.claude\skills\n8n-automation\scripts
pip install -r requirements.txt
python tool_server.py
```

Verify it's running: http://localhost:8000/docs

**Docker Note:** If n8n is in Docker and tool server is on host, use `host.docker.internal:8000` instead of `localhost:8000` in n8n.

## Step 2: Create the Workflow in n8n

### 2.1 Create New Workflow

1. Open n8n (usually http://localhost:5678)
2. Click "Add workflow" 
3. Name it: "SkySpark Spark Triage Agent"

### 2.2 Add Chat Trigger Node

1. Click + to add node
2. Search "Chat Trigger" → add it
3. This gives you a chat interface to test

### 2.3 Add AI Agent Node

1. Click + after Chat Trigger
2. Search "AI Agent" → add it
3. Configure:
   - **Chat Model**: Add OpenAI credential, select gpt-4 or gpt-3.5-turbo
   - **System Message**:
   
```
You are a building automation analyst. You help engineers understand and prioritize SkySpark alerts (sparks).

You have access to tools that let you:
1. List current sparks from building systems
2. Get a prioritized/triaged list of sparks
3. Look up details on specific sparks
4. Calculate energy savings from fixing issues
5. Calculate payback periods for improvements

When asked about building issues or sparks:
- First get the triaged list to see what's most important
- Explain the top issues clearly
- Calculate potential savings when relevant
- Recommend actions based on priority and ROI

Be concise but thorough. Use specific numbers from the data.
```

### 2.4 Add HTTP Request Tool (List Sparks)

1. In AI Agent node, click "Add Tool"
2. Select "HTTP Request Tool"
3. Configure:
   - **Name**: `list_sparks`
   - **Description**: `Get list of current sparks (alerts) from building systems. Can filter by severity (Critical, High, Medium, Low) or building name.`
   - **Method**: GET
   - **URL**: `http://host.docker.internal:8000/sparks/list`
   - **Send Query Parameters**: Define
     - `severity` (string, optional): Filter by severity level
     - `building` (string, optional): Filter by building name
     - `limit` (number, optional): Max results (default 50)

### 2.5 Add HTTP Request Tool (Triage Sparks)

1. Add another HTTP Request Tool
2. Configure:
   - **Name**: `triage_sparks`
   - **Description**: `Get prioritized list of sparks sorted by importance. Returns top sparks with priority scores and reasoning.`
   - **Method**: GET
   - **URL**: `http://host.docker.internal:8000/sparks/triage`
   - **Send Query Parameters**: Define
     - `limit` (number, optional): Number of top sparks to return (default 10)

### 2.6 Add HTTP Request Tool (Get Spark Details)

1. Add another HTTP Request Tool
2. Configure:
   - **Name**: `get_spark`
   - **Description**: `Get detailed information about a specific spark by its ID (e.g., spark_001)`
   - **Method**: GET  
   - **URL**: `http://host.docker.internal:8000/sparks/{{ $json.spark_id }}`
   - **Placeholder Fields**:
     - `spark_id` (string, required): The spark ID to look up

### 2.7 Add HTTP Request Tool (Calculate Savings)

1. Add another HTTP Request Tool
2. Configure:
   - **Name**: `calculate_energy_savings`
   - **Description**: `Calculate annual energy and cost savings from fixing an issue. Provide the daily kWh waste.`
   - **Method**: POST
   - **URL**: `http://host.docker.internal:8000/calculate/energy-savings`
   - **Body Content Type**: JSON
   - **Body Parameters**:
     - `issue_type` (string): Type of issue
     - `current_waste_kwh_day` (number): Daily energy waste in kWh
     - `equipment_type` (string): Equipment type (AHU, VAV, etc.)
     - `fix_effectiveness` (number, default 0.85): Expected fix effectiveness 0-1

### 2.8 Add HTTP Request Tool (Calculate Payback)

1. Add another HTTP Request Tool
2. Configure:
   - **Name**: `calculate_payback`
   - **Description**: `Calculate simple payback period for an improvement. Provide implementation cost and annual savings.`
   - **Method**: POST
   - **URL**: `http://host.docker.internal:8000/calculate/payback`
   - **Body Content Type**: JSON
   - **Body Parameters**:
     - `implementation_cost` (number): Cost to implement fix in USD
     - `annual_savings` (number): Expected annual savings in USD

## Step 3: Test the Workflow

1. Click "Chat" in the Chat Trigger node
2. Try these prompts:

**Basic:**
```
What are the current building alerts?
```

**With Triage:**
```
What are the top 5 priority issues I should focus on?
```

**With Analysis:**
```
Show me the highest priority spark and calculate how much we'd save by fixing it.
```

**Complex:**
```
I have $5000 budget for building improvements. What should I prioritize based on current issues and ROI?
```

## Troubleshooting

### "Connection refused" errors
- Make sure tool_server.py is running
- If n8n is in Docker, use `host.docker.internal:8000` not `localhost:8000`
- Check firewall isn't blocking port 8000

### Agent not using tools
- Check tool descriptions are clear
- Make sure the system prompt mentions the tools
- Try being explicit: "Use the triage_sparks tool to..."

### Empty responses
- Check http://localhost:8000/sparks/list returns data
- Verify the mock data is loading (restart tool server)

## Next Steps (Phase 1)

Once this is working:
1. Expand mock data with more realistic scenarios
2. Add triage agent logic (separate sub-workflow)
3. Build HVAC specialist tool with domain knowledge
4. Add memory/context for multi-turn analysis

---

Last Updated: 2025-11-29
