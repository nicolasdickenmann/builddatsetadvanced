# Author: Alessandro Maissen
# Slim Fly
# Implemented based on Paper: Slim Fly: A Cost Effective Low-Diameter Network Topology

# PARAMETERS
# q: size of Galois Field (q:= 4w + delta, where delta = -1 | 0 | 1 and q power of prime) 

# VARIABLES
# X: 1st generator set
# XX: 2nd generator set (=X')

# PRECONDITIONS
# q:= 4w + delta and q power of prime

# ADDITIONAL NOTES:
# Uses SymPy for Galois Fields


from .TopologyGenerator import TopologyGenerator
from .validate_slimfly import validate
from .common import get_power_of_prime

import itertools
import random
from functools import reduce
from sympy import symbols, Dummy
from sympy.polys.domains import ZZ
from sympy.polys.galoistools import (gf_irreducible_p, gf_add, gf_sub, gf_mul, gf_rem, gf_gcdex)
from sympy.ntheory.primetest import isprime

class SlimFlyGenerator(TopologyGenerator):
    
    def __init(self):
        super(SlimFlyGenerator,self).__init__()
    
    def make(self, q : int ):
        assert((q-1) % 4 == 0 or (q+1) % 4 == 0 or q % 4 == 0)
        
        #print(get_power_of_prime(q))
        prime,prime_power = get_power_of_prime(q)
        assert(prime != 0 and prime_power != 0 and prime**prime_power == q)

        # find the form q = 4w + delta, where delta is 0 | 1 | -1
        w = 0
        delta = 0
        if q % 4 == 3: 
            delta = -1
        elif q % 4 == 2:
            raise Exception("q is not of the form q:= 4w + delta")
        else: 
            delta = q % 4
        
        assert((q - delta) % 4 == 0)
        w = int((q - delta) / 4)
        assert(w >= 1)

        # constructing Galois Field and compute primitive element
        gf = GF(prime,prime_power)
        pe = gf.get_primitive_elem()
        #print(pe)

        # precomputing primitive element powers
        pe_powers = [[1]]
        for i in range(1,q):
            pe_powers.append(gf.mul(pe_powers[i-1],pe))
        
        #print(pe_powers)
        # buliding sets X and XX (=X') according to delta
        X = [[]]
        XX = [[]]
        if delta == 0:
            X = [pe_powers[i] for i in range(0,q-1) if i % 2 == 0]
            XX = [pe_powers[i] for i in range(1,q) if i % 2 == 1]
        elif delta == 1:
            X = [pe_powers[i] for i in range(0,q-2) if i % 2 == 0]
            XX = [pe_powers[i] for i in range(1,q-1) if i % 2 == 1]
        elif delta == -1:
            X = [pe_powers[i] for i in range(0,2*w-1) if i % 2 == 0]
            X.extend([pe_powers[i] for i in range(2*w-1,4*w-2) if i % 2 == 1])
            XX = [pe_powers[i] for i in range(1,2*w) if i % 2 == 1]
            XX.extend([pe_powers[i] for i in range(2*w,4*w-1) if i % 2 == 0])
        else:
            raise Exception("wrong delta, should not occur")
        
        #print(X)
        #print(XX)

        # perpare graph and labels
        labels = [(v,x,y) for v in [1,0] for x in gf.get_elems() for y in gf.get_elems()]
        assert(len(labels) == 2*q**2)
        #print(labels)
        maps = list(zip(labels,[i for i in range(2*q**2)]))
        graph = [[] for _ in range(2*q**2)]
        #print(maps)

        # interconnect routers based on scheme
        for s in maps:
            for t in maps:
        
                #print("pairs: %s %s" % s,t)
                #print(gf.sub(s[0][2],t[0][2]))
                # router (0,x,y) is connected to (0,x,y′) iff y − y′ ∈ X
                if s[0][0] == 0 and t[0][0] == 0 and s[0][1] == t[0][1] and gf.sub(s[0][2],t[0][2]) in X:
                    #print("hit 1: %s %s" % (s,t))
                    graph[s[1]].append(t[1])
                
                # router (1,m,c) is connected to (1,m,c′) iff c − c′ ∈ XX (=X')
                if s[0][0] == 1 and t[0][0] == 1 and s[0][1] == t[0][1] and gf.sub(s[0][2],t[0][2]) in XX:
                    #print("hit 2: %s %s" % (s,t))
                    graph[s[1]].append(t[1])
                
                # router (0,x,y) is connected to (1,m,c) iff y = mx + c
                if s[0][0] == 0 and t[0][0] == 1 and s[0][2] == gf.add(gf.mul(t[0][1],s[0][1]),t[0][2]):
                    #print("hit 3: %s %s" % (s,t))
                    graph[s[1]].append(t[1])
                    graph[t[1]].append(s[1])

        return graph  

    def validate(self, topo : [[int]], q : int) -> bool:
        return validate(topo,q)
    
    def get_folder_path(self):
        return super(SlimFlyGenerator,self).get_folder_path() + "slimflies/"

    def get_file_name(self, q : int) -> str:
        return "SlimFly." + str(q) + ".adj.txt"


# Class to construct Fields for q = p^m, p prime. 
# Based on: https://stackoverflow.com/questions/48065360/interpolate-polynomial-over-a-finite-field/48067397#48067397
# with some additional methods for finding primitive elements
# Polynomials are represented as lists where the highest coeff is first e.g [] = 0, [1,0] = x, [2] = 2
class GF():

    def __init__(self, p, n=1):
        p, n = int(p), int(n)
        if not isprime(p):
            raise ValueError("p must be a prime number, not %s" % p)
        if n <= 0:
            raise ValueError("n must be a positive integer, not %s" % n)
        self.p = p
        self.n = n
        if n == 1:
            self.reducing = [1, 0]
        else:
            for c in itertools.product(range(p), repeat=n):
                poly = (1, *c)
                if gf_irreducible_p(poly, p, ZZ):
                    self.reducing = poly
                    break
        self.elems = None
    
    def get_elems(self):

        if self.elems is None:
            self.elems = [[]]
            for c in range(1, self.p):
                self.elems.append([c])
            for deg in range(1,self.n):
                for c in itertools.product(range(self.p), repeat=deg):
                    for first in range(1, self.p):
                        self.elems.append(list((first, *c)))
            return self.elems
        else:
            return self.elems
    
    def get_primitive_elem(self):
        while True:
            primitive = random.choice(self.get_elems())
            if self.is_primitive_elem(primitive):
                return primitive

    def get_all_primitive_elems(self):
        return [elem for elem in self.get_elems() if self.is_primitive_elem(elem)]

    def is_primitive_elem(self, primitive) -> bool:

        elems = [[]]
        tmp = [1]
        for _ in range(1,self.p**self.n):
            tmp = self.mul(tmp,primitive)
            elems.append(tmp)

        if len(elems) == self.p**self.n and all(elem in elems  for elem in self.get_elems()):
            return True
        else:
            return False

    def add(self, x, y):
        return gf_add(x, y, self.p, ZZ)

    def sub(self, x, y):
        return gf_sub(x, y, self.p, ZZ)

    def mul(self, x, y):
        return gf_rem(gf_mul(x, y, self.p, ZZ), self.reducing, self.p, ZZ)

    def inv(self, x):
        s, t, h = gf_gcdex(x, self.reducing, self.p, ZZ)
        return s

    def eval_poly(self, poly, point):
        val = []
        for c in poly:
            val = self.mul(val, point)
            val = self.add(val, c)
        return val