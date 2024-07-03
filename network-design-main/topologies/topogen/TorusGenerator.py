# Author: Alessandro Maissen
# k-ary n-dimensional Torus

# PARAMETERS
# n: dimension of torus --> n > 1
# k: number of routers/nodes per "edge" --> k > 2 (special case k==2 not handled since this is a Hypercube)

# PRECONDITIONS
# n > 1 and k > 2

# VARIABLES
# N: number of routers/nodes in total

from .TopologyGenerator import TopologyGenerator
from .validate_torus import validate

class TorusGenerator(TopologyGenerator):

    def __init(self):
        super(TorusGenerator,self).__init__()
    
    def make(self, n : int, k : int) -> [[int]]:
        assert(n > 1 and k > 2)
        return build_recurive(n,k)

    def validate(self, topo : [[int]], n : int, k : int) -> bool:
        return validate(topo,n,k)
    
    def get_folder_path(self):
        return super(TorusGenerator,self).get_folder_path() + "tori/"

    def get_file_name(self, n : int, k : int) -> str:
        return str(n) + "DTorus." + str(k) + ".adj.txt"

# ---------------- helper functions ----------------

def build_recurive(n: int, k : int):

    N = k**n

    if n == 1:
        return [[(i-1) % k, (i+1) % k] for i in range(k)] 
    else:
        graph = []
        lower_dim_torus = build_recurive(n-1, k)
        
        # duplicate k times torus of dimension n-1
        for i in range(k):
            graph.extend([[x + i*int(N/k) for x in xs] for xs in lower_dim_torus])

        # connect the two lower dimnesional tori
        for i in range(N):
            graph[i].extend([(int(i-(N/k))) % N, (int(i+(N/k))) % N])

    return graph