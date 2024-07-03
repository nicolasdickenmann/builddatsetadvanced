# Author: Alessandro Maissen
# This script's purpose is to validate a created HyperX topology

from .common import has_double_edges, is_directed, listgraph_to_nxgraph
from random import randint

def validate(graph : [[int]], l : int, s: int):

    from networkx import is_connected
    from networkx.classes.function import degree

    print("--> Validating HyperX%d-%d:" %(l,s))

    # check sizes
    if len(graph) != s**l:
        print("     --> construction error: incorrect number of nodes")
        return 0
    if sum([len(node) for node in graph]) != l*(s-1)*s**l:
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

    # check if graph is regular
    degrees = degree(nx_graph)
    if any([d[1] != l*(s-1) for d in degrees]):
         print("     --> construction error: incorrect degrees")
         return 0

    # TODO: make some clique tests

    return 1

def generate_random_parameters(lmax : int, smax : int,  number : int) -> [int]:

    parameters = []
    while len(parameters) != number:
        l = randint(2, lmax)
        s = randint(3, smax)
        parameters.append((l,s))
    return parameters

def validate_hyperx():
    from .HyperXGenerator import HyperXGenerator

    hyperxs = generate_random_parameters(3,11,5)

    results = []
    for hx in hyperxs:
        g = HyperXGenerator().make(hx[0], hx[1])
        results.append(validate(g, hx[0], hx[1]))
    
    if sum(results) == len(hyperxs):
        print("VALIDATION PASSED")
    else:
        print("VALIDATION NOT PASSED")