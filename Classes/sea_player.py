import pygame
from Managers.config_manager import ConfigManager
from constants import questsPath

"""
Simple player class to appear in the seaFishMinigame, interacts with the sea items generator.
Handles simple events, like keyboard inputs, collision and rendering.
Has typical values and methods.
"""
class SeaPlayer:
    def __init__(self, speed=5):
        self.config = ConfigManager()
        self.image = pygame.image.load(f'{questsPath}/sea/Level2/images/player.png').convert_alpha()
        self.initial_position = (50, 325)
        self.rect = self.image.get_rect(topleft=self.initial_position)
        self.speed = speed
        self.min_y = 166
        self.max_y = 564

    def reset(self):

        self.rect.topleft = self.initial_position

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            new_y = self.rect.y - self.speed
            if new_y < self.min_y:
                new_y = self.min_y
            self.rect.y = new_y

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            new_y = self.rect.y + self.speed
            if new_y > self.max_y:
                new_y = self.max_y
            self.rect.y = new_y

    def render(self, surface):
        surface.blit(self.image, self.rect)