# Author: Alessandro Maissen

from .Topology import Topology
from .Jellyfish import Jellyfish
from .OFTGenerator import OFTGenerator
from .common import approx_inverse, is_prime
from math import ceil

class OFT(Topology):
    
    """
    Fields:
        Public: 
            k: network radix of routers in layer 0 and layer 2
            p: host per router from layer 0 and layer 2
            nr: rounded (pseudo) network radix of router 
            Rl: routers per layer
            r: total radix of a router
            R: total number of routers
            N: total number of endnodes
            fractional_nr: exact (pseudo) network radix of router (2*edges/vertices)
            edge: number that indicates routers with endnodes (the first edge routers in topo have endnodes)
            name: name of topology (default := OFT)
        Private:
            __topo: holds None or the topology in adjacency list

    Methods: 
        get_topo(): return the topoology in adjacency list
        get_jellyfish_eq(): return jellyfish topology that uses same infrastructure
    """

    def __init__(self, k = -1, N = -1):
        
        """
        Parameters:
            k: network radix of routers in layer 0 and layer 2 (k:= q + 1 where q is prime)
            N: total number of endnodes

        Note: Only one of the parameters have to be specified for initialization.

        """

        assert(k != 1 or (k == -1 and N != -1)) 

        if(k == -1 and N != -1):
            candidate_k = approx_inverse(N, lambda k: 2*k**3 - 2*k**2 + 2*k)
            while(not is_prime(candidate_k - 1)):
                candidate_k += 1
            self.k = candidate_k
        elif(k != -1 and N== -1):
            self.k = k
        else:
            raise Exception("invalid combination of arguments in constructor")

        self.p = self.k
        self.Rl = 1 + self.k * (self.k - 1)
        self.r = 2*self.k
        self.R = 3 * self.Rl
        self.fractional_nr = 4*self.k*(1 + self.k*(self.k-1)) / self.R  # double check if correct
        self.nr = int(round(self.fractional_nr))
        self.N = 2 * self.k * self.Rl
        self.edge = 2 * self.Rl
        self.name = 'OFT'

        # private fields
        self.__topo = None

    def get_topo(self):
        if self.__topo is None:
            self.__topo = OFTGenerator().make(self.k)
        return self.__topo
    
    def get_jellyfish_eq(self):

        p = ceil(self.N / self.R) # ceiling because we want at least as many endnodes in JF as in MLFM
        nr = self.r - p

        jf = Jellyfish(nr,self.R,p)
        jf.name += "-" + self.name
        return jf