import pygame
from abc import ABC
from Managers.config_manager import ConfigManager
from Classes.screen import Screen
from Classes.image import Image
from Classes.button import Button
from Classes.text import Text
from Classes.sea_player import SeaPlayer
from Classes.sea_items_counter import SeaItemsCounter
from Classes.sea_items_generator import SeaItemsGenerator
from Managers.sfx_manager import SFXManager
from constants import questsPath, WHITE
import random


"""
A minigame that has fish and objects moving towards the player.
"""
class SeaFishMinigame(Screen, ABC):
    def __init__(self):
        self.config = ConfigManager()
        self.questsPath = questsPath
        self.sfx = SFXManager()
        super().__init__()

    def setup(self):
        self.elements = [
            Image(0, 0, f'{questsPath}/sea/Level2/images/backgroundWide.png'),
            Button('hub', 1058, 15, f'{questsPath}/sea/Level2/buttons/hub.png', None, destination='hub', clickHandler=self.config.hubStateUpdate),
            Image(0, 18, f'{questsPath}/sea/Level2/images/time.png'),
            Text('info', 50, 36, 30, WHITE, font='Assets/Fonts/OSCBold.ttf'),
            SeaItemsCounter(),
            SeaItemsGenerator(speed=self.config.fishSpeed),
            SeaPlayer()
        ]

    def handleEvent(self):

        for element in self.elements:
            if hasattr(element, 'handleEvent') and element.handleEvent():
                break
        self.collisionHandle()

    def handleHover(self):
        for element in self.elements:
            if hasattr(element, 'handleHover'):
                if element.handleHover():
                    break

    def collisionHandle(self):
        player = next(e for e in self.elements if isinstance(e, SeaPlayer))
        objgen = next(e for e in self.elements if isinstance(e, SeaItemsGenerator))
        counter = next(e for e in self.elements if isinstance(e, SeaItemsCounter))

        px = player.rect.centerx
        py = player.rect.centery

        for obj in list(objgen.objects):
            ox, oy, ow, oh = obj['rect']
            if ox > px + 110 or ox + ow < px - 10:
                continue

            if obj['rect'].collidepoint((px, py)):
                t = obj['type']
                if t == 'fish':
                    self.sfx.playSfx('Assets/SFX/collision.mp3')
                    counter.air_bubbles -= 1
                    if counter.air_bubbles < 0:
                        counter.air_bubbles = 0
                        self.config.resetCounters()
                        self.config.airBubbles = counter.air_bubbles
                        self.config.finders = counter.finders
                        self.config.seaRingRestoreObjects = True
                        self.config.state = 'seaDialogue'
                elif t == 'airBubble':
                    counter.air_bubbles += 1
                    self.config.airBubbles += 1
                else:
                    counter.finders += 1
                    self.config.finders += 1

                objgen.objects.remove(obj)
                break

    def handleImportant(self):
        self.restoreObjects()
        self.timer()
        self.elements[0].move(0.15)
        self.elements[-1].move()
        self.collisionHandle()

    def render(self, surface):
        self.handleImportant()
        for element in self.elements:
            element.render(surface)

    def timer(self):
        self.config.frameCounter += 1
        if self.config.frameCounter >= 60:
            self.config.frameCounter = 0
            self.config.timerCounter -= 1
        if self.config.timerCounter <= 0:
            self.config.resetCounters()
            self.config.state = 'seaDialogue'

    def restoreObjects(self):
        if self.config.seaFishRestoreObjects:
            self.config.seaFishRestoreObjects = False
            self.elements[0].xPos = 0
            self.config.frameCounter = 0


            for element in self.elements:
                if hasattr(element, 'reset'):
                    element.reset()


            objgen = next(e for e in self.elements if isinstance(e, SeaItemsGenerator))
            objgen.objects = []


            player = next(e for e in self.elements if isinstance(e, SeaPlayer))
            player.rect.topleft = (50, 325)