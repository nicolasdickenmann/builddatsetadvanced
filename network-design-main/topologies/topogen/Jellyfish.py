# Author: Alessandro Maissen

from .Topology import Topology
from .JellyfishGenerator import JellyfishGenerator

class Jellyfish(Topology):

    """
    Fields:
        Public:
            nr: network radix of routers
            R: total number of routers
            p: hosts per router
            r: total radix of routers
            N: total number of endnodes
            edge: number that indicates routers with endnodes (the first edge routers in topo have endnodes)
            name: name of topology (default := JF)
        Private:
            __topo: holds None or the topology in adjacency list

    Methods: 
        get_topo(): return the topoology in adjacency list
        get_jellyfish_eq(): not implemented

    """
    def __init__(self, nr, R, p):

        """
        Parameters:
            nr: network radix of routers
            R: total number of routers
            p: hosts per router
            
        """
        
        self.nr = nr
        self.R = R
        self.p = p
        self.r = self.nr + self.p
        self.N = self.R * self.p
        self.edge = self.R
        self.name = 'JF'

        # private fields
        self.__topo = None

    def get_topo(self):
        if self.__topo is None:
            self.__topo = JellyfishGenerator().make(self.nr, self.R)
        return self.__topo