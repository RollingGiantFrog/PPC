# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 13:59:03 2019

@author: Victor
"""

import random as rd
import time

from itertools import izip
argmin = lambda array: min(izip(array, xrange(len(array))))[1]

class Node:
    def __init__(self, var, rank, parent, idx):
        self.children = [None,None]
        self.vars = set([var])
        self.rank = rank
        self.parent = parent
        self.idx = idx
        
    def addLabel(self,label):
        self.vars.add(label)
        
    def removeLabel(self,label):
        self.vars.remove(label)
        return len(self.vars) == 0

class Tree:
    def __init__(self,rankFunc):
        self.root = None
        self.min = None
        self.rank = rankFunc

    def getRoot(self):
        return self.root

    def add(self, var):
        if(self.root == None):
            self.root = Node(var,self.rank(var),None,-1)
            self.min = self.root
            return self.root
        else:
            rank = self.rank(var)
            node = self.addRec(var, rank, self.root)
            if self.min == None or rank < self.min.rank:
                self.min = node
            return node

    def addRec(self, var, rank, node):
        if rank < node.rank:
            if(node.children[0] != None):
                return self.addRec(var, rank, node.children[0])
            else:
                node.children[0] = Node(var,rank,node,0)
                return node.children[0]
        else:
            if rank == node.rank:
                node.addLabel(var)
                return node
            else:
                if(node.children[1] != None):
                    return self.addRec(var, rank, node.children[1])
                else:
                    node.children[1] = Node(var,rank,node,1)
                    return node.children[1]

    def delete(self, node, label):
        empty = node.removeLabel(label)
        
        if empty:
            if (node == self.min):
                successor = self.min.children[1]
                if successor != None:
                    while (successor.children[0] != None):
                        successor = successor.children[0]
                    self.min = successor
                else:
                    self.min = self.min.parent
                    
            if (node.children[0] == None):
                if (node.children[1] == None):
                    if (node != self.root):
                        node.parent.children[node.idx] = None
                    else:
                        self.root = None
                        
                else:
                    if (node != self.root):
                        node.parent.children[node.idx] = node.children[1]
                    else:
                        self.root = node.children[1]
                    node.children[1].parent = node.parent
                    node.children[1].idx = node.idx
                    
            else:
                if (node.children[1] == None):
                    if (node != self.root):
                        node.parent.children[node.idx] = node.children[0]
                    else:
                        self.root = node.children[0]
                    node.children[0].parent = node.parent
                    node.children[0].idx = node.idx
                    
                else:
                    parent = node
                    successor = node.children[1]
                    if (successor.children[0] == None):
                        if (node != self.root):
                            node.parent.children[node.idx] = successor
                        else:
                            self.root = successor
                        successor.parent = node.parent
                        successor.idx = node.idx
                        successor.children[0] = node.children[0]
                        node.children[0].parent = successor
                        
                    else:
                        while (successor.children[0] != None):
                            parent = successor
                            successor = successor.children[0]
                        
                        if (node != self.root):
                            node.parent.children[node.idx] = successor
                        else:
                            self.root = successor
                        successor.parent = node.parent
                        successor.idx = node.idx
                        successor.children[0] = node.children[0]
                        successor.children[1] = node.children[1]
                        node.children[0].parent = successor
                        node.children[1].parent = successor
                        parent.children[0] = None

    def getMin(self):
        return self.min

    def find(self, var):
        if(self.root != None):
            return self.findRec(var, self.root)
        else:
            return None

    def findRec(self, var, node):
        if(var == node.v):
            return node
        elif(var < node.v and node.children[0] != None):
            self.findRec(var, node.children[0])
        elif(var > node.v and node.children[1] != None):
            self.findRec(var, node.children[1])

    def deleteTree(self):
        self.root = None


# Implémentation par arbre binaire de recherche
class TreeBrancher:
    def rank(self,x):
        return [rank(self.backtrack,self.csp,x) for rank in self.rankFuncs]
    
    def __init__(self,backtrack,rankFuncs,instanciatedVars,otherVars):
        self.backtrack = backtrack
        self.csp = backtrack.csp
        self.variableOrder = instanciatedVars
        
        self.rankFuncs = rankFuncs
        self.tree = Tree(self.rank)
        self.nodes = [None for k in range(self.csp.size)]
        for var in otherVars:
            self.nodes[var] = self.tree.add(var)
            
        self.timeInc = 0
        self.timeDelete = 0
        self.timeAdd = 0
        
    def headRank(self):
        return self.tree.min.rank
        
    def head(self):
        label = None
        for var in self.tree.min.vars:
            label = var
            break
        return label
        
    def pop(self):
        t = time.clock()
        
        label = None
        for var in self.tree.min.vars:
            label = var
            break
        
        self.tree.delete(self.tree.min,label)
        self.nodes[label] = None
        self.variableOrder += [label]
        
        self.timeInc += time.clock()-t
        return label
        
    def push(self,y):
        self.nodes[y] = self.tree.add(y)
        
    def update(self,changedVars):
        t = time.clock()
        
        for var in changedVars:
            self.tree.delete(self.nodes[var],var)
            self.nodes[var] = None
        
        self.timeDelete += time.clock()-t
        
        t = time.clock()
        
        for var in changedVars:
            self.nodes[var] = self.tree.add(var)

        self.timeAdd += time.clock()-t
                
    def printStats(self):
        print("Time spent in Getting best variable from Brancher (sort) : " + str(self.timeInc))
        print("Time spent in Deleting variables from Brancher (sort) : " + str(self.timeDelete))
        print("Time spent in Adding variables to Brancher (sort) : " + str(self.timeAdd))


# Implémentation par tri à chaque appel
class SortBrancher:
    def rank(self,x):
        return [rank(self.backtrack,self.csp,x) for rank in self.rankFuncs]
    
    def __init__(self,backtrack,rankFuncs,instanciatedVars,otherVars):
        self.backtrack = backtrack
        self.csp = backtrack.csp
        self.rankFuncs = rankFuncs
        self.variableOrder = [(self.rank(var),var) for var in otherVars]
        
        self.timeSort = 0
        
    def head(self):
        self.variableOrder = [(self.rank(var[-1]),var[-1]) for var in self.variableOrder]
        self.variableOrder.sort(reverse=True)
        return self.variableOrder[-1][-1]
        
    def headRank(self):
        return self.rank(self.head())
        
    def pop(self):
        t = time.clock()
        
        self.variableOrder = [(self.rank(var[-1]),var[-1]) for var in self.variableOrder]
        self.variableOrder.sort(reverse=True)
        
        self.timeSort += time.clock()-t
        
        return self.variableOrder.pop()[-1]
        
    def push(self,y):
        self.variableOrder += [(self.rank(y),y)]
        
    def update(self,changedVars):
        pass
    
    def printStats(self):
        print("Time spent in Getting best variable from Brancher (sort) : " + str(self.timeSort))

# Implémentation par étages de tableaux
class ArrayBrancher:
    def rank(self,x):
        return [rank(self.backtrack,self.csp,x) for rank in self.rankFuncs]
    
    def __init__(self,backtrack,rankFuncs,instanciatedVars,otherVars):
        self.backtrack = backtrack
        self.csp = backtrack.csp
        
        self.maxDomainSize = 0
        for var in otherVars:
            if self.csp.domainSize(var) > self.maxDomainSize:
                self.maxDomainSize = self.csp.domainSize(var)
        
        self.rankFuncs = rankFuncs
        
        self.varsOfDomain = [[] for k in range(self.maxDomainSize+1)]
        self.varIndex = [-1 for k in range(self.csp.size)]
        self.varSize = [self.csp.domainSize(var) for var in instanciatedVars + otherVars]
        
        for var in otherVars:
            size = self.csp.domainSize(var)
            self.varsOfDomain[size] += [var]
            self.varIndex[var] = len(self.varsOfDomain[size])-1
        
        self.timeAdd = 0
        self.timeDelete = 0
        self.timeUpdate = 0
        
    def addVar(self,var):
        t = time.clock()        
        
        size = self.csp.domainSize(var)
        self.varSize[var] = size
        self.varsOfDomain[size] += [var]
        self.varIndex[var] = len(self.varsOfDomain[size])-1
        
        self.timeAdd += time.clock()-t
        
    def deleteVar(self,var):
        t = time.clock()
        
        idx = self.varIndex[var]
        size = self.varSize[var]
        self.varIndex[self.varsOfDomain[size][-1]] = idx
        self.varsOfDomain[size][-1],self.varsOfDomain[size][idx] = self.varsOfDomain[size][idx],self.varsOfDomain[size][-1]
        self.varsOfDomain[size].pop()
        
        self.varIndex[var] = -1
        
        self.timeDelete += time.clock()-t
      
    def head(self):
        size = 1
        while len(self.varsOfDomain[size]) == 0:
            size += 1
            
        ranks = [(self.rank(var),var) for var in self.varsOfDomain[size]]
        idx = argmin(ranks)
        var = ranks[idx][1]
        
        return var      

    def pop(self):
        size = 1
        while len(self.varsOfDomain[size]) == 0:
            size += 1
            
        ranks = [(self.rank(var),var) for var in self.varsOfDomain[size]]
        idx = argmin(ranks)
        var = ranks[idx][1]
        
        self.deleteVar(var)
        return var
        
    def push(self,x):
        self.addVar(x)
        
    def __contains__(self,x):        
        return self.varIndex[x] != -1
        
    def update(self,changedVars):
        t = time.clock()
        
        for var in changedVars:
            if var in self:
                self.deleteVar(var)
                self.addVar(var)
            
        self.timeUpdate += time.clock()-t
            
    def printStats(self):
        print("Time spent in Updating Brancher (Adds + Deletes) : " + str(self.timeUpdate))
        print("Time spent in Adding to Brancher : " + str(self.timeAdd))
        print("Time spent in Deleting to Brancher : " + str(self.timeDelete))
            