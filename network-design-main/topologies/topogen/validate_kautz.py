# Author: Jascha Krattenmacher
# This script's purpose is to validate a created Kautz topology

from .common import has_double_edges, is_directed, listgraph_to_nxgraph
from random import randint

def validate(graph : [[int]], b : int, n: int):

    from networkx import is_connected
    from networkx.classes.function import degree

    print("--> Validating Kautz%d-%d:" %(b,n))
 
    # check sizes
    if len(graph) != (b+1)*b**(n-1):
        print("     --> construction error: incorrect number of nodes")
        return 0
    # ToDO: find out correct calculation for 
    # if sum([len(node) for node in graph]) != (b+1)*b**(n):
    #    print("     --> construction error: incorrect number of edges")
    #    return 0
    
    # check for double edges
    if has_double_edges(graph):
        print("     --> construction error: has double edges")
        return 0
    
    # construct a nx graph (undirected, no multi-edges) for further validation
    nx_graph = listgraph_to_nxgraph(graph)

    # check if graph is connected
    if not is_connected(nx_graph):
        print("     --> construnction error: not conncected")
        return 0

    # TODO: make some clique tests

    return 1

def generate_random_parameters(bmax : int, nmax : int,  number : int) -> [int]:

    parameters = []
    while len(parameters) != number:
        b = randint(2, bmax)
        n = randint(2, nmax)
        parameters.append((b,n))
    return parameters

def validate_kautz():
    from .KautzGenerator import KautzGenerator

    kautzs = generate_random_parameters(6,6,5)

    results = []
    for bn in kautzs:
        g = KautzGenerator().make(bn[0], bn[1])
        results.append(validate(g, bn[0], bn[1]))
    
    if sum(results) == len(kautzs):
        print("VALIDATION PASSED")
    else:
        print("VALIDATION NOT PASSED")
