# Author: Jascha Krattenmacher
# used algorithm from Domke
# k-ary-n Tree

# PARAMETERS
# k: half the number of ports per switch -> k > 0
# n: level of the tree -> n > 0

# VARIABLES
# N: number of routers/nodes in total

# PRECONDITIONS
# k,n > 0

from .TopologyGenerator import TopologyGenerator
from .validate_karyn import validate

class KaryNGenerator(TopologyGenerator):

    def __init(self):
        super(KautzGenerator,self).__init__()
    
    def make(self, k : int, n : int) -> [[int]]:
        assert(k > 0 and n > 0)

        topology = {}
        ports = [] 

        # CONFIGS
        num_ports_per_switch = k * 2
        num_ports_per_terminal = 1
        num_terminals = pow(k, n - 1)
        switch_prefix = 'S'
        terminal_prefix = 'T'


        # start algorithm domke
        n_tuples = []
        w = [0 for x in range(n - 1)]
        n_tuples.append(w[:])
        for j in range(pow(k, n - 1)):
            for i in range(len(w)):
                w[i] += 1
                if w[i] == k:
                    w[i] = 0
                else:
                    n_tuples.append(w[:])
                    break

        # generate all switches <w,lvl>
        j = 0
        for lvl in range(n-1, -1, -1):
            for w in n_tuples:
                switch = _get_switch_name(switch_prefix, w, lvl)
                topology[switch] = [j,[]]
                j = j+1
                ports.append(num_ports_per_switch)
        
        # connect all switches
        for lvl in range(n - 1):
            for w1 in n_tuples:
                for w2 in n_tuples:
                    subw1, subw2 = w1[:lvl], w2[:lvl]
                    subw1.extend(w1[lvl + 1:])
                    subw2.extend(w2[lvl + 1:])
                    if subw1 == subw2:
                        switch1 = _get_switch_name(switch_prefix, w1, lvl)
                        switch1_id = topology[switch1][0]
                        switch2 = _get_switch_name(switch_prefix, w2, lvl + 1)
                        switch2_id = topology[switch2][0]
                        topology[switch1][1].append(switch2_id)
                        topology[switch2][1].append(switch1_id)


        # convert dict to list
        karynTopology = [entry[1] for entry in topology.values()]

        return karynTopology


 


    def validate(self, topo : [[int]], k : int, n : int) -> bool:
        return validate(topo,k,n)
    
    def get_folder_path(self):
        return super(KaryNGenerator,self).get_folder_path() + "karynTrees/"

    def get_file_name(self, k : int, n : int) -> str:
        return str(k) + "ary" + str(n) + ".adj.txt"


#------ Hepler functions ---------

def _get_switch_name(prefix, w, lvl):
    return '%s<%s,%i>' % (prefix, ','.join([str(x) for x in w]), lvl)

def _get_terminal_name(prefix, id):
    return '%s<%i>' % (prefix, id) 
