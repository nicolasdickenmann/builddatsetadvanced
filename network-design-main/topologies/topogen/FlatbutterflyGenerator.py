# Author: Alessandro Maissen
# Flattened Butterfly (k-ary n-flat)
# Implemented based on paper: Flattened Butterfly : A Cost-Efficient Topology for High-Radix Networks (2.1)

# PARAMETERS
# n: Specifies the dimensionality n' = n - 1
# k: 

# VARIABLES
# R: number of routers/nodes

# PRECONDITIONS
# n > 1 and k > 1

import math
from .TopologyGenerator import TopologyGenerator
from .validate_flatbutterfly import validate

class FlatbutterflyGenerator(TopologyGenerator):

    def __init(self):
        super(FlatbutterflyGenerator,self).__init__()
    
    def make(self, n : int, k : int) -> [[int]]:
        assert(n > 1 and k > 1)
        
        R = k**(n-1)
        graph = [[] for _ in range(R)]

        for d in range(1, n):
            for i in range(R):
                for m in range(k):
                    j = i + ((m - (math.floor(i/(k**(d-1)))) % k) * k**(d-1))
                    if i != j:
                        graph[i].append(j)
        
        return graph        

    def validate(self, topo : [[int]], n : int, k : int) -> bool:
        return validate(topo,n,k)
    
    def get_folder_path(self):
        return super(FlatbutterflyGenerator,self).get_folder_path() + "flatbutterflies/"

    def get_file_name(self, n : int, k : int) -> str:
        return str(n - 1) + "DFlatButterfly." + str(k) + ".adj.txt"