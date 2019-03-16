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
filename = "./instances/myciel5.col"

nbNodes, edges = readInstance(filename)
model = ColoringModel(nbNodes,edges)

deg = [0 for k in range(nbNodes)]
edge = set()
for u,v in edges:
    deg[u] += 1
    deg[v] += 1
    edge.add((u,v))
    edge.add((v,u))
    
nodes = [(deg[u],u) for u in range(nbNodes)]
nodes.sort(reverse=True)
initOrder = [u for d,u in nodes]
init = [1] + [None for u in range(nbNodes-1)]


class CliqueFinder:
    def findClique(self,depth):    
        if depth == self.k:
            return True
            
        found = False
        if depth == 0:
            k = 0
        else:
            k = self.clique[depth-1] + 1
        
        while k < self.nbNodes and not found:
            validNode = True
            for i in range(depth):
                validNode = validNode and (self.nodes[self.clique[i]],self.nodes[k]) in self.edges
                
            if validNode:
                self.clique[depth] = k
                found = self.findClique(depth+1)
                
            k += 1
            
        
        return found
        
    def __init__(self,nbNodes,edgeSet,k):
        self.n = nbNodes
        
        deg = [0 for u in range(self.n)]
        for u,v in edges:
            deg[u] += 1
            deg[v] += 1
            
        self.nodes = [u for u in range(self.n) if deg[u] >= k-1]
        self.nbNodes = len(self.nodes)
        
        self.edges = edgeSet
        self.k = k
        self.clique = [None for i in range(k)]
        self.foundClique = self.findClique(0)
        
        if self.foundClique:
            self.clique = [self.nodes[i] for i in self.clique]
        

#Kmin = 2
#Kmax = -1
#K = Kmin
#while True:
#    print("K : " + str(K))
#    t = time.clock()
#    
#    cf = CliqueFinder(nbNodes,edge,K)
#    solution = cf.clique
#    feasible = cf.foundClique
#    
#    print("Clique : " + str(time.clock()-t))
#    if feasible:
#        print("Clique found.")
#    else:
#        print("Clique not found.")
#    
#    if feasible:
#        Kmin = K
#        if Kmax == -1:
#            K = 2*K
#        else:
#            oldK = K
#            K = (Kmax+Kmin+1)//2
#            if oldK == K:
#                break
#        
#    else:
#        Kmax = K-1
#        if Kmin == -1:
#            K = K//2
#        else:
#            oldK = K
#            K = (Kmax+Kmin+1)//2
#            if oldK == K:
#                break
#    
#    print("")
#        
#print("")
#print("Kmin = " + str(Kmin))
#print("Kmax = " + str(Kmax))


init = [None for u in range(nbNodes)]
#for k in range(len(cf.clique)):
#    init[cf.clique[k]] = k


N = 5
#Nmin = K
Nmin = 1
Nmax = -1

while True:
    print("N : " + str(N))
    model.setNbColors(N)
    
    t = time.clock()
    
    ArcConsistency(model.csp)
    
    print("Arc consistency : " + str(time.clock()-t))
    
    t = time.clock()
    
    backtrack = Backtrack(model.csp,displayFreq=5000,processingMethod=ForwardCheckingMethod,timeLimit=20)#,initialOrder=initOrder,initialVarSort=None,dynamicVarSort=None)
    solution = backtrack.instanciation
    feasible = backtrack.feasible
    print(model.csp.test(solution))
    print(backtrack.infeasibleVariables)
    
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