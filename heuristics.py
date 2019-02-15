# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 17:11:22 2019

@author: Victor
"""

# Ordonne les variables X du csp par ordre croissant de taille de domaine
def smallestDomain(csp,X):
    variableDomSize = []
    for x in X:
        variableDomSize += [(csp.domainSize(x),x)]
    variableDomSize.sort()
    return [e[1] for e in variableDomSize]
    

# Ordonne les variables X du csp par ordre décroissant de taille de domaine
def largestDomain(csp,X):
    variableDomSize = []
    for x in X:
        variableDomSize += [(csp.domainSize(x),x)]
    variableDomSize.sort(reverse=True)
    return [e[1] for e in variableDomSize]
    