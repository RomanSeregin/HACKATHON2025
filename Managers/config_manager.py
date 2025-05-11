from random import choice

class ConfigManager:
    """
    The universal variable singleton storage that can be accessed from anywhere. All of the class levels have access to it, allowing the variables / any other info to be updated in real time with synchronisation, while also providing multiple methods inside to handle generic events with variables
    Stores all of the settings, bool values, states, counters etc.
    """
    _instance = None

    # ——— Level Completion States —————————————————
    levelCompletionStates = {
        "bastion": None,
        "dungeon": None,
        "jungle": None,
        "palace": None,
        "sea": None
    }

    # ——— Mouse & Event Tracking ———————————————
    mousePos = None
    mouseState = None
    event = None
    eventPos = None

    # ——— Application State ——————————————————
    state = 'menu'
    tooltipName = 'hidden'

    # ——— Unlock & Update Flags ——————————————
    unlockPalace = False
    unlockSea = False
    updateHub = False
    introCompleted = False
    exitFlag = False
    bastionLose = False

    # ——— Counters ———————————————————————————
    frameCounter = 0
    timerCounter = 60
    memoryCounter = 20
    backupTimerCounter = timerCounter
    backupMemoryCounter = memoryCounter
    aboutMePage = 0
    aboutGamePage = 0

    # ——— Audio Settings —————————————————————
    musicVolume = 0.3
    sfxVolume = 0.1
    difficultyLevel = 0

    # ——— Backup Values ——————————————————————
    backupMusicVolume = musicVolume
    backupSFXVolume = sfxVolume
    backupDifficultyLevel = difficultyLevel

    # ——— Dungeon Variables ——————————————————
    iceCollected = 0
    potionCollected = False
    dungeonRestoreIce = False
    dungeonRestoreQTE = False
    bossHP = 100
    backupBossHP = bossHP
    playerHP = 100
    backupPlayerHP = playerHP
    bossDamage = 30
    playerDamageFireball = 20
    playerDamageIcicle = 34
    healingEfficiency = (70, 40)  # 1 - good, 2 - bad

    # ——— Jungle Variables ——————————————————
    jungleRestoreObjects = False
    jungleShowingTooltip = False
    jungleTotalItems = 0

    # ——— Sea Variables —————————————————————
    seaFishRestoreObjects = False
    seaRingRestoreObjects = True
    seaStartTimer = False
    keyLocation = None
    airBubbles = 0
    finders = 0
    finderCharges = 3
    fishSpeed = 2
    ringTimer = 10

    # ——— Bastion Variables —————————————————
    bastionRestoreObjects = False
    displayingTooltip = False
    bastionBookID = choice(range(1, 11))
    bastionTotalBooks = 0
    bastionTrueBooks = 0
    bastionCorrectBooks = 0
    bastionFakeBooks = 0

    # singleton implementation
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.updateDifficulty()
        return cls._instance


    def reset_level_completion_states(self):
        for k in self.levelCompletionStates:
            self.levelCompletionStates[k] = None

    def reset_dungeon_vars(self):
        self.iceCollected = 0
        self.potionCollected = False
        self.dungeonRestoreIce = True
        self.dungeonRestoreQTE = True
        self.bossHP = self.backupBossHP
        self.playerHP = self.backupPlayerHP

    def reset_jungle_vars(self):
        self.jungleRestoreObjects = True
        self.jungleShowingTooltip = False
        self.jungleTotalItems = 0

    def reset_sea_vars(self):
        self.seaFishRestoreObjects = True
        self.seaRingRestoreObjects = True
        self.seaStartTimer = False
        self.keyLocation = None
        self.airBubbles = 0
        self.finders = 0
        self.finderCharges = self.finderCharges

    def reset_bastion_vars(self):
        self.bastionRestoreObjects = True
        self.displayingTooltip = False
        self.bastionBookID = choice(range(1, 11))
        self.bastionTotalBooks = 0
        self.bastionTrueBooks = 0
        self.bastionCorrectBooks = 0
        self.bastionFakeBooks = 0

    def reset_all_levels(self):
        self.reset_level_completion_states()
        self.reset_dungeon_vars()
        self.reset_jungle_vars()
        self.reset_sea_vars()
        self.reset_bastion_vars()
        self.unlockPalace = False
        self.unlockSea = False
        self.updateHub = False
        self.introCompleted = False
        self.bastionLose = False

    def resetCounters(self):
        self.frameCounter = 0
        self.timerCounter = self.backupTimerCounter
        self.memoryCounter = self.backupMemoryCounter


    def mouseUpdate(self, mousePos, mouseState):
        self.mousePos = mousePos
        self.mouseState = mouseState

    # live-updated properties for the texts to allow them to update in real time to real-time texts
    @property
    def dungeonIceText(self):
        return f'Часу на пошук: {self.timerCounter} сек'

    @property
    def dungeonPanelText(self):
        return f'Сфера вогню                 Бурулька {self.iceCollected}/3                 Напій ХП {'1' if self.potionCollected else '0'}/1'

    @property
    def jungleText(self):
        return f'Часу на пошук: {self.timerCounter} сек'

    @property
    def bastionKnowledgeText(self):
        return f'Часу на читання: {self.timerCounter} сек'

    @property
    def bastionMemoryText(self):
        return f"Часу на запам'ятовування: {self.memoryCounter} сек"

    @property
    def seaFishText(self):
        return f'Залишилось кисню: {self.timerCounter} сек'

    @property
    def seaRingText(self):
        return f'Залишилось кисню: {self.timerCounter} сек'

    def hubStateUpdate(self):
        self.resetCounters()
        self.reset_dungeon_vars()
        self.reset_jungle_vars()
        self.reset_sea_vars()
        self.reset_bastion_vars()
        self.updateHub = True
        self.state = 'hub'

    # setting the difficulty settings depending on the state of the difficultyLevel [0 or 1]
    def updateDifficulty(self):
        if self.difficultyLevel == 0:
            # --- Timing & Speed ---
            self.timerCounter = 60
            self.memoryCounter = 20
            self.backupTimerCounter = self.timerCounter
            self.backupMemoryCounter = self.memoryCounter
            self.ringTimer = 10
            self.fishSpeed = 2

            # --- Damage & Healing ---
            self.bossDamage = 30
            self.playerDamageFireball = 20
            self.playerDamageIcicle = 34
            self.healingEfficiency = (70, 40)

            # --- Health & Backups ---
            self.bossHP = 100
            self.backupBossHP = self.bossHP
            self.playerHP = 100
            self.backupPlayerHP = self.playerHP

            # --- Mechanics & Charges ---
            self.finderCharges = 3

        elif self.difficultyLevel == 1:
            # --- Timing & Speed ---
            self.timerCounter = 40
            self.memoryCounter = 5
            self.backupTimerCounter = self.timerCounter
            self.backupMemoryCounter = self.memoryCounter
            self.ringTimer = 5
            self.fishSpeed = 5

            # --- Damage & Healing ---
            self.bossDamage = 50
            self.playerDamageFireball = 10
            self.playerDamageIcicle = 20
            self.healingEfficiency = (40, 10)

            # --- Health & Backups ---
            self.bossHP = 120
            self.backupBossHP = self.bossHP
            self.playerHP = 80
            self.backupPlayerHP = self.playerHP

            # --- Mechanics & Charges ---
            self.finderCharges = 1

    # the function that makes sure that the level of the sound ingame stays synced to the sliders
    # The late imports are used to avoid import circling
    def updateVolumeLevels(self):
        if self.state == 'settings':
            from Managers.music_manager import MusicManager
            from Managers.sfx_manager import SFXManager

            MusicManager().syncVolume()
            SFXManager().syncVolume()

    def soundExclusion(self):
        return self.state in ['bastionKnowledgeMinigame', 'bastionMemoryMinigame', 'dungeonIceMinigame', 'dungeonQTE', 'jungleMinigame',
         'seaFishMinigame', 'seaRingMinigame']