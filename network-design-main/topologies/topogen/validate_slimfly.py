# Author: Alessandro Maissen
# This script's purpose is to validate a created SlimFly topology

from .common import has_double_edges, is_directed, listgraph_to_nxgraph, is_power_of_prime
from random import randint

def validate(graph : [[int]], q : int):

    from networkx import is_connected
    from networkx.classes.function import degree

    print("--> Validating SlimFly(%d):" %q)

    # find the form q = 4w + delta, where delta is 0, 1 or -1
    w = 0
    delta = 0
    if q % 4 == 3: 
        delta = -1 
    else: 
        delta = q % 4
    
    assert((q - delta) % 4 == 0)
    w = int((q - delta) / 4)

    # check sizes
    if len(graph) != 2*q**2:
        print("     --> construction error: incorrect number of nodes")
        return 0
    if sum([len(node) for node in graph]) != 2*q**2 * ((3*q - delta)/2):
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
    if any([d[1] != ((3*q - delta)/2) for d in degrees]):
         print("     --> construction error: incorrect degrees")
         return 0


    return 1

def generate_random_parameters(qmax : int, number : int) -> [int]:

    parameters = []
    while len(parameters) < number:
        q = randint(3, qmax)
        if (q % 4 == 1 or q % 4 == 3 or q % 4 == 0) and is_power_of_prime(q):
            parameters.append(q)
    return parameters

def validate_slimfly():
    from .SlimFlyGenerator import SlimFlyGenerator
    
    slimflies = generate_random_parameters(20,5)

    results = []
    for sf in slimflies:
        g = SlimFlyGenerator().make(sf)
        results.append(validate(g, sf))
    
    if sum(results) == len(slimflies):
        print("VALIDATION PASSED")
    else:
        print("VALIDATION NOT PASSED")