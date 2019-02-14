# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 17:11:22 2019

@author: Victor
"""


def smallestDomain(csp,X):
    variableDomSize = []
    for x in X:
        variableDomSize += [(csp.domainSize(x),x)]
    variableDomSize.sort()
    return [e[1] for e in variableDomSize]
    