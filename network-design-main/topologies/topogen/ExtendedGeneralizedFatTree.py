# Author: Jascha Krattenmacher 

from .Topology import Topology
from .Jellyfish import Jellyfish
from .ExtendedGeneralizedFatTreeGenerator import ExtendedGeneralizedFatTreeGenerator
from math import ceil

class ExtendedGeneralizedFatTree(Topology):

    """
    Fields:
        Public:
            p: number of hosts per router
            nr: network radix of router
            r: total radix of a router
            R: total number of routers
            N: total number of endnodes
            edge: number that indicates routers with endnodes (the first edge routers in topo have endnodes)
            name: name of topology (default := XGFT)
        
        Private:
            __topo: holds None or the topology in adjacency list

    Methods: 
        get_topo(): return the topoology in adjacency list
        get_jellyfish_eq(): return jellyfish topology that uses same infrastructure

    """
    def __init__(self, h = -1, inputs = None, N = -1, variant = -1):

        """
        Parameters:
            h: height h of fat tree
            inputs: number of parents and childnodes:
                m=inputs[:h]: children nodes per level
                w=inputs[h:]: parents nodes per level
        """
        
        if(h == -1 and N != -1 and inputs == None):
            self.p,self.h, self.inputs = getConfig(N, variant)
        elif(h != -1 and N != -1 and inputs == None):
            self.inputs = getConfigWithH(h,N)
            self.h = h
        elif(h != -1 and N == -1, inputs != None):
            self.h = h
            self.inputs = inputs
        else:
            raise Exception("invalid combination of arguments in constructor")
       
        assert(len(self.inputs) == 2*self.h)

        # parameter depend on inputs, here calculated are the inputs for inputs child/parents all the same
        
        self.R = 0
        for i in range(self.h+1):
            temp=1
            for j in range(i,self.h):
                temp = temp*self.inputs[j]
            for j in range(0,i):
                temp = temp*self.inputs[self.h+j]
            self.R = self.R + temp

        self.edge = 1
        for i in range(self.h):
            self.edge = self.edge*self.inputs[i]
        self.name = 'XGFT' + str(variant)
        self.N = self.edge * self.p

        self.fractional_nr = 0
        for i in range(self.h):
            temp=1
            for j in range(i,self.h):
                temp = temp*self.inputs[j]
            for j in range(0,i+1):
                temp = temp*self.inputs[self.h+j]
            self.fractional_nr= self.fractional_nr + temp

        self.fractional_r = self.fractional_nr + self.edge*self.p

        self.r = int(round(self.fractional_r/self.R))
        self.nr = int(round(self.fractional_nr/self.R))

        # private fields
        self.__topo = None

    def get_topo(self):
        if self.__topo is None:
            self.__topo = ExtendedGeneralizedFatTreeGenerator().make(self.h, self.inputs)
        return self.__topo
    
    def get_jellyfish_eq(self):

        p = ceil(self.N / self.R) # ceiling because we want at least as many endnodes in JF as in XGFT 
        nr = self.r - p

        # enforce precondictions for jellyfish
        if self.R*nr % 2 != 0:
            # implies nr is odd
            nr -= 1
            p += 1

        assert(self.r == p + nr)

        jf = Jellyfish(nr,self.R,p)
        jf.name += "-" + self.name
        return jf



############# Helper functions ###############

def getConfig( N : int, variant : str):
    
    if variant == '4':
        if N == 1000:
            return 8,3,[8, 4, 4, 2, 2, 2]
        if N == 10000:
            return 16,5,[8, 4, 4, 4, 4, 2, 2, 2, 2, 2]
        if N == 100000:
            return 24,6,[8, 4, 4, 4, 4, 4, 2, 2, 2, 2, 2, 2]

    elif variant == '8': 
        if N == 1000:
            return 8,2,[16, 8, 4, 4]
        if N == 10000:
            return 16,3,[16, 8, 8, 4, 4, 4]
        if N == 100000:
            return 24,4, [16, 8, 8, 8, 4, 4, 4, 4]
    elif variant == '8S':
        if N == 1000:
            return 8,3,[8, 8, 8, 3, 2, 1]
        if N == 10000:
            return 20,3,[8, 8, 8, 3, 2, 1]
        if N == 100000:
            return 25,4,[8, 8, 8, 8, 4, 3, 2, 1]

    else:
        print("no valid variant or N found found")


def getConfigWithH( h : int, N : int):
    return [4,4, 4, 1]



