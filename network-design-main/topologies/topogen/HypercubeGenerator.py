# Author: Alessandro Maissen
# n-dimensional Hypercube

# PARAMETERS
# n: dimension of hypercube -> n > 0

# VARIABLES
# N: number of routers/nodes in total

# PRECONDITIONS
# n > 0

from .TopologyGenerator import TopologyGenerator
from .validate_hypercube import validate

class HypercubeGenerator(TopologyGenerator):

    def __init(self):
        super(HypercubeGenerator,self).__init__()
    
    def make(self, n : int) -> [[int]]:
        assert(n > 0)
        return build_recurive(n)

    def validate(self, topo : [[int]], n : int) -> bool:
        return validate(topo,n)
    
    def get_folder_path(self):
        return super(HypercubeGenerator,self).get_folder_path() + "hypercubes/"

    def get_file_name(self, n : int) -> str:
        return str(n) + "DHypercube.adj.txt"

# ---------------- helper functions ----------------

def build_recurive(n: int):

    N = 2**n

    if n == 1:
        return [[1],[0]]
    else:
        graph = build_recurive(n-1)
        graph.extend([[x + int(N/2) for x in xs] for xs in graph])

        # connect the to lower dimensional hypercubes 
        for i in range(int(N/2)):
            graph[i].append(i + int(N/2))
            graph[int(N/2) + i].append(i)

    return graph