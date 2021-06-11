from bot import images
from bot.utils import percentage_crop, template_match


# region trophies
def trophy_exclamation(screen):
    crop, offset = percentage_crop(screen, 70, 100, 0, 20)
    return template_match(crop, images.trophy_exclamation, offset)


def trophy_window(screen):
    crop, offset = percentage_crop(screen, 20, 50, 0, 15)
    return template_match(crop, images.achievements_icon, offset)


def trophy_close(screen):
    crop, offset = percentage_crop(screen, 80, 100, 0, 15)
    return template_match(crop, images.trophy_close_X, offset)


def trophy_gem(screen):
    crop, offset = percentage_crop(screen, 60, 95, 5, 95)
    return template_match(crop, images.trophy_gem_green, offset)


# endregion

"""
def wave(screen):
    crop, offset = percentage_crop(screen, 70, 100, 0, 10)
    return template_match(crop, images.wave_button, offset)
"""


# region seller
def okay_farm(screen):
    crop, offset = percentage_crop(screen, 20, 80, 45, 65)
    return template_match(crop, images.okay_farm_template, offset)


def farm_buy(screen):
    crop, offset = percentage_crop(screen, 50, 80, 45, 65)
    return template_match(crop, images.farm_buy, offset)


def no_thanks(screen):
    crop, offset = percentage_crop(screen, 0, 50, 45, 65)
    return template_match(crop, images.no_thanks, offset)


# endregion

# region summon

def go_to_summon(screen):
    crop, offset = percentage_crop(screen, 0, 20, 10, 30)
    return template_match(crop, images.go_to_summon, offset)


def summon(screen):
    crop, offset = percentage_crop(screen, 33, 66, 80, 100)
    return template_match(crop, images.summon_screen, offset)


def summon_button(screen, start_x, end_x):
    crop, offset = percentage_crop(screen, start_x, end_x, 80, 100)
    return template_match(crop, images.summon_on_button, offset)


def summon_off_button(screen, start_x, end_x):
    crop, offset = percentage_crop(screen, start_x, end_x, 80, 100)
    return template_match(crop, images.summon_off_button, offset)


def summon_okay(screen):
    crop, offset = percentage_crop(screen, 20, 80, 50, 70)
    return template_match(crop, images.okay_summon_template, offset)


# endregion

# region level

def level_continue(screen):
    crop, offset = percentage_crop(screen, 10, 90, 50, 90)
    return template_match(crop, images.level_continue, offset)


def level_lost(screen):
    crop, offset = percentage_crop(screen, 10, 90, 50, 70)
    return template_match(crop, images.level_lost, offset)


def level_start_next(screen):
    crop, offset = percentage_crop(screen, 0, 100, 15, 95)
    return template_match(crop, images.level_next_hard, offset)


def level_formation_confirm(screen):
    crop, offset = percentage_crop(screen, 20, 80, 80, 100)
    return template_match(crop, images.level_formation_confirm, offset)


# endregion

# region stuck in menus
def edit_exit(screen):
    crop, offset = percentage_crop(screen, 80, 100, 80, 100)
    return template_match(crop, images.edit_close_X, offset)


def shop_exit(screen):
    crop, offset = percentage_crop(screen, 0, 20, 80, 100)
    return template_match(crop, images.edit_close_X, offset)

# endregion
