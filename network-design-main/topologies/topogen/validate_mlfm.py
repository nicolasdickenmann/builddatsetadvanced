# Author: Alessandro Maissen
# This script purpose is to validate a created h-MLFM

from .common import has_double_edges, is_directed, listgraph_to_nxgraph
from random import randint

def validate(graph : [[int]], h : int):

    from networkx import Graph, is_connected
    from networkx.classes.function import degree
    from networkx.algorithms import bipartite
    
    print("--> Validating %d-MLFM:" %h)
    passed = 1

    # check sizes
    if len(graph) != h*(h+1)*3/2:
        print("     --> construction error: incorrect number of nodes")
        passed = 0
    if sum([len(node) for node in graph]) != h*(h+1)*h + (h+1)*h*h:
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

    # check degrees of each nodes (h + 1)*h/2 nodes have degree 2*h and (h+1)*h nodes have degree h
    degrees = degree(nx_graph)
    gdegree = 0
    ldegree = 0
    odegree = 0

    for d in degrees:
        if d[1] == 2*h:
            gdegree += 1
        elif d[1] == h:
            ldegree += 1
        else:
            odegree += 1

    if gdegree != (h + 1)*h/2 or ldegree != (h+1)*h or odegree != 0: 
        print("     --> construnction error: degree not equal to n")
        passed = 0
    
    # check if graph is bipartite
    if not bipartite.is_bipartite(nx_graph):
         print("     --> construnction error: not bipartid")
         passed = 0
    
    # check sizes of two bipartite set
    bottom_nodes, top_nodes = bipartite.sets(nx_graph)
    len_bn = len(bottom_nodes)
    len_tn = len(top_nodes)
    if not(len_bn == h*(h+1) and len_tn == h*(h+1)/2) and not (len_tn == h*(h+1) and len_bn == h*(h+1)/2):
        print("     --> construnction error: incorrect sizes of bipartite sets")
        passed = 0

    return passed

def generate_random_parameters(nmax : int, number : int):
    
    parameters = []
    for _ in range(number):
        n = randint(1, nmax)
        parameters.append(n)
    
    return parameters

def validate_mlfm():
    from .MLFMGenerator import MLFMGenerator
    
    mlfls = generate_random_parameters(20, 5)

    results = []
    for m in mlfls:
        g = MLFMGenerator().make(m)
        results.append(validate(g, m))
    
    if sum(results) == len(mlfls):
        print("VALIDATION PASSED")
    else:
        print("VALIDATION NOT PASSED")
