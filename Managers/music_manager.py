import pygame
from Managers.config_manager import ConfigManager

# The universal music manager, also a singleton instance that allows the music to be picked from the game manager according to the current state of the game
class MusicManager:
    _instance = None

    _tracks = {
        'hub': 'Assets/Music/menu.mp3',
        'dungeon': 'Assets/Music/dungeon.mp3',
        'jungle': 'Assets/Music/jungle.mp3',
        'bastion': 'Assets/Music/bastion.mp3',
        'sea': 'Assets/Music/sea.mp3',
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = ConfigManager()
            pygame.mixer.music.set_volume(cls._instance.config.musicVolume)
            cls._instance.previousVolume = cls._instance.config.musicVolume
        return cls._instance

    def playTrack(self, trackName: str, loops: int = -1):
        path = self._tracks.get(trackName)
        if not path:
            raise ValueError(f"No such track: {trackName}")
        pygame.mixer.music.stop()
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.config.musicVolume)
        pygame.mixer.music.play(loops)

    def stop(self):
        pygame.mixer.music.stop()

    def syncVolume(self):
        if self.previousVolume != self.config.musicVolume:
            pygame.mixer.music.set_volume(self.config.musicVolume)
        self.previousVolume = self.config.musicVolume