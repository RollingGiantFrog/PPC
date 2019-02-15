# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 17:15:45 2019

@author: Victor
"""

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


#def initArcConsistency2(csp, x, I):
#    Q = []
#    S = {}
#    count = {}
#    
#    if x in csp.constraints2D:
#        for c in csp.constraints2D[x]:
#            v1 = I[c.x1]
#            v2 = I[c.x2]
#            a = I[x]
#            
#            if (c.x1 == x and v2 == None):
#                y = c.x2
#                total = 0
#            
#                for b in csp.getDomain(y):
#                    if c.hasCouple(a,b):
#                        total += 1
#                        if not (y,b) in S:
#                            S[(y,b)] = [(x,a)]
#                        else:
#                            S[(y,b)] += [(x,a)]
#                            
#                count[(x,y,a)] = total
#                if total == 0:
#                    return False, Q, None, None
#                    
#                #
#
#                for b in csp.getDomain(y):
#                    total = 0
#                    
#                    if c.hasCouple(a,b):
#                        total += 1
#                        if not (x,a) in S:
#                            S[(x,a)] = [(y,b)]
#                        else:
#                            S[(x,a)] += [(y,b)]
#                                
#                    count[(x,y,a)] = total
#                    if total == 0:
#                        csp.domain[y].removeValue(b)
#                        Q += [(y,b)]
#                                    
#                    
#            elif (c.x2 == x and v1 == None):
#                y = c.x1
#                
#                total = 0
#            
#                for b in csp.getDomain(y):
#                    if c.hasCouple(b,a):
#                        total += 1
#                        if not (y,b) in S:
#                            S[(y,b)] = [(x,a)]
#                        else:
#                            S[(y,b)] += [(x,a)]
#                            
#                count[(x,y,a)] = total
#                if total == 0:
#                    return False, Q, None, None
#            
#                #
#            
#                for b in csp.getDomain(y):
#                    total = 0
#                    
#                    if c.hasCouple(b,a):
#                        total += 1
#                        if not (x,a) in S:
#                            S[(x,a)] = [(y,b)]
#                        else:
#                            S[(x,a)] += [(y,b)]
#                                
#                    count[(x,y,a)] = total
#                    if total == 0:
#                        csp.domain[y].removeValue(b)
#                        Q += [(y,b)]
#                
#            else:
#                continue
#            
#    
#    return True, Q, S, count
#
#def ArcConsistency2(csp, var, instanciation):
#    B, Q, S, count = initArcConsistency2(csp,var,instanciation)
#    
#    R = Q[:]
#    
#    if not B:
#        return False, R
#        
#    
#    while len(Q) > 0:
#        
#        y,b = Q.pop()
#        if (y,b) in S:
#            for x,a in S[(y,b)]:
#                count[(x,y,a)] -= 1
#                if count[(x,y,a)] == 0 and csp.domain[x].hasValue(a):
#                    csp.domain[x].removeValue(a)
#                    Q += [(x,a)]
#                    R += [(x,a)]
#    
#    return True, R
#    
#def cancelArcConsistency(csp,R):
#    for x,a in R:
#        csp.domain[x].addValue(a)
#        
class ForwardCheckingMethod:
    def __init__(self, csp, x, I):
        self.csp = csp
        self.prunedValues = {}
        self.infeasible = False
        
        if x in csp.constraints2D:
            for c in csp.constraints2D[x]:
                v1 = I[c.x1]
                v2 = I[c.x2]
                a = I[x]
                
                if (c.x1 == x and v2 == None):
                    y = c.x2
                    if not y in self.prunedValues:
                        self.prunedValues[y] = []
                    for b in csp.getDomain(y):
                        if not c.hasCouple(a,b):
                            self.prunedValues[y] += [b]
                        
                elif (c.x2 == x and v1 == None):
                    y = c.x1
                    if not y in self.prunedValues:
                        self.prunedValues[y] = []
                    for b in csp.getDomain(y):
                        if not c.hasCouple(b,a):
                            self.prunedValues[y] += [b]
                
                else:
                    continue
                
                for b in self.prunedValues[y]:
                    if csp.domain[y].hasValue(b):
                        csp.domain[y].removeValue(b)
                        
                if csp.domainSize(y) == 0:
                    self.infeasible = True
                    return
        
                
    def cancel(self):
        for var in self.prunedValues.keys():
            for val in self.prunedValues[var]:
                self.csp.domain[var].addValue(val)
        
        
class ArcConsistencyMethod:
    
    def initArcConsistency(self, csp, x, I):
        S = {}
        count = {}
        
        if x in csp.constraints2D:
            for c in csp.constraints2D[x]:
                v1 = I[c.x1]
                v2 = I[c.x2]
                a = I[x]
                
                if (c.x1 == x and v2 == None):
                    y = c.x2
                    total = 0
                
                    for b in csp.getDomain(y):
                        if c.hasCouple(a,b):
                            total += 1
                            if not (y,b) in S:
                                S[(y,b)] = [(x,a)]
                            else:
                                S[(y,b)] += [(x,a)]
                                
                    count[(x,y,a)] = total
                    if total == 0:
                        self.infeasible = True
                        return None, None
                        
                    #
    
                    for b in csp.getDomain(y):
                        total = 0
                        
                        if c.hasCouple(a,b):
                            total += 1
                            if not (x,a) in S:
                                S[(x,a)] = [(y,b)]
                            else:
                                S[(x,a)] += [(y,b)]
                                    
                        count[(x,y,a)] = total
                        if total == 0:
                            csp.domain[y].removeValue(b)
                            self.prunedValues += [(y,b)]
                                        
                        
                elif (c.x2 == x and v1 == None):
                    y = c.x1
                    
                    total = 0
                
                    for b in csp.getDomain(y):
                        if c.hasCouple(b,a):
                            total += 1
                            if not (y,b) in S:
                                S[(y,b)] = [(x,a)]
                            else:
                                S[(y,b)] += [(x,a)]
                                
                    count[(x,y,a)] = total
                    if total == 0:
                        self.infeasible = True
                        return None, None
                
                    #
                
                    for b in csp.getDomain(y):
                        total = 0
                        
                        if c.hasCouple(b,a):
                            total += 1
                            if not (x,a) in S:
                                S[(x,a)] = [(y,b)]
                            else:
                                S[(x,a)] += [(y,b)]
                                    
                        count[(x,y,a)] = total
                        if total == 0:
                            csp.domain[y].removeValue(b)
                            self.prunedValues += [(y,b)]
                    
                else:
                    continue
                
        
        return S, count    
    
    def __init__(self, csp, var, instanciation):
        self.csp = csp
        self.prunedValues = []
        self.infeasible = False
        
        S, count = self.initArcConsistency(csp,var,instanciation)
    
        if self.infeasible:
            return
            
        Q = self.prunedValues[:]
        
        while len(Q) > 0:
            
            y,b = Q.pop()
            if (y,b) in S:
                for x,a in S[(y,b)]:
                    count[(x,y,a)] -= 1
                    if count[(x,y,a)] == 0 and csp.domain[x].hasValue(a):
                        csp.domain[x].removeValue(a)
                        Q += [(x,a)]
                        self.prunedValues += [(x,a)]
        
    
    def cancel(self):
        for x,a in self.prunedValues:
            self.csp.domain[x].addValue(a)

class NoProcessingMethod:
    def __init__(self, csp, x, I):
        self.infeasible = False
        
    def cancel(self):
        return