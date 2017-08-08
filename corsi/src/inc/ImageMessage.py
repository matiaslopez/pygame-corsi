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
        SIDE = pygame.display.get_surface().get_rect().width
        SIDE = pygame.display.get_surface().get_rect().height/6

        self.image_unpressed = self.image
        self.image_pressed = pygame.image.load("./imgs/check-pressed.png").convert_alpha()


        self.image_unpressed = pygame.transform.smoothscale(self.image_unpressed, (SIDE,SIDE))
        self.image_pressed = pygame.transform.smoothscale(self.image_pressed, (SIDE,SIDE))

        self.image = self.image_unpressed
        self.rect.center = (8.5 * (self.image.get_width() * 1.25), 5 * (self.image.get_height()* 1.25))
        # self.rect.center = (7.5 * (self.image.get_width() * 1.25), 6 * (self.image.get_height()* 1.25))

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


class Feedback(ImageMessage):

    def __init__(self, is_ok=True):
        src = "feed-ok.png" if is_ok else "feed-no.png"
        ImageMessage.__init__(self, src)

        (x,y) = pygame.display.get_surface().get_rect().size
        # (x,y) = Properties.SCREEN_RES
        self.image = pygame.surface.Surface((x*1., y*1.)).convert_alpha()
        # self.background["pasive"].image = pygame.surface.Surface(self.screen.get_size())
        self.image.fill([255,250,104,100] if is_ok else [40,40,40,100])

        emoji = pygame.image.load("./imgs/" + src).convert_alpha()

        self.rect = self.image.get_rect()
        self.image.blit(emoji, (self.rect.centerx-(emoji.get_width()/2), self.rect.centery-(emoji.get_height()/2)))

        self.rect.center = pygame.display.get_surface().get_rect().center

        self.dirty = True
        self.visible = False

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