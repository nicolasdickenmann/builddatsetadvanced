# Author: Alessandro Maissen
# This script purpose is to validate a created Torus 

from .common import is_directed, has_double_edges, listgraph_to_nxgraph
from random import randint

def validate(graph : [[int]], n : int, k: int):

    from networkx import Graph, is_connected
    from networkx.classes.function import degree
    
    print("--> Validating %d-ary %dD-Torus:" %(k, n))
    passed = 1

    # check sizes
    if len(graph) != k**n:
        print("     --> construction error: incorrect number of nodes")
        passed = 0
    if sum([len(node) for node in graph]) != 2*n * k**n:
        print("     --> construction error: incorrect number of edges")
        passed = 0
    
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

    # check degree of each node is equal to 2*n (twice the dimension of torus)
    degrees = degree(nx_graph)
    for d in degrees:
        if d[1] != 2*n:
            print("     --> construnction error: degree not equal to 2*n")
            passed = 0
            break

    return passed

def generate_random_parameters(nmax : int, kmax : int, number : int):
    
    parameters = []
    for _ in range(number):
        n = randint(2, nmax)
        k = randint(3, kmax)
        parameters.append((n,k))
    
    return parameters

def validate_torus():
    from .TorusGenerator import TorusGenerator

    tori = generate_random_parameters(6, 5, 5)

    results = []
    for t in tori:
        g = TorusGenerator().make(t[0], t[1])
        results.append(validate(g, t[0], t[1]))
    
    if sum(results) == len(tori):
        print("VALIDATION PASSED")
    else:
        print("VALIDATION NOT PASSED")
