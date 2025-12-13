import pygame.image


class assethandler:
    def __init__(self):
        self.tree_test = "./src/Asset/ClickButton/test_tree.png"

    def get(self, name):
        if self.__getattribute__(name):
            return self.__getattribute__(name)
        else:
            print("Res : ", name, " failed to load .")
            return None

    def init(self):
        AH = assethandler()
        for name, path in self.__dict__.items():
            try:
                loaded = pygame.image.load(path)
                AH.__setattr__(name, loaded)
                print("Successfully load ressource : ", path)
            except pygame.error as e:
                print("[ERROR]: (from asset.py)",e)
                exit(84)
        return AH