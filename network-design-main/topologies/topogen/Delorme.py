# Author: Alessandro Maissen

from .Topology import Topology
from .Jellyfish import Jellyfish
from .DelormeGenerator import DelormeGenerator
import numpy as np
from .common import read_listgraph
class Delorme(Topology):
    
    """
    Fields:
        Public: 
            q: size of Gallois Field
            p: hosts per router
            nr: network radix of router 
            r: total radix of a router
            R: total number of routers
            N: total number of endnodes
            edge: number that indicates routers with endnodes (the first edge routers in topo have endnodes)
            alpha: where q = 2^(2*a-1)
            sigma: where sigma = 2^a
            name: name of topology (default := DEL)
        Private:
            __topo: holds None or the topology in adjacency list

    Methods: 
        get_topo(): return the topoology in adjacency list
        get_jellyfish_eq(): return jellyfish topology that uses same infrastructure
    """

    def __init__(self, q = -1, N = -1):
        
        """
        Parameters:
            q: size of Gallois Field

        """
        if(q == -1 and N != -1):
            if N >= 10000:
                self.q = 32
            else:
                self.q = 8
        elif(q != -1 and N == -1):
            self.q = q
        else:
            raise Exception("invalid combination of arguments in constructor")

        self.alpha = int((np.log2(self.q) + 1)/2)
        self.sigma = 2**self.alpha
        self.nr = self.q+1
        self.p = int(self.nr/0.75-self.nr)
        self.r = self.p + self.nr
        self.R = (self.q+1)*(self.q**2+1)
        self.N = self.p*self.R
        self.edge = self.R
        self.name = 'DEL'

        # private fields
        self.__topo = None

    def get_topo(self):
        if self.__topo is None:
            # self.__topo = DelormeGenerator().make(self.q)
            self.__topo = read_listgraph("data/Delormes/Delorme."+str(self.q)+".adj.txt")
        return self.__topo
    
    def get_jellyfish_eq(self):
        jf = Jellyfish(self.nr,self.R,self.p)
        jf.name += "-" + self.name
        return jf