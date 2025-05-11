import pygame
from Managers.config_manager import ConfigManager

"""
The text object is hard-coded, which isn't good.
The text object handles real-time updating prompts to give the user info
Oftentimes used in the countdowns, so that the user knows how much time they've got left.
Usual class, long init as for the setup. Handles the prompt automatically via the config. 
"""
class Text:
    def __init__(self, name, xPos, yPos, size, color, eventHandler=None, font=None, opacity=255, lineSpacing=5, method='topleft'):
        self.xPos, self.yPos, self.size, self.lineSpacing = xPos, yPos, size, lineSpacing
        self.color, self.font, self.opacity = color, font, opacity
        self.font = pygame.font.Font(font, self.size)
        self.config = ConfigManager()
        self._prompt = ''
        self.method = method
        self.surface = self.createSurface()
        self.rect = self.createRect()
        self.name = name
        self.eventHandler = eventHandler

    @property
    def prompt(self):
        return self._prompt

    @prompt.setter
    def prompt(self, value):
        self._prompt = value
        self.upd('all')

    def createSurface(self, opacity=None):
        if opacity is None:
            opacity = self.opacity
        lines = self.prompt.split('\n')
        line_surfaces, max_width, total_height = [], 0, 0
        for line in lines:
            line_surface = self.font.render(line, True, self.color)
            line_surface.set_alpha(opacity)
            line_surfaces.append(line_surface)
            max_width = max(max_width, line_surface.get_width())
            total_height += line_surface.get_height()
        self.surface = pygame.Surface((max_width, total_height), pygame.SRCALPHA)
        current_y = 0
        for line_surface in line_surfaces:
            self.surface.blit(line_surface, (0, current_y))
            current_y += line_surface.get_height()
        return self.surface

    def createRect(self):
        if self.method == 'topleft':
            return self.surface.get_rect(topleft=(self.xPos, self.yPos))
        elif self.method == 'center':
            return self.surface.get_rect(center=(self.xPos, self.yPos))

    def upd(self, args='all'):
        if args == 'all':
            self.surface, self.rect = self.createSurface(), self.createRect()
        elif args == 'surf':
            self.surface = self.createSurface()
        elif args == 'rect':
            self.rect = self.createRect()

    def render(self, surface):
        self.handleCustomCases()
        surface.blit(self.surface, self.rect)

    def handleCustomCases(self):
        if self.name == 'info':
            if 'dungeonIce' in self.config.state:
                self.prompt = self.config.dungeonIceText if self.prompt != self.config.dungeonIceText else self.prompt
            elif 'qte' in self.config.state.lower():
                self.prompt = self.config.dungeonPanelText if self.prompt != self.config.dungeonPanelText else self.prompt
            elif 'jungle' in self.config.state:
                self.prompt = self.config.jungleText if self.prompt != self.config.jungleText else self.prompt
            elif 'seaFish' in self.config.state:
                self.prompt = self.config.seaFishText if self.prompt != self.config.seaFishText else self.prompt
            elif 'seaRing' in self.config.state:
                self.prompt = self.config.seaRingText if self.prompt != self.config.seaRingText else self.prompt
            elif 'bastionKnowledge' in self.config.state:
                self.prompt = self.config.bastionKnowledgeText if self.prompt != self.config.bastionKnowledgeText else self.prompt
            elif 'bastionMemory' in self.config.state:
                self.prompt = self.config.bastionMemoryText if self.prompt != self.config.bastionMemoryText else self.prompt