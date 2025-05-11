import pygame
from abc import ABC
from Managers.config_manager import ConfigManager
from Classes.screen import Screen
from Classes.image import Image
from Classes.button import Button
from Classes.slider import Slider
from constants import settingsPath

"""
A screen that handles a lot of config updated to do with the difficulty / the volume settings.
Updates the properties of the game, allowing to get a different gameplay on different difficulty levels.
Supports sliders, toggles, buttons, stores the variables and makes sure that they are processed correctly upon interaction.
"""
class Settings(Screen, ABC):
    def __init__(self):
        self.config = ConfigManager()
        self.settingsPath = settingsPath
        super().__init__()

    def setup(self):
        self.elements = [
            Image(0, 0, f'{settingsPath}/images/background.png'),
            Slider('volumeSlider', (535, 270), self.config.musicVolume, 0, 1,
                   f'{settingsPath}/buttons/sliderTrack.png',
                   f'{settingsPath}/buttons/sliderKnob.png',
                   sliderHandler=self.handleMusicSlider),
            Slider('sfxSlider', (535, 377), self.config.sfxVolume, 0, 0.6,
                   f'{settingsPath}/buttons/sliderTrack.png',
                   f'{settingsPath}/buttons/sliderKnob.png',
                   sliderHandler=self.handleSFXSlider),
            Button('difficultyEasy', 534, 579,
                   f'{settingsPath}/buttons/difficulty-a.png',
                   None,
                   destination='settings', clickHandler=self.handleEasyDifficulty),
            Button('difficultyHard', 683, 579,
                   f'{settingsPath}/buttons/difficulty.png',
                   f'{settingsPath}/buttons/difficulty-a.png',
                   destination='settings', clickHandler=self.handleHardDifficulty),
            Button('accept', 690, 655,
                   f'{settingsPath}/buttons/accept.png',
                   f'{settingsPath}/buttons/accept-a.png',
                   destination='menu', clickHandler=self.handleAcceptButton),
            Button('cancel', 508, 655,
                   f'{settingsPath}/buttons/cancel.png',
                   f'{settingsPath}/buttons/cancel-a.png',
                   destination='menu', clickHandler=self.handleCancelButton)
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
        for element in self.elements:
            element.render(surface)

    def handleMusicSlider(self, value):
        self.config.musicVolume = value

    def handleSFXSlider(self, value):
        self.config.sfxVolume = value

    def handleDifficultyToggle(self, value):
        self.config.difficultyLevel = value

    # handling the cancel button to revert the state if the user decided to cancel their changes.
    def handleCancelButton(self):
        self.config.musicVolume = self.config.backupMusicVolume
        self.config.sfxVolume = self.config.backupSFXVolume
        self.config.difficultyLevel = self.config.backupDifficultyLevel
        self.config.updateVolumeLevels()

        for elem in self.elements:
            if isinstance(elem, Slider):
                if elem.name == 'volumeSlider':
                    elem.setValue(self.config.musicVolume)
                elif elem.name == 'sfxSlider':
                    elem.setValue(self.config.sfxVolume)
            elif isinstance(elem, Button) :
                if elem.name == 'difficultyEasy':
                    if self.config.difficultyLevel == 0:
                        elem.updateTexture(f'{settingsPath}/buttons/difficulty-a.png')
                    if self.config.difficultyLevel == 1:
                        elem.updateTexture(f'{settingsPath}/buttons/difficulty.png')
                elif elem.name == 'difficultyHard':
                    if self.config.difficultyLevel == 1:
                        elem.updateTexture(f'{settingsPath}/buttons/difficulty-a.png')
                    if self.config.difficultyLevel == 0:
                        elem.updateTexture(f'{settingsPath}/buttons/difficulty.png')

        self.config.state = 'menu'

    def handleAcceptButton(self):
        self.config.backupMusicVolume = self.config.musicVolume
        self.config.backupSFXVolume = self.config.sfxVolume
        self.config.backupDifficultyLevel = self.config.difficultyLevel
        self.config.state = 'menu'

    # toggle function for the easy difficulty button (updates the texture to the opposite of the other button)
    def handleEasyDifficulty(self):
        self.config.difficultyLevel = 0
        self.config.updateDifficulty()
        for element in self.elements:
            if isinstance(element, Button):
                if element.name == 'difficultyEasy':
                    element.updateTexture(f'{settingsPath}/buttons/difficulty-a.png', None)
                if element.name == 'difficultyHard':
                    element.updateTexture(f'{settingsPath}/buttons/difficulty.png', f'{settingsPath}/buttons/difficulty-a.png')

    # toggle function for the easy difficulty button (updates the texture to the opposite of the other button)
    def handleHardDifficulty(self):
        self.config.difficultyLevel = 1
        self.config.updateDifficulty()
        for element in self.elements:
            if isinstance(element, Button):
                if element.name == 'difficultyEasy':
                    element.updateTexture(f'{settingsPath}/buttons/difficulty.png', f'{settingsPath}/buttons/difficulty-a.png')
                if element.name == 'difficultyHard':
                    element.updateTexture(f'{settingsPath}/buttons/difficulty-a.png', None)
