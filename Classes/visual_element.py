from abc import ABC
from Classes.ui_element import UIElement
import pygame


"""
Abstract parent for images / any non-interactive elements that won't handle events or hover.
"""
class VisualElement(UIElement, ABC):

    def __init__(self, xPos, yPos, imagePath):
        super().__init__(xPos, yPos)
        self.imagePath = imagePath
        self.image = pygame.image.load(imagePath).convert_alpha()
        self.rect = self.image.get_rect(topleft=(self.xPos, self.yPos))

    def render(self, surface):

        surface.blit(self.image, self.rect)
        return True

    def hovered(self, mousePos):

        return False

    def handleEvent(self):
        return False