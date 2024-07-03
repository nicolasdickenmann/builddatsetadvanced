# Author: Alessandro Maissen

from .Topology import Topology
from .Jellyfish import Jellyfish
from .FatTreeGenerator import FatTreeGenerator
from .common import approx_inverse
from math import ceil

class FatTree(Topology):

    """
    Fields:
        Public: 
            p: number of hosts per edge router
            nr: (pseudo) network radix of router (2*edges/vertices)
            r: total radix of a router (=k)
            R: total number of routers
            N: toal number of endnodes
            fractional_nr: exact (pseudo) network radix of a router (2*edges/routers)
            edge: number that indicates routers with endnodes (the first edge routers in topo have endnodes)
            name: name of topology (default := FT)
        
        Private:
            __topo: holds None or the topology in adjacency list

    Methods: 
        get_topo(): return the topoology in adjacency list
        get_jellyfish_eq(): return jellyfish topology that uses same infrastructure

    """

    def __init__(self, k = -1, N = -1):
        

        if k == -1 and N != -1:
            self.k = approx_inverse(N, lambda k: (k**3/4))
            if self.k % 2 != 0:
                self.k += 1
        elif k != 1 and N == -1 and k % 2 == 0:
            self.k = k
        else:
            raise Exception("invalid combination of arguments in constructor or k is not even")
        
        assert(self.k % 2 == 0)
        
        self.p = int(self.k / 2)
        self.r = self.k
        self.R = int((5*self.k**2)/4)
        self.fractional_nr = (self.k*(self.k**2)/4 + self.k*self.k*(self.k/2) + self.k*(self.k/2)*(self.k/2)) / self.R # pseduo network radix (2*edges/routers)
        self.nr = int(round(self.fractional_nr))
        self.edge = int((self.k**2)/2)
        self.N = self.edge * self.p
        
        assert(self.N == (self.k**3)/4)
        
        self.name = 'FT'
        
        # private fields
        self.__topo = None
    

    def get_topo(self):
        if self.__topo is None:
            self.__topo = FatTreeGenerator().make(self.k)
        return self.__topo
    
    def get_jellyfish_eq(self):

        p = ceil(self.N / self.R) # ceiling because we want at least as many endnodes in JF as in FT
        nr = self.r - p

        # enforce precondictions for jellyfish
        if self.R*nr % 2 != 0:
            # implies nr is odd
            nr -= 1
            p += 1

        assert(self.r == p + nr)

        jf = Jellyfish(nr,self.R,p)
        jf.name += "-" + self.name
        return jf

class FatTree2x(Topology): ## TODO: How are te jellyfish eq. defined?

    """
    Fields:
        Public: 
            p: number of hosts per edge router
            nr: rounded (pseudo) network radix of a router
            r: rounded (pseudo) radix of a router
            R: total number of routers
            N: toal number of endnodes
            fractional_nr: exact (pseudo) network radix of a router (2*edges/routers)
            fractional_r: exact (pseudo) radix of a router (2*edges/routers) inkl. edges to endnodes
            edge: number that indicates routers with endnodes (the first edge routers in topo have endnodes)
            name: name of topology (default := FT)
        
        Private:
            __topo: holds None or the topology in adjacency list

    Methods: 
        get_topo(): return the topoology in adjacency list
        get_jellyfish_eq(): return jellyfish topology that uses same infrastructure

    """

    def __init__(self, k = -1, N = -1):
        

        if k == -1 and N != -1:
            self.k = approx_inverse(N, lambda k: (k**3/2))
            if self.k % 2 != 0:
                self.k += 1
        elif k != 1 and N == -1 and k % 2 == 0:
            self.k = k
        else:
            raise Exception("invalid combination of arguments in constructor or k is not even")
        
        assert(self.k % 2 == 0)
        
        self.p = self.k
        self.fractional_r = 6*self.k/5
        self.r = int(round(self.fractional_r))
        self.R = int((5*self.k**2)/4)
        self.fractional_nr = (self.k*(self.k**2)/4 + self.k*self.k*(self.k/2) + self.k*(self.k/2)*(self.k/2)) / self.R # pseduo network radix (2*edges/routers)
        self.nr = int(round(self.fractional_nr))
        self.edge = int((self.k**2)/2)
        self.N = self.edge * self.p
        
        assert(self.N == (self.k**3)/2)
        
        self.name = 'FT2x'
        
        # private fields
        self.__topo = None
    

    def get_topo(self):
        if self.__topo is None:
            self.__topo = FatTreeGenerator().make(self.k)
        return self.__topo
    
    def get_jellyfish_eq(self):

        p = ceil(self.N / self.R) # ceiling because we want at least as many endnodes in JF as in FT2x
        nr = int(round(self.fractional_r - p)) # radix is rounded since radix might be fractional

        # enforce precondictions for jellyfish
        if self.R*nr % 2 != 0:
            # implies nr is odd
            nr -= 1
            p += 1


        jf = Jellyfish(nr,self.R,p)
        jf.name += "-" + self.name
        return jf