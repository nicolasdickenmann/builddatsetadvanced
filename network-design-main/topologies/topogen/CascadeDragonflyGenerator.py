# Author: Jascha Krattenmacher
# used algorithm from Domke
# Cascade Dragonfly

# PARAMETERS
# g : number of groups

# VARIABLES
# N: number of routers/nodes in total

# PRECONDITIONS
# p,n > 0

from .TopologyGenerator import TopologyGenerator
from .validate_cascadeDragonfly import validate
from math import ceil

class CascadeDragonflyGenerator(TopologyGenerator):

    def __init(self):
        super(CascadeDragonflyGenerator,self).__init__()
    
    def make(self, g : int) -> [[int]]:
        assert(g > 0)
        
        topology = {}
        ports = {}
     
        # CONFIGS
        num_ports_per_switch = 48 
        multi_link = False
        do_port_matching = False

        p = 8
        a = 96
        h = 10 
        num_links = -1
        #number of global links between two groups (min: 4, max: a*h/(g-1))
        if g > 1:
            num_links = 4
            #num_links = a*h/(g-1)    
        
        if g > (a * h / 4) + 1:
            exit('ERR: invalid config (g > (a*h/4)+1 is impossible)')
    
        num_switches = a*g

        # generate all switches
        j = 0
        for group_id in range(g):
            # 16 router per chassi
            for sw_id_x in range(int(a / 6)):
                # 6 chassis in one group
                for sw_id_y in range(int(a / 16)):
                    vector = _get_switch_name(group_id, sw_id_x, sw_id_y)
                    topology[vector] = [j,[]]
                    ports[vector] = num_ports_per_switch
                    j = j + 1

           
        # connect switches in one group (intra-group connection)
        # each group is a 16x6 mesh w/ all-to-all in each dimension
        for group_id in range(g):
            for src_sw_id_x in range(int(a / 6)):
                for src_sw_id_y in range(int(a / 16)):
                    vector1 = _get_switch_name(group_id, src_sw_id_x, src_sw_id_y)
                    switch1 = topology[vector1][0]
                    # green cables (1x per pair)
                    for dst_sw_id_x in range(src_sw_id_x + 1, int(a / 6)):
                        vector2 = _get_switch_name(group_id, dst_sw_id_x, src_sw_id_y)
                        switch2 = topology[vector2][0]
                        topology[vector1][1].append(switch2)
                        topology[vector2][1].append(switch1)
                        ports[vector1] -= 1
                        ports[vector2] -= 1
                    # black cables (3x per pair)
                    for dst_sw_id_y in range(src_sw_id_y + 1, int(a / 16)):
                        vector2 = _get_switch_name(group_id, src_sw_id_x, dst_sw_id_y)
                        switch2 = topology[vector2][0]
                        topology[vector1][1].append(switch2)
                        topology[vector1][1].append(switch2)
                        topology[vector1][1].append(switch2)
                        topology[vector2][1].append(switch1)
                        topology[vector2][1].append(switch1)
                        topology[vector2][1].append(switch1)
                        ports[vector1] -= 3
                        ports[vector2] -= 3

        if g > 1:
            max_global_links = int(a * h / (g - 1))
        else:
            max_global_links = 0
        
        
        # setup inter-group connections, completely connected (N-to-N)
        for group_id in range(g):
            b = num_links
            for remote_group_id in range(group_id + 1, g):
                # 4 links is min. between 2 groups
                for global_link in range(min(max(4, int(b / 4) * 4), max_global_links)):
                    # find switch from local group with max. number of free ports
                    vector1 = _get_switch_in_group_with_max_fre_ports(a, group_id, ports)
                    switch1 = topology[vector1][0]
                    # find switch from remote group with max. number of free ports
                    vector2 = _get_switch_in_group_with_max_fre_ports(a, remote_group_id, ports)
                    switch2 = topology[vector2][0]
                    # connect both
                    topology[vector1][1].append(switch2)
                    topology[vector2][1].append(switch1)
                    ports[vector1] -= 1
                    ports[vector2] -= 1
         
        # convert dict to list
        casDFTopology = [entry[1] for entry in topology.values()]
        
        return casDFTopology


    def validate(self, topo : [[int]], g : int) -> bool:
        return validate(topo,p,g)
    
    def get_folder_path(self):
        return super(CascadeDragonflyGenerator,self).get_folder_path() + "casDragonflies/"

    def get_file_name(self, g : int) -> str:
        return str(g) + ".casDF.adj.txt"


#------ Hepler functions ---------
def _get_switch_name(group_id, sw_id_x, sw_id_y):
    return '%i,%i,%i' % (group_id, sw_id_x, sw_id_y)


def _get_switch_in_group_with_max_fre_ports(switches_per_group, group_id, free_ports):
    max_port_sw = None
    for sw_id_x in range(int(switches_per_group / 6)):
        for sw_id_y in range(int(switches_per_group / 16)):
            switch = _get_switch_name(group_id, sw_id_x,sw_id_y)
            if not max_port_sw or free_ports[max_port_sw] < free_ports[switch]:
                max_port_sw = switch

    return max_port_sw

