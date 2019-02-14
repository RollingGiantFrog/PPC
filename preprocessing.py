# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 17:15:45 2019

@author: Victor
"""

def initArcConsistency(csp):
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
