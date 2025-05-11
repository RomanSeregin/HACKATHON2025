import pygame
from abc import ABC
from Managers.config_manager import ConfigManager
import random
from Classes.screen import Screen
from Classes.image import Image
from Classes.button import Button
from Classes.text import Text
from Classes.bastion_number_tooltips import BastionNumberTooltips
from constants import questsPath, WHITE

"""
A bastion memory minigame with 21 books, out of which only the books on positions 3, 10 and 15 are correct.
All fake books get shuffled to confuse the player. They have 2 instances per book
Real books have 3 real instances, and they should be found after the memorization period is over.
Handles advanced appending logic, with simple handling logic.
Similar to the bastion knowledge minigame in terms of element defining logic.
"""
class BastionMemoryMinigame(Screen, ABC):
    def __init__(self):
        self.config = ConfigManager()
        self.questsPath = questsPath
        super().__init__()

    def setup(self):
        self.handledCount = False
        self.orig_elements = [
            Image(0, 0, f'{questsPath}/bastion/Level4/images/background.png'),
            Image(0, 18, f'{questsPath}/bastion/Level4/images/time.png', name='time'),
            Text('info', 50, 36, 30, WHITE, font='Assets/Fonts/OSCBold.ttf'),
            BastionNumberTooltips(),
        ]

        self.elements = list(self.orig_elements)

        real_positions = [
            (404, 128),
            (588, 337),
            (36, 546),
        ]

        fake_positions = [
            (36, 128), (220, 128), (588, 128), (772, 128), (956, 128), (1140, 128),
            (36, 337), (220, 337), (404, 337), (772, 337), (956, 337), (1140, 337),
            (220, 546), (404, 546), (588, 546), (772, 546), (956, 546), (1140, 546),
        ]

        correct_id = self.config.bastionBookID
        fake_ids = [i for i in range(1, 11) if i != correct_id] * 2
        random.shuffle(fake_ids)


        for idx, (x, y) in enumerate(fake_positions):
            bid = fake_ids[idx]
            num = f"{bid:02d}"
            inactive = f"{questsPath}/bastion/Level4/buttons/normal/{num}.png"
            active = f"{questsPath}/bastion/Level4/buttons/normal-a/{num}.png"
            handler = self.fakeBookHandler

            btn = Button(
                name=f"book_fake_{idx}",
                xPos=x, yPos=y,
                imagePath=inactive,
                hoveredImagePath=active,
                clickHandler=handler
            )
            self.elements.append(btn)


        for idx, (x, y) in enumerate(real_positions):
            bid = correct_id
            num = f"{bid:02d}"
            inactive = f"{questsPath}/bastion/Level4/buttons/normal/{num}.png"
            active = f"{questsPath}/bastion/Level4/buttons/normal-a/{num}.png"
            handler = self.realBookHandler

            btn = Button(name=f"book_real_{idx}", xPos=x, yPos=y, imagePath=inactive, hoveredImagePath=active, clickHandler=handler)
            self.elements.append(btn)

    def handleEvent(self):
        for element in list(self.elements):
            if hasattr(element, 'handleEvent'):
                if isinstance(element, Button):
                    if self.handledCount:
                        if element.handleEvent() and element.name.startswith('book_'):
                            element.updateTexture(element.imagePath.replace('undercover', 'normal'), element.hoveredImagePath.replace('undercover', 'normal'))
                            break
                elif element.handleEvent():
                    break

    def handleHover(self):
        for element in self.elements:
            if hasattr(element, 'handleHover'):
                if element.handleHover():
                    break

    def render(self, surface):
        self.timer()
        for element in self.elements:
            element.render(surface)

    def timer(self):
        if not self.handledCount:
            self.config.frameCounter += 1
            if self.config.frameCounter >= 60:
                self.config.frameCounter = 0
                self.config.memoryCounter -= 1
            if self.config.memoryCounter <= 0:
                self.handledCount = True
                self.elements = [e for e in self.elements if getattr(e, 'name', None) not in ['info', 'time']]
                for book in self.elements:
                    if hasattr(book, 'name') and isinstance(book, Button):
                        if 'book_' in book.name:
                            book.updateTexture(book.imagePath.replace('normal', 'undercover'), book.hoveredImagePath.replace('normal', 'undercover'))

    def fakeBookHandler(self):
        if self.handledCount:
            self.config.bastionFakeBooks += 1
            self.config.bastionLose = True

            if self.config.bastionFakeBooks >= 3:
                self.config.bastionFakeBooks = 0
                self.config.state = 'bastionLose'

            return True
        return False

    def realBookHandler(self):
        if self.handledCount:
            self.config.bastionCorrectBooks += 1

            if self.config.bastionCorrectBooks >= 3:
                self.config.bastionCorrectBooks = 0
                self.config.state = 'bastionWin'

            return True
        return False