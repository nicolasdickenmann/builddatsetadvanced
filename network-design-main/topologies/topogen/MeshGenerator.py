# Author: Jascha Krattenmacher
# used algorithm from Domke
# Mesh n1xn2 

# PARAMETERS
# n1: Array of dimension of Mesh n1xn2x...xnN

# VARIABLES
# N: number of routers/nodes in total

# PRECONDITIONS
# n1,n2,..nN > 0

from .TopologyGenerator import TopologyGenerator
from .validate_mesh import validate
from copy import deepcopy

class MeshGenerator(TopologyGenerator):

    def __init(self):
        super(MeshGenerator,self).__init__()
    
    def make(self, n : int, k : int, g : int) -> [[int]]:
        assert(n > 0)
        assert(g >= 0)
        
        topology = {}
        dims = [k for _ in range(n)]
     
        # CONFIGS that would be given from parameters (in Domke script)
        num_switches = 1
        for dim in dims:
            num_switches *= dim
    
    
        # generate all switches in the integer lattice
        j = 0
        for sw_idx in range(num_switches):
            idx_vector = _get_switch_idx_vector(dims, sw_idx)
            topology[str(idx_vector)] = [j,[]]
            j = j+1
    
        for sw_idx in range(num_switches):
            idx_vector_1 = _get_switch_idx_vector(dims, sw_idx)
            switch1 =  topology[str(idx_vector_1)][0]
            for i in range(len(dims)):
                idx_vector_2 = idx_vector_1[:]
                idx_vector_2[i] = (idx_vector_2[i] + 1) % dims[i]
                if idx_vector_2[i] == 0 or dims[i] == 1:
                    continue
                switch2 =  topology[str(idx_vector_2)][0]
                topology[str(idx_vector_1)][1].append(switch2)
                topology[str(idx_vector_2)][1].append(switch1)

            if g > 0:
                for i in range(len(dims)):
                    for m in range(1, dims[i]):
                        idx_vector_2 = idx_vector_1[:]
                        idx_vector_2[i] += 1 + m * g
                        if idx_vector_2[i] >= dims[i]:
                            continue
                        switch2 = topology[str(idx_vector_2)][0]
                        topology[str(idx_vector_1)][1].append(switch2)
                        topology[str(idx_vector_2)][1].append(switch1)

    
        # convert dict to list
        meshTopology = [ entry[1] for entry in topology.values() ]

        return meshTopology

 


    def validate(self, topo : [[int]], n : [int]) -> bool:
        return validate(topo,n)
    
    def get_folder_path(self):
        return super(MeshGenerator,self).get_folder_path() + "meshes/"

    def get_file_name(self, n : int , k : int, g : int) -> str:
        if g == 0:
            return "Mesh" + str(n) + "." + str(k) + ".adj.txt"
        else:
            return "ExpMesh" + str(n) + "." + str(k) + "gap" + str(g) + ".adj.txt"



#------ Hepler functions ---------

def _get_switch_idx_vector(dims, sw_idx):
    idx_vector = len(dims) * [0]

    for i in range(len(dims)):
        idx_vector[i] = sw_idx % dims[i]
        sw_idx = int(sw_idx / dims[i])

    return idx_vector

