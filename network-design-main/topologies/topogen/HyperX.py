# Author: Alessandro Maissen

from .Topology import Topology
from .Jellyfish import Jellyfish
from .HyperXGenerator import HyperXGenerator
from .common import approx_inverse

class HyperX(Topology):

    """
    Fields:
        Public:
            l: number of dimensions
            s: number of nodes per dimension
            R: total number of routers
            p: number hosts per router
            nr: network radix of routers
            r: total radix of routers
            N: total number of endnodes  
            edge: number that indicates routers with endnodes (the first edge routers in topo have endnodes)
            name: name of topology (default := HX)
        Private:
            __topo: holds None or the topology in adjacency list

    Methods: 
        get_topo(): return the topoology in adjacency list
        get_jellyfish_eq(): return jellyfish topology that uses same infrastructure
    """

    def __init__(self, l = -1, s = -1, N = -1):

        """
        Parameters:
            l: number of dimensions
            s: number of nodes per dimension
            N: total number of endnodes

        Note: Only two of the parameters have to be specified for initialization.

        """

        if(l == -1 and N != -1 and s != -1):
            self.l = approx_inverse(N, lambda l: s**l*(s-1))
            self.s = s
        elif(s == -1 and N != -1 and l != -1):
            self.s = approx_inverse(N, lambda s: s**l*(s-1))
            self.l = l
        elif(l != -1 and s != -1):
            self.l = l
            self.s = s
        elif(l == -1 and s == -1 and N != -1):
            # TODO: implement
            raise Exception("not yet implemented")
        else:
            raise Exception("invalid combination of arguments in constructor")

        self.R = self.s ** self.l
        self.p = self.s - 1  # this is a design choose, if you change this you should also change the lambda functions above
        self.nr = self.l * (self.s - 1)
        self.r = self.nr + self.p
        self.N = self.R * self.p
        self.edge = self.R
        self.name = 'HX' + str(self.l)

        # private fields
        self.__topo = None

    def get_topo(self):
        if self.__topo is None:
            self.__topo = HyperXGenerator().make(self.l, self.s)
        return self.__topo
    
    def get_jellyfish_eq(self):
        jf = Jellyfish(self.nr,self.R,self.p)
        jf.name += "-" + self.name
        return jf