from Classes.interactive_element import InteractiveElement
from Managers.config_manager import ConfigManager
import pygame


"""
Slider object, child on an interactive elemnt handles a slider.
Creates a slider object with an extended hitbox that detects the current position of the slider relative to its
track, and converts it into a usable value
Used in settings to set the SFX volume, and the music volume parameters.
Has typical properties and methods, long init.
"""
class Slider(InteractiveElement):
    def __init__(self, name, position, initial_value, min_value, max_value, track_image_path, knob_image_path, sliderHandler):
        super().__init__(name, position[0], position[1], min_value, max_value, initial_value)
        self.track_surf = pygame.image.load(track_image_path).convert_alpha()
        self.knob_surf = pygame.image.load(knob_image_path).convert_alpha()
        self.track_rect = self.track_surf.get_rect(topleft=position)
        self.collide_rect = self.track_rect.inflate(0, 30)
        self.knob_rect = self.knob_surf.get_rect()
        self._dragging = False
        self.sliderHandler = sliderHandler
        self.name = name
        self.config = ConfigManager()
        self._update_knob_position()

    def setValue(self, value):

        self.value = value
        self._update_knob_position()

    def getValue(self):

        return self.value

    def _update_knob_position(self):
        rel = (self.value - self.min_value) / (self.max_value - self.min_value)
        knob_x = self.track_rect.x + rel * self.track_rect.width
        knob_y = self.track_rect.centery
        self.knob_rect = self.knob_surf.get_rect(center=(knob_x, knob_y))

    def movedSlider(self, event, mouse_state):

        if event.type == pygame.MOUSEBUTTONDOWN and (self.knob_rect.collidepoint(event.pos) or self.collide_rect.collidepoint(event.pos)):
            self._dragging = True
        elif event.type == pygame.MOUSEBUTTONUP or not mouse_state[0]:
            self._dragging = False
        if self._dragging and mouse_state[0]:
            x = event.pos[0] - self.track_rect.x
            x = max(0, min(x, self.track_rect.width))
            self.value = self.min_value + (x / self.track_rect.width) * (self.max_value - self.min_value)
            self._update_knob_position()
            return True
        return False

    def render(self, surface):
        surface.blit(self.track_surf, self.track_rect.topleft)
        surface.blit(self.knob_surf, self.knob_rect.topleft)

    def handleEvent(self):
        if self.movedSlider(self.config.event, self.config.mouseState):
            self.sliderHandler(self.value)
            return True
        return False