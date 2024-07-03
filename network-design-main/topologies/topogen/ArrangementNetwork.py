# Author: Jascha Krattenmacher

from .Topology import Topology
from .Jellyfish import Jellyfish
from .ArrangementNetworkGenerator import ArrangementNetworkGenerator
from .common import approx_inverse
from math import factorial,log,sqrt
from collections import OrderedDict
from bisect import bisect_left


class ArrangementNetwork(Topology):
    
    """
    Fields: 
        Public:
            n: maximum integer
            k: number of permutations
            p: number of hosts per router
            nr: network radix of router
            r: total radix of a router
            R: total number of routers
            N: total number of endnodes
            edge: number that indicates routers with endnodes (the first edge routers in topo have endnodes)
            name: name of topology (default := AN)
        
        Private:
            __topo: holds None or the topology in adjacency list

    Methods: 
        get_topo(): return the topoology in adjacency list
        get_jellyfish_eq(): return jellyfish topology that uses same infrastructure

    """
    def __init__(self, n = -1, k = -1, N = -1):

        """
        Parameters:
            n: maximum integer
            k: number of permutations

        Note: Only one of the parameters have to be specified for initialization.

        """
        # TODO: factorialApproximation
        if(n != -1 and N != -1 and k == -1):
            # approximation for a given n, bad performance for big N, alternatively return value manually
            self.k = approxk(N,n)
            self.n = n
        elif(n == -1 and N != -1 and k != -1):
            # approximation for a given k, bad performance for big N, alternatively return value manually
            self.n = approxn(N, k)
            self.k = k
        elif(n == -1 and N != -1 and k == -1):
            self.n, self.k = approxAll(N)
        elif(n != -1 and k != -1):
            self.k = k
            self.n = n
        elif(n == -1 and k == -1 and N != -1):
            # TODO: implement
            raise Exception("not yet implemented")
        else:
            raise Exception("invalid combination of arguments in constructor")
        
        self.p = self.n+1 
        self.nr = self.k*(self.n - self.k)
        self.r = self.nr + self.p
        self.R = int(factorial(self.n)/factorial(self.n-self.k))
        self.N = self.R * self.p
        self.edge = self.R
        self.name = 'AN' + str(self.k)


        # private fields
        self.__topo = None

    def get_topo(self):
        if self.__topo is None:
            self.__topo = ArrangementNetworkGenerator().make(self.n, self.k)
        return self.__topo
    
    def get_jellyfish_eq(self):
        jf = Jellyfish(self.nr,self.R,self.p)
        jf.name += "-" + self.name
        return jf

############# Hepler Functions ##############

def get_config(N : int):
    return 4,2

# TODO: implement
def approxAll(N : int):
    
    approx_dict = OrderedDict()

    upperBound = approx_inverse(N, lambda n: (n+1)*n) #fact(n+1)/fact(n-k) >= n+1*n
  
    n = 3
    while (n < upperBound): #N~n, +2k to make sure best values are chosen
        for k in range(1,n): 
            value = int(factorial(n+1)/factorial(n-k))
            #print("for n=%i, k=%i   approx=%i" %(n,k,value))

            if k == n-1:
                approx_dict[value] = [n,n-1]
                print("STORE for k=1: for n=%i, k=%i   approx=%i" %(n,k,value))
                n = n+1
            elif value > N:
                approx_dict[value] = [n,k]
                approx_dict[int(factorial(n+1)/factorial(n-k+1))] = [n,k-1]
                print("STORE: for n=%i, k=%i   approx=%i" %(n,k,value))
                print("STORE: for n=%i, k=%i   approx=%i" %(n,k-1,factorial(n+1)/factorial(n-k+1)))
                n = n+1
            

    nodes_list = list(approx_dict.keys())
    nodes_list.sort()
    ind = bisect_left(nodes_list, N)

    print(nodes_list)
    print(ind) 

    if N - nodes_list[ind - 1] < nodes_list[ind] - N:
        res=approx_dict[nodes_list[ind - 1]]
    else:
        res=approx_dict[nodes_list[ind]]

    return res[0],res[1]


def approxn(N : int, k : int):

    approx_dict = OrderedDict()
    value = 0
    n = k
    while(value < N):
        n = n+1
        value = int(factorial(n+1)/factorial(n-k))

    #print("for n=%i, k=%i   approx=%i" %(n,k,value))
    return n


def approxk(N : int, n : int):

    for k in range(1,n): 
        value = int(factorial(n+1)/factorial(n-k))
        if value > N:
           return k
    # all values < N
    return n-1
