import pygame
import os

class assethandler:
    def __init__(self):
        self.assets = {}

    def init(self):
        asset_dir = "./src/Asset/ClickButton"

        if os.path.exists(asset_dir):
            for filename in os.listdir(asset_dir):
                if filename.endswith('.png'):
                    asset_name = filename[:-4]
                    path = os.path.join(asset_dir, filename)
                    try:
                        loaded = pygame.image.load(path)
                        self.assets[asset_name] = loaded
                    except Exception as e:
                        print(f"Failed to load {path}: {e}")

        return self

    def get(self, name: str):
        return self.assets.get(name, None)
