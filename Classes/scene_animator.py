import pygame
from Classes.entity_delay import EntityDelay
from Classes.image import Image

"""
The back bone for all of the animations (specifically in the dungeon level QTE)
The SceneAnimator handles the action that is done at the point in time, handling events via entityDelay, handles multiple different possible animations.
Has default values, except for those in the init.
"""
class SceneAnimator:
    def __init__(self, x, y, name, defaultPath, frameDelay):
        self.x = x
        self.y = y
        self.name = name
        self.defaultPath = defaultPath
        self.frameDelay = frameDelay
        self.delay = EntityDelay()
        self.animations = {}
        self.currentAnim = None
        self.animIndex = 0
        self.animCount = 0
        self.element = Image(self.x, self.y, self.defaultPath, name=self.name)

    def loadAnimation(self, animName, frameCount, animPath):
        self.animations[animName] = [f'{animPath}/{i:03}.png' for i in range(1, frameCount + 1)]

    def play(self, animName):
        if animName not in self.animations:
            return
        self.currentAnim = animName
        self.animIndex = 0
        self.animCount = len(self.animations[animName])
        self.delay.start(animName, self.frameDelay)
        path = self.animations[animName][0]
        self.element = Image(self.x, self.y, path, name=self.name)

    def handleAnimation(self):
        self.delay.increment()
        if self.currentAnim and self.delay.delayOnce(self.currentAnim):
            self.animIndex += 1
            if self.animIndex < self.animCount:
                path = self.animations[self.currentAnim][self.animIndex]
                self.element = Image(self.x, self.y, path, name=self.name)
                self.delay.start(self.currentAnim, self.frameDelay)
            else:
                self.delay.stop(self.currentAnim)
                self.currentAnim = None
                self.element = Image(self.x, self.y, self.defaultPath, name=self.name)
            return True
        return False

    def render(self, surface):
        self.handleAnimation()
        if self.element:
            self.element.render(surface)