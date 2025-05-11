import pygame
from abc import ABC
from Managers.config_manager import ConfigManager
from Classes.screen import Screen
from Classes.image import Image
from Classes.button import Button
from constants import questsPath


class JungleChoose(Screen, ABC):
    def __init__(self):
        self.config = ConfigManager()
        self.questsPath = questsPath
        super().__init__()

    def setup(self):
        self.elements = [
            Image(0, 0, f'{questsPath}/jungle/Level2/images/background.png'),
            Image(325, 112, f'{questsPath}/jungle/Level2/images/choice.png', name='choice'),
            Button('jug', 462, 379, f'{questsPath}/jungle/Level2/buttons/tick.png', f'{questsPath}/jungle/Level2/buttons/tick-a.png', destination='jungleChoose', clickHandler=self.jugHandler),
            Button('coconut0', 563, 379, f'{questsPath}/jungle/Level2/buttons/tick.png', f'{questsPath}/jungle/Level2/buttons/tick-a.png', destination='jungleChoose', clickHandler=self.coconut0Handler),
            Button('coconut1', 664, 379, f'{questsPath}/jungle/Level2/buttons/tick.png', f'{questsPath}/jungle/Level2/buttons/tick-a.png', destination='jungleChoose', clickHandler=self.coconut1Handler),
            Button('coconut2', 765, 379, f'{questsPath}/jungle/Level2/buttons/tick.png', f'{questsPath}/jungle/Level2/buttons/tick-a.png', destination='jungleChoose', clickHandler=self.coconut2Handler),
            Button('coconut3', 451, 526, f'{questsPath}/jungle/Level2/buttons/tick.png', f'{questsPath}/jungle/Level2/buttons/tick-a.png', destination='jungleChoose', clickHandler=self.coconut3Handler),
            Button('flower', 536, 526, f'{questsPath}/jungle/Level2/buttons/tick.png', f'{questsPath}/jungle/Level2/buttons/tick-a.png', destination='jungleChoose', clickHandler=self.flowerHandler),
            Button('flowerInjured', 621, 526, f'{questsPath}/jungle/Level2/buttons/tick.png', f'{questsPath}/jungle/Level2/buttons/tick-a.png', destination='jungleChoose', clickHandler=self.flowerInjuredHandler),
            Button('frog', 706, 526, f'{questsPath}/jungle/Level2/buttons/tick.png', f'{questsPath}/jungle/Level2/buttons/tick-a.png', destination='jungleChoose', clickHandler=self.frogHandler),
            Button('pot', 791, 526, f'{questsPath}/jungle/Level2/buttons/tick.png', f'{questsPath}/jungle/Level2/buttons/tick-a.png', destination='jungleChoose', clickHandler=self.potHandler),
            Button('soil', 866, 379, f'{questsPath}/jungle/Level2/buttons/tick.png', f'{questsPath}/jungle/Level2/buttons/tick-a.png', destination='jungleChoose', clickHandler=self.soilHandler),
            Button('stone', 876, 526, f'{questsPath}/jungle/Level2/buttons/tick.png', f'{questsPath}/jungle/Level2/buttons/tick-a.png', destination='jungleChoose', clickHandler=self.stoneHandler)
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

    def findElements(self, name):
        for element in self.elements:
            if isinstance(element, Button):
                if 'tick' in element.imagePath:
                    if name.lower() in element.name.lower():
                        return element


    def multiHandler(self, name):
        btn = self.findElements(name)
        if not btn:
            return False


        if not getattr(btn, 'toggled', False):
            btn.toggled = True
            btn.unhoveredImage = btn.hoveredImage
            btn.image = btn.hoveredImage
        else:
            btn.toggled = False
            un, hov = btn.backupImages
            btn.unhoveredImage, btn.hoveredImage = un, hov
            btn.image = un

        btn.upd()

        toggled = [e.name for e in self.elements
                   if isinstance(e, Button) and getattr(e, 'toggled', False)]
        if len(toggled) == 4:
            required = {'flowerInjured', 'pot', 'soil', 'jug'}
            if set(toggled) == required:
                self.config.state = 'jungleWin'
            else:
                self.config.state = 'jungleLose'

        return True

    def jugHandler(self):
        self.multiHandler('jug')

    def coconut0Handler(self):
        self.multiHandler('coconut0')

    def coconut1Handler(self):
        self.multiHandler('coconut1')

    def coconut2Handler(self):
        self.multiHandler('coconut2')

    def coconut3Handler(self):
        self.multiHandler('coconut3')

    def flowerHandler(self):
        self.multiHandler('flower')

    def flowerInjuredHandler(self):
        self.multiHandler('flowerInjured')

    def frogHandler(self):
        self.multiHandler('frog')

    def potHandler(self):
        self.multiHandler('pot')

    def soilHandler(self):
        self.multiHandler('soil')

    def stoneHandler(self):
        self.multiHandler('stone')