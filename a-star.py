#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 31 05:06 2023

@author: Samuel Smallman
CSCI-4350-001
Middle Tennessee State University
A* 8-Puzzle Board Solver

Portions based on Python code provided by
Scott P. Morton & Joshua L. Phillips
Saturn Cloud Tutorial (Manhattan Distance function)
https://saturncloud.io/blog/solving-the-8-puzzle-with-a-algorithm/
"""

import heapq, copy, sys

#Checks if arguments given
if (len(sys.argv) != 2):
    print()
    print("Usage: %s [heuristic]" %(sys.argv[0]))
    print()
    sys.exit(1)

class Set(): #Set used for Closed List
    def __init__(self):
        self.thisSet = set()
    def add(self,entry):
        if entry is not None:
            self.thisSet.add(entry.__hash__())
    def length(self):
        return len(self.thisSet)
    def isMember(self,query):
        return query.__hash__() in self.thisSet

#Class represents board state
class state():
    def __init__(self,inputs,xpos,ypos): #Alternative constructor uses our 2D array of txt input file for initial state
        self.xpos = xpos
        self.ypos = ypos
        self.tiles = inputs #Ex: [[0,1,2],[3,4,5],[6,7,8]]
    def left(self):
        if (self.ypos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos-1]
        s.ypos -= 1
        s.tiles[s.xpos][s.ypos] = '0'
        return s
    def right(self):
        if (self.ypos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos][s.ypos+1]
        s.ypos += 1
        s.tiles[s.xpos][s.ypos] = '0'
        return s
    def up(self):
        if (self.xpos == 0):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos-1][s.ypos]
        s.xpos -= 1
        s.tiles[s.xpos][s.ypos] = '0'
        return s
    def down(self):
        if (self.xpos == 2):
            return None
        s = self.copy()
        s.tiles[s.xpos][s.ypos] = s.tiles[s.xpos+1][s.ypos]
        s.xpos += 1
        s.tiles[s.xpos][s.ypos] = '0'
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

class PriorityQueue(): #Used for Frontier/Open List
    def __init__(self):
        self.thisQueue = []
    def push(self, thisNode):
        heapq.heappush(self.thisQueue, (thisNode.val, -thisNode.id, thisNode))
    def pop(self):
        return heapq.heappop(self.thisQueue)[2]
    def isEmpty(self):
        return len(self.thisQueue) == 0
    def length(self):
        return len(self.thisQueue)

nodeid = 0
class node(): #Class used for  tree nodes representation
    def __init__(self,gval,hval,state,parent):
        global nodeid
        self.id = nodeid
        nodeid += 1
        fval = gval + hval
        self.val = fval
        self.gval = gval
        self.hval = hval
        self.state = state
        self.parent = parent #holds parent node
        #self.path = path #path to node
    def __str__(self):
        return 'Node: id=%d val=%d'%(self.id,self.val)

#Heuristic functions

def displacement(inputs,goals): #h(n) = Number of tiles displaced from the goal
    distance = 0
    for i in range(3):
        for j in range(3):
            if inputs[i][j] != goals[i][j]:
                distance += 1
    return distance
    
def manhattan(inputs):  #h(n) = Sum of Manhattan (city-block) distances of all tiles from the goal
    distance = 0
    for i in range(3):
        for j in range(3):
            if inputs[i][j] != 0:
                row = (int(inputs[i][j]) - 1) // 3
                column = (int(inputs[i][j]) - 1) % 3
                distance += abs(row - i) + abs(column - j)
    return distance

def heuristic(inputs,goals): #function to select heuristic from given argument
    h = int(sys.argv[1]) #hold argument for heuristic ID
    if h == 1:
        return displacement(inputs,goals)
    elif h == 2:
        return manhattan(inputs)
    elif h == 3: # h(n) = manhattan distance and tile displacement average
        return (manhattan(inputs) + displacement(inputs,goals)) / 2
    else: # h(n) = 0
        return 0 

def get_path(cur_node): #Function to get a path list to print
    path = []
    while cur_node is not None:
        #print(cur_node.state)
        path += [cur_node.state.tiles]
        cur_node =  cur_node.parent
    path = path[::-1] #invert list to explored order
    return path
        
# There is no error checking in this code
# Well formatted input is assumed as well as
# proper processing given well-formed input

def main():
    goals = [['0','1','2'],['3','4','5'],['6','7','8']] #8-puzzle "win" state
    inputs = [] #inputs will hold initial state of puzzle
    inputs = [line.split() for line in sys.stdin]
    for i in range(3):
        for j in range(3):
            if inputs[i][j] == '0':
                xpos = i
                ypos = j
                break
    #A* Algorithm
    childless_node_count = 0
    s = state(inputs,xpos,ypos)
    closed_list = Set()
    frontier = PriorityQueue()
    frontier.push(node(0,heuristic(s.tiles,goals),s,None))
    while not frontier.isEmpty():
        #Set up current node for inspection
        cur_node = frontier.pop()
        gval = cur_node.gval
        s = cur_node.state
        #print(s.tiles)
        #print("hval is ",cur_node.hval)
        if s.tiles == goals: #solution found if current node is same as goal state! otherwise expand node.
            path = get_path(cur_node)
            print("V=",closed_list.length(),sep='') #Print V statistic
            N = closed_list.length() + frontier.length()
            print("N=",N,sep='') #Print N statistic
            print("d=",len(path),sep='') #Print d (depth of solution)
            print("b=",(closed_list.length() + frontier.length())** (1.0/len(path)),sep='') #N^(1/d) = b (branching factor)
            #print("b=",(N-1) / childless_node_count,sep='') #(N-1)/no child nodes = b (branching factor)
            print(" ")
            for h in range(len(path)): #Print taken solution path
                for i in range(3):
                    print(path[h][i][0],path[h][i][1],path[h][i][2]) #print states of the board
                print(" ")   
            break
        else:
            closed_list.add(cur_node.state) #add current node to closed list
            #print(closed_list.length())
            child_check = 0
            su = s.up()
            #Make sure move is possible and state not on closed list for each, then add expansions to frontier
            if not closed_list.isMember(su) and s.up() is not None: 
                child_check = 1
                frontier.push(node(gval + 1,heuristic(su.tiles,goals),su,cur_node))
            sd = s.down()
            if not closed_list.isMember(sd) and s.down() is not None:
                child_check = 1
                frontier.push(node(gval + 1,heuristic(sd.tiles,goals),sd,cur_node))
            sl = s.left()
            if not closed_list.isMember(sl) and s.left() is not None:
                child_check = 1
                frontier.push(node(gval + 1,heuristic(sl.tiles,goals),sl,cur_node))
            sr = s.right()
            if not closed_list.isMember(sr) and s.right() is not None:
                child_check = 1
                frontier.push(node(gval + 1,heuristic(sr.tiles,goals),sr,cur_node))
            if child_check == 0:
                childless_node_count += 1
                


main()