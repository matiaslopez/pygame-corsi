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
        ImageMessage.__init__(self, "check-unpressed.png")

        self.image_unpressed = self.image
        self.image_pressed = pygame.image.load("./imgs/check-pressed.png").convert_alpha()


        self.image_unpressed = pygame.transform.smoothscale(self.image_unpressed, (Properties.SIDE/9,Properties.SIDE/9))
        self.image_pressed = pygame.transform.smoothscale(self.image_pressed, (Properties.SIDE/9,Properties.SIDE/9))

        self.image = self.image_unpressed
        self.rect.center = (7.5 * (self.image.get_width() * 1.25), 5.8 * (self.image.get_height()* 1.25))

    def set_callback(self, callback):
        self.callback = callback

    def click(self):
        # print "ImageDone clicked"
        self.image = self.image_pressed
        self.dirty = True

    def release_click(self):
        self.image = self.image_unpressed
        self.dirty = True
        # print "ImageDone clicked"
        self.callback()