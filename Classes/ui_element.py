from abc import ABC, abstractmethod
import pygame


"""
Abstact parent class for all of the visual and interactive elements. Not used anywhere by itself, just the bare skeleton that can be built upon.
Has the most basic possible properties.
"""
class UIElement(ABC):
    def __init__(self, xPos, yPos):
        self.xPos = xPos
        self.yPos = yPos

    @abstractmethod
    def handleEvent(self):

        pass

    @abstractmethod
    def render(self, surface):

        pass

    @abstractmethod
    def hovered(self, mousePos):

        pass