# Author: Jascha Krattenmacher

from .Topology import Topology
from .Jellyfish import Jellyfish
from .common import approx_inverse
from .PolarstarGenerator import PolarstarGenerator, config

class Polarstar(Topology):
    
    """
    Fields:
        Public: 
            p: number of hosts per router
            nr: network radix of a router
            r: total radix of a router
            g: total number of groups
            R: total number of routers
            N: toal number of endnodes
            edge: number that indicates routers with endnodes (the first edge routers in topo have endnodes)
            name: name of topology (default := PS + type)
        
        Private:
            __topo: holds None or the topology in adjacency list

    Methods: 
        get_topo(): return the topoology in adjacency list
        get_jellyfish_eq(): return jellyfish topology that uses same infrastructure

    """
   
    def __init__(self, d = -1, pfq = -1, jq = -1, sg = '', N = -1):

        """
        Parameters:
            d: degree
            pfq: parameter for polarfly structure graph
            jq: parameter for subgraph
        Note: Only one of the parameters have to be specified for initialization.
        """

        #TODO
        if(N == -1 and d != -1 and pfq == -1 and jq == -1):
            self.pfq, self.jq, self.sg = config(d,sg,'dummyString')
        elif(N == -1 and d == -1 and pfq != -1 and jq != -1):
            self.jq = jq
            self.pfq = pfq
        elif(N != -1):
            self.R = 1
            self.d = 1
            while(self.R*self.d < N):
                self.d = self.d+1
                self.pfq, self.jq,self.sg,self.R = config(self.d,sg,'iter')
        else:
            raise Exception("invalid combination of arguments in constructor")

        self.R = (self.pfq*self.pfq+self.pfq+1)
        if self.sg == 'bdf':
            self.R = self.R*(2*self.jq+2)
        else:
            self.R = self.R*self.jq
        self.nr = self.d
        self.p = self.d
        self.r = self.nr + self.p 
        self.N = self.p*self.R 
        self.edge = self.R
        self.name = 'PS' + self.sg

        # private fields
        self.__topo = None

    def get_topo(self):
        if self.__topo is None:
            self.__topo = PolarstarGenerator().make(self.d, self.pfq, self.jq, self.sg)
        return self.__topo
    
    def get_jellyfish_eq(self):
        jf = Jellyfish(self.nr,self.R,self.p)
        jf.name += "-" + self.name
        return jf


