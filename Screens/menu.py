import pygame
from abc import ABC
from Managers.config_manager import ConfigManager
from Classes.screen import Screen
from Classes.image import Image
from Classes.button import Button
from constants import menuPath


"""
The title screen of the game
Has the base elements to go to different states, checks for user completing tutorial, handling transfers to other states (levels / screens)
"""
class Menu(Screen, ABC):
    def __init__(self):
        self.config = ConfigManager()
        self.menuPath = menuPath
        super().__init__()

    def setup(self):
        self.elements = [
            Image(0, 0, f'{self.menuPath}/images/background.png'),
            Button('start', 537, 270, f'{self.menuPath}/buttons/play.png', f'{self.menuPath}/buttons/play-a.png',
                   destination='hub', clickHandler=self.handleStartButton),
            Button('settings', 536, 340, f'{self.menuPath}/buttons/settings.png',
                   f'{self.menuPath}/buttons/settings-a.png', destination='settings'),
            Button('aboutMe', 536, 410, f'{self.menuPath}/buttons/about_me.png',
                   f'{self.menuPath}/buttons/about_me-a.png', destination='aboutMe0'),
            Button('aboutGame', 537, 480, f'{self.menuPath}/buttons/about_game.png',
                   f'{self.menuPath}/buttons/about_game-a.png', destination='aboutGame0'),
            Button('exit', 536, 600, f'{self.menuPath}/buttons/exit.png', f'{self.menuPath}/buttons/exit-a.png',
                   destination='exit', clickHandler=self.handleExitButton)
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

    # check if the user has completed the intro, if not - show them, if yes - just skip entirely and get to the hub
    def handleStartButton(self):
        if not self.config.introCompleted:
            self.config.state = 'intro0'
        else:
            self.config.hubStateUpdate()

    def handleExitButton(self):
        self.config.exitFlag = True