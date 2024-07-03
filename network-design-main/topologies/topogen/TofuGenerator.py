# Author: Jascha Krattenmacher
# used algorithm from Domke
 

# PARAMETERS
# d1,d2,d2: dimensions [d1,d2,d3]

# VARIABLES
# N: number of routers/nodes in total

# PRECONDITIONS
# n > 0

from .TopologyGenerator import TopologyGenerator
from .validate_tofu import validate
from math import ceil

class TofuGenerator(TopologyGenerator):

    def __init(self):
        super(TofuGenerator,self).__init__()
    
    def make(self, n) -> [[int]]:
       
        assert(len(n) == 3)
        dims = n+[2,3,2]

        topology = {}
        
        # CONFIGS
        num_switches = 1
        for dim in dims:
            num_switches *= dim
   
        # generate all switches in the integer lattice
        j = 0
        for sw_idx in range(num_switches):
            idx_vector = _get_switch_idx_vector(dims, sw_idx)
            topology[_get_switch_name(idx_vector)] = [j,[]]
            j = j+1

        # connect all switches
        for sw_idx in range(num_switches):
            idx_vector_1 = _get_switch_idx_vector(dims, sw_idx) 
            switch1 = topology[_get_switch_name(idx_vector_1)][0]
    
            # get the idx w.r.t A, B, and C dim within the unit
            sw_idx_a, sw_idx_b, sw_idx_c = idx_vector_1[3:6]
    
            # first connect the switch to its neighbors in the same tofu unit
            # connect mesh-like in A dim
            for adj_sw_idx_a in range(sw_idx_a + 1, 2):
                idx_vector_2 = idx_vector_1[:3] + [adj_sw_idx_a] + idx_vector_1[4:]
                switch2 = topology[_get_switch_name(idx_vector_2)][0]
                topology[_get_switch_name(idx_vector_1)][1].append(switch2)
                topology[_get_switch_name(idx_vector_2)][1].append(switch1)
    
            # connect torus-like in B dim
            for adj_sw_idx_b in range(sw_idx_b + 1, 3):
                idx_vector_2 = idx_vector_1[:4] + [adj_sw_idx_b] + idx_vector_1[5:]
                switch2 = topology[_get_switch_name(idx_vector_2)][0]
                topology[_get_switch_name(idx_vector_1)][1].append(switch2)
                topology[_get_switch_name(idx_vector_2)][1].append(switch1)

            # connect mesh-like in C dim
            for adj_sw_idx_c in range(sw_idx_c + 1, 2):
                idx_vector_2 = idx_vector_1[:5] + [adj_sw_idx_c]
                switch2 = topology[_get_switch_name(idx_vector_2)][0]
                topology[_get_switch_name(idx_vector_1)][1].append(switch2)
                topology[_get_switch_name(idx_vector_2)][1].append(switch1)
    
            # and now connect the switch to neighboring units in the tofu
            # connect to neighbor units in X
            if dims[0] > 1:
                idx_vector_2 = idx_vector_1[:]
                idx_vector_2[0] = (idx_vector_2[0] + 1) % dims[0]
                switch2 = topology[_get_switch_name(idx_vector_2)][0]
                topology[_get_switch_name(idx_vector_1)][1].append(switch2)
                topology[_get_switch_name(idx_vector_2)][1].append(switch1)
    
            # connect to neighbor units in Y
            if dims[1] > 1:
                idx_vector_2 = idx_vector_1[:]
                idx_vector_2[1] = (idx_vector_2[1] + 1) % dims[1]
                switch2 = topology[_get_switch_name(idx_vector_2)][0]
                topology[_get_switch_name(idx_vector_1)][1].append(switch2)
                topology[_get_switch_name(idx_vector_2)][1].append(switch1)
    
            # connect to neighbor units in X
            if dims[2] > 1:
                idx_vector_2 = idx_vector_1[:]
                idx_vector_2[2] = (idx_vector_2[2] + 1) % dims[2]
                switch2 = topology[_get_switch_name(idx_vector_2)][0]
                topology[_get_switch_name(idx_vector_1)][1].append(switch2)
                topology[_get_switch_name(idx_vector_2)][1].append(switch1)

        # convert dict to list
        tofuTopology = [entry[1] for entry in topology.values()]

        return tofuTopology


    def validate(self, topo : [[int]], n : [int]) -> bool:
        return validate(topo,n)
    
    def get_folder_path(self):
        return super(TofuGenerator,self).get_folder_path() + "tofus/"

    def get_file_name(self, n: [int]) -> str:
        return "Tofu6D.(" + ".".join(str(d) for d in n) + ").adj.txt"


#------ Hepler functions ---------

def _get_switch_name(id_vector):
    id_vector = id_vector[:3] + [id_vector[3] + 2*id_vector[5] + 4*id_vector[4]]
    return str(id_vector) 

def _get_terminal_name(id_vector):
    return str(id_vector)

def _get_switch_idx_vector(dims, sw_idx):
    if len(dims) != 6:
        exit('ERR: invalid function parameter type(s)')

    idx_vector = len(dims) * [0]

    for dim in range(3, len(dims)):
        idx_vector[dim] = sw_idx % dims[dim]
        sw_idx = int(sw_idx / dims[dim])
    for dim in range(0, 3):
        idx_vector[dim] = sw_idx % dims[dim]
        sw_idx = int(sw_idx / dims[dim])

    return idx_vector

