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
        self.slots_goal = [32,33,34,35]
        self.slots =  [None for x in range(0,35)]

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

    def status(self):
        print ("Player: %s" % self.name)
        print ("...pegs at: %s"  % (self.pegs))
        print ("...pegs in game: %s"  % (self.pegs_in_game))
        print (self.slots)

    def play(self):
        dice = random.randrange(1,7)
        print("Dice: %s " % dice)

        action = {}
        action['E0'] = 0 # Move peg 1 to enter slot
        action['E1'] = 0 # Move peg 1 to enter slot
        action['E2'] = 0 # Move peg 1 to enter slot
        action['E3'] = 0 # Move peg 1 to enter slot
        action['M0'] = 0 # Move peg 1
        action['M1'] = 0 # Move peg 2
        action['M2'] = 0 # Move peg 3s
        action['M3'] = 0 # Move peg 4
        action['N0'] = 1 # Don't know what to do



        # Move peg to enter slot
        for id in range(0,4):
            target_slot = self.slot_enter
            if self.pegs_in_game == 0 and dice == 6 and self.slots[target_slot] == None:
                action["E%s" % id] += 90
                print ("PEG %s RULE: No pegs in game" % id)

        # Move peg X to goal
        for id in range(0,4):
            target_slot = self.pegs[id] + dice
            if target_slot in self.slots_goal and self.slots[target_slot] == None:
                action["M%s" % id] += 100
                print ("PEG %s RULE: Peg %s can move to goal" % (id,id))

        # Move peg X
        for id in range(0,4):
            target_slot = self.pegs[id] + dice
            if self.pegs[id] >= self.slot_enter and self.slots[target_slot] == None:
                action["M%s" % id] += 1
                print ("PEG %S RULE: Move peg %s" % (id,id))

        print("Rule outcome: %s" % action)

        # Select best rule based on value
        selected_action_max = 0
        selected_action_name = ""
        for k in action.keys():
            if action[k] > selected_action_max:
                selected_action_max = action[k]
                selected_action_name = k

        print("Selected action: %s" % selected_action_name)

        command = selected_action_name[:1]
        p = command = selected_action_name[1:]
        print("Command: %s Peg: %s"  % (command,p))






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
