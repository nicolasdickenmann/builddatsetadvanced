# Author: Jascha Krattenmacher, Algorithm by Kartik Lakhotia
# SpectralFly(p,q)

# PARAMETERS
# v,w: primes

# VARIABLES
# n: total number of routers

# PRECONDITIONS
# v,w > 2, v != w

from .TopologyGenerator import TopologyGenerator
#from .validate_dragonfly import validate
from math import sqrt
import networkx as nx
import numpy as np

class SpectralflyGenerator(TopologyGenerator):

    def __init(self):
        super(SpectralflyGenerator,self).__init__()
    
    def make(self, p : int, q : int) -> [[int]]:

        v = p
        w = q

        assert(is_prime(v))
        assert(is_prime(w))
        assert(v%2 == 1)
        assert(w%2 == 1)
        assert(not (v==w))
        assert(w > 2*sqrt(v))
        
        G       = nx.Graph()
        
        sym     = legendre(v, w)
        assert(sym==1 or sym==-1)
        
        if (sym==1):
            G   = psl_gen(v, w)
        else:
            G   = pgl_gen(v, w)
        
        expV    = ((3-sym)*(w*w*w-w))//4
        assert(G.number_of_nodes()==expV)
        
        print ("number of nodes = " + str(G.number_of_nodes()))
        print ("number of edges = " + str(G.number_of_edges()))
        print ("diameter = " + str(nx.diameter(G)))
        
        G_list = []
        V   = G.number_of_nodes()
        #E   = G.number_of_edges()
    
        for i in range(V):
            neigh   = [n for n in G.neighbors(i)]
            G_list.append(neigh)

        return G_list



    def validate(self, topo : [[int]], p : int) -> bool:
        return validate(topo,p)
    
    def get_folder_path(self):
        return super(SpectralflyGenerator,self).get_folder_path() + "spectralflies/"

    def get_file_name(self, p : int, q : int) -> str:
        return "Spectralfly." + str(p) + "_"  + str(q) + ".adj.txt"


############# Hepler Functions #################
def is_prime(q):
    for i in range(2,q):
        if (q%i == 0):
            return False
    return True

def create_cand(a):
    if (a>0):
        return[a,-a]
    else:
        return [a]
    return init_list

def quad_solve(p):
    sol     = []
    vals    = [_ for _ in range(p)]
    a0vals  = []
    if (p%4 == 1):
        a0vals  = [2*i+1 for i in range((p-1)//2)]
    else:
        assert(p%4 == 3)
        a0vals  = [2*i for i in range(p//2)]

    for a0 in a0vals:
        lhsp1   = a0*a0
        if (lhsp1 > p):
            break
        a0cand  = [a0]
        for a1 in vals:
            if (a0==0 and a1==0):
                continue
            lhsp2   = lhsp1 + a1*a1
            if (lhsp2 > p):
                break
            a1cand  = [a1] if a0==0 else create_cand(a1)
            for a2 in vals:
                lhsp3   = lhsp2 + a2*a2
                if (lhsp3 > p):
                    break
                a2cand  = create_cand(a2)
                for a3 in vals:
                    lhs = lhsp3 + a3*a3
                    a3cand  = create_cand(a3)
                    if (lhs==p):
                        for i in a0cand:
                            for j in a1cand:
                                for k in a2cand:
                                    for l in a3cand:
                                        sol.append([i, j, k, l])
                    if (lhs > p):
                        break

    assert(len(sol) == p+1)
    return sol

def xy_solve(q):
    vals    = [_ for _ in range(q)]
    for x in vals:
        for y in vals:
            lhs = (x*x + y*y + 1)%q
            if (lhs == 0):
                return x,y
    assert(0)

def ff_inv(q):
    inv     = {}
    for i in range(1,q):
        for j in range(1,q):
            mul = (i*j)%q
            if (mul == 1):
                inv[i]  = j
                break
    for i in range(1,q):
        assert(i in inv)
    return inv

def ff_root(q):
    root    = {}
    for i in range(1,q):
        mul         = (i*i)%q
        root[mul]   = i
    return root


def generator(p, q):
    asol    = quad_solve(p)
    x,y     = xy_solve(q)

    genS    = []
    for a in asol:
        m0  = (a[0] + a[1]*x + a[3]*y)%q
        m1  = (-a[1]*y + a[2] + a[3]*x)%q
        m2  = (-a[1]*y - a[2] + a[3]*x)%q
        m3  = (a[0] - a[1]*x - a[3]*y)%q
        m   = np.matrix([[m0, m1], [m2, m3]], dtype='i4')
        genS.append(m)

    assert(len(genS)==p+1)
    return genS

def pgl_normalize(mat, inv, q):
    norm    = mat%q
    fnz     = norm[1,0] if norm[0,0]==0 else norm[0,0]
    assert(fnz > 0)
    if (not fnz==1):
        fnzi    = inv[fnz]
        norm    = (fnzi*norm)%q
    return norm

def pgl_gen(p, q):
    zdet    = 0
    nzdet   = 0
    nodes   = []
    ffElems = [_ for _ in range(q)]
    inv     = ff_inv(q)
    for j in range(q):
        for k in range(q):
            for l in range(q):
                m   = tuple([1, j, k, l])#np.matrix([[1, j], [k, l]])
                det = l - j*k
                if ((det%q)==0):
                    zdet    += 1
                else:
                    nzdet   += 1
                    nodes.append(m)

    for k in range(q):
        for l in range(q):
            m   = tuple([0, 1, k, l])#np.matrix([[0, 1], [k, l]])
            det = -k
            if ((det%q)==0):
                zdet    += 1
            else:
                nzdet   += 1
                nodes.append(m)

    assert(nzdet == q*q*q - q)

    G       = nx.Graph()
    V       = len(nodes)
    vToM    = {}
    for i in range(V):
        G.add_node(i)
        vToM[nodes[i]]  = i

    S   =   generator(p, q)
    for i in range(len(S)):
        S[i]    = pgl_normalize(S[i], inv, q)

    for i in range(V):
        m   = np.matrix([[nodes[i][0], nodes[i][2]], [nodes[i][1], nodes[i][3]]], dtype='i4')
        u   = i
        for s in S:
            neigh   = np.matmul(m,s,dtype='i4')
            neigh   = pgl_normalize(neigh, inv, q)
            neighT  = tuple([neigh[0,0], neigh[1,0], neigh[0,1], neigh[1,1]])
            assert(neighT in vToM)
            v       = vToM[neighT]
            G.add_edge(u,v)

    return G


def psl_normalize(mat, inv, roots, q):
    norm    = mat%q
    det     = (norm[0,0]*norm[1,1] - norm[0,1]*norm[1,0])%q
    if (not det==1):
        assert(det in roots)
        detI    = inv[roots[det]]
        norm    = (norm*detI)%q

    detN    = (norm[0,0]*norm[1,1] - norm[0,1]*norm[1,0])%q
    assert(detN==1)

    fnz     = (norm[1,0] if norm[0,0]==0 else norm[0,0])
    assert(not fnz==0)

    if (fnz > (q-1)//2):
        norm    = (-norm)%q
    assert(detN==1)
    return norm

def psl_gen(p, q):
    ffElems = [_ for _ in range(q)]
    inv     = ff_inv(q)
    roots   = ff_root(q)
    fnzVals = [i+1 for i in range((q-1)//2)]
    nodes   = []
    nzdet   = 0
    for i in fnzVals:
        for j in range(q):
            for k in range(q):
                for l in range(q):
                    m   = tuple([i, j, k, l])#np.matrix([[1, j], [k, l]])
                    det = i*l - j*k
                    if ((det%q)==1):
                        nodes.append(m)
                        nzdet   += 1

    for j in fnzVals:
        for k in range(q):
            for l in range(q):
                m   = tuple([0, j, k, l])#np.matrix([[0, 1], [k, l]])
                det = -j*k
                if ((det%q)==1):
                    nodes.append(m)
                    nzdet   += 1

    assert(nzdet == (q*q*q-q)//2)

    G       = nx.Graph()
    V       = len(nodes)
    vToM    = {}
    for i in range(V):
        G.add_node(i)
        vToM[nodes[i]]  = i

    S       = generator(p,q)
    for i in range(len(S)):
        S[i]    = psl_normalize(S[i], inv, roots, q)
        assert(S[i].shape[0]==2 and S[i].shape[1]==2)

    for i in range(V):
        m   = np.matrix([[nodes[i][0], nodes[i][2]], [nodes[i][1], nodes[i][3]]], dtype='i4')
        u   = i
        for s in S:
            assert(m.shape[0]==2 and m.shape[1]==2)
            neigh   = psl_normalize(np.matmul(m,s,dtype='i4'), inv, roots, q)

            neighT  = tuple([neigh[0,0], neigh[1,0], neigh[0,1], neigh[1,1]])
            if (not neighT in vToM):
                print(neigh)
            assert(neighT in vToM)
            v       = vToM[neighT]
            G.add_edge(u,v)


    return G
                                                                                      
def legendre(p, q):
    exp = (q-1)//2
    i   = 0
    sym = 1
    while(i < exp):
        sym =   (sym*p)%q
        i   +=  1
    if (sym==q-1):
        sym = -1
    return sym

