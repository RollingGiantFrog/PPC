# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 17:09:34 2019

@author: Victor
"""

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
    
    return Q
            
def cancelForwardChecking(csp, Q):
    for var in Q.keys():
        for val in Q[var]:
            csp.domain[var].addValue(val)
                
# n est la taille de l'instanciation partielle
# x est la dernière variable ajoutée
# I est l'instanciation (I[y] est la valeur de y instanciée)
# csp est le csp
# variableOrder est l'ordre dans lequel on branche sur les variables
def backtrack_rec(n, x, I, csp, variableOrder = None, order = None):
    if variableOrder == None:
        variableOrder = range(len(I))
        
    # Vérification des contraintes
    if x in csp.constraints2D:
        for c in csp.constraints2D[x]:
            v1 = I[c.x1]
            v2 = I[c.x2]
            
            # x est l'une des deux variables de la contrainte
            # et les deux variables sont instanciées
            if (c.x1 != x and c.x2 != x) or (v1 == None or v2 == None):
                continue
            
            else:
                # Le couple de valeurs est admissible pour la contrainte c
                if not c.hasCouple(v1,v2):
                    return False
    
    # Test de la complétude de l'instanciation
    if n == len(I):
        return True
        
    # Instanciation d'une nouvelle variable
    y = variableOrder[n]
    domainY = csp.getDomain(y)
    for v in domainY:
        I[y] = v
        Q = forwardChecking(csp,y,I)
        
        if order != None:
            variableOrder[n+1:] = order(csp,variableOrder[n+1:])
        
        found = backtrack_rec(n+1,y,I,csp,variableOrder)
        cancelForwardChecking(csp, Q)
        if found:
            return True
            
    I[y] = None
            
    return False
   
def backtrack(csp, init = None, order = heuristics.smallestDomain, dynamic = True):
    if init == None:
        I = [None for k in range(csp.size)]
        
        variableOrder = order(csp,range(csp.size))
        if dynamic:
            return backtrack_rec(0,None,I,csp,variableOrder,order), I
        else:
            return backtrack_rec(0,None,I,csp,variableOrder), I
        
    else:
        I = init[:]
        if not csp.test(I):
            return False, I
        
        initializedVars = []
        otherVars = []
        for k in range(csp.size):
            if I[k] != None:
                initializedVars += [k]
            else:
                otherVars += [k]
                
        variableOrder = initializedVars + order(otherVars)
        
        if dynamic:
            return backtrack_rec(len(initializedVars),None,I,csp,variableOrder,order), I
        else:
            return backtrack_rec(len(initializedVars),None,I,csp,variableOrder), I
        
    