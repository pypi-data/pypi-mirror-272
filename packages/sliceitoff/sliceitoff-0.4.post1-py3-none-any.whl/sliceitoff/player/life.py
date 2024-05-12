""" player.life - Hearth that will explode """
import pygame

from sliceitoff.display import Scaling
from sliceitoff.text import get_letter_surface, ExplodingSprite

class PieceOfHearth(ExplodingSprite):
    """ Eploding piece. Hearth consist of these """
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect().move(pos)

class Life(pygame.sprite.Group):
    """ The slicer. Special sprite group that only list 1 sprite """
    def __init__(self):
        super().__init__()
        self.timeout = 0

    def update(self, dt = 0, **kwargs):
        """ Quite normal update. Explosion starts when timeout reches 1_000 """
        super().update(dt = dt, explode = self.timeout < 1_000, **kwargs)
        if self.timeout > 0:
            self.timeout -= dt
        else:
            self.empty()

    def lose_life(self):
        """ Commands group to regenerate its sprites and sets timeout """
        self.timeout = 1_500
        srfc = get_letter_surface(("8x8", 200_000, 4), 0x03)
        offset = (
                int(Scaling.factor * 72_500 + Scaling.left),
                int(Scaling.factor * 20_000 + Scaling.top))
        block_width = srfc.get_rect().w // 24
        for x in range(0, block_width * 24, block_width):
            for y in range(0, block_width * 24, block_width):
                image = srfc.subsurface((x, y, block_width, block_width))
                self.add(PieceOfHearth(image, (x + offset[0], y + offset[1])))
