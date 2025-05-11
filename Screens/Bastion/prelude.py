import pygame
from abc import ABC
from Managers.config_manager import ConfigManager
from Classes.screen import Screen
from Classes.image import Image
from Classes.button import Button
from Classes.text import Text
from constants import questsPath


class BastionPrelude(Screen, ABC):
    def __init__(self):
        self.config = ConfigManager()
        self.questsPath = questsPath
        super().__init__()

    def setup(self):
        self.elements = [
            Image(0, 0, f'{questsPath}/bastion/Level3/images/background.png'),
            Button('next', 621, 444, f'{questsPath}/bastion/Level3/buttons/next.png', None, destination='bastionMemoryMinigame'),
            Image(408, 240, f'{questsPath}/bastion/Level4/buttons/normal/{self.config.bastionBookID:02}.png')
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