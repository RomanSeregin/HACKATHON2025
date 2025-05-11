import pygame
from abc import ABC

from Managers.config_manager import ConfigManager
from Classes.screen import Screen
from Classes.image import Image
from Classes.button import Button
from constants import aboutPath


class AboutGame0(Screen, ABC):
    def __init__(self):
        self.config = ConfigManager()
        self.aboutPath = aboutPath
        super().__init__()

    def setup(self):
        self.elements = [
            Image(0, 0, f'{self.aboutPath}/about_game0/images/background.png'),
            Button('previous',  627,  571, f'{self.aboutPath}/about_game0/buttons/previous.png', clickHandler=self.handlePreviousButton),
            Button('next', 695, 571,  f'{self.aboutPath}/about_game0/buttons/next-a.png', clickHandler=self.handleNextButton),
            Button('return', 599, 652, f'{self.aboutPath}/about_game0/buttons/return.png', destination='menu')
        ]

    def handleEvent(self):
        for element in self.elements:
            if not hasattr(element, 'handleEvent'):
                continue

            if element.name == 'previous' and self.config.aboutGamePage == 0:
                continue
            if element.handleEvent():
                break

    def handleHover(self):
        for element in self.elements:
            if hasattr(element, 'handleHover'):
                if element.name in ['previous', 'next']:
                    continue

                if element.handleHover():
                    break

    def render(self, surface):
        for element in self.elements:

            if element.name == 'previous' and self.config.aboutGamePage == 0:
                element.updateTexture(f'{self.aboutPath}/about_game0/buttons/previous.png')
            element.render(surface)

    def handlePreviousButton(self):
        if self.config.aboutGamePage > 0:
            self.config.aboutGamePage -= 1
            self.config.state = f'aboutGame{self.config.aboutGamePage}'
            return True
        return False

    def handleNextButton(self):
        if self.config.aboutGamePage < 15:
            self.config.aboutGamePage += 1
            self.config.state = f'aboutGame{self.config.aboutGamePage}'
            return True
        return False