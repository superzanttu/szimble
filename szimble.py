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

    def __init__(self, player, id):
        self.player = player
        self.id = id
        self.location = 0

    def __str__(self):
        print ("Player %s peg %d is at location %s" %(self.player, self.id, self.location))


class Board():
    """
    Slots 1...28 as circle

    Slots for players
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



    def print_board(self):
        print(self.pegs)

class Szimble():
    """docstring for ."""

    def __init__(self):
        self.board = Board()

        self.board.print_board()



def main():



    log.info("===========================================")
    log.info("START")

    log.info("Game is runnning. Press ESC to stop.")

    game = Szimble()



    log.info("DONE")


if __name__ == "__main__":
    main()
