# Node Connection Validation Algorithm

## Problem Statement

EnergyPlus requires that:
1. **Zone Inlet Nodes** (defined in `ZoneHVAC:EquipmentConnections`) must have corresponding **equipment outlet nodes**
2. **Zone Exhaust Nodes** must have corresponding **equipment inlet nodes**
3. Nodes cannot be orphaned - if a zone expects air from a node, some equipment must supply it

## Root Cause of Missed Errors

Current `validate-idf-structure.py` implementation only:
- Collects inlet and outlet node names from object field names
- Counts them
- Does NOT validate zone-to-equipment connections

## Validation Algorithm

### Step 1: Build Node Usage Map

For every object in the IDF, catalog node usage by role:
- Equipment outlets (supplies air to zones)
- Equipment inlets (receives air from zones)
- Zone inlets (where zone receives air)
- Zone exhausts (where zone exhausts air)
- Zone returns (where zone returns air)

### Step 2: Resolve NodeLists

`ZoneHVAC:EquipmentConnections` often references `NodeList` objects, not individual nodes:
```
ZoneHVAC:EquipmentConnections,
  Thermal Zone: Cardio 1,
  ...,
  Thermal Zone: Cardio 1 Inlet Node List,  ! <-- NodeList reference
  ...
```

Must expand NodeList to get actual node names:
```
NodeList,
  Thermal Zone: Cardio 1 Inlet Node List,
  Node 4,        ! <-- Actual node
  Node 183;      ! <-- Actual node
```

### Step 3: Validate Zone Inlet Connections

For each `ZoneHVAC:EquipmentConnections`:
```python
# Get zone inlet nodes (expand NodeLists)
zone_inlet_nodes = expand_nodelist_or_return_single(zone_conn.Zone_Air_Inlet_Node_or_NodeList_Name)

# Check each inlet node has equipment supplying it
for inlet_node in zone_inlet_nodes:
    # Look for this node as an outlet in any equipment:
    # - AirTerminal:* objects (Outlet_Node)
    # - ZoneHVAC:* objects (Air_Outlet_Node)
    # - Coil:* objects (Air_Outlet_Node_Name)
    # - Fan:* objects (Air_Outlet_Node_Name)

    equipment_found = find_equipment_with_outlet_node(inlet_node)

    if not equipment_found:
        ERROR: "ZoneInlet node did not find an outlet node"
```

### Step 4: Validate Zone Exhaust Connections

For each `ZoneHVAC:EquipmentConnections`:
```python
# Get zone exhaust nodes (expand NodeLists)
zone_exhaust_nodes = expand_nodelist_or_return_single(zone_conn.Zone_Air_Exhaust_Node_or_NodeList_Name)

# Check each exhaust node has equipment consuming it
for exhaust_node in zone_exhaust_nodes:
    # Look for this node as an inlet in any equipment:
    # - Fan:ZoneExhaust objects
    # - Other exhaust equipment

    equipment_found = find_equipment_with_inlet_node(exhaust_node)

    if not equipment_found:
        ERROR: "ZoneExhaust node did not find a matching inlet node"
```

### Step 5: Validation Categories

Check these object types for equipment outlet nodes:
- `AirTerminal:SingleDuct:*` → `Air_Outlet_Node_Name`
- `AirTerminal:DualDuct:*` → `Outlet_Node_Name`
- `ZoneHVAC:*` → various outlet field names
- `Coil:*:*` → `Air_Outlet_Node_Name` (when zone equipment)
- `Fan:*` → `Air_Outlet_Node_Name` (when zone equipment)

Check these object types for equipment inlet nodes:
- `Fan:ZoneExhaust` → `Air_Inlet_Node_Name`
- Zone exhaust equipment

## Implementation Strategy

```python
def expand_nodelist(self, nodelist_or_node_name):
    """
    If name references a NodeList, return all nodes in list.
    Otherwise return single node as list.
    """
    if not nodelist_or_node_name:
        return []

    # Check if this is a NodeList
    if 'NodeList' in self.idf.idfobjects:
        for nodelist in self.idf.idfobjects['NodeList']:
            if nodelist.Name == nodelist_or_node_name:
                # Extract all nodes from the NodeList
                nodes = []
                for i in range(1, 600):  # Max nodes
                    node_field = f'Node_{i}_Name'
                    if hasattr(nodelist, node_field):
                        node_val = getattr(nodelist, node_field)
                        if node_val and str(node_val).strip():
                            nodes.append(str(node_val).strip())
                    else:
                        break
                return nodes

    # Not a NodeList, return as single node
    return [nodelist_or_node_name]

def find_equipment_outlet_for_node(self, node_name):
    """
    Search all equipment for this node as an outlet.
    Returns (obj_type, obj_name) or None.
    """
    equipment_types = {
        'AirTerminal:SingleDuct:Uncontrolled': 'Zone_Supply_Air_Node_Name',
        'AirTerminal:SingleDuct:VAV:NoReheat': 'Air_Outlet_Node_Name',
        'AirTerminal:SingleDuct:VAV:Reheat': 'Air_Outlet_Node_Name',
        # ... more equipment types
    }

    for obj_type, outlet_field in equipment_types.items():
        if obj_type in self.idf.idfobjects:
            for obj in self.idf.idfobjects[obj_type]:
                outlet_node = getattr(obj, outlet_field.replace(' ', '_'), None)
                if outlet_node and str(outlet_node) == node_name:
                    return (obj_type, obj.Name)

    return None

def validate_zone_connections(self):
    """
    Validate that all zone inlet/exhaust nodes have matching equipment.
    """
    errors = 0

    if 'ZoneHVAC:EquipmentConnections' not in self.idf.idfobjects:
        return True

    for zone_conn in self.idf.idfobjects['ZoneHVAC:EquipmentConnections']:
        zone_name = zone_conn.Zone_Name

        # Check inlet nodes
        inlet_ref = zone_conn.Zone_Air_Inlet_Node_or_NodeList_Name
        inlet_nodes = self.expand_nodelist(inlet_ref)

        for inlet_node in inlet_nodes:
            equipment = self.find_equipment_outlet_for_node(inlet_node)
            if not equipment:
                self.add_issue('error', 'nodes', 'ZoneHVAC:EquipmentConnections',
                              zone_name, 'Zone_Air_Inlet_Node',
                              f"ZoneInlet node '{inlet_node}' did not find an outlet node")
                errors += 1

        # Check exhaust nodes
        exhaust_ref = zone_conn.Zone_Air_Exhaust_Node_or_NodeList_Name
        if exhaust_ref:
            exhaust_nodes = self.expand_nodelist(exhaust_ref)

            for exhaust_node in exhaust_nodes:
                equipment = self.find_equipment_inlet_for_node(exhaust_node)
                if not equipment:
                    self.add_issue('error', 'nodes', 'ZoneHVAC:EquipmentConnections',
                                  zone_name, 'Zone_Air_Exhaust_Node',
                                  f"ZoneExhaust node '{exhaust_node}' did not find a matching inlet node")
                    errors += 1

    return errors == 0
```

## Expected Results

After implementation, script should detect:
- ✅ All 12+ zone inlet connection errors
- ✅ All 12+ zone exhaust connection errors
- ✅ Match EnergyPlus severe errors exactly

## Equipment Types to Check

**Common Air Terminals:**
- AirTerminal:SingleDuct:Uncontrolled
- AirTerminal:SingleDuct:VAV:NoReheat
- AirTerminal:SingleDuct:VAV:Reheat
- AirTerminal:SingleDuct:SeriesPIU:Reheat
- AirTerminal:SingleDuct:ParallelPIU:Reheat
- AirTerminal:SingleDuct:ConstantVolume:Reheat
- AirTerminal:DualDuct:VAV

**Zone HVAC Equipment:**
- ZoneHVAC:PackagedTerminalAirConditioner
- ZoneHVAC:PackagedTerminalHeatPump
- ZoneHVAC:WaterToAirHeatPump
- ZoneHVAC:FourPipeFanCoil
- ZoneHVAC:WindowAirConditioner
- ZoneHVAC:UnitHeater
- ZoneHVAC:UnitVentilator

**Exhaust Equipment:**
- Fan:ZoneExhaust
