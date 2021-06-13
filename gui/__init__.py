import threading
import tkinter

from bot import Bot
from bot.utils.structs import *


class MainWindow:
    root: tkinter.Tk
    selected_summon: tkinter.Variable
    selected_level: tkinter.Variable

    summon_button: tkinter.Button
    farm_button: tkinter.Button

    device_id: tkinter.StringVar

    tasks: List[threading.Thread] = []

    def bot(self) -> Bot:
        device_id = self.device_id.get()
        return Bot(None if device_id == "" else device_id)

    def __init__(self):
        self.root = root = tkinter.Tk()
        # root.minsize(550, 600)
        root.title("SummonersBot")

        self.selected_summon = tkinter.Variable(root, Summons.ORBS_10.value)
        self.selected_level = tkinter.Variable(root, (Levels.JOINT_REVENGE.value, LevelVariants.HARD.value))
        self.device_id = tkinter.StringVar(root, "")

        # region ADB options
        adb_options = tkinter.LabelFrame(root, text="ADB")

        tkinter.Label(adb_options, text="Serial or IP (Leave blank if not needed):").grid(row=0, column=0)
        tkinter.Entry(adb_options, textvariable=self.device_id).grid(row=2, column=0, sticky=tkinter.NSEW)

        adb_options.grid(row=0, column=0, columnspan=2, sticky=tkinter.NSEW, padx=10, pady=10)
        # endregion

        # region Bot option
        # region Summon options
        summon_options = tkinter.LabelFrame(root, text="Summon")
        for index, summon in enumerate(list(Summons)):
            summon: Summons
            tkinter.Radiobutton(summon_options, variable=self.selected_summon,
                                text=summon.name.replace("_", " "), value=summon.value).grid(row=index, column=0)
        summon_options.grid(row=1, column=0, sticky=tkinter.NSEW, padx=10)
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
        farm_options.grid(row=1, column=1, sticky=tkinter.NSEW, padx=10)
        # endregion
        # endregion

        # region Bot start buttons
        button_row = tkinter.Frame(root)

        button_row.grid(row=2, column=0, sticky=tkinter.NSEW, padx=10, pady=10, columnspan=2)

        self.summon_button = tkinter.Button(button_row, text="Summon", command=self.summon_button_pressed)
        self.summon_button.grid(row=0, column=0, sticky=tkinter.NSEW)

        self.farm_button = tkinter.Button(button_row, text="Farm", command=self.farm_button_pressed)
        self.farm_button.grid(row=0, column=1, sticky=tkinter.NSEW)

        button_row.columnconfigure(0, weight=1, uniform="group1")
        button_row.columnconfigure(1, weight=1, uniform="group1")
        # endregion

        # region Queue visualization

        # endregion

        # region Console output

        # endregion

        root.columnconfigure(0, weight=1, uniform="group1")
        root.columnconfigure(1, weight=1, uniform="group1")

        root.protocol("WM_DELETE_WINDOW", self.close)
        root.mainloop()

    def close(self):
        self.root.destroy()
        exit(0)

    def summon_button_pressed(self):
        def summon_thread_function():
            # preparing data
            selected_summon = filter(lambda x: x.value == self.selected_summon.get(), Summons).__next__()

            # turning off buttons
            self.buttons_status(summon=False)

            # wait for the last task started to finish if necessary
            if len(self.tasks) > 1:
                self.tasks[-2].join()
                # turning off buttons again (the join might have activated them)
                self.buttons_status(summon=False)

            # starting the task
            try:
                self.bot().summon(selected_summon)
            except Exception as ex:
                print(f"ERROR: {ex}")

            # turning on buttons
            self.buttons_status(farm=True, summon=True)

        self.tasks.append(task := threading.Thread(target=summon_thread_function))
        task.daemon = True
        task.start()

    def farm_button_pressed(self):
        def farm_thread_function():
            # preparing data
            level_value, variant_value = self.selected_level.get()
            selected_level = filter(lambda x: x.value == level_value, Levels).__next__()
            selected_variant = filter(lambda x: x.value == variant_value, LevelVariants).__next__()

            # turning off buttons
            self.buttons_status(farm=False, summon=False)

            # wait for the last task started to finish if necessary
            if len(self.tasks) > 1:
                self.tasks[-2].join()
                # turning off buttons again (the join might have activated them)
                self.buttons_status(farm=False, summon=False)

            # starting the task
            try:
                self.bot().farm_orbs(selected_level, selected_variant)
            except Exception as ex:
                print(f"ERROR: {ex}")

            # turning on buttons
            self.buttons_status(farm=True, summon=True)

        self.tasks.append(task := threading.Thread(target=farm_thread_function))
        task.daemon = True
        task.start()

    def buttons_status(self, summon: bool = None, farm: bool = None):
        if summon is not None:
            self.summon_button.config(state="normal" if summon else "disabled")

        if farm is not None:
            self.farm_button.config(state="normal" if farm else "disabled")
