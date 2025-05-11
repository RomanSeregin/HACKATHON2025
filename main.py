import pygame
from sys import exit
from constants import BLACK, FPS, RESOLUTION
from pygame._sdl2.video import Window
from Managers.game_manager import GameManager
from Managers.config_manager import ConfigManager
from Classes.cursor import Cursor

pygame.display.init()
pygame.font.init()
pygame.mixer.init()

# Loading screen with zero black frames beforehand, done for the best look
screen = pygame.display.set_mode(RESOLUTION, pygame.NOFRAME)
win = Window.from_display_module()
win.hide()
screen.blit(pygame.image.load('Assets/Graphics/loading.png'), (0, 0))
win.show()
pygame.mouse.set_visible(False)
pygame.display.update()

cursor = Cursor(r'Assets\Graphics\0menu\images\cursors\cursor.png')
clock = pygame.time.Clock()

game = GameManager()
config = ConfigManager()

while True:
    # putting the main variables into the universal config - the variable storage for this code. The variables stored in config aren't the same thing as constants, as the constant variables never change
    events = pygame.event.get()
    mousePos = pygame.mouse.get_pos()
    cursor.move(mousePos[0], mousePos[1])
    mouseState = pygame.mouse.get_pressed()
    config.mouseUpdate(mousePos, mouseState)
    config.eventPos = None

    for event in events:
        if event.type == pygame.QUIT or config.exitFlag:
            pygame.quit()
            exit()

        # this is done to directly affect the input latency, as the handleEvent for the game manager may not be able to achieve very fast computational times due to the size.
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            config.eventPos = event.pos

    # the managers do all the work for us. All the managers are singleton instances, meaning that only one example of them can be created at any given moment.
    game.handleEvent(events)
    screen.fill(BLACK)
    game.render(screen)

    cursor.render(screen)

    clock.tick(FPS)
    pygame.display.update()
