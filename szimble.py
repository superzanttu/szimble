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


class Old_Peg():

    peg_instances = []

    def __init__(self, player, id):
        self.player = player
        self.id = id
        self.location = 0
        self.__class__.peg_instances.append(self)

    def __str__(self):
        return ("Player %s peg %s is at location %s" % (self.player, self.id, self.location))

    def move_peg_to_start(self):
        print("Moving player %s peg %s to start position" % (self.player, self.id))
        self.location = 100+self.player*100+self.id

    @classmethod
    def get_player_pegs(cls,player):
        pegs_data= []
        for i in cls.peg_instances:
            if i.player == player:
                pegs_data.append([i.player,i.id,i.location])
        return(pegs_data)

    @classmethod
    def set_player_peg_position(cls,player,id,location):
        for i in cls.peg_instances:
            if i.player == player and i.id == id:
                i.location = location
                break


class Old_Board():
    """
    Slots 0...27 as circle

    Slot definitions
            Enter  Exit  Start    Goal
    0 Blue      0    27  100..103 110..113
    1 Yellow    7     6  200..203 210..213
    2 Green    14    13  300..303 310..313
    3 Red      21    20  400..403 410..413
    """

    def __init__(self):
        self.pegs = []
        for p in range(0,4):
            for c in range(0,4):
                self.pegs.append(Peg(p,c))

    def setup(self):
        print("Setup board")
        for s in self.pegs:
            s.move_peg_to_start()



    def print(self):
        print("Board status")

        board = ["--"]*28

        for player in range(0,4):
            peg_data = Peg.get_player_pegs(player)
            print ("Player %s pegs:" % (player),peg_data)
            for peg in peg_data:

                for slot in range(0,28):
                    #print (slot,peg[2])
                    if slot == peg[2]:
                        print("HIT")
                        board[slot]="%s%s" % (peg[0], peg[1])

        print(board)


class Old_Szimble():
    """docstring for ."""

    def __init__(self):
        self.active_player = 0
        self.board = Board()
        self.board.setup()
        self.board.print()
        Peg.set_player_peg_position(0,1,20)
        self.board.print()

class Player():

    def __init__(self, player_name):
        print("Init player: %s" % player_name)
        self.name = player_name
        # Slot index 0..35
        self.pegs = [None, None, None, None]
        self.slots_start = [0,1,2,3]
        self.slot_enter = 4
        self.slot_enter_enemy = [11,18,25]
        self.slots_goal = [32,33,34,35]
        self.slots =  [None for x in range(0,35)]

    def move_peg_to_start(self,id):
        print("Move player %s peg %s to start" % (self.name, id))
        for i in self.slots_start:
            if self.slots[i] == None:
                self.slots[i] = id
                print("...peg moved to slot %s" % i)
                return

        pass

    def status(self):
        print ("Player: %s" % self.name)
        print ("...spegs at: %s"  % (self.pegs))
        print (self.slots)

def main():



    log.info("===========================================")
    log.info("START")

    log.info("Game is runnning. Press ESC to stop.")

    player = Player("Red")
    player.move_peg_to_start(0)
    player.move_peg_to_start(1)
    player.move_peg_to_start(2)
    player.move_peg_to_start(3)

    player.status()


    log.info("DONE")


if __name__ == "__main__":
    main()
