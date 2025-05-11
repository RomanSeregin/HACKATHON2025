import pygame
import random
from abc import ABC
from Managers.config_manager import ConfigManager
from Classes.screen import Screen
from Classes.image import Image
from Classes.button import Button
from Classes.text import Text
from constants import questsPath, WHITE

"""
A minigame that has the ring moving every 10 seconds on the screen
The ring is barely visible, so tooltips are advised
Manages the time spent on the screen, handles the minigame with extended logic on the generation and the event handling.
"""
class SeaRingMinigame(Screen, ABC):
    def __init__(self):
        self.config = ConfigManager()
        self.questsPath = questsPath
        super().__init__()

    def setup(self):
        self.orig_elements = [
            Image(0, 0, f'{questsPath}/sea/Level4/images/background.png'),
            Button('hub', 1058, 15, f'{questsPath}/sea/Level4/buttons/hub.png', None, destination='hub', clickHandler=self.hubStateUpdate),
            Image(0, 18, f'{questsPath}/sea/Level4/images/time.png'),
            Text('info', 50, 36, 30, WHITE, font='Assets/Fonts/OSCBold.ttf'),
        ]

        self.elements = self.orig_elements

    def handleEvent(self):
        for element in self.elements:
            if hasattr(element, 'handleEvent'):
                if element.handleEvent():
                    break

    def handleHover(self):
        for element in self.elements:
            if hasattr(element, 'handleHover') and self.config.seaStartTimer:
                if element.handleHover():
                    break

    def render(self, surface):
        self.handleImportant()
        for element in self.elements:
            element.render(surface)

    def timer(self):
        self.config.frameCounter += 1
        if self.config.frameCounter >= 60:
            self.config.frameCounter = 0
            self.config.timerCounter -= 1
        if self.config.frameCounter == 0 and self.config.timerCounter % self.config.ringTimer == 0 and self.config.timerCounter != self.config.backupTimerCounter:
            self.moveKey()
        if self.config.timerCounter <= 0:
            self.config.state = 'seaLose'

    def handleImportant(self):
        if self.config.seaStartTimer:
            self.timer()
            if self.config.finders > 0:
                if self.config.finderCharges == 0:
                    self.config.finders = 0
                    self.elements = [e for e in self.elements if getattr(e, 'name', None) != 'GUI']
                else:
                    gui = f'{questsPath}/sea/Level4/images/detectorGUI{self.config.finderCharges}.png'
                    for e in self.elements:
                        if getattr(e, 'name', '') == 'GUI' and e.imagePath != gui:
                            e.updateTexture(gui)

        if self.config.seaRingRestoreObjects:
            self.config.seaRingRestoreObjects = False
            if self.config.airBubbles > 0:
                self.elements += [
                    *[Image(413 + 10 * i, 20, f'{questsPath}/sea/Level4/images/airSphere.png', name=f'airSphere{i}')
                      for i in range(self.config.airBubbles)],
                    Image(493, 46, f'{questsPath}/sea/Level4/images/addTime.png')
                ]
                if self.config.airBubbles > 0:
                    self.config.timerCounter = self.config.backupTimerCounter * self.config.airBubbles
            else:
                self.elements[2].updateTexture(f'{questsPath}/sea/Level4/images/timeShort.png')

            self.elements.append(Button('key', 347, 508, f'{questsPath}/sea/Level4/buttons/key1.png', clickHandler=self.keyHandler))
            self.moveKey()

            if self.config.finders > 0:
                self.elements += [
                    Image(391, 604, f'{questsPath}/sea/Level4/images/GUIBackground.png'),
                    Button('GUI', 531, 647,
                          f'{questsPath}/sea/Level4/images/detectorGUI{self.config.finderCharges}.png', None, clickHandler=self.finderHandler)
                ]

            self.elements += [
                Image(351, 213, f'{questsPath}/sea/Level4/images/tip.png', name='tip'),
                Button('tip', 621, 469,
                       f'{questsPath}/sea/Level4/buttons/next.png',
                       None,
                       clickHandler=self.handleTip)
            ]

    def handleTip(self):
        self.config.seaStartTimer = True
        self.elements = [element for element in self.elements if getattr(element, 'name', None) != 'tip']

    def hubStateUpdate(self):
        self.config.reset_sea_vars()
        self.elements = self.orig_elements
        self.config.hubStateUpdate()

    def finderHandler(self):
        if self.config.finderCharges > 0:
            self.elements = [element for element in self.elements if getattr(element, 'name', None) != 'hint']
            self.elements += [
                Image(468, 527, f'{questsPath}/sea/Level4/images/hints/{self.config.keyLocation}.png', name='hint'),
                Button('hint', 854, 527, f'{questsPath}/sea/Level4/images/hints/close.png', clickHandler=self.handleClosingHint)
            ]
            self.config.finderCharges -= 1
        else:
            self.config.finderCharges = 0


    def moveKey(self):
        positions = {
            'key1': (347, 506),
            'key2': (1130, 615),
            'key3': (828, 542),
            'key4': (130, 531),
            'key5': (1188, 87),
            'key6': (604, 283),
            'key7': (567, 439),
        }
        name, (x, y) = random.choice(list(positions.items()))

        for el in self.elements:
            if isinstance(el, Button) and el.name.startswith('key'):
                el.name = name
                el.move(x, y)
                el.updateTexture(f'{questsPath}/sea/Level4/buttons/{name}.png')
                break

        self.config.keyLocation = name

    def keyHandler(self):
        self.config.state = 'seaResult'

    def handleClosingHint(self):
        self.elements = [element for element in self.elements if getattr(element, 'name', None) != 'hint']