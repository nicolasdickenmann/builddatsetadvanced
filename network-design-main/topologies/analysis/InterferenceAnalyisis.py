# Author: Marcel Schneider and Alessandro Maissen
# Based on Ford-Fulkerson

from .Analysis import Analysis
from. simplepmap import pmap
from .results import Results
from topogen.common import from_list_graph_to_matrix_graph
from itertools import permutations
from .common import is_in_db
import numpy as np
import random
from scipy.sparse import csr_matrix

class InterferenceAnalysis(Analysis):

    bits = np.array(2**np.arange(50), dtype=np.int64)

    def __init__(self, datafilename="interference.db", number_of_samples=1000, all_combinations=False):
        super(InterferenceAnalysis,self).__init__()
        self.datafile = self.datafilefolder + datafilename
        self.number_of_samples = number_of_samples
        self.all_combinations = all_combinations

    def analyse(self, networks, maxlength : int):
        
        res = Results(self.datafile)
        for network in networks:          

            print("Analysing interference on %s with %d endnodes" %(network.name,network.N))
            if not is_in_db(network,res,maxlength):
                    
                matrix_graph = from_list_graph_to_matrix_graph(network.get_topo())
                matrix_graph.edge = network.edge
                matrix_graph.vertices = network.R

                collectx = res.collector(a=Results.Int, b=Results.Int, c=Results.Int, d=Results.Int, 
                        x_abcd=Results.Int, c_abcd=Results.Int, c_acd=Results.Int, c_acb=Results.Int, c_ab=Results.Int, c_cd=Results.Int,
                        len=Results.Int, 
                        topo=network.name, n_r=network.R, r=network.nr, n_e=network.N, p=network.p, tag="interference", maxlen=maxlength)

                collectc = res.collector(a=Results.Int, b=Results.Int,
                        c_ab=Results.Int, len=Results.Int, 
                        topo=network.name, n_r=network.R, r=network.nr, n_e=network.N, p=network.p, tag="connectivity", maxlen=maxlength)

                self.__interference_analysis(g=matrix_graph, limit=maxlength, collectc=collectc, collectx=collectx, count=self.number_of_samples)
                res.commit()
            else:
                print("     --> skip, already in database")

        res.close()
    
    # Priavte Methods
    def __prepare_graph(self,g):
        h = csr_matrix(g)
        for i in range(g.shape[0]):
            idx = h[i,:].nonzero()[1]
            h[i,idx] = 2**np.arange(len(idx))
        return h

    def __bfs(self,X,Y, limit, h):
        fringe = np.zeros((h.shape[0],))
        seen = np.zeros((h.shape[0],))
        fringe[X] = 1
        seen[X] = -1
        for _ in range(limit):
            step = h.dot(fringe)
            new = (step > 0) & (seen == 0)
            fringe[new] = 1
            seen[new] = step[new]
            if new[Y].any():
                break
        found = seen[Y] > 0
        if not found.any():
            return None
        cur = Y[found.nonzero()[0][0]]
        path = []
        while cur not in X:
            nextport = ((self.bits & np.int64(seen[cur])) > 0).nonzero()[0][0]
            next = h[cur,:].indices[nextport]
            path.append((cur, next))
            cur = next
        return path

    def __c_XY(self,X,Y, limit, h):
        g = h.tocsr(copy=True)
        res = np.zeros((limit+1,), dtype=np.int32)
        while True:
            p = self.__bfs(X,Y, limit, g)
            if not p: break
            res[len(p):] += 1
            for s,t in p:
                g[s,t] = 0
                g[t,s] = 0
        return res

    def __interference_analysis(self, g, limit, collectc, collectx, count = 1000):

        r = list(range(0, g.edge))
        if self.all_combinations:
            pairs = list(permutations(r, 4))
        else:
            pairs = [random.sample(r, 4) for _ in range(0, count)]

        h = self.__prepare_graph(g)

        def doall(abcd):
            a,b,c,d = abcd
            c_ab = self.__c_XY([a], [b], limit, h)
            c_cd = self.__c_XY([c], [d], limit, h)
            c_acb = self.__c_XY([a,c], [b], limit, h)
            c_acd = self.__c_XY([a,c], [d], limit, h)
            c_acbd = self.__c_XY([a,c], [b,d], limit, h)
            return c_ab, c_cd, c_acb, c_acd, c_acbd

        out = pmap(doall, pairs)

            
        for (a,b,c,d), (c_ab, c_cd, c_acb, c_acd, c_acbd) in zip(pairs, out):
            for i in range(1, limit+1):
                collectc(len=i, a=a, b=b, c_ab=c_ab[i])
                collectc(len=i, a=c, b=d, c_ab=c_cd[i])
                collectx(len=i, a=a, b=b, c=c, d=d, x_abcd=c_acb[i]+c_acd[i]-c_acbd[i], c_abcd=c_acbd[i], c_acd=c_acd[i], c_acb=c_acb[i], c_ab=c_ab[i], c_cd=c_cd[i])
