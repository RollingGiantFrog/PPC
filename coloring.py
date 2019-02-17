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

# Model reading
def readInstance(filename):
    nbNodes = 0
    edges = []
    with io.open(filename) as f:
        lines = f.readlines()
        for line in lines:
            L = line.split(" ")
            if L[0] == 'e':
                edges += [(int(L[1])-1,int(L[2])-1)]
                
            elif L[0] == 'p':
                nbNodes = int(L[2])
                
    return nbNodes, edges
            

# Model definition
def diff(x,y,a,b):
    return a != b
    
class ColoringModel:
    def __init__(self, nbNodes, edges, N = None):
        self.nbNodes = nbNodes
        self.edges = edges[:]
        self.nbColors = N
        
        self.csp = CSP(self.nbNodes)        
        
        if self.nbColors != None:
            for k in range(self.nbNodes):
                self.csp.setDomain(k,range(self.nbColors))
            
        for u,v in self.edges:
            self.csp.addComprehensiveConstraint(u,v,diff)
            
    def setNbColors(self, N):
        self.nbColors = N
        for k in range(self.nbNodes):
            self.csp.setDomain(k,range(self.nbColors))


# Optimization loop

filename = "./instances/le450_5d.col"
#filename = "./instances/latin_square_10.col"

nbNodes, edges = readInstance(filename)
model = ColoringModel(nbNodes,edges)

deg = [0 for k in range(nbNodes)]
for u,v in edges:
    deg[u] += 1
    deg[v] += 1
nodes = [(deg[u],u) for u in range(nbNodes)]
nodes.sort()
initOrder = [u for d,u in nodes]
init = [1] + [None for u in range(nbNodes-1)]

N = 1
Nmin = 1
Nmax = -1

while True:
    print("N : " + str(N))
    model.setNbColors(N)
    
    t = time.clock()
    
#    ArcConsistency(model.csp)
    
    print("Arc consistency : " + str(time.clock()-t))
    
    t = time.clock()
    
    backtrack = Backtrack(model.csp,processingMethod=ForwardCheckingMethod)#,initialOrder=initOrder,initialVarSort=None,dynamicVarSort=None)
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
    
    print("")
    
print("Nmin = " + str(Nmin))
print("Nmax = " + str(Nmax))