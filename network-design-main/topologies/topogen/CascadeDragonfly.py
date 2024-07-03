# Author: Jascha Krattenmacher 

from .Topology import Topology
from .Jellyfish import Jellyfish
from .CascadeDragonflyGenerator import CascadeDragonflyGenerator
from .common import approx_inverse

class CascadeDragonfly(Topology):
    """
    Fields:
        Public:
            p: number of hosts per router
            nr: network radix of router
            r: total radix of a router
            R: total number of routers
            N: total number of endnodes
            edge: number that indicates routers with endnodes (the first edge routers in topo have endnodes)
            name: name of topology (default := CASDF)
        
        Private:
            __topo: holds None or the topology in adjacency list

    Methods: 
        get_topo(): return the topoology in adjacency list
        get_jellyfish_eq(): return jellyfish topology that uses same infrastructure

    """
    def __init__(self, g = -1, N = -1):

        """
        Parameters:
            g : number of groups
        """

        if(N == -1 and g != -1):
            self.g = g
        elif(N != -1 and g == -1):
            self.g = approx_inverse(N, lambda g: 96*4*g)
            if self.g > 241:
                print("maximum amount is 92'544 nodes routers of radix 48")
                print("set g = 241, N = 92544")
                self.g=241 
        else:
            raise Exception("invalid combination of arguments in constructor")

        assert(self.g > 0)
        self.p = 4 
        self.R = 96*self.g
        self.N = self.p * self.R
        self.fractional_nr = 30 + (4*(self.g-1))/96
        self.nr = int(round(self.fractional_nr))
        self.r = self.nr + self.p

        self.edge = self.R
        self.name = 'CASDF'


        # private fields
        self.__topo = None

    def get_topo(self):
        if self.__topo is None:
            self.__topo = CascadeDragonflyGenerator().make(self.g)
        return self.__topo
    
    def get_jellyfish_eq(self):
        jf = Jellyfish(self.nr,self.R,self.p)
        jf.name += "-" + self.name
        return jf


