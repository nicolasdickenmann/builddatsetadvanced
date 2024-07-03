from bdf import *
from payley import *
from pf import *


def starProdGen(pfq, jnrq, jnrType):
    nx_jnr  = nx.Graph()
    assert(jnrType=="paley" or jnrType=="bdf")
    if (jnrType == "paley"):
        nx_jnr, phi  = payleyGen(jnrq)
    else:
        nx_jnr, phi  = bdfGen(jnrq) 
    nx_pf   = pfGen(pfq)
    nx_graph= nx.Graph()

    superV  = nx_pf.number_of_nodes()
    intraV  = nx_jnr.number_of_nodes()
    V       = superV*intraV

    for i in range(superV):
        nx_graph.add_nodes_from([(i*intraV+j) for j in range(0, intraV)])
        for j in range(intraV):
            u       = i*intraV + j
            neigh   = [n for n in nx_jnr.neighbors(j)]
            for n in neigh:
                v   = i*intraV + n
                nx_graph.add_edge(u, v)

    #add polarfly self-loops
    numQuadrics = 0
    isQuadric   = [False for i in range(superV)]
    for i in range(superV):
        neigh       = [n for n in nx_pf.neighbors(i)]
        isQuadric[i]= (len(neigh)==pfq)
        if (isQuadric[i]):
           nx_pf.add_edge(i, i)
        numQuadrics += 1
                     


    for i in range(superV):
        neigh   = [n for n in nx_pf.neighbors(i)]
        for n in neigh:
            if (i < n):
                for j in range(intraV):
                    u   = i*intraV + j
                    v   = n*intraV + phi[j]
                    if ((i==n) and (u>v)):
                        continue
                    nx_graph.add_edge(u, v)
            if (i == n):
                conn    = [False for j in range(intraV)]
                for j in range(intraV):
                    u   = i*intraV + j
                    v   = n*intraV + phi[j]
                    if (u==v):
                        continue
                    if (conn[j] or conn[phi[j]]):
                        continue
                    else:
                        nx_graph.add_edge(u, v)
                        conn[j]         = True
                        conn[phi[j]]    = True

    if (jnrType == "bdf"):
        expectedV   = (2*jnrq + 2)*(pfq*pfq + pfq + 1)
        obtainedV   = len(list(nx_graph.nodes))
        assert(expectedV == obtainedV)
        

    return nx_graph 


def optConfig(d):
    scale   = 0
    jnrType = "bdf"
    superq  = 0
    jnrq    = 0
    for pfd in range(2, d):
        jnrd    = d - pfd
        if (jnrd < 3):
            continue
        pfq     = pfd - 1
        pfV     = pfq*pfq + pfq + 1
        if (not is_power_of_prime(pfq)):
            continue 

        #can construct paley graph
        #paleyq  = jnrd*2 + 1
        #if (is_power_of_prime(paleyq) and (paleyq%4 == 1)):
        if (0):
            paleyV  = paleyq
            V       = paleyV*pfV
            if (V > scale):
                scale   = V
                jnrType = "paley" 
                superq  = pfq
                jnrq    = paleyq
        else:
            bdfq    = jnrd
            if ((bdfq % 4 == 0) or (bdfq % 4 == 3)):
                bdfV    = 2*bdfq + 2 
                V       = bdfV*pfV
                if (V > scale):
                    scale   = V
                    jnrType = "bdf"
                    superq  = pfq
                    jnrq    = bdfq

    print("max scale at degree " + str(d) + " is " + str(scale) + " vertices")
    print("Joiner graph = " + jnrType + ", joiner q = " + str(jnrq) + ", PF q = " + str(superq))

    return superq, jnrq, jnrType


def pfm3Gen(q):
    pfq, jnrq, jnrType  = optConfig(q)
    return starProdGen(pfq, jnrq, jnrType)

def analyze(nx_graph, d):
    if not nx.is_connected(nx_graph):
        print(" --> construction error: not connected")
        exit()
    
    max_degree  = max(dict(nx_graph.degree).values())
    min_degree  = min(dict(nx_graph.degree).values())
    print("max degree = " + str(max_degree) + ", min degree = " + str(min_degree) + ", expected degree = " + str(d))
    if (max_degree > d):
        print(" --> construction error: max degree greater than expected")
        exit()

    diam        = nx.diameter(nx_graph)
    if (diam > 3):
        print(" --> construction error: diameter greater than 3")
    #print("diameter = " + str(diam), ", expected = 3")

def write_graph(nx_graph, q):
    data_dir    = "./data/"
    if (not os.path.isdir(data_dir)):
        os.mkdir(data_dir)
    pfm3_dir    = data_dir+"pfm3/"
    if (not os.path.isdir(pfm3_dir)):
        os.mkdir(pfm3_dir)
    filename    = pfm3_dir + "pfm3." + str(q) + ".adj.txt" 

    f   = open(filename, "w")
    V   = nx_graph.number_of_nodes()
    E   = nx_graph.number_of_edges()
    f.write(str(V) + " " + str(E) + "\n")

    for i in range(V):
        neigh   = [n for n in nx_graph.neighbors(i)]
        for n in neigh:
            f.write(str(n) + " ")
        f.write("\n")
        
    

if __name__=="__main__":
    parser  = argparse.ArgumentParser(prog="pfm3.py")
    parser.add_argument('-d', dest='d', type=int, required=True, help='degree')
    kwargs  = parser.parse_args()
    g       = pfm3Gen(kwargs.d)
    analyze(g, kwargs.d)
    write_graph(g, kwargs.d)
