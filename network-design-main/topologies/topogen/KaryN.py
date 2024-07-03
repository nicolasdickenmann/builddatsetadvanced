# Author: Jascha Krattenmacher

from .Topology import Topology
from .Jellyfish import Jellyfish
from .KaryNGenerator import KaryNGenerator
from .common import approx_inverse
from math import ceil

class KaryN(Topology):
    """
    Fields:
        Public:
            k: half the number of ports for each switch
            n: numbers of levels in the tree 
            p: number of hosts per router
            nr: network radix of router
            r: total radix of a router
            R: total number of routers
            N: total number of endnodes
            edge: number that indicates routers with endnodes (the first edge routers in topo have endnodes)
            name: name of topology (default := KNT)
        
        Private:
            __topo: holds None or the topology in adjacency list

    Methods: 
        get_topo(): return the topoology in adjacency list
        get_jellyfish_eq(): return jellyfish topology that uses same infrastructure

    """
    def __init__(self, k = -1, n = -1, N = -1):

        """
        Parameters:
            k: half the number of ports for each switch
            n: number of levels in the tree
        """
        if(k != -1 and N != -1 and n == -1):
            self.n = approx_inverse(N, lambda n: k**(n))
            self.k = k
        elif(k == -1 and N != -1 and n != -1):
            self.k = approx_inverse(N, lambda k: k**(n))
            self.n = n
        elif(k != -1 and n != -1):
            self.k = k
            self.n = n
        elif(k == -1 and n == -1 and N != -1):
            self.k, self.n = getConfig(N)
        else:
            raise Exception("invalid combination of arguments in constructor")

        self.p = self.k 
        self.R = self.n*self.k**(self.n - 1)
        self.N = self.k ** self.n
        self.edge = self.k**(self.n - 1) 
        self.name = 'KNT'
        self.fractional_nr =  2*(self.n-1)*self.k**(self.n)/self.R
        self.nr = int(round(self.fractional_nr))
        self.fractional_r = ((2*self.n - 1)*self.k**(self.n))/self.R
        self.r = int(round(self.fractional_r))

        # private fields
        self.__topo = None

    def get_topo(self):
        if self.__topo is None:
            self.__topo = KaryNGenerator().make(self.k, self.n)
        return self.__topo
    
    def get_jellyfish_eq(self):

        p = ceil(self.N / self.R) # ceiling because we want at least as many endnodes in JF as in original network 
        nr = int(round(self.fractional_r - p)) # radix is rounded since radix might be fractional

        jf = Jellyfish(nr,self.R,p)
        jf.name += "-" + self.name
        return jf


################# Helper Functions ############################

def getConfig(N : int):

    if N == 1000:
        k = 8
    elif N == 10000:
        k = 16
    else:
        k = 24 

    return k, approx_inverse(N, lambda n: k**(n))

