import pygame
from Managers.config_manager import ConfigManager


# The universal SFX manager, that is a singleton, that can allow the elements to execute any needed sound effects in game.
class SFXManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = ConfigManager()
            cls._instance.previousVolume = cls._instance.config.sfxVolume
            cls._instance._activeSounds = []
        return cls._instance

    def playSfx(self, path: str):
        snd = pygame.mixer.Sound(path)
        snd.set_volume(self.config.sfxVolume)
        channel = snd.play()
        self._activeSounds.append(snd)
        return channel

    def syncVolume(self):
        if self.previousVolume != self.config.sfxVolume:
            for snd in self._activeSounds:
                snd.set_volume(self.config.sfxVolume)
            self.previousVolume = self.config.sfxVolume