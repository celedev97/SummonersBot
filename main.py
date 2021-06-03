import sys
import logging
import uiautomator2
import time

from enum import Enum

import utils
from utils import *
from utils.match_images import *
from utils.structs import *

logger = logging.getLogger("SummonerGreed")

SAVE_SUMMON = True

start_time = round(time.time() * 1000)


def screenshots_loop(device: uiautomator2.Device):
    print(f"Screenshots initiated in last.png")

    while True:
        screen = screenshot(device, "last")
        time.sleep(3)


def summon(device: uiautomator2.Device, category: Summons = Summons.ORBS_10):
    # creating percentages for the crop based on the orbs number
    start_x, end_x = 0, 0
    if category == Summons.ORBS_10:
        start_x, end_x = 0, 33
    elif category == Summons.ORBS_30:
        start_x, end_x = 33, 66
    else:
        start_x, end_x = 66, 99

    okay_button = None
    summoned = 0

    while True:
        # taking a screenshot
        status = detect_screen(device, react=True)

        if status == Screen.GAME:
            if go_to_summon := match_go_to_summon(utils.last_screenshot):
                click(device, go_to_summon)
            continue
        elif status == Screen.SUMMON:
            if summon_button := match_summon_button(utils.last_screenshot, start_x, end_x):
                summoned += 1
                print(f"Summoning... ({summoned})")
                click(device, summon_button)
                click(device, summon_button)
                click(device, summon_button)
                if SAVE_SUMMON or okay_button is None:
                    screenshot(device)
            elif match_summon_off_button(utils.last_screenshot, start_x, end_x):
                print("Can't summon anymore.")
                break

            if okay_button is None:
                okay_button = match_summon_okay(utils.last_screenshot)

            if okay_button:
                if SAVE_SUMMON:
                    summon_screenshot, _ = percentage_crop(utils.last_screenshot, 20, 80, 10, 50)
                    cv2.imwrite(f"summons/summon_{start_time}_{summoned}.png", summon_screenshot)

                click(device, okay_button)

    print(f"Summon initiated ({category.name})")

    summon_template, no_summon_template = category.get_images()

    no_summon_button = None

    while no_summon_button is None:
        screen = screenshot(device)
        time.sleep(0.2)

        summon_button = template_match(screen, summon_template)
        if summon_button:

            click(device, summon_button, 0.1)
            click(device, summon_button, 0.1)

        okay_button = template_match(screen, images.okay_summon_template)
        if okay_button:
            click(device, okay_button)

            screen = screenshot(device)

        no_summon_button = template_match(screen, no_summon_template)
        if no_summon_button:
            print("Can't summon anymore.")


def farm_orbs(device):
    print("Farm initiated...")

    while True:
        # taking the screenshot
        screen = screenshot(device)

        # detecting the current screen, and reacting to events
        status = detect_screen(device, screen, react=True)

        # if i'm in the summon screen i need to go out
        if status == Screen.SUMMON and (close_summon := match_trophy_close(screen)):
            print("Summon screen detected, going back to farm")
            click(device, close_summon)

        time.sleep(3)


def detect_screen(device, screen=None, react=False) -> Screen:
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
        return Screen.GAME_ACHIEVEMENTS
    # endregion

    # if there are no trophy the most possible solution is that we're just farming
    if match := match_go_to_summon(screen):
        return Screen.GAME

    # if we're not farming either... there's probably the seller
    # region seller stuff
    if farm_buy := match_farm_buy(screen):
        if react:
            print("Buy button found, clicking...")
            click(device, farm_buy)
            return detect_screen(device, None, True)
        return Screen.GAME_SHOPKEEPER
    elif no_thanks := match_no_thanks(screen):
        if react:
            print("No thanks found, clicking...")
            click(device, no_thanks)
            return detect_screen(device, None, True)
        return Screen.GAME_MONITOR

    if okay_button := match_okay_farm(screen):
        if react:
            print("Okay button found, clicking...")
            click(device, okay_button)
            return detect_screen(device, None, True)
        return Screen.GAME_OKAY
    # endregion

    # if we're not using trophies, not farming, and there's no seller/monitor maybe we're in summon
    if match_summon(screen):
        return Screen.SUMMON

    if okay_summon := match_summon_okay(screen):
        if react:
            click(device, okay_summon)
            return detect_screen(device, None, True)
        return Screen.SUMMON_OKAY

    # if we're not even in summon then maybe we're stuck in monster edit or shop as a bug
    if edit_exit := match_edit_exit(screen):
        if react:
            click(device, edit_exit)
            return detect_screen(device, None, True)
        return Screen.STUCK_FORMATION_EDIT

    if shop_exit := match_shop_exit(screen):
        if react:
            click(device, shop_exit)
            return detect_screen(device, None, True)
        return Screen.STUCK_SHOP_POWERUP

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
        if react:
            print("Starting next level.")
            click(device, farm_next_level)
            return detect_screen(device, None, True)
        return Screen.LEVEL_SELECT
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
        screenshots_loop(android_device)

    if "-d" in sys.argv:
        print(detect_screen(android_device).name)

    elif "-f" in sys.argv:
        farm_orbs(android_device)
