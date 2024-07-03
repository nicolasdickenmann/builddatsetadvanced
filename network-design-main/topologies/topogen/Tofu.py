# Author: Jascha Krattenmacher

from .Topology import Topology
from .Jellyfish import Jellyfish
from .TofuGenerator import TofuGenerator
from .common import approx_inverse
from math import sqrt, floor
from random import randint

class Tofu(Topology):
    """
    Fields:
        Public:
            n: array of number of dimensions
            p: number of hosts per router
            nr: network radix of router
            r: total radix of a router
            R: total number of routers
            N: total number of endnodes
            edge: number that indicates routers with endnodes (the first edge routers in topo have endnodes)
            name: name of topology (default := TOFU)
        
        Private:
            __topo: holds None or the topology in adjacency list

    Methods: 
        get_topo(): return the topoology in adjacency list
        get_jellyfish_eq(): return jellyfish topology that uses same infrastructure

    """
    def __init__(self, n = -1 , N = -1):

        """
        Parameters:
            n:  dimension [d1, d2, d3]
        """
 
        if(n == -1 and N != -1):
            temp = approx_inverse(int(N/12), lambda d: d**3)
            self.n = [temp, temp, temp]
        elif(n != -1 and N == -1):
            self.n = n
        else:
            raise Exception("invalid combination of arguments in constructor")
       

        #TODO: parameter calculation
        self.p = 1
        self.nr = 4 
        for i in range(3):
            if self.n[i] > 1:
                self.nr = self.nr + 2
        
        self.r = self.nr + self.p
        self.R = 12 #2*3*2
        for d in self.n:
            self.R = self.R*d 
        self.N = self.R * self.p
        self.edge = self.R
        self.name = 'TOFU'


        # private fields
        self.__topo = None

    def get_topo(self):
        if self.__topo is None:
            self.__topo = TofuGenerator().make(self.n)
        return self.__topo
    
    def get_jellyfish_eq(self):
        jf = Jellyfish(self.nr,self.R,self.p)
        jf.name += "-" + self.name
        return jf

