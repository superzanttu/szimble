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
from dataclasses import dataclass, field
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

class Slot():
    peg_id = None
    peg_owner_id = None


class Board():
    peg_id = [None for x in range(0,28)]
    peg_owner_id = [None for x in range(0,28)]
    player_enter_slot = [0,7,14,21]
    player_exit_slot = [27,6,13,20]

    @classmethod
    def status(cls):
        slots=""
        slots_owner_id=""

        for i in range(0,28):
            #print (cls.peg_id[i],cls.peg_owner_id[i])
            if cls.peg_id[i] == None:
                slots += ".. "
                slots_owner_id += ".. "
            else:
                slots += "{:.>2} ".format(cls.peg_id[i])
                slots_owner_id += "{:.>2} ".format(cls.peg_owner_id[i])

        print ("All players          %s" % slots)
        print ("                     %s" % slots_owner_id)

    @classmethod
    def draw(cls):

        board=[]

        board.append("Szimbe board status:")


        # Top row
        row=""
        for i in range(0,8):
            #print (i)
            #print (cls.peg_id[i],cls.peg_owner_id[i])
            if cls.peg_id[i] == None:
                row += "..-"
            else:
                row += "%s%s-" % (cls.peg_id[i],cls.peg_owner_id[i])

        board.append(row[:-1])

        # left and right sides
        for i in range (8,14):
            row="                   "
            if cls.peg_id[i] == None:
                row += ".."
            else:
                row += "%s%s" % (cls.peg_id[i],cls.peg_owner_id[i])

            j = 35 - i

            if cls.peg_id[j] == None:
                row =".." + row
            else:
                row = "%s%s" % (cls.peg_id[j],cls.peg_owner_id[j]) + row

            #print (i,j)
            board.append(row)

        # Bottom row
        row=""
        for i in range(14,22):
            #print (i)
            #print (cls.peg_id[i],cls.peg_owner_id[i])
            if cls.peg_id[i] == None:
                row = "..-" + row
            else:
                row = "%s%s-" % (cls.peg_id[i],cls.peg_owner_id[i]) + row
        board.append(row[:-1])



        for r in board:
            print(r)


class Player():

    board = Board()

    def __init__(self, player_id):
        print("Init player: %s" % player_id)
        self.id = player_id
        # Slot index 0..35
        self.turn_counter = 0
        self.dice = 0
        self.pegs_location = [0, 1, 2, 3] # All pegs in start
        self.enemy_pegs_location = {}
        self.pegs_in_start = 4
        self.pegs_in_game = 0
        self.pegs_in_goal = 0
        self.slots_start = [0,1,2,3]
        self.slot_enter = 4
        self.slot_enter_enemy = [11,18,25]
        self.slot_goal1 = 32
        self.slot_goal2 = 35
        self.slots =  [None for x in range(0,36)]
        self.slots_owner_id = [None for x in range(0,36)]
        self.status_winner = False
        self.status_peg_eaten = None

        # All pegs in start
        self.slots[0] = 0
        self.slots[1] = 1
        self.slots[2] = 2
        self.slots[3] = 3

    def update_my_slots(self):
        print("Update player %s slots" % self.id)
        for i in range(0,28):
            board_slot = (i + Board.player_enter_slot[self.id]) % 28
            self.slots[i] = Board.peg_id[board_slot]
            self.slots_owner_id[i] = Board.peg_owner_id[board_slot]
            print("player %s slot %s board_slot %s" % (self.id, i,board_slot))

    def update_board(self):
        print("Update board using player %s slot status" % self.id)
        for i in range(0,28):
            if Board.peg_owner_id[i] == self.id: # Remove own pegs
                Board.peg_id[i] = None
                Board.peg_owner_id[i] = None

        #print(self.pegs_location)
        for peg_id in range(0,4):
            peg_location = self.pegs_location[peg_id]
            #print ("peg location:%s slot_enter:%s goal1:%s" % (peg_location,self.slot_enter, self.slot_goal1))
            if peg_location >= self.slot_enter and peg_location < self.slot_goal1:
                board_slot = (peg_location - self.slot_enter + Board.player_enter_slot[self.id]) % 28
                #print ("  update board_slot:%s  " % (board_slot))
                Board.peg_id[board_slot] = peg_id
                Board.peg_owner_id[board_slot] = self.id

                #for i in range (0,28):
                #    print (i,Board.peg_id[i],Board.peg_owner_id[i])

    def x_move_peg_to_start(self,peg_id):
        print("Move player %s peg %s to start" % (self.name, id))

        self.pegs_in_start += 1
        self.pegs_in_game -= 1

        # Clear current location
        if self.pegs[peg_id] != None:
            self.slots[self.pegs[peg_id]] = None
            self.slots_owner_id[self.pegs[peg_id]] = None

        # Move peg to empty start slot
        for i in self.slots_start:
            if self.slots[i] == None:
                self.slots[i] = peg_id
                self.slots_owner_id[i] = self.name
                self.pegs[peg_id] = i
                print("...peg moved to slot %s" % i)
                return

    def move_peg_to_game(self,peg_id):
        print("Move player %s peg %s to game" % (self.name, id))

        self.pegs_in_start -= 1
        self.pegs_in_game += 1

        # Clear current location
        if self.pegs_location[peg_id] != None:
            self.slots[self.pegs_location[peg_id]] = None
            self.slots_owner_id[self.pegs_location[peg_id]] = None

        # Move peg to enter slot
        if self.slots[self.slot_enter] == None:
            self.slots[self.slot_enter] = peg_id
            self.slots_owner_id[self.slot_enter] = self.id
            self.pegs_location[peg_id]= self.slot_enter
        else:
            print("ERROR: Enter slot occupied")
            exit(1)


    def move_peg_to_goal(self,peg_id,target_slot):
        print("Move player %s peg %s to goal slot %s" % (self.name, id,target_slot))

        self.pegs_in_goal += 1
        self.pegs_in_game -= 1

        # Clear current location
        if self.pegs_location[peg_id] != None:
            self.slots[self.pegs_location[peg_id]] = None
            self.slots_owner_id[self.pegs_location[peg_id]] = None

        # Move peg to new slot
        if self.slots[target_slot] == None:
            self.slots[target_slot] = peg_id
            self.slots_owner_id[target_slot] = self.id
            self.pegs_location[peg_id]= target_slot
        else:
            print("ERROR: Target slot occupied")
            exit(1)

        if self.pegs_in_goal == 4: # We are a winner!
            self.status_winner = True


    def move_peg_to_slot(self,peg_id,target_slot):
        print("Move player %s peg %s to slot %s" % (self.name, id,target_slot))

        # Clear current location
        if self.pegs_location[peg_id] != None:
            self.slots[self.pegs_location[peg_id]] = None
            self.slots_owner_id[self.pegs_location[peg_id]] = None

        # Move peg to new slot
        if self.slots[target_slot] == None:
            self.slots[target_slot] = peg_id
            self.slots_owner_id[target_slot] = self.id
            self.pegs_location[peg_id]= target_slot
        else:
            print("ERROR: Target slot occupied")
            exit(1)

    def move_peg_over_enemy(self,peg_id,target_slot):
        print("Move player %s peg %s over enemy in slot %s" % (self.name, id,target_slot))

        # Clear current location
        if self.pegs_location[peg_id] != None:
            self.slots[self.pegs_location[peg_id]] = None
            self.slots_owner_id[self.pegs_location[peg_id]] = None

        # Move peg over enemy
        if self.slots[target_slot] != None:
            self.slots[target_slot] = peg_id
            self.slots_owner_id[target_slot] = self.id
            self.pegs_location[peg_id]= target_slot
        else:
            print("ERROR: Target slot not occupied")
            exit(1)


    def status(self):
        #print ("Player %s, %s %s %s pegs at %s." % (self.name,self.pegs_in_start,self.pegs_in_game,self.pegs_in_goal,self.pegs_location))

        start=""
        for i in range(0,4):
            if self.slots[i] == None:
                start += ". "
            else:
                start += "{:.>1} ".format(self.slots[i])
        #print("Start : %s" % start)

        goal=""
        for i in range(32,36):
            if self.slots[i] == None:
                goal += ". "
            else:
                goal += "{:.>1} ".format(self.slots[i])
        #print("Goal  : %s" % goal)

        slots=""
        slots_owner_id=""
        for i in range(4,32):
            if self.slots[i] == None:
                slots += ".. "
                slots_owner_id += ".. "
            else:
                slots += "{:.>2} ".format(self.slots[i])
                slots_owner_id += "{:.>2} ".format(self.slots_owner_id[i])

        #print("Slots : %s" % slots)

        print ("P%s T%s D%s %s %s %s" % (self.id, str(self.turn_counter).rjust(4,"0"),self.dice, start, slots, goal ))
        print ("        Owner id     %s" % slots_owner_id)

    def play(self):
        print ("Player %s turn" % self.id)
        self.update_my_slots()


        self.dice = random.randrange(1,7)
        self.turn_counter += 1
        #print("\nTurn: %s Dice: %s " % (self.turn_counter,dice))

        rule_score = {}
        rule_target_slot = {}
        # E = move peg to enter slot
        # M = move peg to empty slot
        # X = eat enemy peg
        # G = move peg to goal
        for r in ['E','M','G','X']:
            for p in range(0,4):
                rule_score["%s%s" % (r,p)] =0
                rule_target_slot["%s%s" % (r,p)] = None

        rule_score['N0'] = 1 # Don't know what to do
        rule_target_slot['N0'] = None

        for id in range(0,4):

            target_slot = self.pegs_location[id] + self.dice
            current_slot = self.pegs_location[id]
            target_slot_owner = self.slots_owner_id[target_slot]

            #print (target_slot)

            # Move peg to enter slot
            if self.dice == 6 \
                and self.slots[self.slot_enter] == None \
                and self.pegs_location[id] < self.slot_enter:

                rule_score["E%s" % id] += 80 + id
                rule_target_slot["E%s" % id] = self.slot_enter
                print ("Player %s peg %s enter game [%s]" % (self.id, id,rule_score["E%s" % id]))

            ## Send enemy peg to start
            #if target_slot < self.slot_goal1 and \
            #    self.slots[target_slot] != None:
            #
            #    if self.slots[target_slot] > 9: # Enemy peg ids are over 9
            #        rule_score["X%s" % id] += 90
            #        rule_target_slot["X%s" % id] = target_slot


            # Move peg X to goal
            if self.pegs_location[id] < self.slot_goal1 \
                and target_slot >= self.slot_goal1 \
                and target_slot <= self.slot_goal2 \
                and self.slots[target_slot] == None:

                rule_score["G%s" % id] += 100 + self.pegs_location[id] # Peg closest to the goal have higher score
                rule_target_slot["G%s" % id] = target_slot
                print ("Player %s peg %s move to goal slot %s [%s]" % (self.id,id, target_slot,rule_score["G%s" % id]))

            # Eat enemy peg
            if self.pegs_location[id] >= self.slot_enter \
                and target_slot < self.slot_goal1:

                if target_slot_owner != None and target_slot_owner != self.id: # Target slot have enemy peg
                    rule_score["X%s" % id] += 90 + self.pegs_location[id]
                    rule_target_slot["X%s" % id] = target_slot
                    print ("Player %s peg %s move to enemy %s slot %s [%s]" % (self.id,id, target_slot_owner,target_slot,rule_score["X%s" % id]))

            # Move peg X
            if self.pegs_location[id] >= self.slot_enter \
                and target_slot < self.slot_goal1:

                if self.slots[target_slot] == None :
                    rule_score["M%s" % id] += self.pegs_location[id] # Peg closest to the goal have higher score

                    if target_slot in self.slot_enter_enemy:
                        print("Player %s peg %s target is enemy enter slot [-10]" %  (self.id,id))
                        rule_score["M%s" % id] -= 10

                    if self.pegs_location[id] == self.slot_enter: # Priorize peg in enter slot
                        print("Player %s peg %s is in enter slot [+50]" %  (self.id,id))
                        rule_score["M%s" % id] += 50

                    if self.pegs_location[id] in self.slot_enter_enemy: # Priorize peg in enemy enter slot
                        print("Player %s peg %s is in enemy enter slot %s [+60]" % (self.id,id, self.pegs_location[id]))
                        rule_score["M%s" % id] += 60

                    rule_target_slot["M%s" % id] = target_slot
                    print ("Player %s peg %s move to %s [%s]" % (self.id,id,target_slot,rule_score["M%s" % id]))


            #print (" Scores: E=%s G=%s M=%s Slots: %s %s %s" % (rule_score["E%s" % id],rule_score["G%s" % id],rule_score["M%s" % id],rule_target_slot["E%s" % id],rule_target_slot["G%s" % id],rule_target_slot["M%s" % id]))

        # Select best rule based on score
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
            self.move_peg_to_goal(peg,target_slot )
        elif action == "X": # Eat enemy peg
            self.move_peg_over_enemy(peg,target_slot )

        self.update_board()



def main():

    log.info("===========================================")
    log.info("START")

    random.seed()

    log.info("Game is runnning.")

    players = [Player(0),Player(1),Player(2),Player(3)]

    print ("Players...")

    for p in players:
        p.status()
    Board.status()

    game_is_running = True
    while game_is_running:

        print ("\n-------------------------")
        for current_player in players:
            current_player.play()
            #for other_player in players:
            #    if other_player!=current_player:
            #        other_player.set_enemy_pegs_location(current_player.id, current_player.pegs_location)

            current_player.status()
            #Board.status()

            if current_player.status_winner:
                print ("Winner is %s" % current_player.id)
                game_is_running = False
                return

        Board.status()
        Board.draw()
        key = input("PRESS ENTER TO CONTINUE")

    print("End of the game")

    log.info("DONE")


if __name__ == "__main__":
    main()
