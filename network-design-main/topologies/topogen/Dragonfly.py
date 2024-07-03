# Author: Alessandro Maissen

from .Topology import Topology
from .Jellyfish import Jellyfish
from .DragonflyGenerator import DragonflyGenerator
from .common import approx_inverse

class Dragonfly(Topology):
    
    """
    Fields:
        Public: 
            p: number of hosts per router
            h: number of channels per router connecting to routers of other groups
            a: number of routers in each group
            nr: network radix of a router
            r: total radix of a router
            g: total number of groups
            R: total number of routers
            N: toal number of endnodes
            edge: number that indicates routers with endnodes (the first edge routers in topo have endnodes)
            name: name of topology (default := DF)
        
        Private:
            __topo: holds None or the topology in adjacency list

    Methods: 
        get_topo(): return the topoology in adjacency list
        get_jellyfish_eq(): return jellyfish topology that uses same infrastructure

    """
   
    def __init__(self, p = -1 , N = -1):

        """
        Parameters:
            p: number of hosts per router
            N: total number of endnodes

        Note: Only one of the parameters have to be specified for initialization.

        """
        
        if(p == -1 and N != -1):
            self.p = approx_inverse(N, lambda p: 4*p**4 + 2*p**2)
        elif(p != -1 and N == -1):
            self.p = p
        else:
            raise Exception("invalid combination of arguments in constructor")

        self.h = self.p
        self.a = 2*self.p
        self.nr = self.h + self.a - 1
        self.r = self.nr + self.p
        self.g = self.a*self.h + 1
        self.R = self.g * self.a
        self.N = self.p * self.R

        assert(self.g == 2*self.p**2 + 1)
        assert(self.R == 4*self.p**3 + 2*self.p)
        assert(self.N == 4*self.p**4 + 2*self.p**2)

        self.edge = self.R
        self.name = 'DF'

        # private fields
        self.__topo = None

    def get_topo(self):
        if self.__topo is None:
            self.__topo = DragonflyGenerator().make(self.p)
        return self.__topo
    
    def get_jellyfish_eq(self):
        jf = Jellyfish(self.nr,self.R,self.p)
        jf.name += "-" + self.name
        return jf
