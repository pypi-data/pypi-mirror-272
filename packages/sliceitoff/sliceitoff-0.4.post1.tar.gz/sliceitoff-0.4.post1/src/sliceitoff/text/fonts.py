""" text.fonts - .FNT file loading and storing """
import os
from pathlib import Path
import pygame

DEBUG = os.getenv("DEBUG")

class Fonts:
    """ Fonts - static class to store loaded fonts """
    def __init__(self):
        self.fonts = {}

    def init(self, base_path):
        """ loads fonts found in assets directory """
        for fnt_file in Path(base_path).glob('*.fnt'):
            self.fonts[str(fnt_file.stem)] = Font(fnt_file)


class Font:
    """ Font - font surfaces to be loaded from file """
    def __init__(self, filename, height = 16):
        if DEBUG:
            print(f"Loading font {filename = }")
        self.surfaces = []
        with open(filename, mode="rb") as fnt_file:
            for _ in range(256):
                surface = pygame.Surface((8,height), pygame.SRCALPHA)
                for line in range(16):
                    byte = fnt_file.read(1)[0]
                    if line >= height:
                        continue
                    for bit in range(8):
                        if byte & 0x80:
                            surface.set_at((bit,line),"white")
                        byte <<= 1
                self.surfaces.append(surface)

    def get(self, ch):
        """ Just get surface of the font size 8x16 max """
        return self.surfaces[ch%256]

# Initialize only one time
try:
    # pylint: disable = used-before-assignment
    # This is intented behaviour
    fonts
except NameError:
    fonts = Fonts()
