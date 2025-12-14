from dataclasses import dataclass
from typing import Dict, Optional

@dataclass
class BuildingDef:
    id: str
    name: str
    base_cost: float
    cps: float

BUILDINGS = [
    # Replaced with simple case_* buildings per request
    BuildingDef("case_arrosoir", "Arrosoir", base_cost=10, cps=2.0),
    BuildingDef("case_engrais", "Engrais", base_cost=20, cps=3.0),
    BuildingDef("case_serre", "Serre", base_cost=30, cps=4.0),
    BuildingDef("case_abeille", "Abeilles", base_cost=40, cps=4.0),
]

def building_cost(building_id: str, current_count: int) -> float:
    """Return the cost for purchasing one more of `building_id`.

    Costs are fixed per piece (no exponential multiplier) as requested.
    """
    building = next((b for b in BUILDINGS if b.id == building_id), None)
    if not building:
        return 0
    return building.base_cost

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
