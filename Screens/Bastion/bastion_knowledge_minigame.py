import pygame
from random import sample
from abc import ABC
from Managers.config_manager import ConfigManager
from Managers.sfx_manager import SFXManager
from Classes.screen import Screen
from Classes.image import Image
from Classes.button import Button
from Classes.text import Text
from Classes.bastion_number_tooltips import BastionNumberTooltips
from constants import questsPath, WHITE

"""
A minigame incorporating bastion number tooltips class
Handles a minigame to find all of the books for all possible hints on the later memory minigame
Checks if the player has collected 22 / 22 possible books / the player collected the three right (hint) books
Default screen with an advanced elements appending system.
Has handlers to make the books be able to tell that they are real or not (as there are 19 fake, 3 real books)
Fake being that they are useless.
Real being that they are hint books.
"""
class BastionKnowledgeMinigame(Screen, ABC):
    def __init__(self):
        self.config = ConfigManager()
        self.bastionMinigamePath = questsPath
        self.sfx = SFXManager()
        super().__init__()

    def setup(self):
        self.config.displayingTooltip = False
        self.orig_elements = [
            Image(0, 0, f'{questsPath}/bastion/Level1/images/background.png')
        ]
        positions = [
            (165, 367), (207, 240), (327, 144), (322, 288), (425, 189),
            (488, 175), (518, 238), (602, 212), (583, 280), (694, 198),
            (653,  76), (752, 215), (850, 159), (1030, 359), (752, 322),
            (887, 257), (677, 411), (934, 371), (988, 192), (1263, 266),
            (1099, 380), (1112, 281)
        ]
        real_book_indices = set(sample(range(1, len(positions) + 1), 3))
        for i, (x, y) in enumerate(positions, start=1):
            idx_str = f'{i:02d}'
            if i in real_book_indices:
                handler = self.realBookHandler
            else:
                handler = self.fakeBookHandler
            btn = Button(
                f'book{idx_str}',
                x, y,
                f'{questsPath}/bastion/Level1/buttons/{idx_str}.png',
                f'{questsPath}/bastion/Level1/buttons/a/{idx_str}.png',
                destination='bastionDialogue',
                clickHandler=handler
            )
            self.orig_elements.append(btn)

        self.orig_elements += [
            Image(0, 18, f'{questsPath}/dungeon/Level1/images/time.png'),
            Text('info', 50, 36, 30, WHITE, font='Assets/Fonts/OSCBold.ttf'),
            BastionNumberTooltips()
        ]
        self.elements = self.orig_elements

    def handleEvent(self):
        for element in list(self.elements):
            if self.config.displayingTooltip and getattr(element, 'name', None) == 'tip':
                if element.handleEvent():
                    break
                continue
            if not self.config.displayingTooltip and isinstance(element, Button) and element.handleEvent():
                self.elements = [e for e in self.elements if getattr(e, 'name', None) != element.name]
                self.sfx.playSfx('Assets/SFX/book.mp3')
                break

    def handleHover(self):
        if self.config.displayingTooltip:
            return
        for element in self.elements:
            if hasattr(element, 'handleHover') and element.handleHover():
                break

    def render(self, surface):
        self.restoreObjects()
        self.timer()
        for element in self.elements:
            element.render(surface)

    def restoreObjects(self):
        if self.config.bastionRestoreObjects:
            self.config.bastionRestoreObjects = False
            self.elements = list(self.orig_elements)

    def timer(self):
        self.config.frameCounter += 1
        if self.config.frameCounter >= 60:
            self.config.frameCounter = 0
            self.config.timerCounter -= 1
        if self.config.timerCounter <= 0:
            self.config.state = 'bastionDialogue'

    def tooltipHandler(self):
        self.elements = [e for e in self.elements if getattr(e, 'name', None) != 'tip']
        self.config.displayingTooltip = False
        if self.findBookDisplayHandler().books >= 3:
            self.config.state = 'bastionDialogue'

    def realBookHandler(self):
        if self.config.displayingTooltip:
            return False
        display = self.findBookDisplayHandler()
        next_tip = self.config.bastionTrueBooks + 1
        self.config.bastionTrueBooks = next_tip
        display.books = next_tip
        self.config.bastionTotalBooks += 1
        self.elements.append(
            Image(351, 187,
                  f'{questsPath}/bastion/Level1/images/tipReal{next_tip}.png',
                  name='tip')
        )
        self.elements.append(
            Button('tip', 621, 444,
                   f'{questsPath}/bastion/Level1/buttons/next.png',
                   clickHandler=self.tooltipHandler)
        )
        self.config.displayingTooltip = True
        return True

    def fakeBookHandler(self):
        if self.config.displayingTooltip:
            return False
        self.config.bastionTotalBooks += 1
        self.elements.append(
            Image(351, 187,
                  f'{questsPath}/bastion/Level1/images/tipFake.png',
                  name='tip')
        )
        self.elements.append(
            Button('tip', 621, 444,
                   f'{questsPath}/bastion/Level1/buttons/next.png',
                   clickHandler=self.tooltipHandler)
        )
        self.config.displayingTooltip = True
        return True

    def findBookDisplayHandler(self):
        for e in self.elements:
            if getattr(e, 'name', None) == 'bookDisplayHandler':
                return e