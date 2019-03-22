# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 01:16:27 2019

@author: Victor
"""

from csp import *
from brancher import *
from heuristics import *
from preprocessing import *
from backtrack import *

import time

# Model definition
def diff(x,y,a,b):
    return a != b
    
# Classe pour trouver une N-coloration
class ColorationModel:
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
def findMinColor(nbNodes, edges,timeLimit=100000,init=None,Nmin=1,Nmax=-1):
    N = Nmin
    
    model = ColorationModel(nbNodes, edges)    
    
    while True:
        print("N : " + str(N))
        model.setNbColors(N)
        
        t = time.clock()
        
        ArcConsistency(model.csp)
        
        print("Arc consistency : " + str(time.clock()-t))
        
        t = time.clock()
        
        backtrack = Backtrack(model.csp,displayFreq=5000,rankFuncs=[domainRank,impactRank],brancherType=ArrayBrancher,processingMethod=ForwardCheckingMethod,initialization=init,timeLimit=timeLimit)
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
    