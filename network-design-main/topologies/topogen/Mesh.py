# Author: Jascha Krattenmacher

from .Topology import Topology
from .Jellyfish import Jellyfish
from .MeshGenerator import MeshGenerator
from .common import approx_inverse
from random import randint
from math import sqrt, floor, ceil

class Mesh(Topology):
    """
    Fields:
        Public:
            n: number of  dimensions
            k: number of routers per edge
            g: gap
            p: number of hosts per router
            nr: network radix of router
            r: total radix of a router
            R: total number of routers
            N: total number of endnodes
            edge: number that indicates routers with endnodes (the first edge routers in topo have endnodes)
            name: name of topology (default := xdMESH or xdEXPMESH)
        
        Private:
            __topo: holds None or the topology in adjacency list

    Methods: 
        get_topo(): return the topoology in adjacency list
        get_jellyfish_eq(): return jellyfish topology that uses same infrastructure

    """
    def __init__(self, n = -1, k = -1, g = 0, N = -1):

        """
        Parameters:
            n : number of dimensions of mesh 
            k : number of routers per edge
            g : gap for express mesh
        """

        assert(n > 0)
        assert(g >= 0)


        if(k == -1 and N != -1 and n != -1):
            self.k = approx_inverse(N, lambda k: k**n)
            self.n = n
        elif(k != -1 and N != -1 and n == -1):
            self.n = approx_inverse(N, lambda n: k**n)
            self.k = k
        elif(k != -1 and N == -1 and n != -1):
            self.k = k
            self.n = n
        else:
            raise Exception("invalid combination of arguments in constructor")

        self.g = g
        if g > 0:
            self.g = floor((self.k - 3)/g)
            if self.g == 0:
                self.g = 1

        self.p = 1
        if self.k > 2:
            if self.n == 2:
                self.fractional_nr = 2*4 + 3*4*(self.k-2) + 4*(self.k-2)*(self.k-2)    
            elif self.n == 3:
                self.fractional_nr = 3*8 + 4*12*(self.k-2) + 5*6*(self.k-2)*(self.k-2) + 6*(self.k-2)*(self.k-2)*(self.k-2)
            elif self.n == 4:
                self.fractional_nr = 4*16 + 5*32*(self.k-2) + 6*24*(self.k-2)*(self.k-2) + 7*8*(self.k-2)*(self.k-2)*(self.k-2) + 8*(self.k-2)*(self.k-2)*(self.k-2)*(self.k-2)
            elif self.n == 5:
                self.fractional_nr = 5*32 + 6*80*(self.k-2) + 7*80*(self.k-2)*(self.k-2) + 8*40*(self.k-2)*(self.k-2)*(self.k-2) + 9*10*(self.k-2)*(self.k-2)*(self.k-2)*(self.k-2) +10*(self.k-2)*(self.k-2)*(self.k-2)*(self.k-2)*(self.k-2)
            elif self.n == 6:
                self.fractional_nr = 6*64 + 7*192*(self.k-2) + 8*240*(self.k-2)*(self.k-2) + 9*160*(self.k-2)*(self.k-2)*(self.k-2) + 10*60*(self.k-2)*(self.k-2)*(self.k-2)*(self.k-2) + 11*12*(self.k-2)*(self.k-2)*(self.k-2)*(self.k-2)*(self.k-2) + 12*(self.k-2)*(self.k-2)*(self.k-2)*(self.k-2)*(self.k-2)*(self.k-2)
            else:
                print("fractional nr not implemented for n > 6")
            self.fractional_nr = self.fractional_nr/(self.k**self.n)
        else:
            self.nr = n


        self.nr = int(round(self.fractional_nr))
        if self.g > 0 and self.k > 3:
            self.nr = self.nr + self.n*floor((self.k - 3)/self.g)

        self.r = self.nr + self.p
        self.R = self.k ** self.n
        self.N = self.R * self.p
        self.edge = self.R
        if self.g == 0:
            self.name = str(self.n) + 'dMESH'
        else:
            self.name = str(self.n) + 'DeMESH' + str(g)


        # private fields
        self.__topo = None

    def get_topo(self):
        if self.__topo is None:
            self.__topo = MeshGenerator().make(self.n, self.k, self.g)
        return self.__topo
    
    def get_jellyfish_eq(self):
        jf = Jellyfish(self.nr,self.R,self.p)
        jf.name += "-" + self.name
        return jf

