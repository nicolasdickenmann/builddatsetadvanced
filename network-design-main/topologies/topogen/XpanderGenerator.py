# Author: Marcel Schneider and Alessandro Maissen

# Xpander
# Implemented based on Xpander: Towards Optimal-Performance Datacenters

# PARAMETERS
# d: specifies the initial d-regular complete graph with d+1 vertices
# lifts : specifies the lifts

# VARIABLES
#

# ADDITIONAL NOTES:
#

import random
from .TopologyGenerator import TopologyGenerator
from .validate_xpander import validate

class XpanderGenerator(TopologyGenerator):

    def __init(self):
        super(XpanderGenerator,self).__init__()
    
    def make(self, d : int, lifts : [int]) -> [[int]]:
        g = K(d+1)
        for q in lifts:
            g = lift(g, q)
        return g

    def validate(self, topo : [[int]], d : int, lifts : [int]) -> bool:
        return validate(topo,d,lifts)
    
    def get_folder_path(self):
        return super(XpanderGenerator,self).get_folder_path() + "xpanders/"

    def get_file_name(self, d : int, lifts : [int]) -> str:
        return "Xpander." + str(d) + ".lifts." + ".".join(str(lift) for lift in lifts) + ".adj.txt"

# ---------------- helper functions ----------------

# simple integer factorization
def onefactor(x, q):
    if x % q == 0: return (int(x/q), q)
    return onefactor(x, q+1)

def factors(x, q = 2):
    if x == 1: return []
    else:
        y, p = onefactor(x, q)
        return [p] + factors(y, p)

def inv(perm):
    inverse = [0] * len(perm)
    for i, p in enumerate(perm):
        inverse[p] = i
    return inverse

# fully connected graphs
def K(n):
    return [[j for j in range(n) if j != i] for i in range(n)]

# random k-lift of g
def lift(g, k):
    perms = {}
    def perm(e1, e2):
        if (e1, e2) not in perms:
            p = list(range(k))
            random.shuffle(p)
            perms[(e1, e2)] = p
            perms[(e2, e1)] = inv(p)
        return perms[(e1, e2)]
    
    # copy g k-times (loop order is strange here), rewire edges by random matching
    graph = [[e2 + perm(e1, e2)[i]*len(g) for e2 in node] for i in range(k) for e1, node in enumerate(g)]
    return graph