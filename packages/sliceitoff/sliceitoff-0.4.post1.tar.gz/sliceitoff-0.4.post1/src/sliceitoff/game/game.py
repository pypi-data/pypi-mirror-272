""" game.game - Slice It Off! - Game where you slice the area where smily
    faces reside to the minimum.
"""

from pathlib import Path

import pygame

from sliceitoff.settings import settings
from sliceitoff.display import Display
from sliceitoff.stats import Stats
from sliceitoff.screens import (
    hiscores_screen,
    instructions1_screen,
    instructions2_screen)
from sliceitoff.hiscores import hi_scores
from sliceitoff.text import fonts
from sliceitoff.sfx import sfx
from sliceitoff.menu import (
    Show,
    MainMenu,
    MainMenuItems,
    Initials,
    SettingsMenu)

from .level import Level

class Game:
    """ This is the whole game. """
    def __init__(self):
        assets_path = Path(__file__).parent.parent.resolve().joinpath('assets')
        pygame.init()
        sfx.init(assets_path)
        fonts.init(assets_path)
        self.clock = pygame.time.Clock()
        self.display = Display()
        self.stats = None
        pygame.mouse.set_visible(False)

    def __del__(self):
        pygame.quit()

    def instructions(self):
        """ displays instruction and waits a key """
        for page in [instructions1_screen, instructions2_screen]:
            screen = Show(page())
            while screen.active:
                screen.update(dt = self.clock.tick())
                self.display.update( [screen] )

    def show_highscores(self):
        """ displays highscores and waits a key """
        sfx.music("pimpelipompeli")
        his = Show(hiscores_screen(str(hi_scores)))
        while his.active:
            his.update(dt = self.clock.tick())
            self.display.update( [his] )

    def newgame(self):
        """ new game, new score, runs through levels till game over """
        self.stats = Stats()
        while self.stats.lives:
            level = Level(stats = self.stats)
            while level.active:
                level.update(dt = self.clock.tick())
                self.display.update( [level] )
            if self.stats.lives:
                self.stats.level_up()

    def initials(self):
        """ asks for initials in case of high enough score """
        initials = Initials()
        while initials.active:
            initials.update(dt = self.clock.tick())
            self.display.update([initials])
        return initials.name

    def mainmenu(self):
        """ menu where one select what to do """
        sfx.music("pimpelipompeli")
        menu = MainMenu()
        while menu.active:
            menu.update(dt = self.clock.tick())
            self.display.update([menu])
        return menu.selection

    def settings(self):
        """ settings menu where one can adjust volume for example """
        menu = SettingsMenu()
        while menu.active:
            menu.update(dt = self.clock.tick())
            self.display.update([menu])

    def run(self):
        """ This is the main loop of the game """
        while True:
            match self.mainmenu():
                case MainMenuItems.QUIT:
                    hi_scores.save()
                    settings.save()
                    break
                case MainMenuItems.HISCORES:
                    self.show_highscores()
                case MainMenuItems.INSTRUCT:
                    self.instructions()
                case MainMenuItems.SETTINGS:
                    self.settings()
                case MainMenuItems.NEWGAME:
                    self.newgame()
                    if hi_scores.high_enough(self.stats.score):
                        hi_scores.add( self.stats.score, self.initials())
                    self.show_highscores()
