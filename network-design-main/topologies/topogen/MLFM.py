# Author: Alessandro Maissen

from .Topology import Topology
from .Jellyfish import Jellyfish
from .MLFMGenerator import MLFMGenerator
from .common import approx_inverse
from math import ceil

class MLFM(Topology):
    
    """
    Fields:
        Public:
            h: network radix of local routers
            l: number of layers (l:= h)
            p: number of endnodes per local router (p:= h)
            nr: rounded (pseudo) network radix of router
            Rg: number of global routers
            Rl: number of local routers per layer
            r: total radix of routers
            R: total number of routers
            N: total number of attachable hosts
            fractional_nr: exact (pseudo) network radix of router (2*edges/vertices)
            edge: number that indicates routers with endnodes (the first edge routers in topo have endnodes)
            name: name of topology (default := MLFM)
        
        Private:
            __topo: holds None or the topology in adjacency list

    Methods: 
        get_topo(): return the topoology in adjacency list
        get_jellyfish_eq(): return jellyfish topology that uses same infrastructure
    """

    def __init__(self, h = -1, N = -1):

        """
        Parameters:
            h: network radix of local routers
            N: total number of endnodes

        Note: Only one of the parameters have to be specified for initialization.

        """

        assert(h != -1 or N != -1)

        if(h == -1 and N != -1):
            self.h = approx_inverse(N, lambda h: h**3 + h**2)
        elif(h != 1 and N == -1):
            self.h = h
        else:
            raise Exception("invalid combination of arguments in constructor")
        
        self.l = self.h
        self.p = self.h
        self.Rg = int((self.h * (self.h + 1)) / 2)
        self.Rl = self.h + 1
        self.r = 2*self.l
        self.R = self.Rg + (self.l * self.Rl)
        self.fractional_nr = 2*self.l * self.Rl * (self.Rl - 1) / self.R  # double check if correct
        self.nr = int(round(self.fractional_nr))
        self.N = self.l * self.Rl * self.p
        self.edge = self.l *self.Rl
        self.name = 'MLFM'

        # private fields
        self.__topo = None

    def get_topo(self):
        if self.__topo is None:
            self.__topo = MLFMGenerator().make(self.h)
        return self.__topo
    
    def get_jellyfish_eq(self):

        p = ceil(self.N / self.R) # ceiling because we want at least as many endnodes in JF as in MLFM
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