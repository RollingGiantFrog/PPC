# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 17:09:34 2019

@author: Victor
"""

import time
import preprocessing
import heuristics

def forwardChecking(csp, x, I):
    Q = {}
    
    if x in csp.constraints2D:
        for c in csp.constraints2D[x]:
            v1 = I[c.x1]
            v2 = I[c.x2]
            a = I[x]
            
            if (c.x1 == x and v2 == None):
                y = c.x2
                if not y in Q:
                    Q[y] = []
                for b in csp.getDomain(y):
                    if not c.hasCouple(a,b):
                        Q[y] += [b]
                    
            elif (c.x2 == x and v1 == None):
                y = c.x1
                if not y in Q:
                    Q[y] = []
                for b in csp.getDomain(y):
                    if not c.hasCouple(b,a):
                        Q[y] += [b]
            
            else:
                continue
            
            for b in Q[y]:
                if csp.domain[y].hasValue(b):
                    csp.domain[y].removeValue(b)
                    
            if csp.domainSize(y) == 0:
                return False, Q
    
    return True, Q
            
def cancelForwardChecking(csp, Q):
    for var in Q.keys():
        for val in Q[var]:
            csp.domain[var].addValue(val)            
                
class Backtrack:
    # verbosity = 1 : affiche tout
    # verbosity = 0 : n'affiche rien
    def printStats(self,verbosity):
        if verbosity > 1:
            print("Explored nodes : " + str(self.calls))
            print("Explored : " + str(self.explored))
            print("Nodes open : " + str(self.nodes))
            print("Time spent in Forward Checking : " + str(self.timeForwardChecking))
            print("Time spent in cancelling Forward Checking : " + str(self.timeCancellingForwardChecking))
            print("Time spent in variable branching selection : " + str(self.timeOrder))
            print("Time spent in constraint checking : " + str(self.timeConstraintChecking))
            print("Time spent overall : " + str(self.endTime-self.initTime))
            print("")
    
    
    # n est la taille de l'instanciation partielle
    # x est la dernière variable ajoutée
    # p est le pourcentage que ce noeud représente de l'arbre
    def backtrack(self, n, x, p):
        
        # Gestion des stats
        self.endTime = time.clock()
        self.calls += 1
        if self.calls % self.displayFreq == 0:
            self.printStats(self.verbosity)
            
        if self.endTime-self.initTime > self.timeLimit:
            return False
        
        t = time.clock()
        
        # Vérification des contraintes
        if x in self.csp.constraints2D:
            for c in self.csp.constraints2D[x]:
                v1 = self.instanciation[c.x1]
                v2 = self.instanciation[c.x2]
                
                # x est l'une des deux variables de la contrainte
                # et les deux variables sont instanciées
                if (c.x1 != x and c.x2 != x) or (v1 == None or v2 == None):
                    continue
                
                else:
                    # Le couple de valeurs est admissible pour la contrainte c
                    if not c.hasCouple(v1,v2):
                        self.explored += p
                        return False
        
        self.timeConstraintChecking += time.clock()-t
        
        # Test de la complétude de l'instanciation
        if n == self.csp.size:
            return True
            
        # Instanciation d'une nouvelle variable
        y = self.variableOrder[n]
        domainY = self.csp.getDomain(y)
        
        ny = len(domainY)
        if ny > 0:
            py = p/ny
        self.nodes += ny
        
        for v in domainY:
            self.instanciation[y] = v
            
            t = time.clock()
            
            # Preprocessing avec la nouvelle instanciation
            P = self.processingMethod(self.csp,y,self.instanciation)
            
            self.timeForwardChecking += time.clock()-t
            
            # Si preprocessing rend l'instanciation irréalisable, on annule et on ignore cette valeur de y
            if P.infeasible:
                t = time.clock()
                
                P.cancel()
                
                self.timeCancellingForwardChecking += time.clock()-t
                self.explored += py
                self.nodes -= 1
                continue
            
            # Sinon, on explore cette valeur de y
            else:
                
                # Branchement dynamique sur les variables
                if self.dynamicOrder != None:
                    t = time.clock()
                    self.variableOrder[n+1:] = self.dynamicOrder(self.csp,self.variableOrder[n+1:])
                    self.timeOrder += time.clock()-t
                
                # Exploration de la valeur de y
                found = self.backtrack(n+1,y,py)
                
                self.nodes -= 1            
                
                t = time.clock()
                
                P.cancel()
                
                self.timeCancellingForwardChecking += time.clock()-t
                
                # Si l'exploration a réussi, on propage la valeur "True"
                if found:
                    return True
        
        # Si l'exploration n'a jamais réussi, on désinstancie y
        self.instanciation[y] = None
        
        if ny == 0:
            self.explored += p
            
        return False
   
   
    def __init__(self, csp, **kwargs):
        self.csp = csp
        
        # Paramètres du backtracking
        self.init = None
        self.initialOrder = None
        self.dynamicOrder = heuristics.smallestDomain
        
        self.processingMethod = preprocessing.ForwardCheckingMethod
        
        self.timeLimit = 100000000000
        self.displayFreq = 5000
        self.verbosity = 2
        
        keywords = ["init","initialOrder","dynamicOrder","timeLimit","displayFreq","verbosity","processingMethod"]
        for name in keywords:
            if name in kwargs:
                setattr(self,name,kwargs[name])        
        
        if self.initialOrder == None:
            self.initialOrder = self.dynamicOrder
        
        # Stats du backtracking (temps de calcul, noeuds ouverts, noeuds explorés, % de l'arbre exploré)
        self.nodes = 0
        self.calls = 0
        self.explored = 0
        
        self.timeOrder = 0
        self.timeForwardChecking = 0
        self.timeCancellingForwardChecking = 0
        self.timeConstraintChecking = 0
        self.initTime = time.clock()
        self.endTime = time.clock()
        
        # Cas sans initialisation de l'instanciation
        if self.init == None:
            self.instanciation = [None for k in range(csp.size)]
            
            # Branchement initial des variables
            if self.initialOrder != None:
                t = time.clock()
                self.variableOrder = self.initialOrder(csp,range(csp.size))
                self.timeOrder += time.clock()-t
            else:
                self.variableOrder = range(csp.size)
                
            # Lancement de la récursion
            self.feasible = self.backtrack(0,None,1.)
            
        # Cas avec initialisation de l'instanciation
        else:
            self.instanciation = self.init[:]
            if not csp.test(self.instanciation):
                self.feasible = False
            
            initializedVars = []
            otherVars = []
            for k in range(csp.size):
                if self.instanciation[k] != None:
                    initializedVars += [k]
                else:
                    otherVars += [k]
                    
            # Branchement initial des variables
            if self.initialOrder != None:
                t = time.clock()
                self.variableOrder = initializedVars + self.initialOrder(otherVars)
                self.timeOrder += time.clock()-t
            else:  
                self.variableOrder = initializedVars + otherVars
            
            # Lancement de la récursion
            self.feasible = self.backtrack(len(initializedVars),None,1.)

        