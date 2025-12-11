#!/usr/bin/env python3
"""
SkySpark Axon Query Builder
Generates common SkySpark/Axon queries for building analytics
"""

def build_trend_query(site_name, point_filter, time_range="today"):
    """
    Build Axon query for trending data
    
    Args:
        site_name: Building/site identifier
        point_filter: Point filter criteria
        time_range: Time range for data (default: today)
    """
    
    query = f"""
    readAll(site and dis=="{site_name}")
    .readAll(point and {point_filter})
    .hisRead({time_range})
    """
    
    return query.strip()

def build_equipment_query(equip_type, site_name=None):
    """
    Build query to find equipment of specific type
    """
    base_query = f"readAll(equip and {equip_type})"
    
    if site_name:
        base_query = f'readAll(site and dis=="{site_name}").readAll(equip and {equip_type})'
    
    return base_query

# Example queries
if __name__ == "__main__":
    # Example AHU temperature trend query
    ahu_temp_query = build_trend_query(
        "Building A", 
        "ahu and air and temp and sensor",
        "pastWeek"
    )
    print("AHU Temperature Trend Query:")
    print(ahu_temp_query)
