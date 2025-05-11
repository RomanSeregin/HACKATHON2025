from Classes.interactive_element import InteractiveElement
from Managers.config_manager import ConfigManager
import pygame


"""
A now unused element, which was used to have toggle actions
Later swapped for inter-active buttons.
Was used in the beta version of the settings for the difficulty toggle.
"""
class Toggle(InteractiveElement):
    def __init__(self, name, position, initial_value, min_value, max_value, track_image_path, knob_image_path, toggleHandler):
        super().__init__(name, position[0], position[1], min_value, max_value, initial_value)
        self.track_surf = pygame.image.load(track_image_path).convert_alpha()
        self.knob_surf = pygame.image.load(knob_image_path).convert_alpha()
        self.track_rect = self.track_surf.get_rect(topleft=position)
        self.knob_rect = self.knob_surf.get_rect()
        self.name = name
        self.toggleHandler = toggleHandler
        self.config = ConfigManager()
        self._update_knob_position()

    def _update_knob_position(self):
        self.knob_rect.x = self.track_rect.left + 6 if self.value == self.min_value else self.track_rect.right - self.knob_rect.width - 6
        self.knob_rect.y = self.track_rect.centery - self.knob_rect.height // 2

    def setValue(self, value):
        self.value = value
        self._update_knob_position()

    def toggled(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN and self.track_rect.collidepoint(event.pos):
            self.value = self.min_value if self.value == self.max_value else self.max_value
            self._update_knob_position()
            return True
        return False

    def render(self, surface):
        surface.blit(self.track_surf, self.track_rect.topleft)
        surface.blit(self.knob_surf, self.knob_rect.topleft)

    def handleEvent(self):
        if self.toggled(self.config.event):
            self.toggleHandler(self.value)
            return True
        return False