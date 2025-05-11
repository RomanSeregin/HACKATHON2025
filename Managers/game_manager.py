from Managers.config_manager import ConfigManager
from Managers.music_manager import MusicManager

from Managers.sfx_manager import SFXManager
from Screens.menu import Menu
from Screens.settings import Settings
from Screens.hub import Hub

from Screens.AboutMe.about_me0 import AboutMe0
from Screens.AboutMe.about_me1 import AboutMe1
from Screens.AboutMe.about_me2 import AboutMe2

from Screens.AboutGame.about_game0 import AboutGame0
from Screens.AboutGame.about_game1 import AboutGame1
from Screens.AboutGame.about_game2 import AboutGame2
from Screens.AboutGame.about_game3 import AboutGame3
from Screens.AboutGame.about_game4 import AboutGame4
from Screens.AboutGame.about_game5 import AboutGame5
from Screens.AboutGame.about_game6 import AboutGame6
from Screens.AboutGame.about_game7 import AboutGame7
from Screens.AboutGame.about_game8 import AboutGame8
from Screens.AboutGame.about_game9 import AboutGame9
from Screens.AboutGame.about_game10 import AboutGame10
from Screens.AboutGame.about_game11 import AboutGame11
from Screens.AboutGame.about_game12 import AboutGame12
from Screens.AboutGame.about_game13 import AboutGame13
from Screens.AboutGame.about_game14 import AboutGame14
from Screens.AboutGame.about_game15 import AboutGame15

from Screens.Intro.intro0 import Intro0
from Screens.Intro.intro1 import Intro1
from Screens.Intro.intro2 import Intro2
from Screens.Intro.intro3 import Intro3

from Screens.Ending.ending0 import Ending0
from Screens.Ending.ending1 import Ending1
from Screens.Ending.ending2 import Ending2
from Screens.Ending.ending3 import Ending3

from Screens.Dungeon.entrance import DungeonEntrance
from Screens.Dungeon.ice_minigame import IceMinigame
from Screens.Dungeon.dialogue import DungeonDialogue
from Screens.Dungeon.dungeon_qte import DungeonQTE
from Screens.Dungeon.lose import DungeonLose
from Screens.Dungeon.win import DungeonWin
from Screens.Dungeon.treaty import DungeonTreaty

from Screens.Jungle.entrance import JungleEntrance
from Screens.Jungle.jungle_minigame import JungleMinigame
from Screens.Jungle.jungle_choose import JungleChoose
from Screens.Jungle.lose import JungleLose
from Screens.Jungle.win import JungleWin
from Screens.Jungle.treaty import JungleTreaty

from Screens.Sea.entrance_locked import SeaEntranceLocked
from Screens.Sea.entrance_unlocked import SeaEntranceUnlocked
from Screens.Sea.sea_fish_minigame import SeaFishMinigame
from Screens.Sea.sea_ring_minigame import SeaRingMinigame
from Screens.Sea.dialogue import SeaDialogue
from Screens.Sea.result import SeaResult
from Screens.Sea.lose import SeaLose
from Screens.Sea.win import SeaWin
from Screens.Sea.treaty import SeaTreaty

from Screens.Bastion.entrance import BastionEntrance
from Screens.Bastion.bastion_knowledge_minigame import BastionKnowledgeMinigame
from Screens.Bastion.dialogue import BastionDialogue
from Screens.Bastion.prelude import BastionPrelude
from Screens.Bastion.bastion_memory_minigame import BastionMemoryMinigame
from Screens.Bastion.lose import BastionLose
from Screens.Bastion.win import BastionWin
from Screens.Bastion.treaty import BastionTreaty


class GameManager:
    """
    singleton implementation principle
    the game manager is the upper-most link of all of the code. It is the highest manager in the chain, as it combines and defines what will be displayed, along with calling the respective methods for the classes.
    The ierarchy is this:
    Button -> Screen -> GameManager
    """
    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.currentState = None
        self.config = ConfigManager()
        self.screens = {
            'menu': Menu(),
            'settings': Settings(),
            'hub': Hub(),

            'aboutMe0': AboutMe0(),
            'aboutMe1': AboutMe1(),
            'aboutMe2': AboutMe2(),

            'aboutGame0': AboutGame0(),
            'aboutGame1': AboutGame1(),
            'aboutGame2': AboutGame2(),
            'aboutGame3': AboutGame3(),
            'aboutGame4': AboutGame4(),
            'aboutGame5': AboutGame5(),
            'aboutGame6': AboutGame6(),
            'aboutGame7': AboutGame7(),
            'aboutGame8': AboutGame8(),
            'aboutGame9': AboutGame9(),
            'aboutGame10': AboutGame10(),
            'aboutGame11': AboutGame11(),
            'aboutGame12': AboutGame12(),
            'aboutGame13': AboutGame13(),
            'aboutGame14': AboutGame14(),
            'aboutGame15': AboutGame15(),

            'intro0': Intro0(),
            'intro1': Intro1(),
            'intro2': Intro2(),
            'intro3': Intro3(),

            'dungeonEntrance': DungeonEntrance(),
            'dungeonIceMinigame': IceMinigame(),
            'dungeonDialogue': DungeonDialogue(),
            'dungeonQTE': DungeonQTE(),
            'dungeonLose': DungeonLose(),
            'dungeonWin': DungeonWin(),
            'dungeonTreaty': DungeonTreaty(),

            'jungleEntrance': JungleEntrance(),
            'jungleMinigame': JungleMinigame(),
            'jungleChoose': JungleChoose(),
            'jungleLose': JungleLose(),
            'jungleWin': JungleWin(),
            'jungleTreaty': JungleTreaty(),

            'seaEntranceLocked': SeaEntranceLocked(),
            'seaEntranceUnlocked': SeaEntranceUnlocked(),
            'seaFishMinigame': SeaFishMinigame(),
            'seaDialogue': SeaDialogue(),
            'seaRingMinigame': SeaRingMinigame(),
            'seaResult': SeaResult(),
            'seaLose': SeaLose(),
            'seaWin': SeaWin(),
            'seaTreaty': SeaTreaty(),

            'bastionEntrance': BastionEntrance(),
            'bastionKnowledgeMinigame': BastionKnowledgeMinigame(),
            'bastionDialogue': BastionDialogue(),
            'bastionPrelude': BastionPrelude(),
            'bastionMemoryMinigame': BastionMemoryMinigame(),
            'bastionLose': BastionLose(),
            'bastionWin': BastionWin(),
            'bastionTreaty': BastionTreaty(),

            'ending0': Ending0(),
            'ending1': Ending1(),
            'ending2': Ending2(),
            'ending3': Ending3()
        }

    # universal event and hover handler function for all of the screens (all of the sub-class items have the same function name to keep it simple)
    def handleEvent(self, events):
        self.updateMusic()

        for event in events:
            self.config.event = event
            for name, screen in self.screens.items():
                if name == self.config.state:
                    screen.handleHover()
                    screen.handleEvent()
                    return True
            return False

    # universal drawing function for all of the elements
    def render(self, surface):
        # done here so that the update works even if no event is detected (major flaw of the handleEvent function)
        self.config.updateVolumeLevels()
        for name, screen in self.screens.items():
            if name == self.config.state:
                screen.render(surface)

    # music handler function that works from the global context to only start the music on certain screens (as most times music doesn't need to be reset often)
    def updateMusic(self):
        state = self.config.state

        if state in ('menu', 'settings', 'intro0', 'intro1', 'intro2', 'intro3', 'hub'):
            group = 'hub'
        elif state.startswith('dungeon'):
            group = 'dungeon'
        elif state.startswith('jungle'):
            group = 'jungle'
        elif state.startswith('bastion'):
            group = 'bastion'
        elif state.startswith('sea'):
            group = 'sea'
        else:
            group = None

        # if the music track is detected, and the group exists
        if group and group != getattr(self, 'currentMusicGroup', None):
            self.currentMusicGroup = group
            MusicManager().playTrack(group)