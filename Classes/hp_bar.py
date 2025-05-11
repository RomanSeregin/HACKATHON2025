import pygame
from Classes.image import Image
from Managers.config_manager import ConfigManager

"""
The universal handler of the HP counters (due to the fact that they are actually animations).
Keeps track of the HP values both of the boss and the player. Makes sure that they don't go beyond the limits, updates the state if needed.
Simple animated HP bar class.
"""
class HPBar:
    def __init__(self, x, y, imagesPath, name, _):
        self.xPos = x
        self.yPos = y
        self.imagesPath = imagesPath
        self.name = name
        self.config = ConfigManager()
        self.currentHp = getattr(self.config, self.name)
        self.element = Image(self.xPos, self.yPos, f'{self.imagesPath}/{self.currentHp:03}.png', name=self.name)

    def render(self, surface):
        self.handleUpdate()
        self.element.render(surface)

    def handleUpdate(self):
        newHp = getattr(self.config, self.name)
        if newHp != self.currentHp:
            if newHp <= 0:
                newHp = 1
                if self.name == 'bossHP':
                    self.config.state = 'dungeonWin'
                elif self.name == 'playerHP':
                    self.config.state = 'dungeonLose'
            elif newHp >= self.config.backupPlayerHP:
                newHp = self.config.backupPlayerHP
            self.currentHp = newHp
            self.element = Image(self.xPos, self.yPos, f'{self.imagesPath}/{self.currentHp:03}.png', name=self.name)
            return True
        return False