# Author: Jascha Krattenmacher

from .Topology import Topology
from .Jellyfish import Jellyfish
from .common import approx_inverse
from .MegaflyGenerator import MegaflyGenerator
from math import ceil

class Megafly(Topology):
    
    """
    Fields:
        Public: 
            p: number of hosts per router
            nr: network radix of a router
            r: total radix of a router
            R: total number of routers
            N: toal number of endnodes
            edge: number that indicates routers with endnodes (the first edge routers in topo have endnodes)
            name: name of topology (default := MF)
        
        Private:
            __topo: holds None or the topology in adjacency list

    Methods: 
        get_topo(): return the topoology in adjacency list
        get_jellyfish_eq(): return jellyfish topology that uses same infrastructure

    """
   
    def __init__(self, g = -1, d = -1, N = -1):

        """
        Parameters:
            d: number of routers in each group
            g: each spine router has d/(2*g) global links 

        Note: Only one of the parameters have to be specified for initialization.

        """

        if(g != -1 and N != -1 and d==-1):
            self.g = g
            self.d = approx_inverse(N, lambda d: d*d*d*d/(16*g*g) + d*d/(4*g) )
            
            while(self.d/2 % g != 0):
                self.d = self.d + 1

        elif(g == -1 and N != -1 and d != -1):
            self.d = d
            self.g = approx_inverse(N, lambda g: d*d*d*d/(16*g*g) + d*d/(4*g) )
            print("g=%i" %self.g)

            while(self.d/2 % self.g != 0):
                self.g = self.g - 1

        elif(d != -1 and N==-1 and g != -1):
            self.d = d
            self.g = g
        else:
            raise Exception("invalid combination of arguments in constructor")

        intraConnPerRouter = int(self.d//2//self.g)
        self.fractional_nr = (self.d+intraConnPerRouter)/2
        self.nr = int(round(self.fractional_nr))
        self.p = intraConnPerRouter 
        self.r = int(self.d/2 + intraConnPerRouter)
        self.R = int( self.d*(((self.d*self.d)/(4*self.g))+1) )
        self.N = int( self.p * self.R/2 )
        self.edge = int( self.R/2 )
        self.name = 'MF' + str(g)


        # private fields
        self.__topo = None

    def get_topo(self):
        if self.__topo is None:
            self.__topo = MegaflyGenerator().make(self.g, self.d)
        return self.__topo
    
    def get_jellyfish_eq(self):

        p = ceil(self.N / self.R) # ceiling because we want at least as many endnodes in JF as in FT2x
        nr = int(round(self.r - p)) # radix is rounded since radix might be fractional

        # enforce precondictions for jellyfish
        if self.R*nr % 2 != 0:
            # implies nr is odd
            nr -= 1
            p += 1

        jf = Jellyfish(nr,self.R,p)
        jf.name += "-" + self.name
        return jf

