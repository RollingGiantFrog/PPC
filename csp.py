# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 17:09:05 2019

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
        return self.inDomain.keys()
        
    def setValues(self,values):
        self.inDomain.clear()
        for value in values:
            self.addValue(value)
            
    def size(self):
        return len(self.inDomain)
        
# Contrainte définie par une liste de couples réalisables
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
                self.values2[i] = set([j])
            else:
                self.values2[i].add(j)
                
            if (not j in self.values1):
                self.values1[j] = set([i])
            else: 
                self.values1[j].add(i)
                
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
        
# Contrainte définie par une fonction sur les variables et les valeurs
class ComprehensiveConstraint:
    def __init__(self,x1,x2,possibleCouplesFunc):
        self.x1 = x1
        self.x2 = x2
        self.possibleCouples = possibleCouplesFunc
                
    def hasCouple(self,v1,v2):
        return self.possibleCouples(self.x1,self.x2,v1,v2)

class CSP:
    def __init__(self,size):
        self.size = size
        self.domain = [Domain() for i in range(size)]
        self.constraints = []
        
        self.constraints2D = {}
        
    def setDomain(self,x,values):
        self.domain[x].setValues(values)
        
    def getDomain(self,x):
        return self.domain[x].getValues()
    
    def domainSize(self,x):
        return self.domain[x].size()
    
    # Ajoute une contrainte définie par une liste de couples réalisables
    def addConstraint(self,x,y,possibleCouples):
        c = Constraint(x,y,possibleCouples)
        self.constraints += [c]
        if x in self.constraints2D:
            self.constraints2D[x] += [c]
        else:
            self.constraints2D[x] = [c]
        
        if y in self.constraints2D:
            self.constraints2D[y] += [c]
        else:
            self.constraints2D[y] = [c]

    # Ajoute une contrainte définie par une fonction sur les variables et les valeurs
    def addComprehensiveConstraint(self,x,y,possibleCouplesFunc):
        c = ComprehensiveConstraint(x,y,possibleCouplesFunc)
        self.constraints += [c]
        if x in self.constraints2D:
            self.constraints2D[x] += [c]
        else:
            self.constraints2D[x] = [c]
        
        if y in self.constraints2D:
            self.constraints2D[y] += [c]
        else:
            self.constraints2D[y] = [c]

    # Teste une instanciation donnée et dit si elle est réalisable
    def test(self,I):
        for c in self.constraints:
            if (I[c.x1] == None or I[c.x2] == None):
                continue
            
            if not c.hasCouple(I[c.x1],I[c.x2]):
                return False
                
        return True
        