import pygame
from Managers.config_manager import ConfigManager
from constants import questsPath

"""
The class used in the bastion that keeps track of the unlocked hints of the books
The class handles their display, and being a singleton allows it to be directly called and transferred to the other level
The class also handles simple properties. Total usage: 4 times (in 2 files)
"""
class BastionNumberTooltips:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):

        if self.__class__._initialized:
            return
        self.__class__._initialized = True

        self.positions = {
            'slot1': (549, 18),
            'slot2': (640, 18),
            'slot3': (730, 18),
        }
        self.active_images = [
            pygame.image.load(f'{questsPath}/bastion/Level1/images/active1.png').convert_alpha(),
            pygame.image.load(f'{questsPath}/bastion/Level1/images/active2.png').convert_alpha(),
            pygame.image.load(f'{questsPath}/bastion/Level1/images/active3.png').convert_alpha(),
        ]
        self.inactive_image = pygame.image.load(
            f'{questsPath}/bastion/Level1/images/inactive.png'
        ).convert_alpha()
        self.config = ConfigManager()
        self._books = 0
        self.initial_books = self.config.bastionTrueBooks
        self.name = 'bookDisplayHandler'
        self.reset()

    def reset(self):
        self.books = self.initial_books

    @property
    def books(self):
        return self._books

    @books.setter
    def books(self, value):
        clamped = max(0, min(value, len(self.positions)))
        self._books = clamped
        self.config.bastionTotalBooks = clamped

    def render(self, surface):
        for i, (_, pos) in enumerate(self.positions.items()):
            img = self.active_images[i] if i < self.books else self.inactive_image
            surface.blit(img, pos)