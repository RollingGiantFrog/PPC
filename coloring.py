# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 10:45:49 2019

@author: Victor
"""

from csp import *
from brancher import *
from heuristics import *
from preprocessing import *
from backtrack import *
from cliqueFinder import *

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
    
# Classe pour trouver une N-coloration
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


# Détecte la plus petite couleur pour un graphe donné
def findMinColor(model,timeLimit=100000,N=1,Nmin=1,Nmax=-1):
    Nmin = 1
    Nmax = -1
    
    while True:
        print("N : " + str(N))
        model.setNbColors(N)
        
        t = time.clock()
        
        ArcConsistency(model.csp)
        
        print("Arc consistency : " + str(time.clock()-t))
        
        t = time.clock()
        
        backtrack = Backtrack(model.csp,displayFreq=5000,rankFuncs=[domainRank,impactRank,infeasibilityRank],brancherType=ArrayBrancher,processingMethod=ForwardCheckingMethod,initialization=init,timeLimit=timeLimit)
        solution = backtrack.instanciation
        feasible = backtrack.feasible
        print(model.csp.test(solution))
        
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
        
    return backtrack,Nmin,Nmax
    
# Optimization loop

#filename = "./instances/le450_5d.col"
filename = "./instances/miles500.col"

filenames = ["./instances/fpsol2.i.1.col","./instances/fpsol2.i.2.col","./instances/fpsol2.i.3.col","./instances/anna.col","./instances/david.col","./instances/miles250.col","./instances/miles500.col","./instances/miles750.col","./instances/miles1000.col","./instances/games120.col","./instances/myciel3.col","./instances/myciel4.col","./instances/le450_5a.col","./instances/le450_5b.col","./instances/le450_5c.col","./instances/le450_5d.col","./instances/le450_25a.col","./instances/le450_25b.col","./instances/le450_25c.col","./instances/le450_25d.col"]
results = []
#for file in filenames:
#    ti = time.clock()
    
nbNodes, edges = readInstance(filename)
model = ColoringModel(nbNodes,edges)

deg = [0 for k in range(nbNodes)]
edgeSet = set()
for u,v in edges:
    deg[u] += 1
    deg[v] += 1
    edgeSet.add((u,v))
    edgeSet.add((v,u))
    
nodes = [(deg[u],u) for u in range(nbNodes)]
nodes.sort(reverse=True)
initOrder = [u for d,u in nodes]
init = [1] + [None for u in range(nbNodes-1)]

clique,Kmin,Kmax = findMaxClique(nbNodes,edgeSet,20)

init = [None for u in range(nbNodes)]
for k in range(len(clique)):
    init[clique[k]] = k
    
#backtrack,Nmin,Nmax = findMinColor(model,60,len(clique),len(clique))
    
#    results += [(file,time.clock()-ti,Nmin,Nmax)]
    

model.setNbColors(8)
backtrack = Backtrack(model.csp,displayFreq=5000,rankFuncs=[domainRank,impactRank, infeasibilityRank],useArcConsistency=False,brancherType=SortBrancher,processingMethod=ForwardCheckingMethod,initialization=init)
solution = backtrack.instanciation
feasible = backtrack.feasible
unfinished = backtrack.unfinished
