import logging
import time

import uiautomator2

import bot.utils
from bot.utils import *
import bot.utils.match_images as match
from bot.utils.structs import *

import adbutils

logger = logging.getLogger("SummonerGreed")


class Bot:
    device: uiautomator2.Device
    last_screenshot: np.ndarray

    start_time: int

    def __init__(self, serial=None):
        if serial is not None:
            print(adbutils.adb.connect(serial))

        device = adbutils.adb.device(serial)
        initer = uiautomator2.Initer(device)
        if not initer.check_install():
            initer.install()

        if not initer.check_install():
            raise Exception("Cannot run uiautomator2")

        self.device = uiautomator2.connect(serial)
        self.start_time = round(time.time() * 1000)

    # region helpers
    def _click(self, point: Tuple[int, int], post_sleep: float = 0.15) -> None:
        while not summoner_greed_on(self.device):
            time.sleep(1)

        self.device.click(point[0], point[1])
        time.sleep(post_sleep)

    def _screenshot(self, filename: str = None) -> np.ndarray:
        while not summoner_greed_on(self.device):
            time.sleep(1)

        self.last_screenshot = self.device.screenshot(format='opencv')
        if filename is not None:
            cv2.imwrite(f"{filename}.png", self.last_screenshot)
        return self.last_screenshot

    def _exit_summon(self, screen: np.ndarray = None):
        print("Summon screen:", self.detect_screen(react=True) == Screen.SUMMON)

        if screen is None:
            screen = self._screenshot()

        if close_summon := match.trophy_close(screen):
            self._click(close_summon)

        screen = self._screenshot()
        if close_edit := match.edit_exit(screen):
            self._click(close_edit)

    # endregion

    # region debug functions
    def screenshots_loop(self):
        print(f"Screenshots initiated in last.png")

        while True:
            self._screenshot("last")
            time.sleep(3)

    # endregion

    # region bot functions
    def farm_orbs(self, level=Levels.JOINT_REVENGE, variant=LevelVariants.HARD):
        print("Farm initiated...")

        while True:
            # taking the self._screenshot
            screen = self._screenshot()

            # detecting the current screen, and reacting to events
            status = self.detect_screen(screen, react=True)

            # if i'm in the summon screen i need to go out
            if status == Screen.SUMMON:
                print("Summon screen detected, going back to farm")
                self._exit_summon(screen)

            time.sleep(3)

    def summon(self, category: Summons = Summons.ORBS_10, check_achievements=True, save_screenshot=False):
        # creating percentages for the crop based on the orbs number
        start_x, end_x = {
            Summons.ORBS_10: [0, 33],
            Summons.ORBS_30: [33, 66],
            Summons.GEMS_60: [66, 99],
        }[category]

        okay_button = None
        summoned = 0

        print(f"Summon initiated ({category.name})")

        while True:
            # taking a self._screenshot
            status = self.detect_screen(react=True)

            if status == Screen.GAME:
                if go_to_summon := match.go_to_summon(self.last_screenshot):
                    self._click(go_to_summon)
                continue
            elif status == Screen.SUMMON:
                if summon_button := match.summon_button(self.last_screenshot, start_x, end_x):
                    summoned += 1
                    print(f"Summoning... ({summoned})")
                    self._click(summon_button, post_sleep=0.1)
                    self._click(summon_button, post_sleep=0.1)
                    self._click(summon_button, post_sleep=0)

                    if save_screenshot or (okay_button is None):
                        self._screenshot()
                elif match.summon_off_button(self.last_screenshot, start_x, end_x):
                    print("Can't summon anymore.")
                    break

                if okay_button is None:
                    okay_button = match.summon_okay(self.last_screenshot)

                if okay_button:
                    if save_screenshot:
                        summon_screenshot, _ = percentage_crop(self.last_screenshot, 20, 80, 10, 50)
                        cv2.imwrite(f"summons/summon_{self.start_time}_{summoned}.png", summon_screenshot)

                    self._click(okay_button, post_sleep=0.1)

                if check_achievements and summoned % 5 == 0:
                    print("checking achievements")
                    self._exit_summon()

    # endregion

    # region general bot behaviour
    def detect_screen(self, screen=None, react=False) -> Screen:
        if screen is None:
            screen = self._screenshot("last")

        # region trophies stuff
        if trophy_button := match.trophy_exclamation(screen):
            if react:
                self._click(trophy_button)
                return self.detect_screen(react=True)
            return Screen.GAME

        if match.trophy_window(screen) and (close_button := match.trophy_close(screen)) is not None:
            if react:
                while (gem_button := utils.match_images.trophy_gem(screen)) is not None:
                    print("clicking gem")
                    self._click(gem_button)
                    screen = self._screenshot()

                print("No more gems, closing achievements")
                self._click(close_button)
                return self.detect_screen(react=True)
            return Screen.GAME_ACHIEVEMENTS
        # endregion

        # if there are no trophy the most possible solution is that we're just farming
        if match.go_to_summon(screen):
            return Screen.GAME

        # if we're not farming either... there's probably the seller
        # region seller stuff
        if farm_buy := match.farm_buy(screen):
            if react:
                print("Buy button found, clicking...")
                self._click(farm_buy)
                return self.detect_screen(react=True)
            return Screen.GAME_SHOPKEEPER
        elif no_thanks := match.no_thanks(screen):
            if react:
                print("No thanks found, clicking...")
                self._click(no_thanks)
                return self.detect_screen(react=True)
            return Screen.GAME_MONITOR

        if okay_button := match.okay_farm(screen):
            if react:
                print("Okay button found, clicking...")
                self._click(okay_button)
                return self.detect_screen(react=True)
            return Screen.GAME_OKAY
        # endregion

        # if we're not using trophies, not farming, and there's no seller/monitor maybe we're in summon
        if match.summon(screen):
            return Screen.SUMMON

        # the continue button must be checked before the summon_okay
        # since the summon_okay can get matched on the continue grass
        if farm_continue := match.level_continue(screen):
            if react:
                print("Continue button found!!!")
                self._click(farm_continue)
                return self.detect_screen(react=True)
            return Screen.LEVEL_WON
        elif okay_summon := match.summon_okay(screen):
            if react:
                self._click(okay_summon)
                return self.detect_screen(react=True)
            return Screen.SUMMON_OKAY

        # region last case: less probable events
        if edit_confirm := match.level_formation_confirm(screen):
            if react:
                print("Confirmed formation.")
                self._click(edit_confirm)
                return self.detect_screen(react=True)
            return Screen.LEVEL_FORMATION_CONFIRM

        if farm_lost := match.level_lost(screen):
            if react:
                print("Timewarping...")
                self._click(farm_lost)
                return self.detect_screen(react=True)
            return Screen.LEVEL_FORMATION_CONFIRM

        # this use a pretty big self._screenshot, so it's better if it's the last one
        if farm_next_level := match.level_start_next(screen):
            if react:
                print("Starting next level.")
                self._click(farm_next_level)
                return self.detect_screen(react=True)
            return Screen.LEVEL_SELECT
        # endregion

        # if we're not in any known place maybe we're stuck in shop or edit mode
        if edit_exit := match.edit_exit(screen):
            if react:
                self._click(edit_exit)
                return self.detect_screen(react=True)
            return Screen.STUCK_FORMATION_EDIT

        if shop_exit := match.shop_exit(screen):
            if react:
                self._click(shop_exit)
                return self.detect_screen(react=True)
            return Screen.STUCK_SHOP_POWERUP


    # endregion
