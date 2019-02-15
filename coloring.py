# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 10:45:49 2019

@author: Victor
"""

from csp import *
from heuristics import *
from preprocessing import *
from backtrack import *

import io
import time

# Model definition
def diff(x,y,a,b):
    return a != b

filename = "./instances/le450_5d.col"
#filename = "./instances/queen9_9.col"

t = time.clock()

found = False
N = 1
Nmin = 1
Nmax = -1
while not found:
    print("N : " + str(N))
#    possibleCouples = []
#    for i in range(N):
#        for j in range(N):
#            if i != j:
#                possibleCouples += [(i,j)]
    possibleCouples = diff    
    
    with io.open(filename) as f:
        lines = f.readlines()
        for line in lines:
            L = line.split(" ")
            if L[0] == 'e':
                
                csp.addComprehensiveConstraint(int(L[1])-1,int(L[2])-1,possibleCouples)            
                
            elif L[0] == 'p':
                n = int(L[2])
                csp = CSP(n)
                for k in range(n):
                    csp.setDomain(k,range(N))
            
    
    print("Model loading : " + str(time.clock()-t))
    
    t = time.clock()
    
    ArcConsistency(csp)
    
    print("Arc consistency : " + str(time.clock()-t))
    
    t = time.clock()
    
    backtrack = Backtrack(csp,timeLimit=10,processingMethod=ArcConsistencyMethod)
    solution = backtrack.instanciation
    feasible = backtrack.feasible
    
    print("Backtracking : " + str(time.clock()-t))
    
    if feasible:
        Nmax = N
        oldN = N
        N = (Nmax+Nmin)//2
        if oldN == N:
            break
        
    else:
        Nmin = N+1
        if Nmax == -1:
            N = 2*N
        else:
            oldN = N
            N = (Nmax+Nmin)//2
            if oldN == N:
                break
    
