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


class Peg():

    peg_instances = []

    def __init__(self, player, id):
        self.player = player
        self.id = id
        self.location = 0
        Peg.peg_instances.append(self)

    def __str__(self):
        return ("Player %s peg %s is at location %s" % (self.player, self.id, self.location))

    def move_peg_to_start(self):
        print("Moving player %s peg %s to start position" % (self.player, self.id))
        self.location = 100+self.player*100+self.id

    @classmethod
    def get_player_peg_locations(cls,player):
        locations = []
        for i in cls.peg_instances:
            if i.player == player:
                locations.append(i.location)
        return(locations)


class Board():
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

        for p in range(0,4):
            print ("Player %s pegs:" % (p),Peg.get_player_peg_locations(p))

class Szimble():
    """docstring for ."""

    def __init__(self):
        self.active_player = 0
        print ("sz 0")
        self.board = Board()
        print ("sz 1")
        self.board.setup()
        print ("sz 2")
        self.board.print()
        print ("sz 3")


def main():



    log.info("===========================================")
    log.info("START")

    log.info("Game is runnning. Press ESC to stop.")

    game = Szimble()


    print("DONE 1")
    log.info("DONE")


if __name__ == "__main__":
    main()
