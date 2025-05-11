import pygame
from abc import ABC, abstractmethod

"""
Abstract class
A parent class that is the base for many interactive elements (toggles, sliders..)
The class manages how the base patterns are set, so that the interactive element children always have those methods.
Abstract class so that there is organization for the future children.
Stores default properties (non-extended), being the position, the values, initial values..
"""
class InteractiveElement(ABC):

    def __init__(self, name, xPos, yPos, min_value, max_value, initial_value):
        self.xPos = xPos
        self.yPos = yPos
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.name = name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, newValue):
        self._value = max(min(newValue, self.max_value), self.min_value)

    @abstractmethod
    def handleEvent(self):

        pass

    @abstractmethod
    def render(self):

        pass