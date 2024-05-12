""" sfx.sfx - pygame.mixer initialization and sound effects handling """
import os
from random import choice
from pathlib import Path
import pygame

from sliceitoff.settings import settings

DEBUG = os.getenv("DEBUG")

class Sfx:
    """ Sound Effects and Music? """
    def __init__(self):
        self.initialized = False
        self.sound = {}
        self.bgm = None
        try:
            self.sfx_volume = int(
                    settings.get_value_or_default("sfx_volume"))
            self.music_volume = int(
                    settings.get_value_or_default("music_volume"))
        except ValueError:
            self.sfx_volume = 10
            self.music_volume = 10
        try:
            pygame.mixer.pre_init(channels=2, buffer=512, frequency=48000)
        except pygame.error:
            pass

    def init(self, base_path):
        """ To be called after pygame is initialized. Actual mixer init and
            sample loading happens here """
        try:
            pygame.mixer.init()
            self.initialized = True
            for mp3_file in Path(base_path).glob('*.mp3'):
                self.sound[str(mp3_file.stem)] = pygame.mixer.Sound(mp3_file)
                if DEBUG:
                    print("Loading sound:", mp3_file, str(mp3_file.stem))
        except pygame.error:
            pass

    def sfx_up(self):
        """ Turn volume up. If its turned to 11 it resets back to 0. """
        self.sfx_volume += 1
        self.sfx_volume %= 11
        settings.replace_value("sfx_volume", self.sfx_volume)
        self.play(choice(("baby", "laser", "glass")))

    def music_up(self):
        """ Turn volume up. If its turned to 11 it resets back to 0. """
        self.music_volume += 1
        self.music_volume %= 11
        settings.replace_value("music_volume", self.music_volume)
        if self.initialized and self.bgm:
            self.sound[self.bgm].set_volume(self.music_volume / 10)

    def play(self, sample):
        """ Just plays named sample loaded from assets directory """
        if self.initialized:
            self.sound[sample].set_volume(self.sfx_volume / 10)
            self.sound[sample].play()

    def music(self, music):
        """ Plays sample as music. There is only one music at the time """
        if not self.initialized:
            return
        if self.bgm == music:
            return
        if self.bgm:
            self.sound[self.bgm].fadeout(500)
        self.bgm = music
        if self.bgm:
            self.sound[self.bgm].set_volume(self.music_volume / 10)
            self.sound[self.bgm].play()

# Initialize only one time
try:
    # pylint: disable = used-before-assignment
    # This is intented behaviour
    sfx
except NameError:
    sfx = Sfx()
