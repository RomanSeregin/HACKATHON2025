"""
As Python doesn't have constants, unlike other languages - i just made them UPPERCASE so that they can be seen as constants in the first place.
The only exception being the paths, as they take part in the naming convention, and, to be fair, just look nicer being camelCase
"""


SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 760
FPS = 60
RESOLUTION = (SCREEN_WIDTH, SCREEN_HEIGHT)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

ICE_POSITIONS = [
    (130, 119),
    (452, 22),
    (772, 22),
    (815, 268),
    (480, 268),
    (144, 433),
    (815, 497)
]

# the path variables for objects to use for path length optimizations
menuPath = 'Assets/Graphics/0menu'
settingsPath = 'Assets/Graphics/1settings'
aboutPath = 'Assets/Graphics/2about'
introPath = 'Assets/Graphics/3intro'
hubPath = 'Assets/Graphics/4hub'
questsPath = 'Assets/Graphics/5quests'
endingPath = 'Assets/Graphics/6ending'
