import pygame
from random import sample
from abc import ABC
from Managers.config_manager import ConfigManager
from Classes.screen import Screen
from Classes.image import Image
from Classes.button import Button
from Classes.text import Text
from constants import questsPath, ICE_POSITIONS, WHITE
from Managers.sfx_manager import SFXManager


"""
The default object finding minigame, in this case finding 3 true icicles (very similar to the bastion minigames and jungle minigames)
Handles the generation and overall functionality of icicles, which ones are real, and so on.
"""
class IceMinigame(Screen, ABC):
    def __init__(self):
        self.config = ConfigManager()
        self.iceMinigamePath = questsPath
        self.sfx = SFXManager()
        super().__init__()

    def setup(self):
        self.displayingTooltip = False
        self.orig_elements = [
            Image(0, 0, f'{questsPath}/dungeon/Level1/images/background.png')
        ]
        real_ice_indices = set(sample(range(11), 3))
        positions = [
            (0, -2), (547, 77), (821, -21), (1125, 116),
            (479, 150), (1263, 1), (544, 75), (106, 262),
            (286, 516), (25, 525), (1140, 592)
        ]
        for i in range(0, 11):
            x, y = positions[i]
            is_real = i in real_ice_indices
            handler = self.buttonIceHandler if is_real else self.buttonFakeIceHandler
            name = f'ice{i}' if is_real else f'fakeIce{i}'
            self.orig_elements.append(
                Button(name, x, y,
                       f'{questsPath}/dungeon/Level1/buttons/ice{i}.png',
                       f'{questsPath}/dungeon/Level1/buttons/ice{i}-a.png',
                       destination='dungeonDialogue', clickHandler=handler)
            )
        self.orig_elements.append(
            Button('potion', 1009, 495,
                   f'{questsPath}/dungeon/Level1/buttons/potion.png',
                   f'{questsPath}/dungeon/Level1/buttons/potion-a.png',
                   destination='dungeonDialogue', clickHandler=self.potionClickHandler)
        )
        self.orig_elements.append(Image(0, 18, f'{questsPath}/dungeon/Level1/images/time.png'))
        self.orig_elements.append(Text('info', 50, 36, 30, WHITE, font='Assets/Fonts/OSCBold.ttf'))
        self.orig_elements.append(Button('hub', 1058, 15, f'{questsPath}/dungeon/Level1/buttons/hub.png', None, destination='hub', clickHandler=self.config.hubStateUpdate))
        self.elements = list(self.orig_elements)

    def handleEvent(self):
        for element in list(self.elements):
            if self.displayingTooltip and getattr(element, 'name', None) == 'tip':
                if element.handleEvent():
                    break
            if self.displayingTooltip:
                continue
            if isinstance(element, Button) and element.handleEvent():
                if element.name != 'hub':
                    self.elements.remove(element)
                break

    def handleHover(self):
        if self.displayingTooltip:
            for element in self.elements:
                if getattr(element, 'name', None) == 'tip' and hasattr(element, 'handleHover') and element.handleHover():
                    break
            return
        for element in self.elements:
            if hasattr(element, 'handleHover') and element.handleHover():
                break

    def render(self, surface):
        self.restoreObjects()
        self.timer()
        for element in self.elements:
            element.render(surface)

    def iceHandler(self, isIce=False):
        if self.displayingTooltip:
            return
        if isIce:
            self.config.iceCollected += 1
        tip_img = f'{questsPath}/dungeon/Level1/images/tip{"2" if isIce else "1"}.png'
        self.elements.append(Image(351, 220, tip_img, name='tip'))
        self.elements.append(
            Button('tip', 621, 477,
                   f'{questsPath}/dungeon/Level1/buttons/ok.png', None,
                   destination='dungeonDialogue', clickHandler=self.tooltipHandler)
        )
        self.displayingTooltip = True

    def buttonIceHandler(self):
        if not self.displayingTooltip:
            self.iceHandler(True)
            return True
        return False

    def buttonFakeIceHandler(self):
        if not self.displayingTooltip:
            self.iceHandler(False)
            self.sfx.playSfx('Assets/SFX/icicle.mp3')
            return True
        return False

    def restoreObjects(self):
        if self.config.dungeonRestoreIce:
            self.config.dungeonRestoreIce = False
            self.elements = list(self.orig_elements)

    def timer(self):
        self.config.frameCounter += 1
        if self.config.frameCounter >= 60:
            self.config.frameCounter = 0
            self.config.timerCounter -= 1
        if self.config.timerCounter <= 0:
            self.config.state = 'dungeonDialogue'

    def potionClickHandler(self):
        if not self.displayingTooltip:
            self.config.potionCollected = True
            self.sfx.playSfx('Assets/SFX/healthFind.mp3')
            return True
        return False

    def tooltipHandler(self):
        self.elements = [element for element in self.elements if getattr(element, 'name', None) != 'tip']
        self.displayingTooltip = False
        if self.config.iceCollected >= 3:
            self.config.state = 'dungeonDialogue'