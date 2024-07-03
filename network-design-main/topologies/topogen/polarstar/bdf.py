from topogen.polarstar.paley import *

def baseGraph(q):
    nx_graph    = nx.Graph()
    phi         = {}
    A           = []
    fA          = []
    A           = [0,1,2,3]
    fA          = [4,5,6,7] 
    for i in range(8):
        nx_graph.add_node(i)
    nx_graph.add_edge(0,7)
    nx_graph.add_edge(4,7)
    nx_graph.add_edge(0,1)
    nx_graph.add_edge(4,1)
    nx_graph.add_edge(0,2)
    nx_graph.add_edge(4,2)
    nx_graph.add_edge(1,6)
    nx_graph.add_edge(5,6)
    nx_graph.add_edge(5,3)
    nx_graph.add_edge(5,7)
    nx_graph.add_edge(2,3)
    nx_graph.add_edge(6,3)
    if (q%4 == 0):
        A.append(8)
        fA.append(9)
        nx_graph.add_node(8)
        nx_graph.add_node(9)
        nx_graph.add_edge(8,0)
        nx_graph.add_edge(8,4)
        nx_graph.add_edge(8,1)
        nx_graph.add_edge(8,5)
        nx_graph.add_edge(9,2)
        nx_graph.add_edge(9,6)
        nx_graph.add_edge(9,3)
        nx_graph.add_edge(9,7)
    for i in range(len(A)):
        phi[A[i]]   = fA[i]
        phi[fA[i]]  = A[i]
    #if (q%2 == 1):
    #    nx_graph.add_node(0)
    #    nx_graph.add_node(1) 
    #    nx_graph.add_edge(0, 1)
    #    phi[0]  = 1
    #    phi[1]  = 0
    #    A       = [0] 
    #    fA      = [1] 
    #else:
    #    nx_graph.add_node(0)
    #    nx_graph.add_node(1) 
    #    nx_graph.add_node(2) 
    #    nx_graph.add_node(3) 
    #    nx_graph.add_edge(0, 1)
    #    nx_graph.add_edge(1, 2)
    #    nx_graph.add_edge(2, 3)
    #    nx_graph.add_edge(3, 0)
    #    phi[0]  = 2
    #    phi[1]  = 3
    #    phi[2]  = 0
    #    phi[3]  = 1
    #    A       = [0, 1]
    #    fA      = [2, 3]

    return nx_graph, A, fA, phi

def bdfGen(q):
    assert(((q % 4)==0) or ((q % 4 == 3)))
    nx_graph, A, fA, phi    = baseGraph(q)
    #d   = 2 - (q%2)
    #n   = 2*d
    d   = 4 if ((q % 4) == 0) else 3
    n   = 2*d + 2
    incr= 4
    while(d < q):
        incr_graph, incrA, incrFA, incrPhi  = baseGraph(incr-1)
        incrV   = list(incr_graph.nodes)
        for i in incrV:
            nx_graph.add_node(n + i)
        newE    = incr_graph.edges()
        for e in newE:
            nx_graph.add_edge(n + e[0], n + e[1])
        assert(len(incrA)%2 == 0)
        connA   = len(incrA)//2
        for i in range(connA):
            u   = incrA[i] + n
            fu  = incrPhi[incrA[i]] + n
            phi[u] = fu
            phi[fu] = u   
            for v in A:
                nx_graph.add_edge(u, v)
                nx_graph.add_edge(fu, v)

            u   = incrA[i + connA] + n
            fu  = incrPhi[incrA[i + connA]] + n
            phi[u] = fu
            phi[fu] = u   
            for v in fA:
                nx_graph.add_edge(u, v)
                nx_graph.add_edge(fu, v)

        for i in incrA:
            A.append(i + n)
        for i in incrFA:
            fA.append(i + n)

        d += 4
        n += 8
        
        #nx_graph.add_node(n) #x
        #nx_graph.add_node(n+1) #y
        #nx_graph.add_node(n+2) #f(x)
        #nx_graph.add_node(n+3) #f(y)
        #nx_graph.add_edge(n, n+1)
        #nx_graph.add_edge(n+1, n+2)
        #nx_graph.add_edge(n+2, n+3)
        #nx_graph.add_edge(n+3, n+0)
        #phi[n+0]  = n+2
        #phi[n+1]  = n+3
        #phi[n+2]  = n+0
        #phi[n+3]  = n+1
        #
        #for v in A:
        #    nx_graph.add_edge(v, n+1) 
        #    nx_graph.add_edge(v, n+3) 

        #for v in fA:
        #    nx_graph.add_edge(v, n)
        #    nx_graph.add_edge(v, n+2)

        #A.append(n)
        #A.append(n+1)
        #fA.append(n+2)
        #fA.append(n+3)
        #
        #d += 2
        #n += 4 

    print_graph(nx_graph)

    return nx_graph, phi
            

if __name__=="__main__":
    parser  = argparse.ArgumentParser(prog="bdf.py")
    parser.add_argument('-q', dest='q', type=int, required=True, help='bdf degree')
    kwargs  = parser.parse_args()
    g, phi  = payleyGen(kwargs.q)
