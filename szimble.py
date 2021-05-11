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
        #print("Init player: %s" % player_name)
        self.name = player_name
        # Slot index 0..35
        self.turn_counter = 0
        self.dice = 0
        self.pegs_location = [0, 1, 2, 3] # All pegs in start
        self.enemy_pegs_location = {1: [None,None,None,None], 2: [None,None,None,None],3: [None,None,None,None]}
        self.pegs_in_start = 4
        self.pegs_in_game = 0
        self.pegs_in_goal = 0
        self.slots_start = [0,1,2,3]
        self.slot_enter = 4
        self.slot_enter_enemy = [11,18,25]
        self.slot_goal1 = 32
        self.slot_goal2 = 35
        self.slots =  [None for x in range(0,36)]
        self.status_winner = False

        # All pegs in start
        self.slots[0] = 0
        self.slots[1] = 1
        self.slots[2] = 2
        self.slots[3] = 3

    def set_enemy_pegs_location(self, id,pegs_location):
        #print (id, pegs_location)

        for i in range(self.slot_enter, self.slot_goal1):
            if self.slots[i]!=None:
                p = self.slots[i] % 10
                if p == id:
                    self.slots[i] = None


        for p in range (0,4):
            if pegs_location[p] and  pegs_location[p] >=4 :
                s =  pegs_location[p] + id * 7

                s = (s-4) % 28 + 4

                self.slots[s] = id*10 + p

                #print ("id %s enemy slot %s --> %s"  % (id, pegs_location[p],s))

                #if s == pegs_location[0]:
                #

        #print (self.slots)
        #self.enemy_pegs_location =


    def move_peg_to_start(self,id):
        #print("Move player %s peg %s to start" % (self.name, id))

        self.pegs_in_start += 1
        self.pegs_in_game -= 1

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

    def move_peg_to_game(self,id):
        #print("Move player %s peg %s to game" % (self.name, id))

        self.pegs_in_start -= 1
        self.pegs_in_game += 1

        # Clear current location
        if self.pegs_location[id] != None:
            self.slots[self.pegs_location[id]] = None

        # Move peg to enter slot
        if self.slots[self.slot_enter] == None:
            self.slots[self.slot_enter] = id
            self.pegs_location[id]= self.slot_enter
        else:
            print("ERROR: Enter slot occupied")
            exit(1)


    def move_peg_to_goal(self,id,target_slot):
        #print("Move player %s peg %s to goal slot %s" % (self.name, id,target_slot))

        self.pegs_in_goal += 1
        self.pegs_in_game -= 1

        # Clear current location
        if self.pegs_location[id] != None:
            self.slots[self.pegs_location[id]] = None

        # Move peg to new slot
        if self.slots[target_slot] == None:
            self.slots[target_slot] = id
            self.pegs_location[id]= target_slot
        else:
            print("ERROR: Target slot occupied")
            exit(1)

        if self.pegs_in_goal == 4: # We are a winner!
            self.status_winner = True


    def move_peg_to_slot(self,id,target_slot):
        #print("Move player %s peg %s to slot %s" % (self.name, id,target_slot))

        # Clear current location
        if self.pegs_location[id] != None:
            self.slots[self.pegs_location[id]] = None

        # Move peg to new slot
        if self.slots[target_slot] == None:
            self.slots[target_slot] = id
            self.pegs_location[id]= target_slot
        else:
            print("ERROR: Target slot occupied")
            exit(1)

    def move_peg_over_enemy(self,id,target_slot):
        #print("Move player %s peg %s over enemy in slot %s" % (self.name, id,target_slot))

        # Clear current location
        if self.pegs_location[id] != None:
            self.slots[self.pegs_location[id]] = None

        # Move peg over enemy
        if self.slots[target_slot] != None:
            self.slots[target_slot] = id
            self.pegs_location[id]= target_slot
        else:
            print("ERROR: Target slot occupied")
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
        for i in range(4,32):
            if self.slots[i] == None:
                slots += ".. "
            else:
                slots += "{:.>2} ".format(self.slots[i])
        #print("Slots : %s" % slots)

        print ("%s T%s D%s %s %s %s" % (self.name.ljust(7," "), str(self.turn_counter).rjust(4,"0"),self.dice, start, slots, goal ))

    def play(self):
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
            #print (target_slot)

            # Move peg to enter slot
            if self.dice == 6 \
                and self.slots[self.slot_enter] == None \
                and self.pegs_location[id] < self.slot_enter:

                rule_score["E%s" % id] += 80 + id
                rule_target_slot["E%s" % id] = self.slot_enter
                print ("%s peg %s enter game [%s]" % (self.name, id,rule_score["E%s" % id]))

            # Send enemy peg to start
            if target_slot < self.slot_goal1 and \
                self.slots[target_slot] != None:

                if self.slots[target_slot] > 9: # Enemy peg ids are over 9
                    rule_score["X%s" % id] += 90
                    rule_target_slot["X%s" % id] = target_slot
                    print ("%s peg %s eat enemy peg from %s [%s]" % (self.name,id,target_slot, rule_score["X%s" % id]))

            # Move peg X to goal
            if self.pegs_location[id] < self.slot_goal1 \
                and target_slot >= self.slot_goal1 \
                and target_slot <= self.slot_goal2 \
                and self.slots[target_slot] == None:

                rule_score["G%s" % id] += 100 + self.pegs_location[id] # Peg closest to the goal have higher score
                rule_target_slot["G%s" % id] = target_slot
                print ("%s peg %s move to goal slot %s [%s]" % (self.name,id, target_slot,rule_score["G%s" % id]))

            # Move peg X
            if self.pegs_location[id] >= self.slot_enter \
                and target_slot < self.slot_goal1:

                if self.slots[target_slot] == None :
                    rule_score["M%s" % id] += self.pegs_location[id] # Peg closest to the goal have higher score

                    if target_slot in self.slot_enter_enemy:
                        print("%s peg %s target is enemy enter slot [-10]" %  (self.name,id))
                        rule_score["M%s" % id] -= 10

                    if self.pegs_location[id] == self.slot_enter: # Priorize peg in enter slot
                        print("%s peg %s is in enter slot [+50]" %  (self.name,id))
                        rule_score["M%s" % id] += 50

                    if self.pegs_location[id] in self.slot_enter_enemy: # Priorize peg in enemy enter slot
                        print("%s peg %s is in enemy enter slot %s [+60]" % (self.name,id, self.pegs_location[id]))
                        rule_score["M%s" % id] += 60

                    rule_target_slot["M%s" % id] = target_slot
                    print ("%s peg %s move to %s [%s]" % (self.name,id,target_slot,rule_score["M%s" % id]))


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





def main():

    log.info("===========================================")
    log.info("START")

    random.seed()

    log.info("Game is runnning.")

    players = [Player("Red"),Player("Yellow")]

    for p in players:
        p.set_enemy_pegs_location(1,[0,1,2,3])
        p.set_enemy_pegs_location(2,[0,1,2,3])
        p.set_enemy_pegs_location(3,[0,1,2,3])

    for p in players:
        p.status()

    game_is_running = True
    while game_is_running:
        print ("\n-------------------------")
        p_count=0
        for p in players:
            p.play()
            p.status()
            for o in players:
                if o==p:
                    print (p,o)
            p_count += 1

            if p.status_winner:
                game_is_running = False

    print("End of the game")

    log.info("DONE")


if __name__ == "__main__":
    main()
