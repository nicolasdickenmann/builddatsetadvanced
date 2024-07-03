# Author: Jascha Krattenmacher

from .Topology import Topology
from .Jellyfish import Jellyfish
from .common import approx_inverse
from .SpectralflyGenerator import SpectralflyGenerator, legendre
from collections import OrderedDict
from bisect import bisect_left
from math import sqrt,log

class Spectralfly(Topology):
    
    """
    Fields:
        Public: 
            p: number of hosts per router
            nr: network radix of a router
            r: total radix of a router
            g: total number of groups
            R: total number of routers
            N: toal number of endnodes
            edge: number that indicates routers with endnodes (the first edge routers in topo have endnodes)
            name: name of topology (default := SpF)
        
        Private:
            __topo: holds None or the topology in adjacency list

    Methods: 
        get_topo(): return the topoology in adjacency list
        get_jellyfish_eq(): return jellyfish topology that uses same infrastructure

    """
   
    def __init__(self, v = -1, w = -1, N = -1):

        """
        Parameters:
            v,w primes: 
            N: total number of endnodes

        Note: Only one of the parameters have to be specified for initialization.

        """
        
        if(N != -1):
            self.v, self.w = get_config(N)
        elif(v != -1 and w != -1):
            self.v = v
            self.w = w
        else:
            raise Exception("invalid combination of arguments in constructor")

        sym     = legendre(self.v,self.w)
        assert(sym==1 or sym==-1)
        self.R = ((3-sym)*(self.w*self.w*self.w-self.w))//4
        self.p = self.v - 1 
        self.nr = self.v + 1 
        self.r = self.nr + self.p 
        self.N = self.p*self.R

        self.edge = self.R 
        self.name = 'SpF'


        # private fields
        self.__topo = None

    def get_topo(self):
        if self.__topo is None:
            self.__topo = SpectralflyGenerator().make(self.v, self.w)
        return self.__topo
    
    def get_jellyfish_eq(self):
        jf = Jellyfish(self.nr,self.R,self.p)
        jf.name += "-" + self.name
        return jf


############## Hepler Function ##################

def get_config(N : int):

    #return 3,11

    # approximate p and q, bad performance, alternatively manually calculate values and return
    return approx(N)

def prime_numbers(n : int):

    primes = []

    for i in range(3, n + 1):
        for j in range(2, int(i ** 0.5) + 1):
            if i%j == 0:
                break
        else:
            primes.append(i)
    return primes

def generate_dict(n : int):

    primes = prime_numbers(int(sqrt(n)+1))
    primes_dict = OrderedDict()

    for p in primes:
        for q in primes:
            if q > 2*sqrt(p):
                sym     = legendre(p, q)
                if not (sym==1 or sym==-1):
                    continue
                nodes = ((3-sym)*(q*q*q-q)*(p-1))//4
                primes_dict[nodes] = (p,q)

    return primes_dict

def approx (N : int):
    primes_dict = generate_dict(N)
    nodes_list = sorted(list(primes_dict.keys()))
    pq = 0
    for key in nodes_list:
        #print("key: %i    primes:%s" %(key,str(primes_dict[key])))
        if key > N:
            pq = primes_dict[key]
            break

    p = pq[0]
    q = pq[1]
    sym = legendre(p,q)
    print("for N=%i approx=%i with p,q = %i,%i" %(N,((3-sym)*(q*q*q-q)*(p-1))//4, p, q))
    return p,q

