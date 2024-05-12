""" menu.settings - Settings dialog """
from enum import IntEnum

from sliceitoff.sfx import sfx
from sliceitoff.screens import settings_screen
from .menu import Menu


class SettingsItems(IntEnum):
    """ Items in the menu. Should match settings_screen """
    SFX = 0
    MUSIC = 1
    BACK = 2

class SettingsMenu(Menu):
    """ Settings menu """
    def __init__(self):
        super().__init__(settings_screen, len(SettingsItems))

    def do_selection(self):
        """ Custom actions for menu entries """
        match self.selection:
            case SettingsItems.BACK:
                self.do_fadeout()
            case SettingsItems.SFX:
                sfx.sfx_up()
            case SettingsItems.MUSIC:
                sfx.music_up()
