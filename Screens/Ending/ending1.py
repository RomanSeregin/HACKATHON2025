import pygame
from abc import ABC
from Managers.config_manager import ConfigManager
from Classes.screen import Screen
from Classes.image import Image
from Classes.button import Button
from constants import endingPath


class Ending1(Screen, ABC):
    def __init__(self):
        self.config = ConfigManager()
        self.endingPath = endingPath
        super().__init__()

    def setup(self):
        self.elements = [
            Image(0, 0, f'{endingPath}/ending1/images/background.png'),
            Button('next', 698, 477, f'{endingPath}/ending1/buttons/next.png', None, destination='ending2'),
            Button('back', 545, 477, f'{endingPath}/ending1/buttons/back.png', None, destination='ending0')
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