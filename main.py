import sys
from typing import List

from bot import Bot, Summons

# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    # initializing uiautomator2
    bot = Bot(None)

    # parsing arguments
    if "-s" in sys.argv:
        selected_category = Summons.ORBS_10
        if sys.argv.index("-s") != len(sys.argv) - 1:
            # TODO: Try to convert the arg sys.argv.index("-s") to a Summon enum (10/30/60)
            after_s = sys.argv[sys.argv.index("-s") + 1]
            summon_categories: List[Summons] = list(Summons)

            for category in summon_categories:
                if category.name == after_s:
                    selected_category = category

        bot.summon(selected_category)

    if "-ss" in sys.argv:
        bot.screenshots_loop()

    if "-d" in sys.argv:
        print(bot.detect_screen().name)

    elif "-f" in sys.argv:
        bot.farm_orbs()
