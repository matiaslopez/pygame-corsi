# -*- coding: utf-8 -*-

import pygame

#~ SCREEN_RES = (1200, 900)
#~ SCREEN_RES = (800, 600)

if pygame.display.get_init():
    SCREEN_RES = pygame.display.get_surface().get_size()
else:
    SCREEN_RES = (800, 600)
    SCREEN_RES = (1200, 700)
    # SCREEN_RES = (1200, 900)
    # SCREEN_RES = (1500, 750)

SIDE = int(SCREEN_RES[0] * (4/3.0)/(SCREEN_RES[0]/SCREEN_RES[1]) * 0.7)
# print SIDE
# DIVISOR = SCREEN_RES[0]
# DELTA_OK = 0.1
