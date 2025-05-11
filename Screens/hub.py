import pygame
from abc import ABC
from Managers.config_manager import ConfigManager
from Classes.screen import Screen
from Classes.image import Image
from Classes.button import Button
from Classes.tooltip import Tooltip
from constants import hubPath

"""
The class that is the gateway for most levels (like jungle, sea, dungeon, bastion, the palace etc.
Allows the setup and departure of the buttons to the other states with optimizations. The hub is a singleton to prevent any mistakes if called incorrectly (which it shouldn't be)
"""
class Hub(Screen, ABC):
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self.__class__._initialized:
            return
        self.config = ConfigManager()
        self.hubPath = hubPath
        super().__init__()
        self.__class__._initialized = True

    # the general setup procedure: populating self.elements with images, buttons and a tooltip. Handles lower-level objects like buttons, images..
    def setup(self):
        self.elements = [
            Image(0, 0, f'{hubPath}/images/background.png'),
            Button('bastion', 222, 133, f'{hubPath}/buttons/bastion.png', f'{hubPath}/buttons/bastion-a.png', destination='bastionEntrance', hoverHandler=self.buttonHoverState),
            Button('dungeon', 608, 116, f'{hubPath}/buttons/dungeon.png', f'{hubPath}/buttons/dungeon-a.png', destination='dungeonEntrance', hoverHandler=self.buttonHoverState),
            Button('jungle', 250, 380, f'{hubPath}/buttons/jungle.png', f'{hubPath}/buttons/jungle-a.png', destination='jungleEntrance', hoverHandler=self.buttonHoverState),
            Button('palace', 582, 448, f'{hubPath}/buttons/palace.png', f'{hubPath}/buttons/palace-a.png', destination='ending0', clickHandler=self.handlePalaceButton, hoverHandler=self.buttonHoverState),
            Button('sea', 880, 396, f'{hubPath}/buttons/sea.png', f'{hubPath}/buttons/sea-a.png', destination='seaEntranceLocked', clickHandler=self.handleSeaButton, hoverHandler=self.buttonHoverState),
            Tooltip('hidden', 0, 0, f'{hubPath}/images/tipsSuggest.png'),
            Button('menu', 1058, 15, f'{hubPath}/buttons/menu.png', None, destination='menu')
        ]

    def handleEvent(self):
        for element in self.elements:
            if hasattr(element, 'handleEvent'):
                if element.handleEvent():
                    break

    def handleHover(self):
        for element in self.elements:
            if hasattr(element, 'handleHover'):
                if element.handleHover():
                    break

    def render(self, surface):
        self.updateButtonStates()
        for element in self.elements:
            element.render(surface)

    # check for the locked palace button unless all of the levels are complete
    def handlePalaceButton(self):
        if self.config.unlockPalace:
            self.config.state = 'ending0'
            self.config.levelCompletionStates['palace'] = True
            return True
        return False

    # Assigns the island gateways to the levels an updated texture if it detects that they have been completed. Unlocks the palace if the condition that 4 items in the dict are unlocked - unlocks palace afterwards
    def updateButtonStates(self):
        if self.config.updateHub:
            self.config.updateHub = False
            self.config.updateDifficulty()
            for element in self.elements:
                if isinstance(element, Button) and element.name in self.config.levelCompletionStates:
                    imagePath = f"{hubPath}/buttons/{'complete/' if self.config.levelCompletionStates[element.name] else ''}{element.name}.png"
                    hoveredPath = f"{hubPath}/buttons/{'complete/' if self.config.levelCompletionStates[element.name] else ''}{element.name}-a.png"
                    element.updateTexture(imagePath, hoveredPath)
                    if self.config.levelCompletionStates[element.name] is True:
                        element.clickHandler = self.wonButtonHandler
            completed_count = sum(
                1 for level, done in self.config.levelCompletionStates.items()
                if level != "palace" and done is True
            )
            if completed_count >= 4:
                self.config.unlockPalace = True

    def buttonHoverState(self, name):
        self.config.tooltipName = name

    def wonButtonHandler(self):
        pass

    # handles the fact that the player can't enter the sea bastion unless they complete the air bastion first for a bless (a shield of air)
    def handleSeaButton(self):
        if self.config.unlockSea:
            self.config.state = 'seaEntranceUnlocked'
            return
        self.config.state = 'seaEntranceLocked'
        return
