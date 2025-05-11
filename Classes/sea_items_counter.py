import pygame
from Managers.config_manager import ConfigManager
from constants import questsPath


"""
Class similar to bastion_number_tooltips, as it handles the display and proper handling of the variables in config.
Has typical values and methods, the main difference being the textures themselves.
"""
class SeaItemsCounter:
    def __init__(self, initial_air=0, initial_finder=0):
        self.air_positions = {
            'slot1': (467, 20),
            'slot2': (524, 20),
            'slot3': (581, 20),
        }
        self.finder_positions = {
            'slot4': (638, 20),
        }
        self.images = {
            'air_active': pygame.image.load(f'{questsPath}/sea/Level2/images/statusAirBubble-a.png').convert_alpha(),
            'air_inactive': pygame.image.load(f'{questsPath}/sea/Level2/images/statusAirBubble.png').convert_alpha(),
            'finder_active': pygame.image.load(f'{questsPath}/sea/Level2/images/statusFinder-a.png').convert_alpha(),
            'finder_inactive': pygame.image.load(f'{questsPath}/sea/Level2/images/statusFinder.png').convert_alpha(),
        }
        self.config = ConfigManager()
        self._air_bubbles = 0
        self._finders = 0
        self.initial_air = initial_air
        self.initial_finder = initial_finder
        self.reset()

    def reset(self):

        self.air_bubbles = self.initial_air
        self.finders = self.initial_finder

    @property
    def air_bubbles(self):
        return self._air_bubbles

    @air_bubbles.setter
    def air_bubbles(self, value):
        self._air_bubbles = max(0, min(value, len(self.air_positions)))
        if value < 0:
            self.config.airBubbles = 0
            self.config.seaFishRestoreObjects = True
            self.config.state = 'seaDialogue'


    @property
    def finders(self):
        return self._finders

    @finders.setter
    def finders(self, value):
        if value:
            self._finders = max(0, min(value, len(self.finder_positions)))
            self.config.finders = self._finders

    def render(self, surface):
        for i, (slot, pos) in enumerate(self.air_positions.items()):
            img = (self.images['air_active'] if i < self.air_bubbles
                   else self.images['air_inactive'])
            surface.blit(img, pos)
        for i, (slot, pos) in enumerate(self.finder_positions.items()):
            img = (self.images['finder_active'] if i < self.finders
                   else self.images['finder_inactive'])
            surface.blit(img, pos)