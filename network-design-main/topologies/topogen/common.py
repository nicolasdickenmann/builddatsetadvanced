# Author: Alessandro Maissen
# Commonly used functions

from math import floor
import numpy as np
from .naming import topo_folders
from os import system
import scipy.sparse as ss

def listgraph_to_nxgraph(list_graph : [[int]]):
    from networkx import Graph

    graph = Graph()
    for i in range(len(list_graph)):
        graph.add_node(i)
        for j in list_graph[i]:
            graph.add_edge(i, j)
    return graph

def has_double_edges(list_graph : [[int]]) -> bool:
    
    for node in list_graph:
        if len(list(set(node))) != len(node):
            print(len(list(set(node))))
            return True
    return False

def is_directed(list_graph : [[int]]) -> bool:
    
    n = len(list_graph)

    for i in range(n):
        for j in range(n):
            t1 = [x for x in list_graph[i] if x == j]
            t2 = [x for x in list_graph[j] if x == i]
            if not(len(t1) == 1 and len(t2) == 1) and not(len(t1) == 0 and len(t2) == 0):
                return True
    return False

def output_graph(graph, file=None):
    with open(file, "w") as f:
        print(len(graph), int(sum(len(n) for n in graph) / 2), file=f)
        for node in graph:
            print( " ".join(str(e) for e in node) + " ", file=f)


# approxiamtes f(x)^-1 = c for monocally increasing f and f(0) < = c
def approx_inverse(c : int, f) -> int:
    assert(f(0) <= c)

    ub = 0
    lb = 0
    # raw estimate of upper bound
    while f(ub) < c:
        if ub == 0:
            ub = 1
        else:   
            ub *= 2
    
    # binary search
    while lb <= ub:
        mid = floor((ub + lb) / 2)
        if f(mid) > c:
            ub = mid - 1
        elif f(mid) < c:
            lb = mid + 1
        else:
            return mid

    return lb

def is_prime(x : int) -> bool:
    return len([d for d in range(1,x+1) if x % d == 0]) == 2

# returns (0,0) if q not a prime power else retruns (p,m) where q = p^m
def get_power_of_prime(q : int):
    
    prime_divisors = [d for d in range(2,q+1) if q % d == 0 and is_prime(d)]

    if len(prime_divisors) != 1:
        return (0,0)
    else:
        prime = prime_divisors[0]
        m = 0
        while(q != 1):
            if q % prime == 0:
                q = q / prime
                m += 1
            else:
                return (0,0)

    return (prime, m)

def is_power_of_prime(q : int) -> bool:
    return get_power_of_prime(q)[0] > 0 and get_power_of_prime(q)[1] > 0


def read_listgraph(filepath : str) -> [[int]]:

    f = open(filepath)

    firstline = f.readline().split(" ")
    edges = int(firstline[1])
    vertices = int(firstline[0])

    list_graph = [[] for _ in range(vertices)]

    vertex = 0
    for line in f:
        s = line.split(" ")
        for i in range(len(s)-1):
            list_graph[vertex].append(int(s[i]))
        vertex += 1
    
    if 2*edges != sum(len(row) for row in list_graph):
        raise Exception('Malformed graph file')
    
    return list_graph

def read_matrixgraph(filepath: str):
    f = open(filepath)

    firstline = f.readline().split(" ")
    edges = int(firstline[1])
    vertices = int(firstline[0])
    
    matrix_graph = np.matrix(np.zeros((vertices, vertices)), dtype=np.float64)

    vertex = 0
    for line in f:
        s = line.split(" ")
        for i in range(len(s)-1):
            eid = int(s[i])
            matrix_graph[vertex, eid] += 1
        vertex=vertex+1
    if matrix_graph.sum() != edges*2:
        raise Exception("Malformed graph file!")
    
    return matrix_graph

def from_list_graph_to_matrix_graph(list_graph : [[int]]):
    
    vertices = len(list_graph)
    edges = int(sum([len(row) for row in list_graph]) / 2)

    matrix_graph = np.matrix(np.zeros((vertices, vertices)), dtype=np.float64)

    for i in range(vertices):
        for j in list_graph[i]:
            matrix_graph[i,j] += 1
    
    assert(2 * edges == matrix_graph.sum())

    return matrix_graph

# converts a list graph to a sparce matrix (csr)
def from_list_graph_to_sparse_matrix(listgraph : [[int]]):

    n = len(listgraph)
    rows = []
    cols = []

    for i in range(n):
        for j in listgraph[i]:
            rows.append(i)
            cols.append(j)
    data = np.ones(len(rows), np.uint32)
    matrix = ss.coo_matrix((data, (rows, cols)))

    return matrix.tocsr()


def clean_topologies(topos : [str], databases : [str], p : bool, a : bool ):

    if a:
        topos = []
        databases = []
        p = True
        system("rm -r data/")

    for t in topos:
        if t == 'all':
            for it in scandir('data/'):
                if it.is_dir() and it.path != 'data/analysis':
                    system("rm -r %s/" %it.path)
        else:
            system("rm -r data/%s/" %t)

    for db in databases:
        if db == 'all':
            system("rm -r data/analysis/")
        else:
            system("rm data/analysis/%s" %db)

    if p:
        system("rm *_plot.pdf")
        system("rm *_plot.info")

