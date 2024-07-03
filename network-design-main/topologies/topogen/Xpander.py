# Author: Alessandro Maissen

from .Topology import Topology
from .Jellyfish import Jellyfish
from .XpanderGenerator import XpanderGenerator
from .common import approx_inverse
from functools import reduce

class Xpander(Topology):

    """
    Fields:
        Public: 
            p: number of hosts per router
            nr: network radix of a router
            r: total radix of a router
            R: total number of routers
            N: toal number of endnodes
            edge: number that indicates routers with endnodes (the first edge routers in topo have endnodes)
            name: name of topology (default := Xpander)
        
        Private:
            __topo: holds None or the topology in adjacency list

    Methods: 
        get_topo(): return the topoology in adjacency list
        get_jellyfish_eq(): return jellyfish topology that uses same infrastructure

    """

    def __init__(self, d = -1 ,lifts = None, N = -1, lifting_strategy = None):

        """
        Parameters:
            d: regularity of Xpander (= network radix)
            N: total number of endnodes

        Note: Either provide d and lifts (as array) or lift strategy and N to create a Xpander

        """

        if (N != -1 and lifting_strategy == 'simple' and d == -1 and lifts is None):     
            q = approx_inverse(N,lambda x: (2**x + 1) * (2**x) * 2**(x-1))
            self.nr = 2**q
            self.lifts = [self.nr]
            assert(self.nr*self.lifts[0] == 2**(2*q))
            self.name = 'Xp'
        elif (N != -1 and lifting_strategy == '2-lifts' and d == -1 and lifts is None):
            q = approx_inverse(N,lambda x: (2**x + 1) * (2**x) * 2**(x-1))
            self.nr = 2**q
            self.lifts = [2] * q
            assert(self.nr * reduce(lambda x,y: x*y, self.lifts , 1) == 2**(2*q))
            self.name = 'Xpp'
        elif (N == -1 and lifting_strategy == None and d != -1 and lifts is not None):
            self.nr = d
            self.lifts = lifts
            self.name = 'Xpander'
        else:
            raise Exception("invalid combination of arguments in constructor")

        assert(self.nr % 2 == 0)

        self.p = int(self.nr/2)
        self.r = self.p + self.nr
        self.R = (self.nr + 1) * reduce(lambda x,y: x*y, self.lifts , 1) # multiplies entries of array
        self.N = self.p * self.R
        self.edge = self.R

        # private fields
        self.__topo = None

    def get_topo(self):
        if self.__topo is None:
            self.__topo = XpanderGenerator().make(self.nr,self.lifts)
        return self.__topo
    
    def get_jellyfish_eq(self):
        jf = Jellyfish(self.nr,self.R,self.p)
        jf.name += "-" + self.name
        return jf