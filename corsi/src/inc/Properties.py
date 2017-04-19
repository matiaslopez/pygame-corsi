# -*- coding: utf-8 -*-

import pygame

#~ SCREEN_RES = (1200, 900)
#~ SCREEN_RES = (800, 600)

if pygame.display.get_init():
    SCREEN_RES = pygame.display.get_surface().get_size()
else:
    SCREEN_RES = (800, 600)

# DELTA_OK = 0.1
