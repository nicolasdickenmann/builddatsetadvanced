# Author: Alessandro Maissen
# Jellyfish (r-regular)
# Implemented based on Paper: Jellyfish: Networking Data Centers Randomly

# PARAMETERS
# r: network radix/degree of routers/nodes
# n: total number of routers/nodes 

# PRECONDITIONS
# r < n and r*n % 2 == 0

# ADDITIONAL NOTES
# created topology can be unconnected

import random
from .TopologyGenerator import TopologyGenerator
from .validate_jellyfish import validate

class JellyfishGenerator(TopologyGenerator):

    def __init(self):
        super(JellyfishGenerator,self).__init__()
    
    def make(self, r : int, n : int) -> [[int]]:

        assert(r < n and r*n % 2 == 0) # necessary and sufficient condition such that an r-regular graph can exist
            
        graph = [[] for _ in range(n)]
        
        free = [node for node in enumerate(graph)]
        while True:
            #free = [node for node in enumerate(graph) if len(node[1]) < r]
            if len(free) >= 2:
                pair = random.sample(free, 2)
                pair[0][1].append(pair[1][0])
                pair[1][1].append(pair[0][0])
                if len(pair[0][1]) >= r:
                    free.remove(pair[0])
                if len(pair[1][1]) >= r:
                    free.remove(pair[1])
            else:
                # eliminate multiedges. not 100% sure this will always terminate...
                graph = [list(set(node)) for node in graph]
                free = [node for node in enumerate(graph) if len(node[1]) < r]
                if len(free) <= 2:
                    break
        if any(len(node) != r for node in graph): # retry if non-regular.
            return self.make(r, n)
        return graph


    def validate(self, topo : [[int]], r : int, n : int) -> bool:
        return validate(topo,r,n)
    
    def get_folder_path(self):
        return super(JellyfishGenerator,self).get_folder_path() + "jellyfishes/"

    def get_file_name(self, r : int, n : int) -> str:
        return "Jellyfish." + str(r) + "." + str(n) + ".adj.txt"