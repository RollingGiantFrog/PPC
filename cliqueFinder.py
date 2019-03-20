# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 10:17:15 2019

@author: Victor
"""

import time

# Classe pour trouver une clique de taille k
class CliqueFinder:
    def findClique(self,depth):   
        if depth == self.k:
            return True
        
        if time.clock()-self.initTime >= self.timeLimit:
            return False
        
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
        
    def __init__(self,nbNodes,edges,k,timeLimit=10000):
        self.timeLimit = timeLimit
        self.initTime = time.clock()        
        
        self.n = nbNodes
        
        deg = [0 for u in range(self.n)]
        for u,v in edges:
            deg[u] += 1
            deg[v] += 1
            
        self.nodes = [u for u in range(self.n) if deg[u] >= k-1]
        self.nbNodes = len(self.nodes)
        
        self.edges = edges
        self.k = k
        self.clique = [None for i in range(k)]
        self.foundClique = self.findClique(0)
        
        if self.foundClique:
            self.clique = [self.nodes[i] for i in self.clique]
        

# Détecte la plus grande clique pour un graphe donné
def findMaxClique(nbNodes,edges,timeLimit=10000):
    Kmin = 2
    Kmax = -1
    K = Kmin
    while True:
        print("K : " + str(K))
        cf = CliqueFinder(nbNodes,edges,K,timeLimit)
        solution = cf.clique
        feasible = cf.foundClique
        
        if feasible:
            print("Clique found.")
        else:
            print("Clique not found.")
        
        if feasible:
            Kmin = K
            if Kmax == -1:
                K = 2*K
            else:
                oldK = K
                K = (Kmax+Kmin+1)//2
                if oldK == K:
                    break
            
        else:
            Kmax = K-1
            if Kmin == -1:
                K = K//2
            else:
                oldK = K
                K = (Kmax+Kmin+1)//2
                if oldK == K:
                    break
        
        print("")
            
    print("")
    
    return solution,Kmin,Kmax