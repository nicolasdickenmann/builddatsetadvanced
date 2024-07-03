# Author: Jascha Krattenmacher
# This script purpose is to validate a created k-ary-n Network

from .common import has_double_edges, is_directed, listgraph_to_nxgraph
from random import randint

def validate(graph : [[int]], k : int, n : int):

    from networkx import Graph, is_connected
    from networkx.classes.function import degree
    
    print("--> Validating %d-ary-%d:" %(k,n))
    passed = 1

    # TODO: calculate specific values
    # check sizes
#    if len(graph) != 2**n:
#        print("     --> construction error: incorrect number of nodes")
#        passed = 0
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

def generate_random_parameters(kmax : int, nmax : int, number : int):
    
    parameters = []
    for _ in range(number):
        n = randint(1, nmax)
        k = randint(1, kmax)
        parameters.append((k,n))
    
    return parameters

def validate_karyn():
    from .KaryNGenerator import KaryNGenerator
    
    karyns = generate_random_parameters(10, 10, 5)

    results = []
    for kn in karyns:
        g = KaryNGenerator().make(kn)
        results.append(validate(g, kn))
    
    if sum(results) == len(karyns):
        print("VALIDATION PASSED")
    else:
        print("VALIDATION NOT PASSED")

