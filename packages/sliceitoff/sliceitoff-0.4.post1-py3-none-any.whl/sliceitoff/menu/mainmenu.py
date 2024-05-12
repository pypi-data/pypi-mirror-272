""" menu.mainmenu - Let's user choose """
from enum import IntEnum

from sliceitoff.screens import mainmenu_screen
from .menu import Menu

class MainMenuItems(IntEnum):
    """ Items in the menu. Should match mainmenu_screen """
    NEWGAME = 0
    HISCORES = 1
    INSTRUCT = 2
    SETTINGS = 3
    QUIT = 4

class MainMenu(Menu):
    """ Main menu """
    def __init__(self):
        super().__init__(mainmenu_screen, len(MainMenuItems))
