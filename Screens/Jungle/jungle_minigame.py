import pygame
from abc import ABC
from Managers.config_manager import ConfigManager
from Classes.screen import Screen
from Classes.image import Image
from Classes.button import Button
from Classes.text import Text
from constants import questsPath, WHITE

"""
Jungle object finding minigame that requires the players to find all of the objects.
Handles the removal of the objects manually with advanced element lists and methods.
"""
class JungleMinigame(Screen, ABC):
    def __init__(self):
        self.config = ConfigManager()
        super().__init__()

    def setup(self):
        self.displayingTooltip = False
        self.orig_elements = [
            Image(0, 0, f'{questsPath}/jungle/Level1/images/background.png'),
            Button('jug', 633, 304, f'{questsPath}/jungle/Level1/buttons/jug.png', f'{questsPath}/jungle/Level1/buttons/jug-a.png', destination='jungleMinigame', clickHandler=self.jugHandler),
            Button('coconut0', 302, 654, f'{questsPath}/jungle/Level1/buttons/coconut0.png', f'{questsPath}/jungle/Level1/buttons/coconut0-a.png', destination='jungleMinigame', clickHandler=self.coconutHandler),
            Button('coconut1', 1130, 664, f'{questsPath}/jungle/Level1/buttons/coconut1.png', f'{questsPath}/jungle/Level1/buttons/coconut1-a.png', destination='jungleMinigame', clickHandler=self.coconutHandler),
            Button('coconut2', 1198, 168, f'{questsPath}/jungle/Level1/buttons/coconut2.png', f'{questsPath}/jungle/Level1/buttons/coconut2-a.png', destination='jungleMinigame', clickHandler=self.coconutHandler),
            Button('coconut3', 389, 113, f'{questsPath}/jungle/Level1/buttons/coconut3.png', f'{questsPath}/jungle/Level1/buttons/coconut3-a.png', destination='jungleMinigame', clickHandler=self.unripeCoconutHandler),
            Button('flower', 386, 514, f'{questsPath}/jungle/Level1/buttons/flower.png', f'{questsPath}/jungle/Level1/buttons/flower-a.png', destination='jungleMinigame', clickHandler=self.flowerHandler),
            Button('flowerInjured', 688, 669, f'{questsPath}/jungle/Level1/buttons/flowerInjured.png', f'{questsPath}/jungle/Level1/buttons/flowerInjured-a.png', destination='jungleMinigame', clickHandler=self.flowerInjuredHandler),
            Button('frog', 697, 514, f'{questsPath}/jungle/Level1/buttons/frog.png', f'{questsPath}/jungle/Level1/buttons/frog-a.png', destination='jungleMinigame', clickHandler=self.frogHandler),
            Button('pot', 608, 619, f'{questsPath}/jungle/Level1/buttons/pot.png', f'{questsPath}/jungle/Level1/buttons/pot-a.png', destination='jungleMinigame', clickHandler=self.potHandler),
            Button('soil', 353, 698, f'{questsPath}/jungle/Level1/buttons/soil.png', f'{questsPath}/jungle/Level1/buttons/soil-a.png', destination='jungleMinigame', clickHandler=self.soilHandler),
            Button('stone', 1017, 693, f'{questsPath}/jungle/Level1/buttons/stone.png', f'{questsPath}/jungle/Level1/buttons/stone-a.png', clickHandler=self.stoneHandler),
            Button('boss', 16, 256, f'{questsPath}/jungle/Level1/buttons/boss.png', f'{questsPath}/jungle/Level1/buttons/boss-a.png', destination='jungleMinigame', clickHandler=self.bossHandler),
            Image(0, 18, f'{questsPath}/jungle/Level1/images/time.png'),
            Text('info', 50, 36, 30, WHITE, font='Assets/Fonts/OSCBold.ttf'),
            Button('hub', 1058, 15, f'{questsPath}/dungeon/Level1/buttons/hub.png', None, destination='hub', clickHandler=self.config.hubStateUpdate)
        ]

        self.elements = list(self.orig_elements)

    def handleEvent(self):
        for element in list(self.elements):
            if self.displayingTooltip and getattr(element, 'name', None) == 'tip':
                if hasattr(element, 'handleEvent'):
                    if element.handleEvent():
                        return
            if self.displayingTooltip:
                continue
            if isinstance(element, Button) and element.handleEvent():
                if element.name != 'hub':
                    name = element.name
                    for ele in self.elements:
                        if name == ele.name:
                            self.elements = [element for element in self.elements if getattr(element, 'name', None) != name]

                break

    def handleHover(self):
        if self.displayingTooltip:
            for element in self.elements:
                if getattr(element, 'name', None) == 'tip' and hasattr(element, 'handleHover') and element.handleHover():
                    break
            return
        for element in self.elements:
            if hasattr(element, 'handleHover') and element.handleHover():
                break

    def render(self, surface):
        self.restoreObjects()
        self.timer()
        for element in self.elements:
            element.render(surface)

    def hubStateUpdate(self):
        self.elements = [element for element in self.elements if getattr(element, 'name', None) != 'tip']
        self.displayingTooltip = False
        self.config.hubStateUpdate()

    def restoreObjects(self):
        if self.config.jungleRestoreObjects:
            self.config.jungleRestoreObjects = False
            self.elements = self.orig_elements

    def timer(self):
        self.config.frameCounter += 1
        if self.config.frameCounter >= 60:
            self.config.frameCounter = 0
            self.config.timerCounter -= 1
        if self.config.timerCounter <= 0:
            self.config.state = 'jungleLose'

    def multiHandler(self, name):
        self.config.jungleTotalItems += 1

        newPrompt = ''
        match name:
            case 'jug': newPrompt = 'Вода. Просто вода. Свіжа, але нічого\nособливого, навіть роги не повиростали.'
            case 'coconut': newPrompt = 'Хм, чи згодиться кокос? \nМоже зіграти ним з володарем Землі в боулінг? \nА чи може зробити кокосовий напій?'
            case 'unripeCoconut': newPrompt = 'Зелений кокос. Якщо його з’їсти -\nприхопить живота. Такий собі початок\nпереговорів.'
            case 'flower': newPrompt = 'Квітка — гарний подарунок будь-якій дівчині.\nА раптом володар — гарна дівчина?'
            case 'flowerInjured': newPrompt = 'Нещасне створіння, зовсім ще паросток.\nТи, як і я, волаєш подолати перешкоди\nта вижити. Як би тобі допомогти, крихто?'
            case 'pot': newPrompt = 'Глечик з залишками землі. Певно він стояв не пеньку,\nа жаба спихнула його.'
            case 'soil': newPrompt = 'Земля. Пахуча, плодовита. Будь-яка квітка\nбуде щасливою пустити в неї коріння.\nОдно тільки жаль — зовсім суха.'
            case 'stone': newPrompt = 'Ти диви, який масивний камінь.\nТаким межи очі зарядити, то одразу всі\nзірки й планети побачиш.'
            case 'frog': newPrompt = 'Жаба <витріща очі>: Пор-ква?\nОлек: Може ти зачарована царівна?\nДавай поцілую!\nЖаба <з жахом>: Квакнувся?'
            case 'boss': newPrompt = 'Ви помітили загадкову та погрозливу тінь.\nАле тільки-но ви спробували розрізнити\nїї обриси, як вона зникла.'

        newText = Text('tip', 615, 411, 26, (37, 69, 105), font='Assets/Fonts/OSCBold.ttf', method='center')
        newText.prompt = newPrompt
        self.elements.append(Image(278, 257, f'{questsPath}/jungle/Level1/images/tip.png', name='tip'))
        self.elements.append(Button('tip', 548, 514,f'{questsPath}/jungle/Level1/buttons/ok.png', None, destination='jungleMinigame', clickHandler=self.tipButtonHandler))
        self.elements.append(newText)
        self.displayingTooltip = True
        return True

    def tipButtonHandler(self):
        self.elements = [element for element in self.elements if getattr(element, 'name', None) != 'tip']
        self.displayingTooltip = False

        if self.config.jungleTotalItems >= 12:
            self.config.jungleTotalItems = 0
            self.config.state = 'jungleChoose'

    def jugHandler(self):
        self.multiHandler('jug')

    def coconutHandler(self):
        self.multiHandler('coconut')

    def unripeCoconutHandler(self):
        self.multiHandler('unripeCoconut')

    def flowerHandler(self):
        self.multiHandler('flower')

    def flowerInjuredHandler(self):
        self.multiHandler('flowerInjured')

    def frogHandler(self):
        self.multiHandler('frog')

    def potHandler(self):
        self.multiHandler('pot')

    def soilHandler(self):
        self.multiHandler('soil')

    def stoneHandler(self):
        self.multiHandler('stone')

    def bossHandler(self):
        self.elements[0].updateTexture(f'{questsPath}/jungle/Level1/images/background2.png')
        self.multiHandler('boss')