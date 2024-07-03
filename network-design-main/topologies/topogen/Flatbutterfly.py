# Author: Alessandro Maissen

from .Topology import Topology
from .Jellyfish import Jellyfish
from .FlatbutterflyGenerator import FlatbutterflyGenerator
from .common import approx_inverse

class Flatbutterfly(Topology):

    """
    Fields:
        Public: 
            n: number of dimensions
            k: ? 
            p: number of hosts per router (p:= k)
            nr: network radix of router
            r: total radix of a router
            R: total number of routers
            N: total number of endnodes
            edge: number that indicates routers with endnodes (the first edge routers in topo have endnodes)
            name: name of topology (default := FB)
        
        Private:
            __topo: holds None or the topology in adjacency list

    Methods: 
        get_topo(): return the topoology in adjacency list
        get_jellyfish_eq(): return jellyfish topology that uses same infrastructure
    """
    
    def __init__(self, n = -1, k = -1, N = -1):

        """
        Fields:
            n: number of dimensions
            k: ?
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

        self.p = self.k
        self.nr = self.n * (self.k - 1) + 1 - self.k
        self.r = self.n * (self.k - 1) + 1
        self.R = self.k**(self.n - 1)
        self.N = self.R * self.p
        self.edge = self.R
        self.name = str(self.n - 1) + 'DFB' # a k-ary n-flat is flattened butterfly in n-1 dimensions

        # private fields
        self.__topo = None

    def get_topo(self):
        if self.__topo is None:
            self.__topo = FlatbutterflyGenerator().make(self.n, self.k)
        return self.__topo
    
    def get_jellyfish_eq(self):
        jf = Jellyfish(self.nr,self.R,self.p)
        jf.name += "-" + self.name
        return jf