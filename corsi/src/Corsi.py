# -*- coding: utf-8 -*-
try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
except ImportError:
    pass

import pygame
import sys
from pygame import time
#import pygame._view
#from pygame.locals import *
from random import choice
import time

import json
import datetime

import inc.Properties as Properties

from inc.EventHandler import EventHandler
from inc.Event import Event
from inc.ExpRunner import *
from inc.Box import *
# from inc.Feedback import *
#from inc.Message import *
from inc.ImageMessage import *
from inc.Instruction import *
# from inc.ImageMessageBar import *
from inc.Trial import *

# SUBJECT_NAME = raw_input('Nombre: ')
SUBJECT_NAME = 'Nombre: '

(BACKGR_lyr,
    BOXES_lyr,
    STIM_lyr,
    BTN_lyr,
    FEED_lyr,
    INST_lyr,
    ) = [ p for p in range(0,6) ]

INTERACTIVE, PASSIVE = [ p for p in range(0,2) ]


class FileLogger():

    def __init__(self):
        import os
        directory = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(directory):
            os.makedirs(directory)

        d = datetime.datetime.today().strftime("%Y-%m-%d_%H.%M.%S")
        file_name = SUBJECT_NAME + "_" + d + ".csv"
        file_path = os.path.join(directory, file_name)

        self.f = open(file_path, 'w')

        self.log_headers()

    def get_str_time(self):
        return str(datetime.datetime.today().strftime("[%Y-%m-%d %H.%M.%S.%f] "))

    def log_headers(self):

        str_store = ["KIND_OF_LOG","Date","trial_id","col1", "col2","col3","col4","col5","col6","col7","col8"]
        self.write_down(str_store)

        str_store = ["CLICK","Date","trial_id","box_clicked_num",
            "click_num","box_name","expected_box_name","time","correct","x","y"]
        self.write_down(str_store)

        str_store = ["RESULT","Date","trial_id","was_correct","number_of_box_clicked",
            "number_of_clicks", "expected_sequence", "result_sequence"]
        self.write_down(str_store)

        str_store = ["TRIAL START","Date","trial_id","sequence", "Feedback"]
        self.write_down(str_store)


    def log_click(self, trial_id, box_clicked_num, click_num, box_name, expected_box_name, time, correct, x, y):
        str_store = []
        str_store.append("CLICK")
        str_store.append(self.get_str_time())
        str_store.append(str(trial_id))
        str_store.append(str(box_clicked_num))
        str_store.append(str(click_num))
        str_store.append(str(box_name))
        str_store.append(str(expected_box_name))
        str_store.append(str(time))
        str_store.append(str(correct))
        str_store.append(str(x))
        str_store.append(str(y))

        self.write_down(str_store)

    def log_trial_result(self, trial_id, correct, box_clicked_num,
                number_of_clicks, expected_sequence, result_sequence):
        str_store = []
        str_store.append("RESULT")
        str_store.append(self.get_str_time())
        str_store.append(str(trial_id))
        str_store.append(str(correct))
        str_store.append(str(box_clicked_num))
        str_store.append(str(number_of_clicks))
        str_store.append(str(expected_sequence))
        str_store.append(str(result_sequence))

        self.write_down(str_store)

    def log_trial_start(self, trial_id, sequence, feedback):
        str_store = []
        str_store.append("TRIAL START")
        str_store.append(self.get_str_time())
        str_store.append(str(trial_id))
        str_store.append(str(sequence))
        str_store.append(str(feedback))

        self.write_down(str_store)

    def log_invalid_press(self):
        str_store = []
        str_store.append("INVALID PRESS")
        str_store.append(self.get_str_time())

        self.write_down(str_store)

    def log_message(self, message):
        str_store = []
        str_store.append(message.upper())
        str_store.append(self.get_str_time())

        self.write_down(str_store)

    def write_down(self, arr):
        str_store = ";".join(arr)
        str_store = str_store + ";\n"

        self.f.write(str_store)

    def close(self):
        self.f.close()

class Corsi():
    def __init__(self, experiment):
        self.logger = FileLogger()

        self.screen = pygame.display.get_surface()

        self.clock = pygame.time.Clock()
        self.experiment = experiment

        self.event_handler = EventHandler()
        self.keyboard_handler = Event()

        self.sprites_group = pygame.sprite.LayeredDirty()

        self.background = {}
        self.background["pasive"] = pygame.sprite.DirtySprite()
        # self.background["pasive"].image = pygame.surface.Surface(Properties.SCREEN_RES)
        self.background["pasive"].image = pygame.surface.Surface(self.screen.get_size())
        self.background["pasive"].image.fill([40,40,40])
        self.background["pasive"].rect = self.background["pasive"].image.get_rect()
        self.sprites_group.add(self.background["pasive"], layer=BACKGR_lyr)

        # self.background["active"] = pygame.sprite.DirtySprite()
        # self.background["active"].image = pygame.surface.Surface(Properties.SCREEN_RES)
        # # self.background["active"].image = pygame.surface.Surface(self.screen.get_size())
        # self.background["active"].image.fill([80,80,80])
        # self.background["active"].rect = self.background["active"].image.get_rect()
        # self.sprites_group.add(self.background["active"], layer=BACKGR_lyr)

        # self.background["active"].visible = False
        self.feedback_ok = Feedback()
        self.feedback_no = Feedback(False)
        self.sprites_group.add(self.feedback_ok, layer=FEED_lyr)
        self.sprites_group.add(self.feedback_no, layer=FEED_lyr)

        self.msgs = {}
        self.boxes = {}

        self.instruction =  Instruction()
        self.instruction.hide()
        self.sprites_group.add(self.instruction, layer=INST_lyr)

        self.msgs["done"] =  ImageDone()
        for v in self.msgs.itervalues():
            self.sprites_group.add(v, layer=BTN_lyr)

        for box_name, position in self.experiment["box_positions"].iteritems():
            box = Box(box_name, json.loads(position), self.experiment["properties"])
            self.sprites_group.add(box, layer=BOXES_lyr)
            self.boxes[box_name] = box


        self.tic_group = []

        self.trial = Trial(self.logger, self.experiment["properties"],
                self.change_to_active_mode,
                None,
                {"ok": self.feedback_ok.show, "no": self.feedback_no.show,
                "off": (lambda: [self.feedback_ok.hide(), self.feedback_no.hide()])})
        self.exp_runner = ExpRunner(self.experiment, self.trial, self.boxes)
        self.exp_runner.end_test = self.terminar_juego
        self.exp_runner.instruction = self.instruction
        self.trial.handle_end = self.exp_runner.next_trial
        self.trial.set_boxes(self.boxes, self.suscribe_box_on, self.unsuscribe_box)
        self.boxes_on = []


        self.msgs["done"].set_callback(self.trial.next_by_usr)

        self.change_to_active_mode(False)

    def change_to_active_mode(self, toActive=True):
        # self.change_background(toActive)
        if toActive:
            self.state = INTERACTIVE
            self.msgs["done"].show()
        else:
            self.state = PASSIVE
            self.msgs["done"].hide()


    def change_background(self, toActive=True):
        if toActive:
            self.background["active"].visible = True
            self.background["pasive"].visible = False
        else:
            self.background["active"].visible = False
            self.background["pasive"].visible = True

        self.background["active"].dirty = True
        self.background["pasive"].dirty = True

    def set_events(self):
        key_suscribe = self.keyboard_handler.suscribe
        self.event_handler.suscribe(pygame.KEYDOWN, lambda ev: self.keyboard_handler.dispatch(ev.key, ev))

        key_suscribe(pygame.K_ESCAPE, (lambda ev: [self.logger.log_message("esc pressed"), self.terminar_juego(ev)]))

        self.event_handler.suscribe(pygame.QUIT,
            (lambda ev: [self.logger.log_message("pygame quit"), self.terminar_juego(ev)]))
        self.event_handler.suscribe(pygame.MOUSEBUTTONDOWN, self.click)
        # self.event_handler.suscribe(pygame.MOUSEBUTTONUP, self.click)
        self.event_handler.suscribe(pygame.MOUSEBUTTONUP, self.release_click)

    # def click(self, res):
    #     (x, y) = pygame.mouse.get_pos()

    #     if self.state == INTERACTIVE:
    #         for i in self.sprites_group.get_sprites_from_layer(BOXES_lyr):
    #             if (i.rect.collidepoint(x, y)):
    #                 a = i.tic_off
    #                 ev = pygame.USEREVENT + 1
    #                 print "Suscribing event ", ev
    #                 self.event_handler.suscribe(ev, a)
    #                 i.click(lambda: self.event_handler.unsuscribe(ev, a))
    #                 pygame.time.set_timer(ev, self.experiment["properties"]["tansweron"])

    def click(self, res):
        (x, y) = pygame.mouse.get_pos()

        if self.state == INTERACTIVE:
            click_in_box = False
            for i in self.sprites_group.get_sprites_from_layer(BOXES_lyr):
                if (i.rect.collidepoint(x, y)):
                    # print "Click box ", i.box_name
                    if not i.is_on:
                        self.suscribe_box_on(i)
                        i.click(self.experiment["properties"]["tansweron"], self.unsuscribe_box)
                        self.trial.usr_answer(i.box_name, (x,y))
                        click_in_box = True

            for i in self.sprites_group.get_sprites_from_layer(BTN_lyr):
                if (i.rect.collidepoint(x, y)):
                    # print "Click button "
                    click_in_box = True
                    i.click()

            if not click_in_box:
                self.trial.usr_answer(None, (x,y))
        elif self.state == PASSIVE:
            if self.instruction.visible:
                self.instruction.hide()

    def release_click(self, res):
        (x, y) = pygame.mouse.get_pos()

        if self.state == INTERACTIVE:
            for i in self.sprites_group.get_sprites_from_layer(BTN_lyr):
                if (i.rect.collidepoint(x, y)):
                    # print "Click button "
                    click_in_box = True
                    i.release_click()


    def suscribe_box_on(self, box):
        self.boxes_on.append(box)

    def unsuscribe_box(self, box):
        # import pdb; pdb.set_trace();
        self.boxes_on.remove(box)


    def terminar_juego(self, ev=None):
        print "TERMINANDO"
        self.logger.log_message("end game")
        self.logger.close()
        self.running = False

    def report_answ(self, ev=None):
        if not self.trial.usr_answer():
            self.logger.log_invalid_press()


    def run(self):
        #~ import pdb; pdb.set_trace()
        self.running = True
        self.set_events()
        self.exp_runner.next()
        self.mainLoop()

    def trial_handle_next(self):
        pass

    def mainLoop(self):
        pygame.display.flip()
        self.playing = None

        while self.running:
            self.clock.tick(60)

            self.event_handler.handle()
            self.trial.tic()
            for box in self.boxes_on:
                box.tic()
            self.sprites_group.draw(self.screen)

            pygame.display.flip()

def main():
    json_data=open("default.json").read()
    experiment = json.loads(json_data)
    if len(sys.argv) == 2:
        print "Cargando opciones de ", sys.argv[1]
    
        prot_f=open(sys.argv[1]).read()
        prot_data = json.loads(prot_f)
        experiment["trials"] = prot_data["trials"]
        if prot_data.has_key("protocolo"):
            if prot_data["protocolo"].has_key("nombre"):
                experiment["protocolo"]["nombre"] = prot_data["protocolo"]["nombre"] 

        if prot_data.has_key("properties"):
            if prot_data["properties"].has_key("tiempoEncendidoLuz"):
                experiment["properties"]["tstim"] = prot_data["properties"]["tiempoEncendidoLuz"] 
            if prot_data["properties"].has_key("tiempoEntreLuces"):
                experiment["properties"]["tinterstim"] = prot_data["properties"]["tiempoEntreLuces"] 

        # Maxi
        # "tiempoComienzaIntento": 1000,
        # "timeoutRespuesta": 35000
        # Pygame
        # "tprev": 500,
        # "tansweron": 800,
        # "tfeedback": 1500



    # print(experiment.keys())
    # print(experiment)
    # sys.exit(1)


    SCREEN_RES = (int(experiment["screen_res"]["x"]), int(experiment["screen_res"]["y"]))

    pygame.init()
    # pygame.display.set_mode(SCREEN_RES)
    pygame.display.set_mode(SCREEN_RES,pygame.FULLSCREEN)


    game = Corsi(experiment)
    game.run()

    print "Saliendo"
    pygame.quit()

if __name__ == '__main__':
    main()
