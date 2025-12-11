#!/usr/bin/env python3
"""
Building Analytics Tool Server for n8n Multi-Agent System
Phase 0: Foundation - Local development with mock data

Run with: uvicorn tool_server:app --reload --port 8000
Or: python tool_server.py
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timedelta
from enum import Enum
import random
import uvicorn

# ============================================================================
# API SETUP
# ============================================================================

app = FastAPI(
    title="SkySpark Analytics Tool Server",
    description="""
    Tool server for n8n AI agents to analyze building automation data.
    
    **Available Tools:**
    - /sparks/list - Get current sparks (alerts) from building systems
    - /sparks/triage - Prioritize sparks by severity and cost impact
    - /sparks/{id} - Get detailed info on a specific spark
    - /calculate/energy-savings - Estimate savings from fixing an issue
    - /calculate/payback - Calculate simple payback period
    
    **Phase 0:** Using mock data. Phase 2+ will connect to live SkySpark.
    """,
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# DATA MODELS
# ============================================================================

class Severity(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class SparkType(str, Enum):
    HIGH_ENERGY = "High Energy Consumption"
    EQUIPMENT_OFFLINE = "Equipment Offline"
    TEMP_DEVIATION = "Temperature Setpoint Deviation"
    SCHEDULE_OVERRIDE = "Schedule Override Active"
    DAMPER_STUCK = "Damper Position Stuck"
    FILTER_MAINTENANCE = "Filter Maintenance Required"
    CHILLER_EFFICIENCY = "Chiller Low Efficiency"
    FAN_ANOMALY = "AHU Fan Speed Anomaly"
    SIMULTANEOUS_HC = "Simultaneous Heating and Cooling"
    ECONOMIZER_FAULT = "Economizer Not Operating"

class Spark(BaseModel):
    id: str = Field(..., description="Unique spark identifier")
    timestamp: str = Field(..., description="When the spark was generated")
    type: SparkType = Field(..., description="Category of the issue")
    equipment: str = Field(..., description="Equipment tag (e.g., AHU-01)")
    severity: Severity = Field(..., description="Issue severity level")
    description: str = Field(..., description="Human-readable description")
    building: str = Field(..., description="Building name")
    zone: Optional[str] = Field(None, description="Zone or area affected")
    energy_impact_kwh_day: float = Field(..., description="Estimated daily energy waste in kWh")
    cost_impact_month: float = Field(..., description="Estimated monthly cost impact in USD")
    confidence: float = Field(..., description="Detection confidence 0-1")
    recommended_action: str = Field(..., description="Suggested fix")

class TriagedSpark(Spark):
    priority_score: float = Field(..., description="Computed priority 0-100")
    priority_rank: int = Field(..., description="Rank among all sparks")
    triage_reasoning: str = Field(..., description="Why this priority was assigned")

class EnergySavingsRequest(BaseModel):
    issue_type: str = Field(..., description="Type of issue being fixed")
    current_waste_kwh_day: float = Field(..., description="Current daily energy waste in kWh")
    equipment_type: str = Field(..., description="Type of equipment")
    fix_effectiveness: float = Field(0.85, description="Expected fix effectiveness 0-1")

class EnergySavingsResponse(BaseModel):
    annual_kwh_savings: float
    annual_cost_savings: float
    annual_co2_reduction_lbs: float
    assumptions: str

class PaybackRequest(BaseModel):
    implementation_cost: float = Field(..., description="Cost to implement the fix in USD")
    annual_savings: float = Field(..., description="Expected annual savings in USD")

class PaybackResponse(BaseModel):
    simple_payback_years: float
    recommendation: str

# ============================================================================
# MOCK DATA GENERATOR
# ============================================================================

RECOMMENDED_ACTIONS = {
    SparkType.HIGH_ENERGY: "Review operating schedules and setpoints. Check for simultaneous heating/cooling.",
    SparkType.EQUIPMENT_OFFLINE: "Verify network connectivity. Check for tripped breakers or safety faults.",
    SparkType.TEMP_DEVIATION: "Inspect zone sensors and recalibrate. Check damper/valve operation.",
    SparkType.SCHEDULE_OVERRIDE: "Review override reason with occupants. Consider schedule adjustment.",
    SparkType.DAMPER_STUCK: "Inspect actuator and linkage. Check for obstructions or actuator failure.",
    SparkType.FILTER_MAINTENANCE: "Replace filters. Check filter rack seal and housing.",
    SparkType.CHILLER_EFFICIENCY: "Check condenser cleanliness, refrigerant charge, and approach temps.",
    SparkType.FAN_ANOMALY: "Check VFD parameters, belt tension, and bearing condition.",
    SparkType.SIMULTANEOUS_HC: "Review deadband settings. Check for valve/damper hunting.",
    SparkType.ECONOMIZER_FAULT: "Verify OA damper operation and sensor calibration.",
}

def generate_mock_sparks(count: int = 25, seed: int = 42) -> List[Spark]:
    random.seed(seed)
    
    equipment_prefixes = ["AHU", "VAV", "RTU", "FCU", "CHW-P", "HW-P", "CT", "CH"]
    buildings = ["Main Campus", "Building A", "Building B", "North Wing", "Data Center"]
    
    sparks = []
    base_time = datetime.now()
    
    for i in range(count):
        spark_type = random.choice(list(SparkType))
        severity = random.choices(
            list(Severity),
            weights=[0.1, 0.25, 0.4, 0.25]
        )[0]
        
        severity_mult = {"Critical": 4, "High": 2.5, "Medium": 1.5, "Low": 1}[severity.value]
        energy_impact = random.uniform(5, 30) * severity_mult
        cost_impact = energy_impact * 30 * 0.10
        
        equipment = f"{random.choice(equipment_prefixes)}-{random.randint(1, 20):02d}"
        
        spark = Spark(
            id=f"spark_{i+1:03d}",
            timestamp=(base_time - timedelta(hours=random.randint(1, 72))).isoformat(),
            type=spark_type,
            equipment=equipment,
            severity=severity,
            description=f"{spark_type.value} detected on {equipment}",
            building=random.choice(buildings),
            zone=f"Zone {random.randint(1, 12)}" if random.random() > 0.3 else None,
            energy_impact_kwh_day=round(energy_impact, 1),
            cost_impact_month=round(cost_impact, 2),
            confidence=round(random.uniform(0.65, 0.98), 2),
            recommended_action=RECOMMENDED_ACTIONS[spark_type]
        )
        sparks.append(spark)
    
    return sparks

MOCK_SPARKS = generate_mock_sparks()

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/", tags=["Info"])
async def root():
    return {
        "service": "SkySpark Analytics Tool Server",
        "version": "0.1.0",
        "phase": "Phase 0 - Mock Data",
        "docs": "/docs"
    }

@app.get("/health", tags=["Info"])
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/sparks/list", response_model=List[Spark], tags=["Sparks"],
         summary="List all current sparks")
async def list_sparks(
    severity: Optional[Severity] = Query(None, description="Filter by severity"),
    building: Optional[str] = Query(None, description="Filter by building"),
    limit: int = Query(50, le=100)
) -> List[Spark]:
    results = MOCK_SPARKS.copy()
    if severity:
        results = [s for s in results if s.severity == severity]
    if building:
        results = [s for s in results if building.lower() in s.building.lower()]
    return results[:limit]

@app.get("/sparks/triage", response_model=List[TriagedSpark], tags=["Sparks"],
         summary="Get prioritized spark list")
async def triage_sparks(limit: int = Query(10, le=50)) -> List[TriagedSpark]:
    severity_weights = {"Critical": 40, "High": 25, "Medium": 15, "Low": 5}
    
    triaged = []
    for spark in MOCK_SPARKS:
        sev_score = severity_weights[spark.severity.value]
        cost_score = min(spark.cost_impact_month / 10, 30)
        conf_score = spark.confidence * 20
        
        type_bonus = 10 if spark.type in [SparkType.EQUIPMENT_OFFLINE, SparkType.SIMULTANEOUS_HC] else 0
        
        priority = min(sev_score + cost_score + conf_score + type_bonus, 100)
        
        reasoning = f"Severity: {spark.severity.value} (+{sev_score}pts) | "
        reasoning += f"Cost: ${spark.cost_impact_month:.0f}/mo (+{cost_score:.0f}pts) | "
        reasoning += f"Confidence: {spark.confidence:.0%} (+{conf_score:.0f}pts)"
        if type_bonus:
            reasoning += f" | Critical type (+{type_bonus}pts)"
        
        triaged.append(TriagedSpark(
            **spark.model_dump(),
            priority_score=round(priority, 1),
            priority_rank=0,
            triage_reasoning=reasoning
        ))
    
    triaged.sort(key=lambda x: x.priority_score, reverse=True)
    for i, s in enumerate(triaged):
        s.priority_rank = i + 1
    
    return triaged[:limit]

@app.get("/sparks/{spark_id}", response_model=Spark, tags=["Sparks"],
         summary="Get spark details")
async def get_spark(spark_id: str) -> Spark:
    for spark in MOCK_SPARKS:
        if spark.id == spark_id:
            return spark
    raise HTTPException(status_code=404, detail=f"Spark {spark_id} not found")

@app.post("/calculate/energy-savings", response_model=EnergySavingsResponse, 
          tags=["Calculations"], summary="Calculate energy savings")
async def calculate_energy_savings(req: EnergySavingsRequest) -> EnergySavingsResponse:
    daily_savings = req.current_waste_kwh_day * req.fix_effectiveness
    annual_kwh = daily_savings * 365
    rate = 0.10
    annual_cost = annual_kwh * rate
    co2_factor = 0.85
    annual_co2 = annual_kwh * co2_factor
    
    return EnergySavingsResponse(
        annual_kwh_savings=round(annual_kwh, 0),
        annual_cost_savings=round(annual_cost, 2),
        annual_co2_reduction_lbs=round(annual_co2, 0),
        assumptions=f"{req.fix_effectiveness:.0%} effectiveness, ${rate}/kWh, {co2_factor} lbs CO2/kWh"
    )

@app.post("/calculate/payback", response_model=PaybackResponse,
          tags=["Calculations"], summary="Calculate payback period")
async def calculate_payback(req: PaybackRequest) -> PaybackResponse:
    if req.annual_savings <= 0:
        raise HTTPException(status_code=400, detail="Annual savings must be positive")
    
    payback = req.implementation_cost / req.annual_savings
    
    if payback < 1:
        rec = "Excellent ROI - implement immediately"
    elif payback < 2:
        rec = "Strong ROI - high priority"
    elif payback < 5:
        rec = "Good ROI - include in planned maintenance"
    elif payback < 10:
        rec = "Moderate ROI - consider bundling"
    else:
        rec = "Long payback - may not be cost-effective standalone"
    
    return PaybackResponse(simple_payback_years=round(payback, 2), recommendation=rec)

# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("SkySpark Analytics Tool Server - Phase 0")
    print("="*60)
    print("API Docs:  http://localhost:8000/docs")
    print("Sparks:    http://localhost:8000/sparks/list")
    print("Triage:    http://localhost:8000/sparks/triage")
    print("="*60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
