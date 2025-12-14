import pygame
import os

class assethandler:
    def __init__(self):
        self.assets = {}

    def init(self):
        asset_dir = "./src/Asset/ClickButton"

        if os.path.exists(asset_dir):
            for filename in os.listdir(asset_dir):
                if filename.lower().endswith('.png'):
                    asset_name = os.path.splitext(filename)[0]
                    key = asset_name.lower()
                    path = os.path.join(asset_dir, filename)
                    try:
                        # Load the image without forcing a display-dependent convert.
                        # convert()/convert_alpha() require a display surface; calling them
                        # here can fail if assets are loaded before display.set_mode().
                        loaded = pygame.image.load(path)
                        self.assets[key] = loaded
                    except Exception as e:
                        print(f"Failed to load {path}: {e}")

        return self

    def get(self, name: str):
        return self.assets.get(name, None)
