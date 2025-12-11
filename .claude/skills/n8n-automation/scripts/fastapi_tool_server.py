#!/usr/bin/env python3
"""
FastAPI Tool Server Template for n8n Integration
Template for creating tool servers that n8n AI agents can call
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import uvicorn

app = FastAPI(title="Building Analytics Tool Server", version="1.0.0")

class EnergyCalculationRequest(BaseModel):
    """Request model for energy calculations"""
    building_area: float
    fuel_type: str
    efficiency: float
    annual_usage: float

class CalculationResponse(BaseModel):
    """Response model for calculations"""
    annual_cost: float
    annual_emissions: float
    savings_potential: float

@app.post("/calculate/energy-cost", response_model=CalculationResponse)
async def calculate_energy_cost(request: EnergyCalculationRequest):
    """
    Calculate annual energy costs and potential savings
    """
    try:
        # Simplified calculation - replace with actual formulas
        fuel_rates = {
            "natural_gas": 0.95,  # per therm
            "electricity": 0.12,  # per kWh
            "propane": 2.50      # per gallon
        }
        
        rate = fuel_rates.get(request.fuel_type, 0.12)
        annual_cost = request.annual_usage * rate
        
        # Calculate potential savings (simplified)
        baseline_efficiency = 0.80
        savings_potential = annual_cost * (1 - request.efficiency / baseline_efficiency)
        
        # Emissions calculation (simplified)
        emission_factors = {
            "natural_gas": 11.7,  # lbs CO2 per therm
            "electricity": 0.85,  # lbs CO2 per kWh
            "propane": 12.7      # lbs CO2 per gallon
        }
        
        emission_factor = emission_factors.get(request.fuel_type, 0.85)
        annual_emissions = request.annual_usage * emission_factor
        
        return CalculationResponse(
            annual_cost=round(annual_cost, 2),
            annual_emissions=round(annual_emissions, 2),
            savings_potential=round(savings_potential, 2)
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Building Analytics Tool Server"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
