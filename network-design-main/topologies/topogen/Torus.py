# Author: Alessandro Maissen

from .Topology import Topology
from .Jellyfish import Jellyfish
from .TorusGenerator import TorusGenerator
from .common import approx_inverse

class Torus(Topology):
    
    """
    Fields:
        Public:
            n: number of dimensions
            k: number of routers per "edge"
            p: number of hosts per router
            nr: network radix of router
            r: total radix of a router
            R: total number of routers
            N: total number of endnodes
            edge: number that indicates routers with endnodes (the first edge routers in topo have endnodes)
            name: name of topology (default := nDTorus)
        
        Private:
            __topo: holds None or the topology in adjacency list

    Methods: 
        get_topo(): return the topoology in adjacency list
        get_jellyfish_eq(): return jellyfish topology that uses same infrastructure
    """
    
    def __init__(self, n = -1, k = -1, N = -1):

        """
        Parameters:
            n: number of dimensions
            k: number of routers per "edge"
            N: total number of endnodes

        Note: Only two of the parameters have to be specified for initialization.

        """

        if(n == -1 and N != -1 and k != -1):
            self.n = approx_inverse(N, lambda n: k**n)
            self.k = k
        elif(k == -1 and N != -1 and n != -1):
            self.k = approx_inverse(N, lambda k: k**n)
            self.n = n
        elif(k != -1 and n != -1):
            self.k = k
            self.n = n
        elif(k == -1 and n == -1 and N != -1):
            # TODO: implement
            raise Exception("not yet implemented")
        else:
            raise Exception("invalid combination of arguments in constructor")
        
        self.p = 1
        self.nr = 2*self.n
        self.r = self.nr + self.p
        self.R = self.k**self.n
        self.N = self.R * self.p
        self.edge = self.R
        self.name = str(self.n) + 'DTorus'

        # private fields
        self.__topo = None

    def get_topo(self):
        if self.__topo is None:
            self.__topo = TorusGenerator().make(self.n, self.k)
        return self.__topo
    
    def get_jellyfish_eq(self):
        jf = Jellyfish(self.nr,self.R,self.p)
        jf.name += "-" + self.name
        return jf
