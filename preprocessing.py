# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 17:15:45 2019

@author: Victor
"""

# Ce fichier contient :
#   - l'arc-consistance
#   - les méthodes de preprocessing pluggable dans la classe Backtrack :
#       - pas de processing
#       - forward-checking
#       - arc-consistance (implémentation avec AC3 pour tenir compte de la variable instanciée
#                          par le backtrack et faire moins de calculs)
#       - arc-consistance (implémentation avec AC4 qui recalcule toute l'arc-consistance)

def initArcConsistency(csp, instanciation = None):
    Q = []
    S = {}
    count = [[{} for i in range(csp.size)] for i in range(csp.size)]
    
    for c in csp.constraints:
        x = c.x1
        y = c.x2
        
        i = 0
        while i < csp.domainSize(x):
            a = csp.getDomain(x)[i]
            total = 0
            
            for b in csp.getDomain(y):
                if c.hasCouple(a,b):
                    total += 1
                    if not (y,b) in S:
                        S[(y,b)] = [(x,a)]
                    else:
                        S[(y,b)] += [(x,a)]
                        
            count[x][y][a] = total
            if total == 0:
                csp.domain[x].removeValue(a)
                Q += [(x,a)]
            else:
                i += 1
    
    for c in csp.constraints:
        y = c.x1
        x = c.x2
        
        i = 0
        while i < csp.domainSize(x):
            a = csp.getDomain(x)[i]
            total = 0
            
            for b in csp.getDomain(y):
                if c.hasCouple(b,a):
                    total += 1
                    if not (y,b) in S:
                        S[(y,b)] = [(x,a)]
                    else:
                        S[(y,b)] += [(x,a)]
                        
            count[x][y][a] = total
            if total == 0:
                csp.domain[x].removeValue(a)
                Q += [(x,a)]
            else:
                i += 1

    return Q, S, count
    
    
def ArcConsistency(csp):
    Q, S, count = initArcConsistency(csp)
    R = Q[:]
    
    while len(Q) > 0:
        
        y,b = Q.pop()
        if (y,b) in S:
            for x,a in S[(y,b)]:
                count[x][y][a] -= 1
                if count[x][y][a] == 0 and csp.domain[x].hasValue(a):
                    csp.domain[x].removeValue(a)
                    Q += [(x,a)]
                    R += [(x,a)]
    
    return R


class ForwardCheckingMethod:
    def __init__(self, csp, X, I):
        self.csp = csp
        self.prunedValues = {}
        self.infeasible = False
        
        for x in X:
            for c in csp.constraints2D[x]:
                v1 = I[c.x1]
                v2 = I[c.x2]
                a = I[x]
                
                if (c.x1 == x and v2 == None):
                    y = c.x2
                    for b in csp.getDomain(y):
                        if not c.hasCouple(a,b):
                            if not y in self.prunedValues:
                                self.prunedValues[y] = [b]
                            else:
                                self.prunedValues[y] += [b]
                            
                            csp.domain[y].removeValue(b)
                            if csp.domainSize(y) == 0:
                                self.infeasible = True
                                return
                        
                elif (c.x2 == x and v1 == None):
                    y = c.x1
                    for b in csp.getDomain(y):
                        if not c.hasCouple(b,a):
                            if not y in self.prunedValues:
                                self.prunedValues[y] = [b]
                            else:
                                self.prunedValues[y] += [b]
                            
                            csp.domain[y].removeValue(b)
                            if csp.domainSize(y) == 0:
                                self.infeasible = True
                                return
                else:
                    continue
        
                
    def cancel(self):
        for x,vals in self.prunedValues.items():
            for val in vals:
                self.csp.domain[x].addValue(val)
            

class NoProcessingMethod:
    def __init__(self, csp, x, I):
        self.infeasible = False
        self.prunedValues = {}
        
    def cancel(self):
        return
        
class ArcConsistencyMethod3:
    
    def __init__(self, csp, variables, I):
        self.csp = csp
        self.prunedValues = {}
        self.infeasible = False
        
        for var in variables:        
            aTester = []
            for c in csp.constraints2D[var]:
                aTester += [c]
            
        while len(aTester) > 0:
            c = aTester.pop()
            tempPrunedValues = []            
            
            if I[c.x1] == None:
                domain1 = csp.getDomain(c.x1)
            else:
                domain1 = [I[c.x1]]
            
            if I[c.x2] == None:
                domain2 = csp.getDomain(c.x2)
            else:
                domain2 = [I[c.x2]]
            
            for a in domain1:
                total = 0
                for b in domain2:
                    if c.hasCouple(a,b):
                        total += 1
                
                if total == 0:
                    if not c.x1 in self.prunedValues:
                        self.prunedValues[c.x1] = [a]
                    else:
                        self.prunedValues[c.x1] += [a]
                        
                    tempPrunedValues += [a]
            
            for a in tempPrunedValues:
                csp.domain[c.x1].removeValue(a)
                
            if I[c.x1] == None:
                if csp.domainSize(c.x1) == 0:
                    self.infeasible = True
                    return
                    
            elif len(tempPrunedValues) > 0:
                self.infeasible = True
                return
            
            if len(tempPrunedValues) > 0:
                for s in csp.constraints2D[c.x1]:
                    if s.x1 != c.x2 and s.x2 != c.x2:
                        aTester += [s]
            
            tempPrunedValues = []            
            
            if I[c.x1] == None:
                domain1 = csp.getDomain(c.x1)
            else:
                domain1 = [I[c.x1]]
            
            if I[c.x2] == None:
                domain2 = csp.getDomain(c.x2)
            else:
                domain2 = [I[c.x2]]
            
            for b in domain2:
                total = 0
                for a in domain1:
                    if c.hasCouple(a,b):
                        total += 1
                
                if total == 0:
                    if not c.x2 in self.prunedValues:
                        self.prunedValues[c.x2] = [b]
                    else:
                        self.prunedValues[c.x2] += [b]
                        
                    tempPrunedValues += [b]
            
            for b in tempPrunedValues:
                csp.domain[c.x2].removeValue(b)
                
            if I[c.x2] == None:
                if csp.domainSize(c.x2) == 0:
                    self.infeasible = True
                    return
            elif len(tempPrunedValues) > 0:
                self.infeasible = True
                return
            
            if len(tempPrunedValues) > 0:
                for s in csp.constraints2D[c.x2]:
                    if s.x1 != c.x1 and s.x2 != c.x1:
                        aTester += [s]
            
    def cancel(self):
        for x,vals in self.prunedValues.items():
            for val in vals:
                self.csp.domain[x].addValue(val)
            
            
class ArcConsistencyMethod:
    def initArcConsistency(self):
        S = {}
        count = [[{} for i in range(self.csp.size)] for i in range(self.csp.size)]
        
        for c in self.csp.constraints:
            x = c.x1
            y = c.x2
            
            if self.I[x] == None:
                domainX = self.csp.getDomain(x)
            else:
                domainX = [self.I[x]]
            
            if self.I[y] == None:
                domainY = self.csp.getDomain(y)
            else:
                domainY = [self.I[y]]
            
            
            for a in domainX:
                total = 0
                
                for b in domainY:
                    if c.hasCouple(a,b):
                        total += 1
                        if not (y,b) in S:
                            S[(y,b)] = [(x,a)]
                        else:
                            S[(y,b)] += [(x,a)]
                            
                count[x][y][a] = total
                if total == 0:
                    self.csp.domain[x].removeValue(a)
                    
                    self.tempPrunedValues += [(x,a)]
                    if not x in self.prunedValues:
                        self.prunedValues[x] = [a]
                    else:
                        self.prunedValues[x] += [a]
                    
                    if self.I[x] != None:
                        self.infeasible = True
                        return None, None
                            
                    elif self.csp.domainSize(x) == 0:
                        self.infeasible = True
                        return None, None
        
        for c in self.csp.constraints:
            y = c.x1
            x = c.x2
            
            if self.I[x] == None:
                domainX = self.csp.getDomain(x)
            else:
                domainX = [self.I[x]]
            
            if self.I[y] == None:
                domainY = self.csp.getDomain(y)
            else:
                domainY = [self.I[y]]
            
            
            for a in domainX:
                total = 0
                
                for b in domainY:
                    if c.hasCouple(b,a):
                        total += 1
                        if not (y,b) in S:
                            S[(y,b)] = [(x,a)]
                        else:
                            S[(y,b)] += [(x,a)]
                            
                count[x][y][a] = total
                if total == 0:
                    self.csp.domain[x].removeValue(a)
                    
                    self.tempPrunedValues += [(x,a)]
                    if not x in self.prunedValues:
                        self.prunedValues[x] = [a]
                    else:
                        self.prunedValues[x] += [a]
                        
                    if self.I[x] != None:
                        self.infeasible = True
                        return None, None
                            
                    elif self.csp.domainSize(x) == 0:
                        self.infeasible = True
                        return None, None
    
        return S, count    
    
    
    def __init__(self,csp,var,I):
        self.csp = csp
        self.prunedValues = {}
        self.tempPrunedValues = []
        self.infeasible = False
        self.I = I
        S, count = self.initArcConsistency()
        
        if self.infeasible:
            return
            
        while len(self.tempPrunedValues) > 0:
            
            y,b = self.tempPrunedValues.pop()
            if (y,b) in S:
                for x,a in S[(y,b)]:
                    count[x][y][a] -= 1
                    if count[x][y][a] == 0 and self.csp.domain[x].hasValue(a):
                        self.csp.domain[x].removeValue(a)
                        
                        if not x in self.prunedValues:
                            self.prunedValues[x] = [a]
                        else:
                            self.prunedValues[x] += [a]
                        
                        self.tempPrunedValues += [(x,a)]
        
    
    def cancel(self):
        for x,vals in self.prunedValues.items():
            for val in vals:
                self.csp.domain[x].addValue(val)
            