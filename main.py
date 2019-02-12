# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 10:45:49 2019

@author: Victor
"""



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
       

class Model:
    def __init__(self,size):
        self.size = size
        self.domains = [[] for i in range(size)]
        self.constraints = []
        
    def setDomain(self,x,domain):
        self.domains[x] = domain[:]
        
    def getDomain(self,x):
        return self.domains
        
    def addConstraint(self,x,y,possibleCouples):
        self.constraints += [Constraint(x,y,possibleCouples)]


# n est la taille de l'instanciation partielle
# x est la dernière variable ajoutée
# I est l'instanciation (I[y] est la valeur de y instanciée)
# D est le domaine des variables
# C est l'ensemble des contraintes
# variableOrder est l'ordre dans lequel on branche sur les variables
def backtrack(n, x, I, M, variableOrder = range(len(I))):
    print(x)
    # Vérification des contraintes
    for c in M.constraints:
        v1 = I[c.x1]
        v2 = I[c.x2]
        
        # x est l'une des deux variables de la contrainte
        # et les deux variables sont instanciées
        if (c.x1 != x and c.x2 != x) or (v1 == None or v2 == None):
            pass
        
        else:
            # La valeur est admissible pour la contrainte c
            if not v2 in c.values1:
                return False
            if not v1 in c.values2:
                return False
            
            # Le couple de valeurs est admissible pour la contrainte c
            if len(c.values1[v2]) > len(c.values2[v1]):
                if not v2 in c.values2[v1]:
                    return False
            else:
                if not v1 in c.values1[v2]:
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
    

M = Model(3)

M.setDomain(0,[10,0,3])
M.setDomain(0,[2,3])
M.setDomain(0,[4,5,6])

M.addConstraint(0,1,[(10,2),(3,2),(0,3)])
M.addConstraint(2,1,[(6,2)])

I = [None for k in range(M.size)]
variableOrder = [1,2,0]

b = backtrack(0,None,I,M)
print(I)