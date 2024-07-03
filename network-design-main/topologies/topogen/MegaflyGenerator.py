# Author: Jascha Krattenmacher, Algorithm by Kartik Lakhotia
# Megafly(d,g)

# PARAMETERS
# d: total radix, must be even
# g: number of links between each pair of groups

# VARIABLES
# n: total number of routers

# PRECONDITIONS
# d even, d,g > 0

from .TopologyGenerator import TopologyGenerator
#from .validate_dragonfly import validate
from math import sqrt
import networkx as nx
import numpy as np

class MegaflyGenerator(TopologyGenerator):

    def __init(self):
        super(MegaflyGenerator,self).__init__()
    
    def make(self, g : int, d : int) -> [[int]]:

        assert(d%2 == 0)
        
        G       = mega_gen(d//2, g)
        print ("number of nodes = " + str(G.number_of_nodes()))
        print ("number of edges = " + str(G.number_of_edges()))
        print ("diameter = " + str(nx.diameter(G)))

        V   = G.number_of_nodes()
        E   = G.number_of_edges()
        G_list = []
    
        for i in range(V):
            neigh   = [n for n in G.neighbors(i)]
            G_list.append(neigh)

        return G_list


    def validate(self, topo : [[int]], p : int) -> bool:
        return validate(topo,p)
    
    def get_folder_path(self):
        return super(MegaflyGenerator,self).get_folder_path() + "megaflies/"

    def get_file_name(self, g : int, d : int) -> str:
        return "Megafly." + str(g) + "_"  + str(d) + ".adj.txt"


########### Hepler Functions #############

def get_start_link(srcGrp, dstGrp, g):
    assert(not(srcGrp == dstGrp))
    if (dstGrp > srcGrp):
        dstGrp -= 1
    link    = g*dstGrp
    return link

#p -> # routers on each side in a group
#g -> # links between each pair of groups
def mega_gen(p, g):
    numGlobLinks    = p*p
    assert(numGlobLinks % g == 0)

    numGroups       = numGlobLinks//g + 1
    numDirRouters   = numGroups*p
    numIndirRouters = numGroups*p
    numRouters      = numDirRouters + numIndirRouters

    G               = nx.Graph()
    V               = numRouters
    for i in range(V):
        G.add_node(i)

    #Add intra-group links
    for i in range(numRouters):
        classOff    = numDirRouters if (i >= numDirRouters) else 0
        classId     = i - classOff
        assert(classId >= 0)

        grpId       = (classId//p)

        neighOff    = numDirRouters - classOff
        neighStart  = grpId*p + neighOff
        neighEnd    = (grpId + 1)*p + neighOff

        for j in range(neighStart, neighEnd):
            assert(j < numRouters)
            G.add_edge(i, j)

    #Add inter-group links
    for i in range(numRouters):
        if (i < numDirRouters):
            continue
        indirRouterId   = (i - numDirRouters)
        grpId           = indirRouterId//p
        grpRouterOff    = indirRouterId%p
        for j in range(p):
            grpLinkId   = grpRouterOff*p + j
            dstGrpId    = grpLinkId//g
            if (dstGrpId >= grpId):
                dstGrpId    += 1
            assert(dstGrpId < numGroups)
            dstLinkId   = get_start_link(dstGrpId, grpId, g) + (grpLinkId%g)
            dstRouterId = (dstLinkId)//p + dstGrpId*p + numDirRouters
            assert(dstRouterId < numRouters)
            G.add_edge(i, dstRouterId)


    return G

