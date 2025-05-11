import pygame
from abc import ABC
from Managers.config_manager import ConfigManager
from Classes.screen import Screen
from Classes.image import Image
from Classes.button import Button
from constants import questsPath


class DungeonEntrance(Screen, ABC):
    def __init__(self):
        self.config = ConfigManager()
        self.entrancePath = questsPath
        super().__init__()

    def setup(self):
        self.elements = [
            Image(0, 0, f'{questsPath}/dungeon/Level0/images/background.png'),
            Image(351, 220, f'{questsPath}/dungeon/Level0/images/tip.png'),
            Button('next', 621, 476, f'{questsPath}/dungeon/Level0/buttons/next.png', None, destination='dungeonIceMinigame', clickHandler=self.buttonCustomHandler),
            Button('hub', 1058, 15, f'{questsPath}/dungeon/Level0/buttons/hub.png', None, destination='hub', clickHandler=self.config.hubStateUpdate),
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

    def buttonCustomHandler(self):
        self.config.reset_dungeon_vars()
        self.config.state = 'dungeonIceMinigame'