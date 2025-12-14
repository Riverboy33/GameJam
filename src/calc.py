from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class BuildingDef:
    id: str
    name: str
    base_cost: float
    cps: float

BUILDINGS = [
    BuildingDef("cursor", "Cursor", base_cost=15, cps=1.0),
    BuildingDef("bouteille", "Bouteille", base_cost=50, cps=10.0),
    BuildingDef("arrosoir", "Arrosoir", base_cost=200, cps=20.0),
    BuildingDef("serre", "Serre", base_cost=750, cps=40.0),
]

COST_MULTIPLIER = 1.15

def building_cost(building_id: str, current_count: int) -> float:
    building = next((b for b in BUILDINGS if b.id == building_id), None)
    if not building:
        return 0
    return building.base_cost * (COST_MULTIPLIER ** current_count)

def calc_cps(state: Dict, upgrade_manager=None) -> float:
    buildings = state.get("buildings", {})
    total_cps = 0.0

    for building_def in BUILDINGS:
        count = buildings.get(building_def.id, 0)
        total_cps += building_def.cps * count

    if upgrade_manager:
        effects = upgrade_manager.apply_upgrades(state)
        total_cps *= effects.get("cps_multiplier", 1.0)

    return total_cps
