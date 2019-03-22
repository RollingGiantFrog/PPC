# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 10:45:49 2019

@author: Victor
"""

from csp import *
from heuristics import *
from preprocessing import *
from backtrack import *

import time

import matplotlib.pyplot as plt

# Model definition
def queenDiff(x,y,a,b):
    return a != b and abs(x-y) != abs(a-b)

def printSolution(sol):
    for i in range(N):
        s = ""
        for j in range(N):
            if solution[i] != j:
                s += "o "
            else:
                s += "+ "
        print(s)

tests = []
solvingTime = []
solutions = []
feasibles = []

for N in range(10,151):
    print(N)
    
    t = time.clock()
    csp = CSP(N)
    for k in range(N):
        csp.setDomain(k,range(N))
        
    for x in range(N):
        for y in range(N):
            if x != y:
                csp.addComprehensiveConstraint(x,y,queenDiff)
    
    feasible = False
    i = 0
    timeLimit = 1.

    while not feasible:
        backtrack = Backtrack(csp,verbosity=0,displayFreq=10,processingMethod=ForwardCheckingMethod,useArcConsistency=False,rankFuncs=[domainRank,randomRank],timeLimit=timeLimit)
        solution = backtrack.instanciation
        feasible = backtrack.feasible
    
    solutions += [solution]
    tests += [N]
    solvingTime += [time.clock()-t]
    feasibles += [feasible]
    
plt.figure(1)
plt.plot(tests,solvingTime,'r*')