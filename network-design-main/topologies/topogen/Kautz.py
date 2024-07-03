# Author: Jascha Krattenmacher

from .Topology import Topology
from .Jellyfish import Jellyfish
from .KautzGenerator import KautzGenerator
from .common import approx_inverse

class Kautz(Topology):
    """
    Fields:
        Public:
            b: base of Kautz Graph K(b,n)
            n: length of Kautz Graph K(b,n)
            p: number of hosts per router
            nr: network radix of router
            r: total radix of a router
            R: total number of routers
            N: total number of endnodes
            edge: number that indicates routers with endnodes (the first edge routers in topo have endnodes)
            name: name of topology (default := KA)
        
        Private:
            __topo: holds None or the topology in adjacency list

    Methods: 
        get_topo(): return the topoology in adjacency list
        get_jellyfish_eq(): return jellyfish topology that uses same infrastructure

    """
    def __init__(self, b = -1, n = -1, N = -1):

        """
        Parameters:
            b: base b of the Kautz graph K(b,n)
            n: length n of the Kautz graph K(b,n)
        """
        
        if(b == -1 and N != -1 and n == -1):
            b_ = 0
            n_ = 0
            bestApprox = 0
            for b_i in range(2,8):
                n_temp = approx_inverse(N/b_i, lambda n: (b_i + 1)*b_i**(n-1))
                approx = (b_i + 1)*b_i**(n_temp)

                if abs(N-approx) < (N-bestApprox):
                    bestApprox = approx
                    b_ = b_i
                    n_ = n_temp

            self.b = b_
            self.n = n_
            #print("Approx=%i, with b=%i and n=%i" %(bestApprox, b_, n_))
        elif(b != -1 and N != -1 and n == -1):
            self.n = approx_inverse(N, lambda n: (b + 1)*b**(n))
            self.b = b                
        elif(b != -1 and n != -1):
            self.b = b
            self.n = n
        elif(k == -1 and n == -1 and N != -1):
            # TODO: implement
            raise Exception("not yet implemented")
        else:
            raise Exception("invalid combination of arguments in constructor")
       
        self.p = self.b 
        self.nr = 2*self.b
        if self.n == 2:
            self.nr = self.nr - 1
        self.r = self.nr + self.p
        self.R = (self.b + 1)*self.b**(self.n-1)
        self.N = (self.b + 1)*self.b**(self.n) 
        self.edge = self.R
        self.name = 'KA' + str(self.b)

        # private fields
        self.__topo = None

    def get_topo(self):
        if self.__topo is None:
            self.__topo = KautzGenerator().make(self.b, self.n)
        return self.__topo
    
    def get_jellyfish_eq(self):
        jf = Jellyfish(self.nr,self.R,self.p)
        jf.name += "-" + self.name
        return jf
