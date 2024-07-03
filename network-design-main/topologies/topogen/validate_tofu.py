# Author: Jascha Krattenmacher
# This script purpose is to validate a created HyperCube

from .common import has_double_edges, is_directed, listgraph_to_nxgraph
from random import randint

def validate(graph : [[int]], d1 : int, d2 : int, d3 : int):

    from networkx import Graph, is_connected
    from networkx.classes.function import degree
    
    print("--> Validating %dx%dx%dx2x3x2-Tofu:" %(d1,d2,d3))
    passed = 1

    # check sizes
    if len(graph) != d1*d2*d3*2*3*2:
        print("     --> construction error: incorrect number of nodes")
        passed = 0
#    if sum([len(node) for node in graph]) != n * 2**n:
#        print("     --> construction error: incorrect number of edges")
#        passed = 0
    
    # check for double edges
    if has_double_edges(graph):
        print("     --> construction error: has double edges")
        passed = 0

    # check if graph is undirected
    if is_directed(graph):
        print("     --> construction error: not undirected")
        passed = 0

    # construct a nx graph (undirected, no multi-edges) for further validation
    nx_graph = listgraph_to_nxgraph(graph)

    # check if graph is connected
    if not is_connected(nx_graph):
        print("     --> construnction error: not conncected")
        passed = 0

    return passed

def generate_random_parameters(dmax : int, number : int):
    
    parameters = []
    for _ in range(number):
        d1 = randint(1, dmax)
        d2 = randint(1, dmax)
        d3 = randint(1, dmax)
        parameters.append((d1,d2,d3))
    
    return parameters

def validate_tofu():
    from .TofuGenerator import TofuGenerator
    
    tofus = generate_random_parameters(5, 5)

    results = []
    for t in tofus:
        g = TofuGenerator().make(t)
        results.append(validate(g, t))
    
    if sum(results) == len(tofus):
        print("VALIDATION PASSED")
    else:
        print("VALIDATION NOT PASSED")

