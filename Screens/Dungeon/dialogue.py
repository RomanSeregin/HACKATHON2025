import pygame
from abc import ABC
from Managers.config_manager import ConfigManager
from Classes.screen import Screen
from Classes.image import Image
from Classes.button import Button
from constants import questsPath


class DungeonDialogue(Screen, ABC):
    def __init__(self):
        self.config = ConfigManager()
        self.questsPath = questsPath
        super().__init__()

    def setup(self):
        self.elements = [
            Image(0, 0, f'{questsPath}/dungeon/Level2/images/background.png'),
            Button('next', 525, 615, f'{questsPath}/dungeon/Level2/buttons/next.png', None, destination='dungeonQTE', clickHandler=self.dungeonQTEClickHandler)
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

    def dungeonQTEClickHandler(self):
        self.config.dungeonRestoreQTE = True
        self.config.state = 'dungeonQTE'