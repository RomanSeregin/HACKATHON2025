import os
import pygame
from abc import ABC
from Classes.visual_element import VisualElement
from Managers.config_manager import ConfigManager
from Managers.sfx_manager import SFXManager

"""
The backbone, one of the most simple objects (low level) in the entire code. Handles basic interactions and hover actions.
Has a handleEvent method for universal usage in the screens. Can get a click / hover handler in its arguments to process events depending on which exact button was pressed.
Has properties like name for seeing which button to remove if needed, and property destination lets it use its 
default click handler to get to the state the mouse is pointing to, if no special action is required
Stores general methods that can be called by upper-level functions, or in the outside context (screen or game manager)
The button handles its own event, depending on the self.config for the checks, in the result no arguments need to be provided
"""
class Button(VisualElement, ABC):
    def defaultClickHandler(self, *args, **kwargs):
        self.config.state = self.destination
        return True

    def defaultHoverHandler(self, *args, **kwargs):
        return True

    def __init__(self, name, xPos, yPos, imagePath, hoveredImagePath=None, destination=None, clickHandler=None, hoverHandler=None):
        super().__init__(xPos, yPos, imagePath)
        self.sfx = SFXManager()
        self.imagePath = imagePath
        if hoveredImagePath is None:
            directory = os.path.dirname(imagePath)
            base_name = os.path.splitext(os.path.basename(imagePath))[0]
            candidate = os.path.join(directory, f'{base_name}-a.png')
            if os.path.isfile(candidate):
                hoveredImagePath = candidate
        self.hoveredImagePath = hoveredImagePath
        self.unhoveredImage = pygame.image.load(imagePath).convert_alpha()
        self.hoveredImage = pygame.image.load(hoveredImagePath).convert_alpha() if hoveredImagePath else self.image
        self.backupImages = self.unhoveredImage, self.hoveredImage
        self.image = self.unhoveredImage

        self.name = name
        self.hovered = False
        self.destination = destination

        self.config = ConfigManager()
        self.toggled = False

        if clickHandler is None: self.clickHandler = self.defaultClickHandler
        else: self.clickHandler = clickHandler

        if hoverHandler is None: self.hoverHandler = self.defaultHoverHandler
        else: self.hoverHandler = hoverHandler

    def createSurface(self, hovered=False):
        self.surface = self.hoveredImage if hovered else self.image
        return self.surface

    def createRect(self):
        return self.surface.get_rect(topleft=(self.xPos, self.yPos))

    def upd(self, args='all'):
        if args == 'all':
            self.surface, self.rect = self.createSurface(self.hovered), self.createRect()
        elif args == 'surf':
            self.surface = self.createSurface(self.hovered)
        elif args == 'rect':
            self.rect = self.createRect()

    def updateTexture(self, imagePath, hoveredImagePath=None):
        self.unhoveredImage = pygame.image.load(imagePath).convert_alpha()
        if hoveredImagePath:
            self.hoveredImage = pygame.image.load(hoveredImagePath).convert_alpha()
        else:
            self.hoveredImage = self.unhoveredImage
        if self.hovered:
            self.image = self.hoveredImage
        else:
            self.image = self.unhoveredImage
        self.imagePath = imagePath
        self.hoveredImagePath = hoveredImagePath
        self.upd()

    def move(self, x, y):
        self.xPos, self.yPos = x, y
        self.upd()

    def render(self, surface):
        surface.blit(self.image, self.rect)

    def clicked(self):
        if self.config.eventPos is not None:
            if self.rect.collidepoint(self.config.eventPos):
                return True
        return False

    def onHover(self, mousePos):

        if self.rect.collidepoint(mousePos) and not self.hovered:
            self.image = self.hoveredImage
            self.hovered = True
            self.upd('surf')
            self.hoverHandler(self.name)
            return True
        elif not self.rect.collidepoint(mousePos) and self.hovered:
            self.image = self.unhoveredImage
            self.hovered = False
            self.upd('surf')
            self.hoverHandler('hidden')
        return False

    def handleEvent(self):
        if self.clicked():
            if not self.config.soundExclusion():
                self.sfx.playSfx('Assets/SFX/click.mp3')
            self.clickHandler()
            return True
        return False

    def handleHover(self):
        if self.onHover(self.config.mousePos):
            if not self.config.soundExclusion():
                self.sfx.playSfx('Assets/SFX/hover.mp3')
            self.hoverHandler(self.name)
            return True
        return False