# Author: Alessandro Maissen
# This script's purpose is to validate a created Two-Level Orthogonal Fat-Tree

from .common import has_double_edges, is_directed, listgraph_to_nxgraph, is_prime
from random import randint

def validate(graph : [[int]], k : int) -> int:

    from networkx import Graph, is_connected
    from networkx.classes.function import degree, neighbors
    from networkx.algorithms import bipartite
    
    print("--> Validating %d-OFT:" %k)

    # check sizes
    if len(graph) != 3*(1 + k*(k-1)):
        print("     --> construction error: incorrect number of nodes")
        return 0
    if sum([len(node) for node in graph]) != 4*k*(1 + k*(k-1)):
        print("     --> construction error: incorrect number of edges")
        return 0
    
    # check for double edges
    if has_double_edges(graph):
        print("     --> construction error: has double edges")
        return 0

    # check if graph is undirected
    if is_directed(graph):
        print("     --> construction error: not undirected")
        return 0

    # construct a nx graph (undirected, no multi-edges) for further validation
    nx_graph = listgraph_to_nxgraph(graph)

    # check if graph is connected
    if not is_connected(nx_graph):
        print("     --> construnction error: not conncected")
        return 0

    # check if graph is bipartite
    if not bipartite.is_bipartite(nx_graph):
         print("     --> construnction error: not bipartid")
         return 0

    # check sizes of two bipartite sets
    bottom_nodes, top_nodes = bipartite.sets(nx_graph)
    len_bn = len(bottom_nodes)
    len_tn = len(top_nodes)
    if not(len_bn == (1 + k*(k-1)) and len_tn == 2*(1 + k*(k-1))) and not (len_tn == (1 + k*(k-1)) and len_bn == 2*(1 + k*(k-1))):
        print("     --> construnction error: incorrect sizes of bipartite sets")
        return 0

    # exploit the different layers
    L1 = set()
    L02 = set()
    if len_bn == (1 + k*(k-1)):
        L1 = list(bottom_nodes)
        L02 = list(top_nodes)
    else:
        L1 = list(top_nodes)
        L02 = list(bottom_nodes)

    # check degrees of layers
    degrees_L1 = degree(nx_graph, L1)
    degrees_L02 = degree(nx_graph, L02)

    if len(set([d[1] for d in degrees_L1])) != 1 or len(set([d[1] for d in degrees_L02])) != 1:
        print("     --> construnction error: degree are not all the same in one layer")
        return 0 
    else:
        L1_node = next(iter(L1))
        L02_node = next(iter(L02))
        if not (degrees_L1(L1_node) == 2*k and degrees_L02(L02_node) == k):
            print("     --> construnction error: incorrect degree in one layer")
            return 0

    # check that two distinct nodes in Layer 02 connect two exacly one or exactly k in common nodes of Layer 1
    for i, j in [(i,j) for i in list(L02) for j in list(L02)]:
        if i != j:
            l = len(set(neighbors(nx_graph, i)).intersection(neighbors(nx_graph, j)))
            if l != 1 and l != k:
                print("     --> construnction error: maybe k - 1 is not prime, if it is conntact developer")
                return 0

    return 1

def generate_random_parameters(kmax : int, number : int) -> [int]:
    
    parameters = []
    while len(parameters) != number:
        k = randint(3, kmax)
        if(is_prime(k-1)):
            parameters.append(k)
    
    return parameters

def validate_oft():
    from .OFTGenerator import OFTGenerator
    
    ofts = generate_random_parameters(40, 5)

    results = []
    for o in ofts:
        g = OFTGenerator().make(o)
        results.append(validate(g, o))
    
    if sum(results) == len(ofts):
        print("VALIDATION PASSED")
    else:
        print("VALIDATION NOT PASSED")

