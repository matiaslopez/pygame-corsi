# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame
import time

import Properties

INIT, STIM, WAIT, ANSW, FEEDBACK, END = [ p for p in range(6) ]

current_milli_time = lambda: int(round(time.time() * 1000))


class Trial():

    def __init__(self, logger,  properties, change_to_active_mode, handle_end,feedback_handler):
        self.state = None
        self.running = False
        self.handle_end = None
        self.logger = logger
        self.properties = properties
        self.change_to_active_mode = change_to_active_mode
        self.handle_end = handle_end
        self.feedback_handler = feedback_handler

    def set_boxes(self, boxes, suscribe_box, unsuscribe_box):
        self.boxes = boxes
        self.suscribe_box = suscribe_box
        self.unsuscribe_box = unsuscribe_box

    def start(self, trial_name ,sequence, feedback):
        print "sequence: ", sequence
        self.state = INIT
        self.trial_name  = trial_name
        self.sequence = list(sequence)
        self.init_time = current_milli_time()
        self.trial_base_line_time = current_milli_time()
        self.running = True
        self.feedback = feedback
        self.correct_answer = True
        self.logger.log_trial_start(self.trial_name, sequence)
        # self.logger.

    def usr_answer(self, box_name, pos):
        # print "--- usr answer - boxclicked: ", self.box_clicked_num, " - current box: ", box_name
        # print " - expected: ", self.sequence[self.box_clicked_num]
        if self.state == ANSW:
            delta = current_milli_time() - self.init_time
            correct = None
            self.click_num += 1
            expected_box_name = self.sequence[min(self.box_clicked_num, len(self.sequence)-1)]
            if box_name is not None:
                if self.box_clicked_num < len(self.sequence):
                    correct = box_name == expected_box_name
                    self.correct_answer &=  correct
                    # print "CORRECT" if correct else "INCORRECT"
                self.box_clicked_num += 1
            # print "ANSWER in: ", delta
            (x,y) = pos
            self.logger.log_click(self.trial_name, self.box_clicked_num, self.click_num, box_name, expected_box_name,
                delta, correct, x, y)
            return True
        else:
            return False

    def next_by_usr(self):
        if self.state == ANSW:
            self.next()


    def next(self):
        self.init_time = current_milli_time()
        # print "leaving ", self.state,
        if self.state == INIT:
            self.state = STIM
            self.stim_index = 0
        elif self.state == STIM:
            # self.state = WAIT
        # elif self.state == WAIT:
            self.box_clicked_num = 0
            self.click_num = 0
            self.state = ANSW
            self.change_to_active_mode(True)
        elif self.state == ANSW:
            self.change_to_active_mode(False)
            if self.feedback:
                print "Showing feedback"
                self.state = FEEDBACK
                correct = self.correct_answer & (self.box_clicked_num == len(self.sequence))
                if correct:
                    self.feedback_handler["ok"]()
                else:
                    self.feedback_handler["no"]()
            else:
                self.state = END
        elif self.state == FEEDBACK:
            self.feedback_handler["off"]()
            self.state = END

        if self.state == END and self.handle_end is not None:
            # print "Summary, self.correct_answer", self.correct_answer
            # print "All clicked: ", self.box_clicked_num == len(self.sequence)
            correct = self.correct_answer & (self.box_clicked_num == len(self.sequence))
            self.logger.log_trial_result(self.trial_name, "CORRECT" if correct else "INCORRECT", self.box_clicked_num)
            self.handle_end(correct)
        # print " - new state: ", self.state


    def hide(self):
        self.stim.hide()
        self.target_img.hide()
        self.feed.hide()

    def tic(self):
        if self.running:
            if self.state == INIT:
                if self.init_time + self.properties["tprev"]  < current_milli_time():
                    self.next()
            elif self.state == STIM:
                appear_time = self.stim_index * (self.properties["tstim"] + self.properties["tinterstim"])
                if self.init_time + appear_time < current_milli_time():
                    if self.stim_index >= len(self.sequence):
                        self.next()
                        # print "END of STIM"
                    else:
                        current_box_id = self.sequence[self.stim_index]
                        self.boxes[current_box_id].click(self.properties["tstim"], self.unsuscribe_box)
                        self.suscribe_box(self.boxes[current_box_id])
                        self.stim_index += 1
            elif self.state == WAIT:
                if self.init_time + self.properties["tprev"]  < current_milli_time():
                    self.next()
            elif self.state == FEEDBACK:
                if self.init_time + self.properties["tfeedback"]  < current_milli_time():
                    self.next()
            # elif self.state == ANSW:
                # if (self.init_time + self.properties["timeoutextra"] +
                    # self.properties["timeoutperanswer"] * len(self.sequence)) < current_milli_time():
                    # self.next()
            # elif self.state == END:
                # if self.init_time + self.properties["tprev"]  < current_milli_time():
                    # self.next()

