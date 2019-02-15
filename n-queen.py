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

t = time.clock()

N = 101
csp = CSP(N)
for k in range(N):
    csp.setDomain(k,range(N))
    
for x in range(N):
    for y in range(N):
        if x != y:
#            C = []
#            for i in range(N):
#                for j in range(N):
#                    if i != j and abs(x-y) != abs(i-j):
#                        C += [(i,j)]
#                        
#            csp.addConstraint(x,y,C)
            csp.addComprehensiveConstraint(x,y,queenDiff)


print("Model loading : " + str(time.clock()-t))

t = time.clock()

#ArcConsistency(csp)

print("Arc consistency : " + str(time.clock()-t))

t = time.clock()

backtrack = Backtrack(csp)
solution = backtrack.instanciation
feasible = backtrack.feasible

print("Backtracking : " + str(time.clock()-t))
    

if feasible:
    print(solution)
#    for i in range(N):
#        s = ""
#        for j in range(N):
#            if solution[i] != j:
#                s += "o "
#            else:
#                s += "+ "
#        print(s)