# Author: Jascha Krattenmacher
# used algorithm from Domke

# PARAMETERS
# h: height -> h > 0

# VARIABLES
# N: number of routers/nodes in total

# PRECONDITIONS
# b,n > 0

from .TopologyGenerator import TopologyGenerator
from .validate_extendedGeneralizedFatTree import validate
from functools import reduce

class ExtendedGeneralizedFatTreeGenerator(TopologyGenerator):

    def __init(self):
        super(ExtendedGeneralizedFatTreeGenerator,self).__init__()
    
    def make(self, h : int, inputs : [int]) -> [[int]]:
        
        assert(h > 0)
        assert(2*h == len(inputs))

        m = inputs[:h] # children per level
        w = inputs[h:] # parents per level

        topology = {}
 
        # CONFIGS
        num_ports_per_switch = 128
        #switch_prefix = 'S'
        terminal_prefix = 'T'
        multi_link = False
        num_ports_per_terminal = 1

        # add dummy at beginning
        m.insert(0, 0)
        w.insert(0, 0)
    
        # generate a list of all switch nodes (Vh) and list of edges (Eh)
        Vh = _get_Vh(h, m, w)
        Eh = _get_Eh(h, m, w)
           
        num_switches = len(Vh)
        num_leaf_switches = 0
        for xgft_str in Vh:
            sw_lvl = _get_switch_level(None, xgft_str)
            if sw_lvl == 0:
                num_leaf_switches += 1
        
        num_terminals = num_leaf_switches
        num_terminals = 8

 
        if num_ports_per_switch == -1:
            min_ports_needed = int(ceil(num_terminals / num_leaf_switches)) + w[1]
            for lvl in range(1, h):
                if m[lvl] + w[lvl + 1] > min_ports_needed:
                    min_ports_needed = m[lvl] + w[lvl + 1]
            num_ports_per_switch = min_ports_needed
    
        # generate all switch names and add them to the topology
        j = 0

        for xgft_str in Vh:
            topology[str(xgft_str)] = [j,[]]
            j = j+1
   
        # connect all switches
        for xgft_str_1, xgft_str_2 in Eh:
            switch1 = topology[str(xgft_str_1)]
            switch2 = topology[str(xgft_str_2)]
            switch1[1].append(switch2[0])
            switch2[1].append(switch1[0])

        """                
        # connect terminals
        set_term = 0
        while set_term < num_terminals:
            for xgft_str in Vh:
                sw_lvl = _get_switch_level(None, xgft_str)
                if sw_lvl != 0:
                    continue
                switch = str(xgft_str)
                switch_id = topology[switch][0]
                terminal = _get_terminal_name(terminal_prefix, set_term)
                topology[terminal] = [j,[]]
                for x in range(num_ports_per_terminal):
                    topology[switch][1].append(j)
                    topology[terminal][1].append(switch_id)
                    ports[switch_id] -= 1
                set_term += 1
                j = j+1
                if set_term >= num_terminals:
                    break
        
        """


        # Convert to list (already indirect graph
        xgftTopology = [entry[1] for entry in topology.values()]      
        return xgftTopology


    def validate(self, topo : [[int]], h : int, inputs : [int]) -> bool:
        return validate(topo,h, inputs)
    
    def get_folder_path(self):
        return super(ExtendedGeneralizedFatTreeGenerator,self).get_folder_path() + "extGenFatTree/"

    def get_file_name(self, h : int, inputs : [int]) -> str:
        return str(h) + ".xgft.(" + ".".join(str(i) for i in inputs[:h]) + ")(" + ".".join(str(i) for i in inputs[h:]) + ").adj.txt"


#------ Hepler functions ---------

def _get_switch_name(prefix, z):
    return '%s<%s>' % (prefix, ','.join([str(x) for x in z]))

def _get_terminal_name(prefix, id):
    return '%s<%i>' % (prefix, id)

def _get_switch_level(name_str, id_vector):
    if name_str is not None and name_str != '':
        return int(name_str.split(",")[0].split("<")[1])
    elif len(id_vector) > 0:
        return id_vector[0]
    else:
        return None

def _get_array_product(array):
    if len(array) == 0:
        return 1
    else:
        return reduce(lambda x, y: x * y, array)


def _get_lambda(m, w, lvl, h):
    _lambda = _get_array_product(w[1:lvl + 1])
    _lambda *= _get_array_product(m[lvl + 1:h + 1])

    return _lambda


def _get_Vjh(j, h, m, w):
    Vjh = []

    for lvl in range(0, h + 1):
        lam = _get_lambda(m, w, lvl, h)
        for a in range(j * lam, (j + 1) * lam):
            Vjh.append([lvl, a])

    return Vjh

def _get_Vh(hp1, m, w):
    if not isinstance(hp1, int) or not isinstance(
            m, list) or not isinstance(w, list):
        exit('ERR: invalid function parameter type(s)')

    if hp1 == 0:
        return [[0, 0]]

    # first part
    Vjh = []
    h = hp1 - 1
    for j in range(0, m[hp1]):
        Vjh.extend(_get_Vjh(j, h, m, w))
    # second part
    Vh = []
    for a in range(0, _get_array_product(w[1:hp1 + 1])):
        Vh.append([hp1, a])
    # add two sets and return
    Vjh.extend(Vh)
    Vjh.sort()

    return Vjh


def _get_Ejh(j, h, m, w):
    Ejh = []
    Vjh = _get_Vjh(j, h, m, w)
    Eh = _get_Eh(h, m, w)

    for lvl in range(0, h):
        lam1 = _get_lambda(m, w, lvl, h)
        lam2 = _get_lambda(m, w, lvl + 1, h)
        wh = _get_array_product(w[1:h + 1])
        for la in Vjh:
            if la[0] != lvl:
                continue
            for lb in Vjh:
                if lb[0] != lvl + 1:
                    continue
                if Eh.count([[la[0], la[1] - j * lam1],
                             [lb[0], lb[1] - j * lam2]]) > 0:
                    Ejh.append([la, lb])

    return Ejh

def _get_Eh(hp1, m, w):
    if not isinstance(hp1, int) or not isinstance(
            m, list) or not isinstance(w, list):
        exit('ERR: invalid function parameter type(s)')

    if hp1 == 0:
        return []

    Eh = []
    h = hp1 - 1

    # first part
    for j in range(0, m[hp1]):
        Eh.extend(_get_Ejh(j, h, m, w))
    # second part
    lam1 = _get_lambda(m, w, h, hp1)
    lam2 = _get_lambda(m, w, hp1, hp1)
    wh = _get_array_product(w[1:h + 1])
    for b in range(0, lam2):
        for a in range(0, lam1):
            if a % wh == int(b / w[hp1]):
                Eh.append([[h, a], [hp1, b]])

    return Eh

