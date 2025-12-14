from dataclasses import dataclass


@dataclass
class UpgradeDef:
    key: str
    name: str
    description: str
    cost: float
    effect_type: str
    effect_value: float
    target: str = None


UPGRADES = [
    UpgradeDef(
        key="reinforced_cursor",
        name="Curseur renforcé",
        description="Double la production des curseurs",
        cost=500,
        effect_type="building_boost",
        effect_value=2.0,
        target="cursor"
    ),
    UpgradeDef(
        key="golden_touch",
        name="Touche dorée",
        description="Les clics donnent +5 cookies",
        cost=1000,
        effect_type="click_multiplier",
        effect_value=5.0
    ),
    UpgradeDef(
        key="grandma_wisdom",
        name="Sagesse de mamie",
        description="Double la production des mamies",
        cost=5000,
        effect_type="building_boost",
        effect_value=2.0,
        target="grandma"
    ),
    UpgradeDef(
        key="productivity_boost",
        name="Boost de productivité",
        description="Augmente la production globale de 10%",
        cost=50000,
        effect_type="cps_multiplier",
        effect_value=1.1
    ),
]

class UpgradeManager:
    def __init__(self):
        self.purchased = set()

    def is_purchased(self, upgrade_key: str) -> bool:
        return upgrade_key in self.purchased

    def purchase(self, upgrade_key: str):
        self.purchased.add(upgrade_key)

    def get_available_upgrades(self) -> list:
        return [u for u in UPGRADES if u.key not in self.purchased]

    def apply_upgrades(self, state: dict) -> dict:
        click_mult = 1.0
        cps_mult = 1.0
        building_mults = {}

        for upgrade in UPGRADES:
            if upgrade.key in self.purchased:
                if upgrade.effect_type == "click_multiplier":
                    click_mult += upgrade.effect_value
                elif upgrade.effect_type == "cps_multiplier":
                    cps_mult *= upgrade.effect_value
                elif upgrade.effect_type == "building_boost":
                    if upgrade.target not in building_mults:
                        building_mults[upgrade.target] = 1.0
                    building_mults[upgrade.target] *= upgrade.effect_value

        return {
            "click_multiplier": click_mult,
            "cps_multiplier": cps_mult,
            "building_multipliers": building_mults
        }

    def to_dict(self) -> dict:
        return {"purchased": list(self.purchased)}

    def from_dict(self, data: dict):
        self.purchased = set(data.get("purchased", []))