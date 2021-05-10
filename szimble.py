#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Kimble clone
#
# Copyright (C) 2021 Kai Käpölä
#


# Time-stamp: <2021-02-28 08:04:42>
import logging
import sys
import math
import os
import random
from collections import defaultdict

# Start logging before other libraries
# import argparse
# from apscheduler.schedulers.blocking import BlockingScheduler
# import csv
import pprint
# import time
# import docstrings

FOLDER_HOME = os.path.dirname(os.path.abspath(__file__))
FOLDER_LOG = os.path.join(FOLDER_HOME,"log")
# Initialize log folder
if not os.path.exists(FOLDER_LOG):
    os.makedirs(FOLDER_LOG)
print("Log folder:",FOLDER_LOG)

# Logging
class ListHandler(logging.Handler):  # Inherit from logging.Handler
    def __init__(self, log_list):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Our custom argument
        self.log_list = log_list

    def emit(self, record):
        # record.message is the log message
        self.log_list.append(record.msg)


logging.basicConfig(format='%(asctime)s|%(levelname)s|%(filename)s|%(funcName)s|%(lineno)d|%(message)s',
                    filename='./log/main.log', level=logging.DEBUG)

hud_console_log = []
hud_console = ListHandler(hud_console_log)
hud_console.setLevel(logging.INFO)

hud_formatter = logging.Formatter('%(asctime)s|%(message)s')
hud_console.setFormatter(hud_formatter)

logging.getLogger('').addHandler(hud_console)



log = logging.getLogger()


class Player():

    def __init__(self, player_name):
        print("Init player: %s" % player_name)
        self.name = player_name
        # Slot index 0..35
        self.pegs = [None, None, None, None]
        self.pegs_in_game = 0
        self.slots_start = [0,1,2,3]
        self.slot_enter = 4
        self.slot_enter_enemy = [11,18,25]
        self.slot_goal1 = 32
        self.slot_goal2 = 35
        self.slots =  [None for x in range(0,36)]

    def move_peg_to_start(self,id):
        print("Move player %s peg %s to start" % (self.name, id))

        # Clear current location
        if self.pegs[id] != None:
            self.slots[self.pegs[id]] = None

        # Move peg to empty start slot
        for i in self.slots_start:
            if self.slots[i] == None:
                self.slots[i] = id
                self.pegs[id] = i
                print("...peg moved to slot %s" % i)
                return

        # Pegs in the Game
        if self.pegs_in_game > 0:
            self.pegs_in_game -= 1

    def move_peg_to_game(self,id):
        print("Move player %s peg %s to game" % (self.name, id))

        # Clear current location
        if self.pegs[id] != None:
            self.slots[self.pegs[id]] = None

        # Move peg to enter slot
        if self.slots[self.slot_enter] == None:
            self.slots[self.slot_enter] = id
            self.pegs[id]= self.slot_enter
        else:
            print("ERROR: Enter slot occupied")
            exit(1)


        # Pegs in the Game
        self.pegs_in_game += 1

    def move_peg_to_goal(self,id,target_slot):
        print("Move player %s peg %s to goal slot %s" % (self.name, id,target_slot))

        # Clear current location
        if self.pegs[id] != None:
            self.slots[self.pegs[id]] = None

        # Move peg to new slot
        if self.slots[target_slot] == None:
            self.slots[target_slot] = id

        else:
            print("ERROR: Target slot occupied")
            exit(1)

        # Pegs in the Game
        self.pegs_in_game -= 1
        self.pegs[id]= None

        print("FIXME: don't move if peg is in goal allready")


    def move_peg_to_slot(self,id,target_slot):
        print("Move player %s peg %s to slot %s" % (self.name, id,target_slot))

        # Clear current location
        if self.pegs[id] != None:
            self.slots[self.pegs[id]] = None

        # Move peg to new slot
        if self.slots[target_slot] == None:
            self.slots[target_slot] = id
            self.pegs[id]= target_slot
        else:
            print("ERROR: Target slot occupied")
            exit(1)


    def status(self):
        print ("Player %s have %s pegs in game at %s" % (self.name,self.pegs_in_game,self.pegs))
        print (self.slots)

    def play(self):
        dice = random.randrange(1,7)
        print("Dice: %s " % dice)

        rule_score = {}
        rule_target_slot = {}
        # E = move peg to enter slot
        # M = move peg to empty slot
        # G = move peg to goal
        for r in ['E','M','G']:
            for p in range(0,4):
                rule_score["%s%s" % (r,p)] =0
                rule_target_slot["%s%s" % (r,p)] = None

        rule_score['N0'] = 1 # Don't know what to do
        rule_target_slot['N0'] = None




        for id in range(0,4):
            print ("Checking peg %s:" % id),
            target_slot = self.pegs[id] + dice

            # Move peg to enter slot
            if dice == 6 and self.slots[target_slot] == None and self.pegs[id] < self.slot_enter:
                rule_score["E%s" % id] += 90
                rule_target_slot["E%s" % id] = self.slot_enter
                print ("...enter game with score %s" % (rule_score["E%s" % id]))

            # Move peg X to goal
            if target_slot >= self.slot_goal1 and target_slot <= self.slot_goal2 and self.slots[target_slot] == None:
                rule_score["G%s" % id] += 100 + self.pegs[id] # Peg closest to the goal have higher score
                rule_target_slot["G%s" % id] = target_slot
                print ("...move to goal slot %s with score %s" % (target_slot,rule_score["G%s" % id]))

            # Move peg X
            if self.pegs[id] >= self.slot_enter and target_slot < self.slot_goal1 and self.slots[target_slot] == None :
                rule_score["M%s" % id] += self.pegs[id] # Peg closest to the goal have higher score

                if self.pegs[id] == self.slot_enter: # Priorize peg in enter slot
                    print("...is at enter slot")
                    rule_score["M%s" % id] += 50

                if self.pegs[id] in self.slot_enter_enemy: # Priorize peg in enemy enter slot
                    print("...is at enemy enter slot")
                    rule_score["M%s" % id] += 60


                rule_target_slot["M%s" % id] = target_slot
                print ("...move to %s with score %s" % (target_slot,rule_score["M%s" % id]))

        print("Rule scores: %s" % rule_score)
        print("Rule target slots: %s" % rule_target_slot)

        # Select best rule based on value
        selected_rule_score = 0
        selected_rule_name = ""
        for k in rule_score.keys():
            if rule_score[k] > selected_rule_score:
                selected_rule_score = rule_score[k]
                selected_rule_name = k
                target_slot = rule_target_slot[k]

        # print("Selected rule: %s" % selected_rule_name)

        action = selected_rule_name[:1]
        peg = int(selected_rule_name[1:])
        #print("Command: %s Peg: %s Target slot: %s"  % (action,peg,target_slot))

        if action == "E": # Move peg to enter slot
            self.move_peg_to_game(peg)
        elif action == "M": # Move peg to enter slot
            self.move_peg_to_slot(peg,target_slot )
        elif action == "G": # Move peg to goal slot
            self.move_peg_to_slot(peg,target_slot )





def main():

    log.info("===========================================")
    log.info("START")

    random.seed()

    log.info("Game is runnning.")

    player = Player("Red")
    player.move_peg_to_start(0)
    player.move_peg_to_start(1)
    player.move_peg_to_start(2)
    player.move_peg_to_start(3)

    player.status()

    user_input=""
    while user_input == "":
        player.play()
        player.status()
        user_input = input()

    log.info("DONE")


if __name__ == "__main__":
    main()
