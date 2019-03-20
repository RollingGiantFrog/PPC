# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 17:09:34 2019

@author: Victor
"""

import time
import preprocessing
import heuristics
import brancher
import random

class Backtrack:
    # verbosity = 1 : affiche tout
    # verbosity = 0 : n'affiche rien
    def printStats(self,verbosity):
        if verbosity >= 1:
            print("*************** Globals stats ***************")
            print("Explored nodes : " + str(self.calls))
            print("Explored : " + str(self.explored))
            print("Nodes opened : " + str(self.nodes))
            print("Current depth : " + str(self.currentDepth))
            print("Average depth : " + str(float(self.averageDepth)/self.calls))
            print("Time spent overall : " + str(self.endTime-self.initTime))
            
            print("")
            print("*************** Processing method  ***************")
        if verbosity >= 2:
            print("Time spent in Forward Checking : " + str(self.timeForwardChecking))
            print("Time spent in cancelling Forward Checking : " + str(self.timeCancellingForwardChecking))
            print("Time spent in Arc-Consistency : " + str(self.timeAC))
            print("Time spent in cancelling Arc-Consistency : " + str(self.timeCancellingAC))
            
            print("")
            print("*************** Branching method  ***************")
            print("Time spent in Variable Branching Selection : " + str(self.timeVarSort))
            if verbosity >= 3:
                self.brancher.printStats()
                
            print("Time spent in Impact computation : " + str(self.timeImpact))
                
            print("")
            print("*************** Constraint checking  ***************")
            print("Time spent in constraint checking : " + str(self.timeConstraintChecking))
            print("")
        if verbosity > 0:
            print("")
    
    # n est la taille de l'instanciation partielle
    # x est la dernière variable ajoutée
    # p est le pourcentage que ce noeud représente de l'arbre
    def backtrack(self, n, x, p):
        
        # Gestion des stats
        self.endTime = time.clock()
        if x != None:
            self.instanciatedVariables[x] += 1
        self.calls += 1
        self.currentDepth = n
        self.averageDepth += n
        if self.calls % self.displayFreq == 0:
            self.printStats(self.verbosity)
            
        if self.endTime-self.initTime > self.timeLimit:
            self.unfinished = True
            return False
        
        t = time.clock()
        
        # Vérification des contraintes
        if x != None:
            for c in self.csp.constraints2D[x]:
                v1 = self.instanciation[c.x1]
                v2 = self.instanciation[c.x2]
                
                if v1 != None and v2 != None:
                    # Le couple de valeurs est admissible pour la contrainte c
                    if not c.hasCouple(v1,v2):
                        self.explored += p
                        self.infeasibleVariables[x] += 1
                        return False
        
        self.timeConstraintChecking += time.clock()-t
        
        # Test de la complétude de l'instanciation
        if n == self.csp.size:
            return True
            
        # Instanciation d'une nouvelle variable
        t = time.clock()
        y = self.brancher.pop()
        self.timeVarSort += time.clock()-t
        domainY = self.csp.getDomain(y)
        
        ny = len(domainY)
        py = p/self.initialDomainSizes[y]
        self.explored += py*(self.initialDomainSizes[y]-ny)
        self.nodes += ny
        
        for v in domainY:
            self.instanciation[y] = v
            
            # Application d'une méthode de preprocessing (forward-checking, AC)
            t = time.clock()
            
            P = self.processingMethod(self.csp,[y],self.instanciation)
            
            self.timeForwardChecking += time.clock()-t
            
            if self.useArcConsistency and self.endTime > self.lastCallAC + self.arcConsistencyWeight*self.durationAC:
                self.lastCallAC = self.endTime
                t = time.clock()
                PAC = preprocessing.ArcConsistencyMethod(self.csp,[y],self.instanciation)
                self.durationAC = time.clock()-t
                self.timeAC += self.durationAC
            else:
                PAC = preprocessing.NoProcessingMethod(None,None,None)
            
            # Calcul de l'impact de x
            t = time.clock()
            
            d = 1.
            for var,vals in P.prunedValues.items():
                size = self.csp.domainSize(var)
                d *= size/(size + len(vals))
            for var,vals in PAC.prunedValues.items():
                size = self.csp.domainSize(var)
                d *= size/(size + len(vals))
                
            if x != None:
                self.impactVariables[x] += 1-d
            
            self.timeImpact += time.clock()-t
            
            # Si preprocessing rend l'instanciation irréalisable, on annule et on ignore cette valeur de y
            if P.infeasible or PAC.infeasible:
                t = time.clock()
                PAC.cancel()
                self.timeCancellingAC += time.clock()-t
                
                t = time.clock()
                P.cancel()
                self.timeCancellingForwardChecking += time.clock()-t
                
                t = time.clock()
#                self.brancher.update(P.prunedValues.keys())
                self.timeVarSort += time.clock()-t
                
                self.explored += py
                self.nodes -= 1
                continue
            
            # Sinon, on explore cette valeur de y
            else:
                
                # Branchement dynamique sur les variables
                t = time.clock()
#                self.brancher.update(P.prunedVars)
                self.brancher.update(P.prunedValues.keys())
                self.timeVarSort += time.clock()-t
                
                explored = self.explored
                
                # Exploration de la valeur de y
                found = self.backtrack(n+1,y,py)
#                if self.endTime-self.initTime > self.timeLimit:
#                    return found
                
                self.explored = explored + py
                self.nodes -= 1            
                
                t = time.clock()
                PAC.cancel()
                self.timeCancellingAC += time.clock()-t
                
                t = time.clock()
                P.cancel()
                self.timeCancellingForwardChecking += time.clock()-t
                
                t = time.clock()
                self.brancher.update(P.prunedValues.keys())
                self.timeVarSort += time.clock()-t
                
                # Si l'exploration a réussi, on propage la valeur "True"
                if found:
                    return True
                    
        
        # Si l'exploration n'a jamais réussi, on désinstancie y
        self.instanciation[y] = None
        
        self.brancher.push(y)
        
        if ny == 0:
            self.explored += p
            
        if x != None:
            self.infeasibleVariables[x] += 1
            
        return False
   
   
    def __init__(self, csp, **kwargs):
        self.csp = csp
        self.initialDomainSizes = [csp.domainSize(x) for x in range(self.csp.size)]
        self.feasible = False
        self.unfinished = False
        
        # Paramètres du backtracking
        self.initialization = None
        self.initialOrder = range(csp.size)
        self.rankFuncs = [heuristics.domainRank]
        self.brancherType = brancher.ArrayBrancher
        
        self.processingMethod = preprocessing.ForwardCheckingMethod
        self.arcConsistencyWeight = 5
        self.lastCallAC = 0
        self.durationAC = 0
        self.useArcConsistency = True
        
        self.instanciatedVariables = [0 for k in range(self.csp.size)]
        self.infeasibleVariables = [0 for k in range(self.csp.size)]
        self.impactVariables = [1. for k in range(self.csp.size)]
        
        self.timeLimit = 100000000000
        self.displayFreq = 5000
        self.verbosity = 10
        
        keywords = ["initialization","initialOrder","rankFuncs","brancherType","timeLimit","displayFreq","verbosity","processingMethod","arcConsistencyWeight","useArcConsistency"]
        for name in keywords:
            if name in kwargs:
                setattr(self,name,kwargs[name])        
        
        # Stats du backtracking (temps de calcul, noeuds ouverts, noeuds explorés, % de l'arbre exploré, profondeur)
        self.nodes = 0
        self.calls = 0
        self.explored = 0
        self.currentDepth = 0
        self.averageDepth = 0
        
        self.timeVarSort = 0
        self.timeForwardChecking = 0
        self.timeCancellingForwardChecking = 0
        self.timeAC = 0
        self.timeCancellingAC = 0
        self.timeConstraintChecking = 0
        self.timeImpact = 0
        self.initTime = time.clock()
        self.endTime = time.clock()
        
        # Cas sans initialisation de l'instanciation
        if self.initialization == None:
            self.instanciation = [None for k in self.initialOrder]
            
            # Branchement initial des variables
            t = time.clock()
            self.brancher = self.brancherType(self,self.rankFuncs,[],self.initialOrder)   
            self.timeVarSort += time.clock()-t             
                
            # Lancement de la récursion
            self.feasible = self.backtrack(0,None,1.)
            
        # Cas avec initialisation de l'instanciation
        else:
            self.instanciation = self.initialization[:]
            if not csp.test(self.instanciation):
                self.feasible = False
                return
            
            initializedVars = []
            otherVars = []
            for k in self.initialOrder:
                if self.instanciation[k] != None:
                    initializedVars += [k]
                else:
                    otherVars += [k]
                    
            for var in initializedVars:
                self.instanciatedVariables[var] = 1
            
            # Branchement initial des variables
            t = time.clock()
            self.brancher = self.brancherType(self,self.rankFuncs,initializedVars,otherVars) 
            self.timeVarSort += time.clock()-t               
                
            # Lancement de la récursion
            self.feasible = self.backtrack(len(initializedVars),None,1.)

        