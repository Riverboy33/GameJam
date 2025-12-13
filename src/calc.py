from dataclasses import dataclass

@dataclass
class BuildingDef:
    key: str
    name: str
    base_cost: float
    cps: float
    cost_mult: float = 1.15


BUILDINGS = [
    BuildingDef("cursor", "Curor", base_cost=15, cps=0.1),
    BuildingDef("grandma", "Mamie", base_cost=100, cps=1.0),
    BuildingDef("farm", "Ferme", base_cost=1100, cps=8.0),
    BuildingDef("factory", "Usine", base_cost=13000, cps=47.0),
]

def calc_cps(state: dict) -> float:
    total = 0.0
    for b in BUILDINGS:
        qty = int(state["buildings"].get(b.key, 0))
        total += qty * b.cps
    return total


def building_cost(b: BuildingDef, owned: int) -> float:
    return b.base_cost * (b.cost_mult ** owned)


def click_upgrade_cost(click_power: float) -> float:
    level = max(0, int(round(click_power - 1)))
    return 50 * (1.35 ** level)