# Author: Kartik Lakhotia

import networkx as nx
import random

def validate(graph: [[int]], q : int):

    print("--> Validating Bundlefly(%d):" %q)
    
    nx_graph    = nx.Graph()
    for i in range(len(graph)):
        nx_graph.add_node(i)
        for j in graph[i]:
            nx_graph.add_edge(i, j)

    #check if graph is connected
    if not nx.is_connected(nx_graph):
        print("     --> construction error: not connected")
        return 0 

    #check max degree
    max_degree  = max(dict(nx_graph.degree).values())
    if (max_degree != q):
        print("     --> construction error: incorrect max degree")
        return 0

    min_degree  = min(dict(nx_graph.degree).values())
    if (min_degree != q):
        print("     --> construction error: incorrect min degree")
        return 0

    #check diameter
    diameter    = nx.diameter(nx_graph)
    if (diameter > 3):
        print("     --> construction error: incorrect diameter")
        return 0

    return 1 



def generate_random_params(qmax: int, num_tests: int) -> [int]:

    q_candidates    = [i for i in range(8, qmax)]
    params  = []
    for i in range(num_tests):
        qrnd        = random.randint(0, len(q_candidates))
        q           = q_candidates[qrnd]
        
        params.append(q)
    return params


def validate_bundlefly():
    from .BundleflyGenerator import BundleflyGenerator
    
    params  = generate_random_params(48, 20)
    results = []

    for param in params:
        g   = BundleflyGenerator().make(param)
        if (len(g) > 1):
            results.append(validate(g, param))
        else:
            results.append(1)
    
    if sum(results)==len(params):
        print("VALIDATION PASSED")
    else:
        print("VALIDATION NOT PASSED")
