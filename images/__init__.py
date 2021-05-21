import logging

import cv2


def _try_load(filename):
    try:
        return cv2.imread("images/" + filename)
    except:
        logging.Logger.warning("Cannot read " + filename)
        return None


# SUMMON

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
trophy_close_X = _try_load("trophy_close_X.png")

no_thanks = _try_load("no_thanks.png")
farm_buy = _try_load("farm_buy.png")
okay_farm_template = _try_load("okay_farm.png")

farm_continue = _try_load("farm_continue.png")
farm_next_level = _try_load("farm_next_level.png")
edit_confirm = _try_load("edit_confirm.png")

