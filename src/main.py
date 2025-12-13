from dataclasses import dataclass

import json
import math
import os
import time

import pygame
from Class.CookieButton import CookieButton
from Class.UiButton import UiButton
from calc import calc_cps, click_upgrade_cost, building_cost
from save import save_state, reset_save

SAVE_PATH = os.path.join(os.path.dirname(__file__), "save.json")

WIDTH = 1100
HEIGHT = 650
FPS = 60

BG = (18, 18, 22)
PANEL = (28, 28, 34)
PANEL_2 = (35, 35, 44)
ACCENT = (255, 205, 70)
GOOD = (120, 240, 160)
BAD = (255, 120, 120)


TEXT = (235, 235, 240)
MUTED = (170, 170, 180)


@dataclass
class BuildingDef:
    key: str
    name: str
    base_cost: float
    cps: float
    cost_mult: float = 1.15


BUILDINGS = [
    BuildingDef("cursor", "Curseur", base_cost=15, cps=0.1),
    BuildingDef("grandma", "Mamie", base_cost=100, cps=1.0),
    BuildingDef("farm", "Ferme", base_cost=1100, cps=8.0),
    BuildingDef("factory", "Usine", base_cost=13000, cps=47.0),
]


def format_num(x: float) -> str:
    if x < 1000:
        return f"{x:.0f}"
    for suffix, div in (("K", 1e3), ("M", 1e6), ("B", 1e9), ("T", 1e12)):
        if x < div * 1000:
            return f"{x / div:.2f}{suffix}"
    return f"{x:.2e}"


def load_state() -> dict:
    if not os.path.exists(SAVE_PATH):
        return {
            "coins": 0.0,
            "click_power": 1.0,
            "buildings": {b.key: 0 for b in BUILDINGS},
            "last_ts": time.time(),
        }

    try:
        with open(SAVE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        return {
            "coins": 0.0,
            "click_power": 1.0,
            "buildings": {b.key: 0 for b in BUILDINGS},
            "last_ts": time.time(),
        }

    buildings = data.get("buildings") or {}
    for b in BUILDINGS:
        buildings.setdefault(b.key, 0)

    coins = float(data.get("coins", 0.0))
    click_power = float(data.get("click_power", 1.0))
    last_ts = float(data.get("last_ts", time.time()))

    return {
        "coins": coins,
        "click_power": click_power,
        "buildings": buildings,
        "last_ts": last_ts,
    }


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Clicker Pygame")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("segoeui", 20)
    font_big = pygame.font.SysFont("segoeui", 34, bold=True)
    font_title = pygame.font.SysFont("segoeui", 28, bold=True)

    state = load_state()

    cps = calc_cps(state)
    now = time.time()
    offline_dt = max(0.0, min(60 * 60 * 24, now - float(state.get("last_ts", now))))
    if offline_dt > 1.0:
        state["coins"] += cps * offline_dt
    state["last_ts"] = now

    cookie = CookieButton(center=(330, 340), radius=120)

    shop_x = 660
    shop_w = WIDTH - shop_x - 30

    btn_save = UiButton(pygame.Rect(30, 20, 120, 36), "Sauver (S)")
    btn_reset = UiButton(pygame.Rect(160, 20, 120, 36), "Reset (R)")

    running = True
    accum = 0.0
    autosave_t = 0.0

    while running:
        dt = clock.tick(FPS) / 1000.0
        accum += dt
        autosave_t += dt

        cps = calc_cps(state)
        state["coins"] += cps * dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_s:
                    save_state(state)
                    autosave_t = 0.0
                if event.key == pygame.K_r:
                    reset_save()
                    state = load_state()
            if btn_save.handle_event(event):
                save_state(state)
                autosave_t = 0.0
            if btn_reset.handle_event(event):
                reset_save()
                state = load_state()

            if cookie.handle_event(event):
                state["coins"] += float(state["click_power"])

        if autosave_t >= 10.0:
            save_state(state)
            autosave_t = 0.0

        screen.fill(BG)

        pygame.draw.rect(screen, PANEL, pygame.Rect(20, 70, 610, HEIGHT - 90), border_radius=14)
        pygame.draw.rect(screen, PANEL_2, pygame.Rect(shop_x, 70, shop_w, HEIGHT - 90), border_radius=14)

        btn_save.enabled = True
        btn_reset.enabled = True
        btn_save.draw(screen, font)
        btn_reset.draw(screen, font)

        coins = float(state["coins"])
        click_power = float(state["click_power"])

        t1 = font_big.render(f"Pièces: {format_num(coins)}", True, TEXT)
        screen.blit(t1, (50, 90))

        t2 = font.render(f"Par clic: {format_num(click_power)}", True, MUTED)
        screen.blit(t2, (50, 135))

        t3 = font.render(f"CPS: {format_num(cps)} / sec", True, MUTED)
        screen.blit(t3, (50, 160))

        cookie.draw(screen)

        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(50, 510, 540, 2))

        click_cost = click_upgrade_cost(click_power)
        can_buy_click = coins >= click_cost

        click_rect = pygame.Rect(50, 535, 540, 70)
        hover = click_rect.collidepoint(pygame.mouse.get_pos())
        base = (52, 52, 64) if not hover else (70, 70, 88)
        if not can_buy_click:
            base = (40, 40, 48)
        pygame.draw.rect(screen, base, click_rect, border_radius=12)
        pygame.draw.rect(screen, (90, 90, 110), click_rect, width=2, border_radius=12)

        title = font_title.render("Upgrade de clic", True, TEXT if can_buy_click else MUTED)
        screen.blit(title, (click_rect.x + 18, click_rect.y + 10))

        sub = font.render(f"+1 par clic | Coût: {format_num(click_cost)}", True, MUTED)
        screen.blit(sub, (click_rect.x + 18, click_rect.y + 42))

        if pygame.mouse.get_pressed(num_buttons=3)[0] and hover and can_buy_click:
            state["coins"] -= click_cost
            state["click_power"] = click_power + 1.0
            time.sleep(0.09)

        shop_title = font_big.render("Boutique", True, TEXT)
        screen.blit(shop_title, (shop_x + 18, 90))

        y = 140
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed(num_buttons=3)[0]

        for b in BUILDINGS:
            owned = int(state["buildings"].get(b.key, 0))
            cost = building_cost(b, owned)
            can_buy = coins >= cost

            rect = pygame.Rect(shop_x + 18, y, shop_w - 36, 78)
            h = rect.collidepoint(mouse_pos)
            base = (52, 52, 64) if not h else (70, 70, 88)
            if not can_buy:
                base = (40, 40, 48)

            pygame.draw.rect(screen, base, rect, border_radius=12)
            pygame.draw.rect(screen, (90, 90, 110), rect, width=2, border_radius=12)

            name = font_title.render(b.name, True, TEXT if can_buy else MUTED)
            screen.blit(name, (rect.x + 16, rect.y + 10))

            info = font.render(
                f"Possédés: {owned} | +{format_num(b.cps)} CPS chacun | Coût: {format_num(cost)}",
                True,
                MUTED,
            )
            screen.blit(info, (rect.x + 16, rect.y + 44))

            if mouse_pressed and h and can_buy:
                state["coins"] -= cost
                state["buildings"][b.key] = owned + 1
                time.sleep(0.09)

            y += 92

        pygame.display.flip()

    save_state(state)
    pygame.quit()


if __name__ == "__main__":
    main()
