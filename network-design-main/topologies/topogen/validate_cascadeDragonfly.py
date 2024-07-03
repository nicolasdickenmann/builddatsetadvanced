# Author: Jascha Krattenmacher 
# This script's purpose is to validate a created Cascade Dragonfly topology

from .common import has_double_edges, is_directed, listgraph_to_nxgraph
from random import randint

def validate(graph : [[int]], p : int, g : int):

    from networkx import is_connected
    from networkx.classes.function import degree

    print("--> Validating Cascade Dragonfly(%d,%d):" %(p,g))

    # check sizes
    if len(graph) != 4*p**3 + 2*p:
        print("     --> construction error: incorrect number of nodes")
        return 0
    if sum([len(node) for node in graph]) != (4*p**3 + 2*p) * (3*p - 1):
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
    if any([d[1] != (3*p - 1) for d in degrees]):
         print("     --> construction error: incorrect degrees")
         return 0

    # TODO: more tests

    return 1

def generate_random_parameters(pmax : int, gmax : int, number : int) -> [int]:

    parameters = []
    for _ in range(number):
        p = randint(1, pmax)
        g = randint(1, gmax)
        parameters.append((p,g))
    return parameters

def validate_cascadeDragonfly():
    from .CascadeDragonflyGenerator import CascadeDragonflyGenerator
    
    dragonflies = generate_random_parameters(10,5,5)

    results = []
    for df in dragonflies:
        g = CascadeDragonflyGenerator().make(df)
        results.append(validate(g, df))
    
    if sum(results) == len(dragonflies):
        print("VALIDATION PASSED")
    else:
        print("VALIDATION NOT PASSED")
