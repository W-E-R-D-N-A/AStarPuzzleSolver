#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 30 01:17 2023

@author: Samuel Smallman
CSCI-4350-001
Middle Tennessee State University
8-Puzzle Board Generator

Portions based on Python code provided by
Scott P. Morton & Joshua L. Phillips
"""

import sys, copy, numpy.random as random

#Checks if 3 arguments given
if (len(sys.argv) != 3):
    print()
    print("Usage: %s [seed] [number of random moves]" %(sys.argv[0]))
    print()
    sys.exit(1)

#Class represents board state
class state():
    def __init__(self,inputs): #Alternative constructor uses our 2D array of txt input file for initial state
        self.xpos = 0
        self.ypos = 0
        self.tiles = inputs #[[0,1,2],[3,4,5],[6,7,8]]
    def left(self):
        if (self.ypos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos-1]
        s.ypos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def right(self):
        if (self.ypos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos+1]
        s.ypos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def up(self):
        if (self.xpos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos-1][s.ypos]
        s.xpos -= 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def down(self):
        if (self.xpos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos+1][s.ypos]
        s.xpos += 1
        s.tiles[s.xpos][s.ypos] = 0
        return s
    def __hash__(self):
        return (tuple(self.tiles[0]),tuple(self.tiles[1]),tuple(self.tiles[2]))
    def __str__(self):
        return '%d %d %d\n%d %d %d\n%d %d %d\n'%(
                self.tiles[0][0],self.tiles[0][1],self.tiles[0][2],
                self.tiles[1][0],self.tiles[1][1],self.tiles[1][2],
                self.tiles[2][0],self.tiles[2][1],self.tiles[2][2])
    def copy(self):
        s = copy.deepcopy(self)
        return s

# There is no error checking in this code
# Well formatted input is assumed as well as
# proper processing given well-formed input

def main():
    inputs = []
    inputs = [line.split() for line in sys.stdin]

    #print(inputs)
    s = state(inputs)
    #print(s.tiles)

    # Just once
    rng = random.default_rng(int(sys.argv[1]))
    number_of_moves = int(sys.argv[2])
    
    # Can call this as many times as needed to generate moves...
    for x in range(number_of_moves):
        # These moves will be 0,1,2,3 which can each be
        # associated with a particular movement direction
        # (i.e. up, down, left, right).
        move = rng.integers(4) 
        #print(move)
        if move == 0:
            if s.up() is not None:
                s = s.up()
                #print("up")
        elif move == 1:
            if s.down() is not None:
                s = s.down()
                #print("down")
        elif move == 2:
            if s.left() is not None:
                s = s.left()
                #print("left")
        elif move == 3:
            if s.right() is not None:
                s = s.right()
                #print("right")
        else:
            pass
    for i in range(3):
       print(s.tiles[i][0],s.tiles[i][1],s.tiles[i][2]) #print resulting shuffled board
        
main()