# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 10:45:49 2019

@author: Victor
"""

class Domain:
    def __init__(self):
        self.inDomain = {}
        
    def addValue(self,v):
        self.inDomain[v] = True
        
    def hasValue(self,v):
        return v in self.inDomain
        
    def removeValue(self,v):
        del self.inDomain[v]
        
    def getValues(self):
        return self.inDomain.values()
        
class Constraint:
    def __init__(self,x1,x2,possibleCouples):
        self.x1 = x1
        self.x2 = x2
        # values 1 indexé par les valeurs de v2, stocke les valeurs de v1
        self.values1 = {}
        # values 2 indexé par les valeurs de v1, stocke les valeurs de v2
        self.values2 = {}
        
        # initialisation des dictionnaires de contraintes
        for i,j in possibleCouples:
            if (not i in self.values2):
                self.values2[i] = [j]
            else:
                self.values2[i] += [j]
                
            if (not j in self.values1):
                self.values1[j] = [i]
            else: 
                self.values1[j] += [i]
                
    def hasValue1(self,v1):
        return v1 in self.values2
        
    def hasValue2(self,v2):
        return v2 in self.values1
    
    def hasCouple(self,v1,v2):
        if not self.hasValue1(v1) or not self.hasValue2(v2):
            return False
        if len(self.values1[v2]) > len(self.values2[v1]):
            if not v2 in self.values2[v1]:
                return False
        else:
            if not v1 in self.values1[v2]:
                return False
        
        return True

class CSP:
    def __init__(self,size):
        self.size = size
        # passer en dictionnaire le domaine de chaque variable
#        self.domains = [{} for i in range(size)]
        self.domains = [[] for i in range(size)]
        self.constraints = []
        
    def setDomain(self,x,domain):
        self.domains[x] = domain[:]
        
    def getDomain(self,x):
        return self.domains
        
    def addConstraint(self,x,y,possibleCouples):
        self.constraints += [Constraint(x,y,possibleCouples)]


def initAC4(csp):
    Q = []
    S = {}
    count = [[{} for i in range(csp.size)] for i in range(csp.size)]
    
    for c in csp.constraints:
        x = c.x1
        y = c.x2
        
        i = 0
        while i < len(csp.domains[x]):
            a = csp.domains[x][i]
            total = 0
            
            for b in csp.domains[y]:
                if c.hasCouple(a,b):
                    total += 1
                    if not (y,b) in S:
                        S[(y,b)] = [(x,a)]
                    else:
                        S[(y,b)] += [(x,a)]
                        
            count[x][y][a] = total
            if total == 0:
                del csp.domains[x][i]
                Q += [(x,a)]
            else:
                i += 1
    
    for c in csp.constraints:
        y = c.x1
        x = c.x2
        
        i = 0
        while i < len(csp.domains[x]):
            a = csp.domains[x][i]
            total = 0
            
            for b in csp.domains[y]:
                if c.hasCouple(b,a):
                    total += 1
                    if not (y,b) in S:
                        S[(y,b)] = [(x,a)]
                    else:
                        S[(y,b)] += [(x,a)]
                        
            count[x][y][a] = total
            if total == 0:
                del csp.domains[x][i]
                Q += [(x,a)]
            else:
                i += 1

    return Q, S, count
    
def AC4(csp):
    Q, S, count = initAC4(csp)
    while len(Q) > 0:
        
        y,b = Q.pop()
        if (y,b) in S:
            for x,a in S[(y,b)]:
                count[x][y][a] -= 1
                if count[x][y][a] == 0 and a in csp.domains[x]:
                    csp.domains[x].remove(a)
    #                M.getDomain(x).remove(a)
                    Q += [(x,a)]

# n est la taille de l'instanciation partielle
# x est la dernière variable ajoutée
# I est l'instanciation (I[y] est la valeur de y instanciée)
# M est le csp
# variableOrder est l'ordre dans lequel on branche sur les variables
def backtrack(n, x, I, M, variableOrder = range(len(I))):
    # Vérification des contraintes
    for c in M.constraints:
        v1 = I[c.x1]
        v2 = I[c.x2]
        
        # x est l'une des deux variables de la contrainte
        # et les deux variables sont instanciées
        if (c.x1 != x and c.x2 != x) or (v1 == None or v2 == None):
            pass
        
        else:
            # Le couple de valeurs est admissible pour la contrainte c
            if not c.hasCouple(v1,v2):
                return False
    
    # Test de la complétude de l'instanciation
    if n == len(I):
        return True
        
    y = variableOrder[n]
    for v in M.domains[y]:
        I[y] = v
        if backtrack(n+1,y,I,M,variableOrder):
            return True
            
    return False
    

#csp = CSP(3)
#
#csp.setDomain(0,[10,0,3])
#csp.setDomain(1,[1,2,3])
#csp.setDomain(2,[4,5,6])
#
#csp.addConstraint(0,1,[(10,2),(3,2),(0,3)])
#csp.addConstraint(2,1,[(6,2)])

csp = CSP(3)
csp.setDomain(0,[0,1])
csp.setDomain(1,[2,3])
csp.setDomain(2,[4,5])

csp.addConstraint(0,1,[(0,2),(1,2)])
csp.addConstraint(1,2,[(2,4),(3,4)])
csp.addConstraint(2,0,[(4,0),(5,0)])

I = [None for k in range(csp.size)]
variableOrder = [1,2,0]

AC4(csp)
b = backtrack(0,None,I,csp)
print(I)