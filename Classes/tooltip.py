from abc import ABC
from Classes.visual_element import VisualElement
from Managers.config_manager import ConfigManager
from constants import hubPath
import pygame


"""
A tooltip, being used in the hub to display the status of the levels that its hovered on.
Tied with the hub logic, only appears upon hovering on top of a level.
Simple object that handles its own image independently.
Uses usual parameters, as it is simple.
"""
class Tooltip(VisualElement, ABC):
    def __init__(self, name, xPos, yPos, imagePath):

        super().__init__(xPos, yPos, imagePath)
        self.imagePath = imagePath

        self.config = ConfigManager()

        self.tipsPalace = pygame.image.load(f"{hubPath}/images/tipsPalace.png").convert_alpha()
        self.tipsSuccess = pygame.image.load(f"{hubPath}/images/tipsSuccess.png").convert_alpha()
        self.tipsSuggest = pygame.image.load(f"{hubPath}/images/tipsSuggest.png").convert_alpha()

        self.image = self.tipsSuggest

        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, newName):
        self._name = newName

    def render(self, surface):

        self.name = self.config.tooltipName

        if self.name == 'hidden':
            return False


        if self.name == 'palace':

            if not self.config.unlockPalace:
                self.image = self.tipsPalace
            else:
                return False
        else:
            state = self.config.levelCompletionStates.get(self.name)
            if state is True:
                self.image = self.tipsSuccess
            else:
                self.image = self.tipsSuggest

        self.rect = self.image.get_rect(topleft=self.config.mousePos)
        surface.blit(self.image, self.rect)

        return True

    def handleEvent(self):
        pass