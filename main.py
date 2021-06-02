import sys
import logging
from enum import Enum

from utils import *

logger = logging.getLogger("SummonerGreed")

SAVE_SUMMON = True

start_time = round(time.time() * 1000)


class Screen(Enum):
    GAME = 10
    ACHIEVEMENTS = 11
    SHOPKEEPER = 12
    MONITOR = 13

    SCREEN_SUMMON = 20
    SCREEN_SUMMON_OKAY = 21

    LEVEL_SELECT = 30
    LEVEL_FORMATION_CONFIRM = 31
    LEVEL_LOST = 32
    LEVEL_WON = 33

    GAME_SHOP = 41
    FORMATION_EDIT = 42
    SCREEN_SETTINGS = 43
    SCREEN_LANGUAGE = 44


class Summons(Enum):
    ORBS_10 = 10
    ORBS_30 = 30
    GEMS_60 = 60

    def get_images(self):
        if self.value == Summons.ORBS_10.value:
            return images.summon_10_on, images.summon_10_off
        elif self.value == Summons.ORBS_30.value:
            return images.summon_30_on, images.summon_30_off
        elif self.value == Summons.GEMS_60.value:
            return images.summon_60_on, images.summon_60_off


def screenshots(device: uiautomator2.Device):
    print(f"Screenshots initiated in last.png")

    while True:
        screen = screenshot(device, "last")
        time.sleep(3)


def summon(device: uiautomator2.Device, category: Summons = Summons.ORBS_10):
    while True:
        status = detect_screen(device, react=True)
        if status == Screen.GAME:
            screen = screenshot(device)
            if go_to_summon := match_go_to_summon(screen):
                click(device, go_to_summon)
            status = detect_screen(device, react=True)

        if status == Screen.SCREEN_SUMMON:
            break

    print(f"Summon initiated ({category.name})")

    summon_template, no_summon_template = category.get_images()

    summoned = 0
    no_summon_button = None

    while no_summon_button is None:
        screen = screenshot(device)
        time.sleep(0.2)

        summon_button = template_match(screen, summon_template)
        if summon_button:
            summoned += 1
            print(f"Summoning... ({summoned})")
            click(device, summon_button, 0.1)
            click(device, summon_button, 0.1)

        okay_button = template_match(screen, images.okay_summon_template)
        if okay_button:
            click(device, okay_button)

            if SAVE_SUMMON:
                height, width, _ = screen.shape[::]
                summon = screen[height // 8: height // 2, (width // 4): (width * 3 // 4)]

                cv2.imwrite(f"summons/summon_{start_time}_{summoned}.png", summon)

            screen = screenshot(device)

        no_summon_button = template_match(screen, no_summon_template)
        if no_summon_button:
            print("Can't summon anymore.")


def farm_orbs(device):
    print("Farm initiated...")

    while True:
        time.sleep(3)
        screen = screenshot(device)
        detect_screen(device, screen, react=True)


def detect_screen(device, screen=None, react=True) -> Screen:
    if screen is None:
        screen = screenshot(device, "last")

    # region trophies stuff
    if trophy_button := match_trophy_exclamation(screen):
        if react:
            click(device, trophy_button)
            return detect_screen(device, None, True)
        return Screen.GAME

    if match_trophy_window(screen) and (close_button := match_trophy_close(screen)) is not None:
        if react:
            while (gem_button := match_trophy_gem(screen)) is not None:
                print("clicking gem")
                click(device, gem_button)
                screen = screenshot(device)

            print("No more gems, closing achievements")
            click(device, close_button)
            return detect_screen(device, None, True)
        return Screen.ACHIEVEMENTS
    # endregion

    # if there are no trophy the most possible solution is that we're just farming
    if match := match_wave(screen):
        return Screen.GAME

    # if we're not farming either... there's probably the seller
    # region seller stuff
    if farm_buy := match_farm_buy(screen):
        if react:
            print("Buy button found, clicking...")
            click(device, farm_buy)
            return detect_screen(device, None, True)
        return Screen.SHOPKEEPER
    elif no_thanks := match_no_thanks(screen):
        if react:
            print("No thanks found, clicking...")
            click(device, no_thanks)
            return detect_screen(device, None, True)
        return Screen.MONITOR

    if okay_button := match_okay_farm(screen):
        if react:
            print("Okay button found, clicking...")
            click(device, okay_button)
            return detect_screen(device, None, True)
        return Screen.SCREEN_GAME_OKAY  # TODO: HA SENSO?
    # endregion

    # if we're not using trophies, not farming, and there's no seller/monitor maybe we're in summon
    if match_summon(screen):
        return match

    if okay_summon := match_summon_okay(screen):
        

    # if we're not even in summon then maybe we're stuck in monster edit or shop as a bug

    # region last case: the level is ending
    if farm_continue := match_level_continue(screen):
        if react:
            print("Continue button found!!!")
            click(device, farm_continue)
            return detect_screen(device, None, True)
        return Screen.LEVEL_WON

    if edit_confirm := match_level_formation_confirm(screen):
        if react:
            print("Confirmed formation.")
            click(device, edit_confirm)
            return detect_screen(device, None, True)
        return Screen.LEVEL_FORMATION_CONFIRM

    if farm_lost := match_level_lost(screen):
        if react:
            print("Timewarping...")
            click(device, farm_lost)
            return detect_screen(device, None, True)
        return Screen.LEVEL_FORMATION_CONFIRM

    # this use a pretty big screenshot, so it's better if it's the last one
    if farm_next_level := match_level_start_next(screen):
        print("Starting next level.")
        click(device, farm_next_level)
    # endregion


def init():
    import adbutils

    serial = None
    device = adbutils.adb.device(serial)
    initer = uiautomator2.Initer(device)
    if not initer.check_install():
        initer.install()
    return initer.check_install()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # initializing uiautomator2
    if not init():
        print("can't use uiautomator2")
        exit(1)
    android_device = uiautomator2.connect()

    if "-s" in sys.argv:
        if sys.argv.index("-s") != len(sys.argv) - 1:
            # TODO: Try to convert the arg sys.argv.index("-s") to a Summon enum (10/30/60)
            pass
        summon(android_device, Summons.ORBS_10)

    if "-ss" in sys.argv:
        screenshots(android_device)

    if "-d" in sys.argv:
        print(detect_screen(android_device, react=True).name)

    elif "-f" in sys.argv:
        farm_orbs(android_device)
