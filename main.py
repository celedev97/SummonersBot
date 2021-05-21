import argparse
import sys
import logging
from enum import Enum

from utils import *

from optparse import OptionParser

logger = logging.getLogger("SummonerGreed")


class Summons(Enum):
    ORBS_10 = 10
    ORBS_30 = 30
    GEMS_60 = 60

    def get_images(self):
        if self.value == Summons.ORBS_10.value:
            return images.summon_10_on, images.summon_10_off
        elif self.value == Summons.ORBS_30.value:
            return images.summon_30_on, images.summon_30_off
        elif self.value == Summons.ORBS_60.value:
            return images.summon_60_on, images.summon_60_off


def summon(device: uiautomator2.Device, category: Summons = Summons.ORBS_10):
    print("Summon initiated")

    summon_template, no_summon_template = category.get_images()

    summoned = 0
    no_summon_button = None

    while no_summon_button is None:
        screen = screenshot(device)
        time.sleep(0.2)

        okay_button = template_match(device, screen, images.okay_summon_template)
        if okay_button:
            click(device, okay_button)
            screen = screenshot(device)

        summon_button = template_match(device, screen, summon_template)
        if summon_button:
            summoned += 1
            print(f"Summoning... ({summoned})")
            click(device, summon_button)
            click(device, summon_button)

        no_summon_button = template_match(device, screen, no_summon_template)
        if no_summon_button:
            print("Can't summon anymore.")


def farm_orbs(device):
    print("Farm initiated...")

    while True:
        time.sleep(3)
        screen = screenshot(device)

        if okay_button := template_match(device, screen, images.okay_farm_template):
            print("Okay button found, clicking...")
            click(device, okay_button)
            continue

        if farm_buy := template_match(device, screen, images.farm_buy):
            print("Buy button found, clicking...")
            click(device, farm_buy)
        elif no_thanks := template_match(device, screen, images.no_thanks):
            print("No thanks found, clicking...")
            click(device, no_thanks)

        if trophy_button := template_match(device, screen, images.trophy_exclamation):
            print("Trophy (!) detected")
            click(device, trophy_button)
            screen = screenshot(device)
            while (gem_button := template_match(device, screen, images.trophy_gem_green)) is not None:
                print("clicking gem")
                click(device, gem_button)
                screen = screenshot(device)

            print("No more gems, closing achievements")
            
            if close_button := template_match(device, screen, images.trophy_close_X):
                click(device, close_button)
                continue

        if farm_continue := template_match(device, screen, images.farm_continue):
            print("Continue button found!!!")
            click(device, farm_continue)

        if farm_next_level := template_match(device, screen, images.farm_next_level):
            print("Starting next level.")
            click(device, farm_next_level)

        if edit_confirm := template_match(device, screen, images.edit_confirm):
            print("Confirmed formation.")
            click(device, edit_confirm)



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
        summon(android_device)

    elif "-f" in sys.argv:
        farm_orbs(android_device)
