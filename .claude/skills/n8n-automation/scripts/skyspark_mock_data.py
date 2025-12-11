#!/usr/bin/env python3
"""
SkySpark Mock Data Generator
Creates realistic mock data for testing n8n workflows before SkySpark API access
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict

def generate_mock_sparks(count: int = 20) -> List[Dict]:
    """
    Generate mock SkySpark sparks for testing
    """
    
    spark_types = [
        "High Energy Consumption",
        "Equipment Offline", 
        "Temperature Setpoint Deviation",
        "Schedule Override Active",
        "Damper Position Stuck",
        "Filter Maintenance Required",
        "Chiller Low Efficiency",
        "AHU Fan Speed Anomaly"
    ]
    
    equipment_types = ["AHU", "VAV", "Chiller", "Boiler", "RTU", "FCU"]
    severities = ["Critical", "High", "Medium", "Low"]
    
    sparks = []
    base_time = datetime.now()
    
    for i in range(count):
        spark = {
            "id": f"spark_{i+1:03d}",
            "timestamp": (base_time - timedelta(hours=random.randint(1, 72))).isoformat(),
            "type": random.choice(spark_types),
            "equipment": f"{random.choice(equipment_types)}-{random.randint(1, 50):02d}",
            "severity": random.choice(severities),
            "description": f"Automated detection of {random.choice(spark_types).lower()} on equipment",
            "building": f"Building {chr(65 + random.randint(0, 4))}",
            "zone": f"Zone {random.randint(1, 10)}",
            "energy_impact": random.uniform(0.1, 50.0),  # kWh/day
            "cost_impact": random.uniform(5, 500),  # $/month
            "confidence": random.uniform(0.6, 0.95)
        }
        sparks.append(spark)
    
    return sparks

def save_mock_data(sparks: List[Dict], filename: str = "mock_sparks.json"):
    """Save mock sparks to JSON file"""
    with open(filename, 'w') as f:
        json.dump(sparks, f, indent=2)
    print(f"Saved {len(sparks)} mock sparks to {filename}")

if __name__ == "__main__":
    # Generate and save mock data
    mock_sparks = generate_mock_sparks(20)
    save_mock_data(mock_sparks)
    
    # Print sample for verification
    print("\nSample mock spark:")
    print(json.dumps(mock_sparks[0], indent=2))
