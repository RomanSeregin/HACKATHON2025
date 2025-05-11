import pygame
from abc import ABC
from Managers.config_manager import ConfigManager
from Classes.screen import Screen
from Classes.image import Image
from Classes.button import Button
from constants import introPath


class Intro0(Screen, ABC):
    def __init__(self):
        self.config = ConfigManager()
        self.introPath = introPath
        super().__init__()

    def setup(self):
        self.elements = [
            Image(0, 0, f'{introPath}/images/0/background.png'),
            Button('next', 621, 477, f'{introPath}/buttons/0/next.png', None, destination='intro1')
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