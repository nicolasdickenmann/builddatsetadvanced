# Author: Jascha Krattenmacher, Algorithm by Kartik Lakhotia
# Polarfly(d)

# PARAMETERS
# d: degree

# VARIABLES
# n: total number of routers


from .TopologyGenerator import TopologyGenerator
#from .validate_dragonfly import validate


from topogen.polarstar.bdf import *
from topogen.polarstar.paley import *
from topogen.polarstar.pf import *
from topogen.polarstar.route import RouteValidate



class PolarstarGenerator(TopologyGenerator):

    def __init(self):
        super(PolarstarGenerator,self).__init__()
    
    def make(self,d: int,pfq : int,jq : int,sg : str) -> [[int]]:

        if d!= -1:
            pfq,jq,sg, N = config(d,sg,'dummyString')

        if sg == 'max':
            sg = 'bdf'

        self.pfq = pfq
        self.jq = jq
        self.sg = sg

        g, pfg, jnrg, phi  = starProdGen(pfq, jq, sg)
        jrnq = jq

        #analyze(g, d)
        V = g.number_of_nodes()
        
        G = []
        for i in range(V):
            neigh = [n for n in g.neighbors(i)]
            G.append(neigh)

        return G


    def validate(self, topo : [[int]], d : int, sg : str) -> bool:
        return validate(topo,d,sg)
    
    def get_folder_path(self):
        return super(PolarstarGenerator,self).get_folder_path() + "polarstars/"

    def get_file_name(self, d: int, pfq : int, jq : int,sg : str) -> str:
        if d == -1:
            return "Polarstar." + str(pfq) + "." + str(jq) + "." + sg + ".adj.txt"
        else:
            return "Polarstar.deg" + str(d) + "." + sg + ".adj.txt"


########### Hepler Functions #############
def config(d, sg, string):
    scale   = 0
    jnrType = "bdf"
    superq  = 0
    jnrq    = 0
    jnrVMax = 0
    pfVMax  = 0
    for pfd in range(2, d):
        jnrd    = d - pfd
        if (jnrd < 3):
            continue
        pfq     = pfd - 1
        pfV     = pfq*pfq + pfq + 1
        if (not is_power_of_prime(pfq)):
            continue

        #can construct paley graph
        paleyq  = jnrd*2 + 1
        if (sg != "bdf" and is_power_of_prime(paleyq) and (paleyq%4 == 1)):
        #if (1):
            paleyV  = paleyq
            V       = paleyV*pfV
            if (V > scale):
                scale   = V
                jnrType = "paley"
                superq  = pfq
                jnrq    = paleyq
                jnrVMax = paleyV
                pfVMax  = pfV
        #else:
        elif (sg != "paley"):
            bdfq    = jnrd
            if ((bdfq % 4 == 0) or (bdfq % 4 == 3)):
                bdfV    = 2*bdfq + 2
                V       = bdfV*pfV
                if (V > scale):
                    scale   = V
                    jnrType = "bdf"
                    superq  = pfq
                    jnrq    = bdfq
                    jnrVMax = bdfV
                    pfVMax  = pfV

    if string != 'iter':
        print("max scale at degree " + str(d) + " is " + str(scale) + " vertices")
        print("Joiner graph = " + jnrType + ", joiner q = " + str(jnrq) + ", PF q = " + str(superq))
        print("SuperNodeSize = " + str(jnrVMax))
        print("Num SuperNodes: " + str(pfVMax))

    return superq, jnrq, jnrType, scale


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


    return nx_graph, nx_pf, nx_jnr, phi

def pfm3Gen(pfq, jq, sg):

    g, pfg, jnrg, phi   = starProdGen(pfq, jq, sg)
    return g, pfg, jnrg, phi, pfq, jnrq

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


