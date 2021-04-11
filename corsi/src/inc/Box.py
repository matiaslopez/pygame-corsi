# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame
import Properties
import time


current_milli_time = lambda: int(round(time.time() * 1000))


class Box(pygame.sprite.DirtySprite):

    def __init__(self, box_name, position, props):
        pygame.sprite.DirtySprite.__init__(self)
        self.box_name = box_name
        self.box_num = ord(box_name)-64
        self.position = position
        self.props = props

        self.interactive = True
        self.is_on = None
        self.init_time = current_milli_time()

        self.set()

    def set(self):
        SIDE = pygame.display.get_surface().get_rect().width
        SIDE = pygame.display.get_surface().get_rect().height/6
        self.image_on = pygame.image.load("./imgs/box-on.png").convert_alpha()
        self.image_off = pygame.image.load("./imgs/box-off.png").convert_alpha()

        self.image_on = pygame.transform.smoothscale(self.image_on, (SIDE,SIDE))
        self.image_off = pygame.transform.smoothscale(self.image_off, (SIDE,SIDE))
        self.image = self.image_off
        self.rect = self.image.get_rect()

        (x, y) = self.position
        self.rect.center = (x * (self.image.get_width() * 1.25) + 150,
                            y * (self.image.get_height()* 1.25) - 20)
        self.is_on = False

    def on(self):
        self.image = self.image_on
        self.dirty = True
        self.is_on = True

    def off(self):
        self.image = self.image_off
        self.dirty = True
        self.is_on = False

    def switch(self):
        if self.is_on:
            self.off()
        else:
            self.on()

    def click(self, time_off, unsuscribe):
        if self.interactive:
            if not self.is_on:
                self.init_time = current_milli_time()
                self.on()
                self.time_off = time_off
                self.unsuscribe = unsuscribe

    def tic_off(self, ev):
        delta = current_milli_time() - self.init_time
        # print 'tick off: ', delta

        self.off()
        self.unsuscribe()

    def tic(self, ev=None):
        delta = current_milli_time() - self.init_time
        if delta > self.time_off:
            # print 'tick off: ', delta
            self.off()
            self.unsuscribe(self)


