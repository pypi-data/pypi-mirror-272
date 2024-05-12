""" menu.menu - Skeleton for menus """
import pygame

from sliceitoff.display import Scaling

from .explodeout import ExplodeOutGroup

MOUSE_TRESHOLD = 100

class Menu(ExplodeOutGroup):
    """ sprite group with imputs to make selection """
    def __init__(self, screen, items):
        super().__init__()
        self.items = items
        self.selection = 0
        self.mousey = 0
        self.screen = screen
        self.add(self.screen(self.selection))

    def do_selection(self):
        """ Default selection handler. Every action just ends menu. """
        self.do_fadeout()

    def update(self, dt = 0, **kwargs):
        """ Does it all. Reads keyboard and updates screen """
        if not super().update(dt = dt, **kwargs) or self.explode:
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.selection = self.items - 1
                self.do_selection()
                break
            if event.type == pygame.MOUSEBUTTONDOWN and event.button <= 3:
                self.do_selection()
                break
            if event.type == pygame.KEYDOWN:
                if self.process_key(event.key):
                    break
            elif event.type == pygame.MOUSEMOTION:
                self.process_mouse_motion()
        self.empty()
        self.add(self.screen(self.selection))

    def process_mouse_motion(self):
        """ Mouse movement up or down moves menu selection """
        self.mousey += pygame.mouse.get_rel()[1]
        pygame.mouse.set_pos(Scaling.center)
        if abs(self.mousey) > MOUSE_TRESHOLD:
            self.selection += 1 if self.mousey > 0 else -1
            self.selection %= self.items
            self.mousey = 0

    def process_key(self, key):
        """ Processes known key presses """
        match key:
            case pygame.K_KP_ENTER | pygame.K_RETURN | pygame.K_RIGHT:
                self.do_selection()
                return True
            case pygame.K_ESCAPE | pygame.K_q | pygame.K_LEFT:
                self.selection = self.items - 1
                self.do_selection()
                return True
            case pygame.K_UP:
                self.selection -= 1
                self.selection %= self.items
            case pygame.K_DOWN:
                self.selection += 1
                self.selection %= self.items
        return False
