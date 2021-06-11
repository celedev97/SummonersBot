import threading
import tkinter

from bot import Bot
from bot.utils.structs import *


class MainWindow:
    root: tkinter.Tk
    selected_summon: tkinter.Variable
    selected_level: tkinter.Variable

    def __init__(self):
        self.root = root = tkinter.Tk()
        root.title("SummonersBot")

        self.selected_summon = tkinter.Variable(root, Summons.ORBS_10.value)
        self.selected_level = tkinter.Variable(root, (Levels.JOINT_REVENGE.value, LevelVariants.HARD.value))

        # region Summon options
        summon_options = tkinter.LabelFrame(root, text="Summon")
        for index, summon in enumerate(list(Summons)):
            summon: Summons
            tkinter.Radiobutton(summon_options, variable=self.selected_summon,
                                text=summon.name.replace("_", " "), value=summon.value).grid(row=index, column=0)
        summon_options.grid(row=0, column=0, sticky=tkinter.NSEW)
        # endregion

        # region Farm Options
        farm_options = tkinter.LabelFrame(root, text="Farm")
        y_index = 0
        for level in Levels:
            level: Levels

            if len(variants := level.variants()) == 0:
                continue

            tkinter.Label(farm_options, text=level.name).grid(row=y_index, column=0, columnspan=3)

            for x_index, variant in enumerate(variants):
                tkinter.Radiobutton(farm_options, variable=self.selected_level,
                                    text=variant.name, value=(level.value, variant.value)
                                    ).grid(row=y_index + 1, column=x_index)

            y_index += 2
        farm_options.grid(row=0, column=1, sticky=tkinter.NSEW)
        # endregion

        tkinter.Button(root, text="Summon", command=self.summon_button_pressed
                       ).grid(row=1, column=0, sticky=tkinter.NSEW)
        tkinter.Button(root, text="Farm", command=self.farm_button_pressed
                       ).grid(row=1, column=1, sticky=tkinter.NSEW)

        root.columnconfigure(0, minsize=239)
        root.mainloop()


    _bot: Bot = None

    def bot(self) -> Bot:
        if self._bot is None:
            self._bot = Bot()
        return self._bot

    def summon_button_pressed(self):
        selected_summon = filter(lambda x: x.value == self.selected_summon.get(), Summons).__next__()
        threading.Thread(target=lambda: self.bot().summon(selected_summon)).start()

    def farm_button_pressed(self):
        level_value, variant_value = self.selected_level.get()
        selected_level = filter(lambda x: x.value == level_value, Levels).__next__()
        selected_variant = filter(lambda x: x.value == variant_value, LevelVariants).__next__()

        self.bot().farm_orbs(selected_level, selected_variant)
