# Author: Marcel Schneider and Alessandro Maissen
# Regular HyperX(l,s,1,t)
# Implemented based on Paper: HyperX: Topology, Routing, and Packaging of Efficient Large-Scale Networks

# PARAMETERS
# l: dimension of HyperX
# s: number of nodes per dimension

# VARIABLES
# n: number of total routers

# PRECONDITIONS
# TODO:

# ADDITIONAL NOTES
# We do not care about t: number of endnotes per router here.

from .TopologyGenerator import TopologyGenerator
from .validate_hyperx import validate

class HyperXGenerator(TopologyGenerator):

    def __init(self):
        super(HyperXGenerator,self).__init__()
    
    def make(self, l: int, s : int) -> [[int]]:
        n = s ** l
        graph = [[] for _ in range(n)]
        
        for i in range(0, n):
            for j in range(0, n):
                if i==j: continue
                if (l-1) == sum(int(i/s**k) % s == int(j/s**k) % s for k in range(0,l)):
                    graph[i].append(j)
        return graph       

    def validate(self, topo : [[int]], l: int, s : int) -> bool:
        return validate(topo,l,s)
    
    def get_folder_path(self):
        return super(HyperXGenerator,self).get_folder_path() + "hyperxs/"

    def get_file_name(self, l: int, s : int) -> str:
        return "HyperX" + str(l) + "." + str(s) + ".adj.txt"