# Author: Alessandro Maissen
# This script's purpose is to validate a created Dragonfly topology

from .common import has_double_edges, is_directed, listgraph_to_nxgraph
from random import randint

def validate(graph : [[int]], p : int):

    from networkx import is_connected
    from networkx.classes.function import degree

    print("--> Validating Dragonfly(%d):" %p)

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

def generate_random_parameters(pmax : int, number : int) -> [int]:

    parameters = []
    for _ in range(number):
        p = randint(1, pmax)
        parameters.append(p)
    return parameters

def validate_dragonfly():
    from .DragonflyGenerator import DragonflyGenerator
    
    dragonflies = generate_random_parameters(10,5)

    results = []
    for df in dragonflies:
        g = DragonflyGenerator().make(df)
        results.append(validate(g, df))
    
    if sum(results) == len(dragonflies):
        print("VALIDATION PASSED")
    else:
        print("VALIDATION NOT PASSED")