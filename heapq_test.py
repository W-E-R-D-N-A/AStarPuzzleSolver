#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 20:26:15 2019

@author: Joshua L. Phillips
Department of Computer Science
Middle Tennessee State University
Illustration of heapq and operator overloading

Portions based on Python code provided by
Scott P. Morton
Center for Computational Science
Middle Tennessee State University
"""

import heapq

class PriorityQueue():
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
class node():
    def __init__(self,val):
        global nodeid
        self.id = nodeid
        nodeid += 1
        self.val = val
    def __str__(self):
        return 'Node: id=%d val=%d'%(self.id,self.val)


def main():
    
    node1 = node(5)
    node2 = node(3)
    node3 = node(6)
    node4 = node(4)
    node5 = node(3)

    print("All Nodes")
    print(node1)
    print(node2)
    print(node3)
    print(node4)
    print(node5)
    print()

    myqueue = PriorityQueue()
    myqueue.push(node1)
    myqueue.push(node2)
    myqueue.push(node3)
    myqueue.push(node4)
    myqueue.push(node5)

    print("Traversing the PQ (for debugging ONLY!)")
    for x in range(myqueue.length()):
        print(myqueue.thisQueue[x][2])
    print()
    
    print("Popping Nodes Off")
    while not myqueue.isEmpty():
        print(myqueue.pop())
    print()
    
main()
