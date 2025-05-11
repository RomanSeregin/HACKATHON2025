import pygame

"""
Simple image drawing cursor that updates in real time to the position of the mouse pointer.
Effectively replaces the default pointer, as there is a texture in the game that corresponds to it.
Makes a custom cursor.
"""
class Cursor:
    _instance = None
    def __new__(cls, imagePath, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, imagePath):
        self.imagePath = imagePath
        self.surface = pygame.image.load(imagePath).convert_alpha()
        self.rect = self.surface.get_rect()

    def move(self, x, y):
        self.rect.topleft = (x, y)

    def updateImage(self, imagePath):
        self.imagePath = imagePath
        self.surface = pygame.image.load(imagePath).convert_alpha()
        self.rect = self.surface.get_rect(topleft=self.rect.topleft)

    def render(self, surface):
        surface.blit(self.surface, self.rect)