# Author: Jascha Krattenmacher
# used algorithm from Domke
# K(b,n) Kautz Graph

# PARAMETERS
# b: base -> b > 0
# n: length -> n > 0

# VARIABLES
# N: number of routers/nodes in total

# PRECONDITIONS
# b,n > 0

from .TopologyGenerator import TopologyGenerator
from .validate_kautz import validate
from copy import deepcopy

class KautzGenerator(TopologyGenerator):

    def __init(self):
        super(KautzGenerator,self).__init__()
    
    def make(self, b : int, n : int) -> [[int]]:
        assert(n > 0 and b > 0)
        
        # configure the namespace for Kautz switches
        KautzSpace = []
        topology = {} #
 
        multi_link = True
        

        z = [0 for x in range(n)]
        for j in range(pow(b + 1, n)):
            for i in range(len(z)):
                z[i] += 1
                if z[i] == b + 1:
                    z[i] = 0
                else:
                    KautzSpace.append(z[:])
                    break
        # test, whether the combination is really a Kautz graph
        # i.e., for all i: z(i) != z(i+1), or remove duplicates
        j = 0
        while j < len(KautzSpace):
            z = KautzSpace[j]
            try:
                for i in range(len(z) - 1):
                    if z[i] == z[i + 1]:
                        KautzSpace.remove(z)
                        raise StopIteration()
                j += 1
            except StopIteration:
                pass
   
        # generate all switches S<Kautz string>
        i = 0
        for z in KautzSpace:
            topology[str(z)] = [i,[]]
            i = i+1
   

        # now actually set a link between switches
        for z in KautzSpace:
            for a in range(b + 1):
                if z[-1] != a:
                    switch1 = topology[str(z)][0]
                    switch2 = topology[str(z[1:] + [a])][0]
                    topology[str(z)][1].append(switch2)
                    topology[str(z[1:] + [a])][1].append(switch1)
            

        KautzTopology = [entry[1] for entry in topology.values() ]
 

        return KautzTopology


    def validate(self, topo : [[int]], b : int, n : int) -> bool:
        return validate(topo, b, n)
    
    def get_folder_path(self):
        return super(KautzGenerator,self).get_folder_path() + "kautz/"

    def get_file_name(self, b : int, n : int) -> str:
        return str(b) + "Kautz." + str(n) + ".adj.txt"


#------ Hepler functions ---------

def _get_switch_name(prefix, z):
    return '%s<%s>' % (prefix, ','.join([str(x) for x in z]))
 
