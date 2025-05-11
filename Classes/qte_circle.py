import os
import pygame
from Managers.config_manager import ConfigManager

"""
The core mechanic for the dungeon level QTE
the QTE circle is an animated simple object that can return whether it was clicked in time or not
Has the typical methods (render, handleEvent), and typical parameters (pos, animation path etc.)
"""
class QTECircle:
    def __init__(self, x, y, animationPath):
        self.x = x
        self.y = y
        self.animationFrames = []
        self.currentFrame = 0
        self.config = ConfigManager()
        self.loadAnimationFrames(animationPath)
        self.rect = self.animationFrames[0].get_rect(topleft=(x, y))
        self.hitFrames = range(91, 116 + 1)
        self.finished = False

    def loadAnimationFrames(self, animationPath):
        for i in range(120):
            framePath = os.path.join(animationPath, f"{i:04d}.png")
            self.animationFrames.append(pygame.image.load(framePath).convert_alpha())

    def render(self, screen):
        self.handlePress()
        screen.blit(self.animationFrames[self.currentFrame], (self.x, self.y))
        if not self.finished:
            if self.currentFrame < len(self.animationFrames) - 1:
                self.currentFrame += 1
            else:
                self.finished = True

    def click(self):
        return self.currentFrame in self.hitFrames

    def handlePress(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.finished:
            self.finished = True
            return self.click()
        return False


    def reset(self):
        self.currentFrame = 0
        self.finished = False