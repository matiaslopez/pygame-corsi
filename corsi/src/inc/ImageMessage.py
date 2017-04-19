# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame
import Properties



class ImageMessage(pygame.sprite.DirtySprite):

    def __init__(self, name):
        pygame.sprite.DirtySprite.__init__(self)
        self.name = name

        self.set()

    def set(self):
        self.image = pygame.image.load("./imgs/" + self.name).convert_alpha()
        # self.image = pygame.transform.scale(self.image,(Properties.SCREEN_RES[0],Properties.SCREEN_RES[1]))
        self.rect = self.image.get_rect()

        self.hide()

    def hide(self):
        self.visible =  False
        self.dirty = True

    def show(self):
        self.visible =  True
        self.dirty = True

class ImageDone(ImageMessage):
    def __init__(self):
        ImageMessage.__init__(self, "done.png")

        self.image = pygame.transform.smoothscale(self.image, (Properties.SCREEN_RES[0]/9,Properties.SCREEN_RES[0]/9))

        self.rect.center = (7.5 * (self.image.get_width() * 1.25), 5.8 * (self.image.get_height()* 1.25))

    def set_callback(self, callback):
        self.callback = callback

    def click(self):
        # print "ImageDone clicked"
        self.callback()