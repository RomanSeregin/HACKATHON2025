import random
import pygame
from Managers.config_manager import ConfigManager
from constants import questsPath

"""
The backbone class of the seaFishMinigame.
Handles the entire level generation, the guaranteed bubble and finder spawns, although random, in the level.
Handles the movement of the object, optimizes them via removing them if they can't be seen.
"""
class SeaItemsGenerator:
    def __init__(self, spawn_interval=2.0, total_time=45, speed=2):
        self.spawn_x = 1360
        self.row_ys = [164, 336, 508]
        self.textures = {
            'fish': pygame.image.load(f'{questsPath}/sea/Level2/images/fish.png').convert_alpha(),
            'airBubble': pygame.image.load(f'{questsPath}/sea/Level2/images/airBubble.png').convert_alpha(),
            'finder': pygame.image.load(f'{questsPath}/sea/Level2/images/finder.png').convert_alpha(),
        }


        self.initial_spawn_interval = spawn_interval
        self.initial_total_time = total_time
        self.initial_speed = speed


        self.reset()

    def reset(self):


        total_columns = int(self.initial_total_time / self.initial_spawn_interval)
        spawnable_columns = list(range(min(total_columns, 23)))
        random.shuffle(spawnable_columns)

        self.bubble_cols = set(spawnable_columns[:3])
        self.finder_cols = set(spawnable_columns[3:4])
        self.column_count = 0
        self.prev_empty = None
        self.objects = []
        self.speed = self.initial_speed


        self.spawn_timer = 0
        self.spawn_interval = self.initial_spawn_interval * 60

    def generate_column(self):

        fish_positions = [0, 1, 2]


        if self.column_count == 0:

            empty = random.choice([0, 1, 2])
        else:

            if self.prev_empty == 0:
                empty = random.choice([0, 1])
            elif self.prev_empty == 2:
                empty = random.choice([1, 2])
            else:
                empty = random.choice([0, 1, 2])


        fish_positions.remove(empty)


        special_item = None
        if self.column_count in self.bubble_cols:
            special_item = 'airBubble'
        elif self.column_count in self.finder_cols:
            special_item = 'finder'


        for row in fish_positions:
            img = self.textures['fish']
            rect = img.get_rect(topleft=(self.spawn_x, [173, 345, 517][row]))
            self.objects.append({'type': 'fish', 'rect': rect, 'image': img})


        if special_item:
            img = self.textures[special_item]
            rect = img.get_rect(topleft=(self.spawn_x - 40, [153, 326, 488][empty]))
            self.objects.append({'type': special_item, 'rect': rect, 'image': img})

        self.prev_empty = empty
        self.column_count += 1

    def render(self, surface):

        self.spawn_timer += 1


        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            self.generate_column()


        for obj in list(self.objects):
            obj['rect'].x -= self.speed
            if obj['rect'].right < -200:
                self.objects.remove(obj)
            else:
                surface.blit(obj['image'], obj['rect'])