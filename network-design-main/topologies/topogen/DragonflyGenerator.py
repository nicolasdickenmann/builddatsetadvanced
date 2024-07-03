# Author: Alessandro Maissen
# Dragonfly(a,p,h) 
# Implemented based on Paper: Technology-Driven, Highly-Scalable Dragonfly Topology

# PARAMETERS
# p: number of hosts per router 

# VARIABLES
# n: total number of routers
# a: number of routers in each group
# h: number of channels per router connecting to routers of other groups
# g: total number of groups

# PRECONDITIONS
# p > 0

# ADDITIONAL NOTES
# This script implements the balanced version of Dragonfly where a==2*h==2*p

from .TopologyGenerator import TopologyGenerator
from .validate_dragonfly import validate

class DragonflyGenerator(TopologyGenerator):

    def __init(self):
        super(DragonflyGenerator,self).__init__()
    
    def make(self, p : int) -> [[int]]:
        assert(p > 0)     

        n = 4*p**3 + 2*p
        a = 2*p
        h = p
        g = a*h + 1
        assert(n == a*g)

        graph = [[] for _ in range(n)]
        
        for i in range(0, g):
            for j in range(0, a):
                v = i*a+j
                local = [i*a+x for x in range(0,a) if x != j]
                graph[v] += local
        gnode = [a*x for x in range(0,g)] # initially holds first node of each group
        gcount = [0] * g # initializes array with g zeros
        for i in range(0, g):
            for j in range(i+1, g):
                v1 = gnode[i]
                v2 = gnode[j]
                gcount[i] += 1
                gcount[j] += 1
                if gcount[i] >= h:
                    gcount[i] = 0
                    gnode[i] += 1
                if gcount[j] >= h:
                    gcount[j] = 0
                    gnode[j] += 1
                graph[v1].append(v2)
                graph[v2].append(v1)
        assert(all([len(v) == (3*p-1) for v in graph]))

        return graph


    def validate(self, topo : [[int]], p : int) -> bool:
        return validate(topo,p)
    
    def get_folder_path(self):
        return super(DragonflyGenerator,self).get_folder_path() + "dragonflies/"

    def get_file_name(self, p : int) -> str:
        return "Dragonfly." + str(p) + ".adj.txt"