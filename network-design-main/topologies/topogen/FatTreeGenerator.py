# Author: Marcel Schneider and Alessandro Maissen

# Tree-stage Fat-Tree
# Based on A Scalable, Commodity Data Center Network Architecture (slighty diffrent strategy with same result)

# PARAMETERS
# k: total radix of per router

# VARIABLES
# n: nummber of total routers

# ADDITIONAL NOTES:
# The first k^2/2 nodes/routers are edge routers.
# Only edge routers can have hosts attached.


from .TopologyGenerator import TopologyGenerator
from .validate_fattree import validate

class FatTreeGenerator(TopologyGenerator):

    def __init(self):
        super(FatTreeGenerator,self).__init__()
    
    def make(self, k : int) -> [[int]]:
        assert(k % 2 == 0)
        p = int(k / 2)
        n = 5*p**2
        
        graph = [[] for _ in range(n)]
        
        # the FT is a mirror-symmetric structre of 5 groups of p*p nodes
        node = enumerate(graph)
        def p_square_group():
            return [[next(node) for _ in range(p)] for __ in range(p)]
        
        edge_left  = p_square_group() # the edge has the low node numbers
        edge_right = p_square_group()
        aggr_left  = p_square_group()
        aggr_right = p_square_group()
        core = p_square_group()
        
        for ee, aa in [(edge_left, aggr_left), (edge_right, aggr_right)]:
            # connect edge and aggregation
            for e, a in zip(ee, aa):
                for i in range(p):
                    for j in range(p):
                        a[i][1].append(e[j][0])
                        e[j][1].append(a[i][0])
            # connect core and aggregation
            for c in core:
                for a in aa:
                    for i in range(p):
                        c[i][1].append(a[i][0])
                        a[i][1].append(c[i][0])
        return graph



    def validate(self, topo : [[int]], k : int) -> bool:
        return validate(topo,k)
    
    def get_folder_path(self):
        return super(FatTreeGenerator,self).get_folder_path() + "fattrees/"

    def get_file_name(self, k : int) -> str:
        return "FatTree." + str(k) + ".adj.txt"