import pygame
from abc import ABC
from Managers.config_manager import ConfigManager
from Classes.screen import Screen
from Classes.image import Image
from Classes.button import Button
from constants import questsPath


class SeaTreaty(Screen, ABC):
    def __init__(self):
        self.config = ConfigManager()
        self.questsPath = questsPath
        super().__init__()

    def setup(self):
        self.elements = [
            Image(0, 0, f'{questsPath}/sea/Treaty/images/background.png'),
            Button('next', 525, 561, f'{questsPath}/sea/Treaty/buttons/next.png', None, destination='hub', clickHandler=self.hubStateUpdate)
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

    def hubStateUpdate(self):
        self.config.levelCompletionStates['sea'] = True
        self.config.hubStateUpdate()