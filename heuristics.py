# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 17:11:22 2019

@author: Victor
"""

import random as rd

# Fonctions de rang

def domainRank(backtrack,csp,x):
    return csp.domainSize(x)
    
def infeasibilityRank(backtrack,csp,x):
    return -backtrack.infeasibleVariables[x]
  
def constraintRank(backtrack,csp,x):
    return -len(csp.constraints2D[x])

def impactRank(backtrack,csp,x):
    if backtrack.instanciatedVariables[x] > 0:
        return backtrack.impactVariables[x]/backtrack.instanciatedVariables[x]
    else:
        return 0
        
def randomRank(backtrack,csp,x):
    return rd.random()


# Algorithmes de tri par critères

# Ordonne les variables X du csp par ordre croissant de taille de domaine
def smallestDomain(backtrack,csp,X):
    variableDomSize = []
    for x in X:
        variableDomSize += [(csp.domainSize(x),x)]
    variableDomSize.sort()
    return [e[1] for e in variableDomSize]
    

# Ordonne les variables X du csp par ordre décroissant de taille de domaine
def largestDomain(backtrack,csp,X):
    variableDomSize = []
    for x in X:
        variableDomSize += [(csp.domainSize(x),x)]
    variableDomSize.sort(reverse=True)
    return [e[1] for e in variableDomSize]
    
# Ordonne les variables X du csp par ordre décroissant d'infaisabilité
def largestInfeasible(backtrack,csp,X):
    variableDomSize = []
    for x in X:
        variableDomSize += [(csp.domainSize(x),-backtrack.infeasibleVariables[x],x)]
    variableDomSize.sort()
    return [e[2] for e in variableDomSize]
    
# Ordonne les variables X du csp par ordre décroissant d'infaisabilité
def smallestInfeasible(backtrack,csp,X):
    variableDomSize = []
    for x in X:
        variableDomSize += [(csp.domainSize(x),backtrack.infeasibleVariables[x],x)]
    variableDomSize.sort()
    return [e[2] for e in variableDomSize]    
    
# Ordonne les variables X du csp par ordre décroissant d'infaisabilité
def biggestImpact(backtrack,csp,X):
    variableDomSize = []
    for x in X:
        if backtrack.instanciatedVariables[x] > 0:
            variableDomSize += [(csp.domainSize(x),backtrack.impactVariables[x]/backtrack.instanciatedVariables[x],-backtrack.infeasibleVariables[x],x)]
        else:
            variableDomSize += [(csp.domainSize(x),0,-backtrack.infeasibleVariables[x],x)]
        
    variableDomSize.sort()
    return [e[3] for e in variableDomSize]
    
# Ordonne les variables X du csp par ordre décroissant d'infaisabilité
def biggestImpact2(backtrack,csp,X):
    variableDomSize = []
    for x in X:
        if backtrack.instanciatedVariables[x] > 0:
            variableDomSize += [(csp.domainSize(x),-backtrack.infeasibleVariables[x],backtrack.impactVariables[x]/backtrack.instanciatedVariables[x],x)]
        else:
            variableDomSize += [(csp.domainSize(x),-backtrack.infeasibleVariables[x],0,x)]
        
    variableDomSize.sort()
    return [e[3] for e in variableDomSize]
    
# Ordonne les variables X du csp par ordre décroissant d'infaisabilité
def mostConstrained(backtrack,csp,X):
    variableDomSize = []
    for x in X:
        variableDomSize += [(csp.domainSize(x),-backtrack.infeasibleVariables[x],-len(csp.constraints2D[x]),x)]
    variableDomSize.sort()
    return [e[3] for e in variableDomSize]
    
# La première variable sera une voisine d'une variable de plus petit domaine et qui casse souvent la faisabilité
def largestInfeasibleNeighbor(backtrack,csp,X):
    if len(X) > 0:
        variableDomSize = []
        for x in X:
            variableDomSize += [(csp.domainSize(x),-backtrack.infeasibleVariables[x],x)]
        variableDomSize.sort()
        
        minVar = variableDomSize[0][2]  
        
        for i in range(len(X)):
            if (X[i],minVar) in csp.neighbors:
                variableDomSize[i],variableDomSize[0] = variableDomSize[0],variableDomSize[i]
                break
        
        return [e[2] for e in variableDomSize]
    
    return []