""" screens.mainmenu - Screen for mainmenu"""
from random import randrange
from sliceitoff.text import TextPage
from sliceitoff.sfx import sfx

def settings_screen(selection):
    """ Screen where current selection is flashing """
    sfx_slider = '#' * sfx.sfx_volume + ' ' * (10 - sfx.sfx_volume)
    bgm_slider = '#' * sfx.music_volume + ' ' * (10 - sfx.music_volume)
    active = randrange(0xe9,0xf0)
    inactive = 0xe7
    text =  (
            f"    Settings:\n"
            f"\n\n"
            f"\xe7SFX: "
            f"{chr(active if selection == 0 else inactive)}"
            f"[{sfx_slider}]\n\n"
            f"\xe7BGM: "
            f"{chr(active if selection == 1 else inactive)}"
            f"[{bgm_slider}]\n\n"
            f"{chr(active if selection == 2 else inactive)}"
            f"Back.")
    return TextPage(
            text,
            font = '8x8',
            size = (16_000, 16_000),
            pos = (32_000, 16_000) )
