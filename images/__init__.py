import logging

import cv2


def _try_load(filename):
    try:
        image = cv2.imread("images/" + filename)
        height, width, _ = image.shape
        # image = cv2.resize(image, (width//2, height//2))
        return image
    except Exception as e:
        print("Cannot read " + filename + " " + str(e))
        return None


# SUMMON

go_to_summon = _try_load("go_to_summon.png")

summon_10_on = _try_load("summon_10_on.png")
summon_30_on = _try_load("summon_30_on.png")
summon_60_on = _try_load("summon_60_on.png")

summon_10_off = _try_load("summon_10_off.png")
summon_30_off = _try_load("summon_30_off.png")
summon_60_off = _try_load("summon_60_off.png")

okay_summon_template = _try_load("okay_summon.png")

# FARM

trophy_exclamation = _try_load("trophy_exclamation.png")
trophy_gem_green = _try_load("trophy_gem_green.png")
achievements_icon = _try_load("achievements_icon.png")
trophy_close_X = _try_load("trophy_close_X.png")

no_thanks = _try_load("no_thanks.png")
farm_buy = _try_load("farm_buy.png")
okay_farm_template = _try_load("okay_farm.png")

level_continue = _try_load("level_continue.png")
level_lost = _try_load("level_lost.png")
level_next_hard = _try_load("level_next_hard.png")
level_formation_confirm = _try_load("level_formation_confirm.png")

wave_button = _try_load("wave_button.png")

