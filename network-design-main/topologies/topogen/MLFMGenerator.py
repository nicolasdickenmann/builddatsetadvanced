# Author: Alessandro Maissen
# h-MLFM (Multi-Layer Full-Mesh) 
# Implemented based on Paper: Cost-Effective Diameter-Two Topologies: Analysis and Evaluation (2.2.3)

# PARAMETERS
# h: degree of local routers

# VARIABLES
# l: number of layers
# Rg: number of global routers
# Rl: number of local routers per layer
# n: total number of routers

# PRECONDITIONS
# h > 0

# ADDITIONAL NOTES:
# The first l*Rl (0...l*Rl-1) nodes/routers are edge routers. Only edge routers can have hosts attached.

from .TopologyGenerator import TopologyGenerator
from .validate_mlfm import validate

class MLFMGenerator(TopologyGenerator):

    def __init(self):
        super(MLFMGenerator,self).__init__()
    
    def make(self, h : int) -> [[int]]:
        assert(h > 0)

        l = h
        Rg = int(h * (h + 1) / 2)
        assert(h * (h + 1) == Rg * 2)
        Rl = h + 1
        n = Rg + (l * Rl)
        
        graph = [[] for _ in range(n)]

        for k in range(0,l):
            currentGR = l*Rl
            for i in range(Rl*k, Rl*(k + 1)):
                for j in range(Rl*k, Rl*(k + 1)):
                    if i < j:
                        graph[i].append(currentGR)
                        graph[j].append(currentGR)
                        graph[currentGR].append(i)
                        graph[currentGR].append(j)
                        currentGR += 1
        return graph         

    def validate(self, topo : [[int]], h : int) -> bool:
        return validate(topo,h)
    
    def get_folder_path(self):
        return super(MLFMGenerator,self).get_folder_path() + "mlfms/"

    def get_file_name(self, h: int) -> str:
        return "MLFM." + str(h) + ".adj.txt"