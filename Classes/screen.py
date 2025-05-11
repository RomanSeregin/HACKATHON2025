import pygame
from Managers.config_manager import ConfigManager
from abc import ABC, abstractmethod

"""
The second-level parental class of the code. The screen structure is defined by this parent.
Is abstract to make sure that all the children have the required methods to be later processed at the GameManager
Doesn't do much by itself.
"""
class Screen(ABC):
    def __init__(self):
        self.config = ConfigManager()
        self.elements = []
        self.setup()

    @abstractmethod
    def setup(self):

        pass

    @abstractmethod
    def handleEvent(self):

        pass

    @abstractmethod
    def handleHover(self):
        pass

    @abstractmethod
    def render(self):

        pass