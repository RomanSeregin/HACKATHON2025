import pygame
from abc import ABC
from Managers.config_manager import ConfigManager
from Classes.screen import Screen
from Classes.image import Image
from Classes.button import Button
from constants import questsPath

# entrance unlocks upon completing the air bastion
class SeaEntranceUnlocked(Screen, ABC):
    def __init__(self):
        self.config = ConfigManager()
        self.questsPath = questsPath
        super().__init__()

    def setup(self):
        self.elements = [
            Image(0, 0, f'{questsPath}/sea/Level1/images/background.png'),
            Button('next', 621, 476, f'{questsPath}/sea/Level1/buttons/next.png', None, destination='seaFishMinigame', clickHandler=self.minigameUpdate),
            Button('hub', 1058, 15, f'{questsPath}/sea/Level1/buttons/hub.png', None, destination='hub', clickHandler=self.config.hubStateUpdate)
        ]

    def handleEvent(self):
        for element in self.elements:
            if hasattr(element, 'handleEvent'):
                if element.handleEvent():
                    break

    def handleHover(self):
        for element in self.elements:
            if hasattr(element, 'handleHover'):
                if element.handleHover():
                    break

    def render(self, surface):
        for element in self.elements:
            element.render(surface)

    def minigameUpdate(self):
        self.config.reset_sea_vars()
        self.config.state = 'seaFishMinigame'