# Author: Alessandro Maissen
# This script's purpose is to validate a created Jellyfish topology

from .common import has_double_edges, is_directed, listgraph_to_nxgraph
from random import randint

def validate(graph : [[int]], r : int, n: int):

    from networkx.classes.function import degree

    print("--> Validating Jellyfish(%d,%d):" %(r,n))

    # check sizes
    if len(graph) != n:
        print("     --> construction error: incorrect number of nodes")
        return 0
    if sum([len(node) for node in graph]) != r * n:
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

    # check if graph is r-regular
    degrees = degree(nx_graph)
    if any([d[1] != r for d in degrees]):
         print("     --> construction error: incorrect degrees")
         return 0

    return 1

def generate_random_parameters(rmax : int, nmax : int,  number : int) -> [int]:
    assert(rmax < nmax)

    parameters = []
    while len(parameters) != number:
        r = randint(2, rmax)
        n = randint(3, nmax)
        if r < n and r*n % 2 == 0:
            parameters.append((r,n))
    
    return parameters

def validate_jellyfish():
    from .JellyfishGenerator import JellyfishGenerator

    jellyfishes = generate_random_parameters(20, 2000, 5)
    #jellyfishes = [(6, 1000), (35, 1058)]

    results = []
    for jf in jellyfishes:
        g = JellyfishGenerator().make(jf[0], jf[1])
        results.append(validate(g, jf[0], jf[1]))
    
    if sum(results) == len(jellyfishes):
        print("VALIDATION PASSED")
    else:
        print("VALIDATION NOT PASSED")