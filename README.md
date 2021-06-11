# SummonersBot

A bot for automating the game [Summoner's Greed](https://play.google.com/store/apps/details?id=com.pixio.google.mtd)

## Getting Started

In order to use the bot you need 
- [python 3.9.5](https://www.python.org/downloads/release/python-395/)
- [git](https://git-scm.com/downloads) (Optional but you cannot update without it)

### Installing

Once you have both python and git installed you can simply run:

```
git clone https://github.com/fcdev/SummonersBot
```

to download the bot;

Then run:
```
pip install -r requirements.txt
```
to install the required dependencies for the bot.


## Running the bot

### GUI

To run the bot in GUI mode just open it without passing any command arguments to it.

### Command Line

If you prefer to run it via command line (for example for automating it on a raspberry ;) ) these are some helpful command:

Summon with 10 orbs till possible:

```
main.py -s ORBS_10
```

Farm in Joint Revenge Hard with no limit:

```
main.py -f JOINT_REVENGE HARD
```

Use all the orbs, then farm:

```
main.py -s ORBS_10 -f
```

Show help for all the commands:

```
main.py -h
```

## Contributing

Feel free to open issues or do pull requests if you have any changes or issues with the bot.

## Authors

  - **fcdev** - *All the initial work and the GUI* - [fcdev](https://github.com/fcdev)

See also the list of
[contributors](https://github.com/fcdev/SummonersBot/contributors)
who participated in this project.
