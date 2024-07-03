# Author: Alessandro Maissen
# This script purpose is to validate a created Torus 

from .common import is_directed, has_double_edges, listgraph_to_nxgraph
from random import randint
from functools import reduce

def validate(graph : [[int]], d : int, lifts: [int]):

    from networkx import Graph, is_connected
    from networkx.classes.function import degree
    
    print("--> Validating Xpander(%d) with lifts %s:" %(d, lifts))

    # check sizes
    if len(graph) != (d + 1) * reduce(lambda x,y: x*y, lifts, 1):
        print("     --> construction error: incorrect number of nodes")
        return 0
    if sum([len(node) for node in graph]) != (d + 1) * reduce(lambda x,y: x*y, lifts, 1) * d:
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

    # check degree of each node is equal to d
    degrees = degree(nx_graph)
    for deg in degrees:
        if deg[1] != d:
            print("     --> construnction error: degree not equal to d")
            return 0

    return 1

def generate_random_parameters(dmax : int, number : int):
    from .XpanderGenerator import factors

    parameters = []
    for _ in range(number):
        d = randint(1, int(dmax/2))*2
        lifts1 = [d]
        parameters.append((d,lifts1))
        lifts2 = factors(d,q=2)
        parameters.append((d,lifts2))
    
    return parameters

def validate_xpander():
    from .XpanderGenerator import XpanderGenerator,factors

    xpanders = generate_random_parameters(16, 5)

    results = []
    for xp in xpanders:
        g = XpanderGenerator().make(xp[0], xp[1])
        results.append(validate(g, xp[0], xp[1]))
    
    if sum(results) == len(xpanders):
        print("VALIDATION PASSED")
    else:
        print("VALIDATION NOT PASSED")
