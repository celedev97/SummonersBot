from enum import Enum
from typing import List


class Screen(Enum):
    GAME = 10
    GAME_ACHIEVEMENTS = 11
    GAME_SHOPKEEPER = 12
    GAME_MONITOR = 13
    GAME_OKAY = 14

    SUMMON = 20
    SUMMON_OKAY = 21

    LEVEL_SELECT = 30
    LEVEL_FORMATION_CONFIRM = 31
    LEVEL_LOST = 32
    LEVEL_WON = 33

    STUCK_SHOP_POWERUP = 41
    STUCK_FORMATION_EDIT = 42
    STUCK_SCREEN_SETTINGS = 43
    STUCK_SCREEN_LANGUAGE = 44


class Summons(Enum):
    ORBS_10 = 10
    ORBS_30 = 30
    GEMS_60 = 60


class LevelVariants(Enum):
    NORMAL = 1
    HARD = 2
    NIGHTMARE = 3


class Levels(Enum):
    KING = 1
    RAGEFIST_CHIEFTAIN = 2
    JOINT_REVENGE = 3

    EVIL_SUMMONER = 4
    MASTER_SUMMONER = 5
    ICE_QUEEN = 6

    def variants(self) -> List[LevelVariants]:
        return {
            Levels.KING: [LevelVariants.NORMAL, LevelVariants.HARD, LevelVariants.NIGHTMARE],
            Levels.RAGEFIST_CHIEFTAIN: [LevelVariants.NORMAL, LevelVariants.HARD, LevelVariants.NIGHTMARE],
            Levels.JOINT_REVENGE: [LevelVariants.NORMAL, LevelVariants.HARD, LevelVariants.NIGHTMARE],

            Levels.EVIL_SUMMONER: [],
            Levels.MASTER_SUMMONER: [],
            Levels.ICE_QUEEN: [],
        }[self]

