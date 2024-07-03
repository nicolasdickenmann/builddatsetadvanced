# Author: Jascha Krattenmacher 
# This script purpose is to validate a created Mesh

from .common import has_double_edges, is_directed, listgraph_to_nxgraph
from random import randint

def validate(graph : [[int]], n1 : int, n2 : int):

    from networkx import Graph, is_connected
    from networkx.classes.function import degree
    
    print("--> Validating %dx%d-Mesh:" %(n1,n2))
    passed = 1

    # check sizes
    if len(graph) != n1*n2:
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

def generate_random_parameters(nmax : int, number : int):
    
    parameters = []
    for _ in range(number):
        n1 = randint(1, nmax)
        n2 = randint(1, nmax)
        parameters.append((n1,n2))
    
    return parameters

def validate_mesh():
    from .MeshGenerator import MeshGenerator
    
    meshes = generate_random_parameters(10, 5)

    results = []
    for m in meshes:
        g = HypercubeGenerator().make(m)
        results.append(validate(g, m))
    
    if sum(results) == len(meshes):
        print("VALIDATION PASSED")
    else:
        print("VALIDATION NOT PASSED")

