import os
import json
import time

SAVE_PATH = os.path.join(os.path.dirname(__file__), "save.json")

def save_state(state: dict) -> None:
    data = {
        "coins": state["coins"],
        "click_power": state["click_power"],
        "buildings": state["buildings"],
        "last_ts": time.time(),
    }
    tmp_path = SAVE_PATH + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, SAVE_PATH)


def reset_save() -> None:
    if os.path.exists(SAVE_PATH):
        os.remove(SAVE_PATH)
