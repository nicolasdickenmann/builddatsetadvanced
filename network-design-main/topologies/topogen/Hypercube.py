# Author: Alessandro Maissen

from .Topology import Topology
from .Jellyfish import Jellyfish
from .HypercubeGenerator import HypercubeGenerator
from .common import approx_inverse

class Hypercube(Topology):
    
    """
    Fields:
        Public:
            n: number of dimensions
            p: number of hosts per router
            nr: network radix of router
            r: total radix of a router
            R: total number of routers
            N: total number of endnodes
            edge: number that indicates routers with endnodes (the first edge routers in topo have endnodes)
            name: name of topology (default := HC)
        
        Private:
            __topo: holds None or the topology in adjacency list

    Methods: 
        get_topo(): return the topoology in adjacency list
        get_jellyfish_eq(): return jellyfish topology that uses same infrastructure

    """
    def __init__(self, n = -1, N = -1):

        """
        Parameters:
            n: number of dimensions
            N: total number of endnodes

        Note: Only one of the parameters have to be specified for initialization.

        """

        assert(n != 1 or (n == -1 and N != -1)) 

        if(n == -1 and N != -1):
            self.n = approx_inverse(N, lambda n: 2**n)
        elif(n != -1 and N == -1):
            self.n = n
        else:
            raise Exception("invalid combination of arguments in constructor")
        
        self.p = 1
        self.nr = self.n
        self.r = self.nr + self.p
        self.R = 2**self.n
        self.N = 2**self.n * self.p
        self.edge = self.R
        self.name = 'HC'

        # private fields
        self.__topo = None

    def get_topo(self):
        if self.__topo is None:
            self.__topo = HypercubeGenerator().make(self.n)
        return self.__topo
    
    def get_jellyfish_eq(self):
        jf = Jellyfish(self.nr,self.R,self.p)
        jf.name += "-" + self.name
        return jf