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

solvingTime = []
solutions = []
feasibles = []

for N in range(10,101):
    print(N)
    
    t = time.clock()
    csp = CSP(N)
    for k in range(N):
        csp.setDomain(k,range(N))
        
    for x in range(N):
        for y in range(N):
            if x != y:
                csp.addComprehensiveConstraint(x,y,queenDiff)
    
    
    print("Model loading : " + str(time.clock()-t))
    
    t = time.clock()
    
    #ArcConsistency(csp)
    
    #print("Arc consistency : " + str(time.clock()-t))
    
    t = time.clock()
    
    backtrack = Backtrack(csp,verbosity=3,displayFreq=10,processingMethod=ForwardCheckingMethod,dynamicVarSort=smallestDomain,rankFunc=infeasibilityRank)
    solution = backtrack.instanciation
    feasible = backtrack.feasible
    
    print("Backtracking : " + str(time.clock()-t))
    
    solutions += [solution]
    solvingTime += [time.clock()-t]
    feasibles += [feasible]
    