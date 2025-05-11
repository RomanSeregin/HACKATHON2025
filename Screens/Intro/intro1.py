import pygame
from abc import ABC
from Managers.config_manager import ConfigManager
from Classes.screen import Screen
from Classes.image import Image
from Classes.button import Button
from constants import introPath


class Intro1(Screen, ABC):
    def __init__(self):
        self.config = ConfigManager()
        self.introPath = introPath
        super().__init__()

    def setup(self):
        self.elements = [
            Image(0, 0, f'{introPath}/images/1/background.png'),
            Button('back', 545, 469, f'{introPath}/buttons/1/back.png', None, destination='intro0'),
            Button('next', 698, 468, f'{introPath}/buttons/1/next.png', None, destination='intro2')
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