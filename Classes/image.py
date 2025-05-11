from abc import ABC
from Classes.visual_element import VisualElement
import pygame

"""
The child of the VisualElement abstract class. Has simple methods like move() and updateTexture() to build on top of the parental' base.
Has default properties of an image. Doesn't handle any events.
"""
class Image(VisualElement, ABC):

    def __init__(self, xPos, yPos, imagePath, name=None):
        super().__init__(xPos, yPos, imagePath)
        self.name = name

    def updateTexture(self, imagePath):
        self.imagePath = imagePath
        self.image = pygame.image.load(imagePath).convert_alpha()
        self.rect = self.image.get_rect(topleft=(self.xPos, self.yPos))

    def move(self, x):
        if not self.xPos - x < -540:
            self.xPos -= x
            self.rect = self.image.get_rect(topleft=(self.xPos, self.yPos))