import pygame
from abc import ABC

from Classes.qte_circle import QTECircle
from Managers.config_manager import ConfigManager
from Managers.sfx_manager import SFXManager
from Classes.screen import Screen
from Classes.image import Image
from Classes.button import Button
from Classes.hp_bar import HPBar
from Classes.delay import Delay
from Classes.text import Text
from Classes.scene_animator import SceneAnimator
from Classes.entity_delay import EntityDelay
from constants import questsPath

"""
The QTE minigame
Has multiple class instances incorporated within, like hp bars, qte circle objects and on
Handles advanced overall logic to do with the fights of the player and the boss.
Stores the animations for the entities to reuse them later.
Generally handles most of the events by itself, sometimes reverting to the config managers variables.
"""
class DungeonQTE(Screen, ABC):
    def __init__(self):
        self.config = ConfigManager()
        self.questsPath = questsPath
        self.sfx = SFXManager()
        super().__init__()

    def setup(self):
        self.currentPhase       = 'attackPreparation'
        self.currentAction      = None
        self.lastQteSuccess     = False
        self.lastBossQteSuccess = False

        self.delayCounter = 0
        self.delayActive  = False

        self.waitingForHpChange = False
        self.hpChangeDelayCounter = 0

        animator = SceneAnimator(0, 0, 'animator', 'Assets/Animations/default.png', 10)
        self.animator = animator
        animator.loadAnimation('bossAttackFail',     9, 'Assets/Animations/bossAttackFail')
        animator.loadAnimation('bossAttackSuccess', 10, 'Assets/Animations/bossAttackSuccess')

        animator.loadAnimation('playerFireballAttackFail',  10, 'Assets/Animations/playerFireballAttackFail')
        animator.loadAnimation('playerFireballAttackSuccess',10,'Assets/Animations/playerFireballAttackSuccess')

        animator.loadAnimation('playerIcicleAttackFail', 10, 'Assets/Animations/playerIcicleAttackFail')
        animator.loadAnimation('playerIcicleAttackSuccess', 10, 'Assets/Animations/playerIcicleAttackSuccess')

        animator.loadAnimation('playerHealFail', 8, 'Assets/Animations/playerHealFail')
        animator.loadAnimation('playerHealSuccess', 8, 'Assets/Animations/playerHealSuccess')

        self.orig_elements = [
            animator,
            HPBar(0,   498, f'Assets/Animations/HPLeft',  'bossHP',   self.config.bossHP),
            HPBar(1048,498, f'Assets/Animations/HPRight', 'playerHP', self.config.playerHP),
        ]

        self.attack_preparation_elements = [
            Image(266, 537, f'{questsPath}/dungeon/Level3/images/gui.png', name='gui'),
            Button('fireball', 484, 606, f'{questsPath}/dungeon/Level3/buttons/fireball.png', clickHandler=self.fireballHandler),
            Button('icicle',   640, 606, f'{questsPath}/dungeon/Level3/buttons/icicle.png',   clickHandler=self.icicleHandler),
            Button('potion',   796, 606, f'{questsPath}/dungeon/Level3/buttons/potion.png',   clickHandler=self.potionHandler),
            Text('info', 460, 694, 22, (37, 69, 105))
        ]

        self.qte_elements = [
            QTECircle(563, 240, 'Assets/Animations/QTECircle')
        ]

        self.elements = list(self.orig_elements)
        self.updating = True

    def handleEvent(self):
        if self.currentPhase in ('playerQTE', 'bossQTE'):
            self.qte_elements[0].handlePress()
            return
        for element in self.elements:
            if hasattr(element, 'handleEvent') and element.handleEvent():
                break

    def update(self):
        if self.config.dungeonRestoreQTE:
            self.config.dungeonRestoreQTE = False
            self.resetLevel()
        if self.currentPhase == 'playerQTE':
            q = self.qte_elements[0]
            if q.finished:
                self.lastQteSuccess = q.click()
                if self.currentAction == 'fireball':
                    anim = 'playerFireballAttackSuccess' if self.lastQteSuccess else 'playerFireballAttackFail'
                    self.sfx.playSfx('Assets/SFX/fireball.mp3')
                elif self.currentAction == 'icicle':
                    anim = 'playerIcicleAttackSuccess' if self.lastQteSuccess else 'playerIcicleAttackFail'
                    self.sfx.playSfx('Assets/SFX/fireball.mp3')
                elif self.currentAction == 'potion':
                    anim = 'playerHealSuccess' if self.lastQteSuccess else 'playerHealFail'
                    self.sfx.playSfx('Assets/SFX/healthUse.mp3')

                if anim:
                    self.animator.play(anim)

                self.hpChangeDelayCounter = 0
                self.waitingForHpChange = True
                self.currentPhase = 'playerDelay'
                self.delayActive = True
                self.delayCounter = 0
                self.updating = True


        elif self.currentPhase == 'bossQTE':
            if self.config.bossHP <= 0:
                self.currentPhase = 'attackPreparation'
                self.updating = True
            else:
                q = self.qte_elements[0]
                if q.finished:
                    self.lastBossQteSuccess = q.click()
                    self.animator.play('bossAttackFail' if self.lastBossQteSuccess else 'bossAttackSuccess')
                    self.hpChangeDelayCounter = 0
                    self.waitingForHpChange = True
                    self.currentPhase = 'bossDelay'
                    self.delayActive = True
                    self.delayCounter = 0
                    self.updating = True


        if self.currentPhase == 'playerDelay' and self.delayActive:
            self.delayCounter += 1
            if self.waitingForHpChange:
                self.hpChangeDelayCounter += 1
                if self.hpChangeDelayCounter >= 80:
                    self.waitingForHpChange = False

                    if self.currentAction == 'fireball' and self.lastQteSuccess:
                        self.config.bossHP -= self.config.playerDamageFireball
                    elif self.currentAction == 'icicle' and self.lastQteSuccess:
                        self.config.bossHP -= self.config.playerDamageIcicle
                    elif self.currentAction == 'potion':
                        self.config.playerHP += (self.config.healingEfficiency[0] if self.lastQteSuccess else self.config.healingEfficiency[1])

            if self.delayCounter >= 120:
                self.currentPhase = 'bossQTE'
                self.updating = True
                self.delayActive = False

        elif self.currentPhase == 'bossDelay' and self.delayActive:
            self.delayCounter += 1
            if self.waitingForHpChange:
                self.hpChangeDelayCounter += 1
                if self.hpChangeDelayCounter >= 80:
                    self.waitingForHpChange = False
                    if not self.lastBossQteSuccess:
                        self.config.playerHP -= self.config.bossDamage

            if self.delayCounter >= 120:
                self.currentPhase = 'attackPreparation'
                self.updating = True
                self.delayActive = False

        if self.updating:
            self.updating = False
            if self.currentPhase == 'attackPreparation':
                self.elements = self.orig_elements + self.attack_preparation_elements
            elif self.currentPhase == 'playerQTE':
                self.qte_elements[0].reset()
                self.elements = self.orig_elements + self.qte_elements
            elif self.currentPhase == 'playerDelay':
                self.elements = self.orig_elements
            elif self.currentPhase == 'bossQTE':
                self.qte_elements[0].reset()
                self.elements = self.orig_elements + self.qte_elements
            else:
                self.elements = self.orig_elements

    def handleHover(self):
        pass

    def render(self, surface):
        self.update()
        for element in self.elements:
            element.render(surface)

    def fireballHandler(self):
        self.currentAction = 'fireball'
        self.qte_elements[0].reset()
        self.currentPhase = 'playerQTE'
        self.updating     = True

    def icicleHandler(self):
        if self.config.iceCollected > 0:
            self.config.iceCollected -= 1
            self.currentAction = 'icicle'
            self.qte_elements[0].reset()
            self.currentPhase = 'playerQTE'
            self.updating     = True

    def potionHandler(self):
        if self.config.potionCollected:
            self.config.potionCollected = False
            self.currentAction = 'potion'
            self.qte_elements[0].reset()
            self.currentPhase = 'playerQTE'
            self.updating     = True

    def resetLevel(self):
        print("Resetting DungeonQTE level...")


        self.currentPhase = 'attackPreparation'
        self.currentAction = None
        self.lastQteSuccess = False
        self.lastBossQteSuccess = False


        self.delayCounter = 0
        self.delayActive = False
        self.waitingForHpChange = False
        self.hpChangeDelayCounter = 0

        self.config.bossHP = self.config.backupBossHP
        self.config.playerHP = self.config.backupPlayerHP


        self.animator.play('default')


        self.qte_elements[0].reset()
        self.elements = self.orig_elements + self.attack_preparation_elements


        self.updating = True