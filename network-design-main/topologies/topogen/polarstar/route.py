import networkx as nx
import random
import statistics

#A new routing scheme for PolarStar with Inductive-Quad
#Requires PolarFly and Inductive-Quad coordinates of each node : (x,xp)
#x <- supernode ID in PolarFly
#xp <- node ID in Inductive-quad supernonde
class RouteValidate():
    def __init__(self, d, G, pfG, jnrG, pfq, phi):
        self.d      = d
        self.G      = G
        self.pfG    = pfG
        self.jnrG   = jnrG
        self.pfq    = pfq
        self.V      = G.number_of_nodes()
        self.pfV    = pfq*pfq + pfq + 1
        self.phi    = phi
        assert(self.V%self.pfV == 0) 
        self.jnrSize= self.V//self.pfV
        assert(self.jnrG.number_of_nodes()==self.jnrSize)
        assert(self.jnrG.number_of_nodes()==len(self.phi))

        self.pfAdjList   = [[] for _ in range(self.pfV)]
        self.buildPFAdjList()
        
        self.pfCommNeigh = [[-1 for _ in range(self.pfV)] for _ in range(self.pfV)]
        self.build2HopTable()

        self.edgeSP = {}
        print("POLORSTAR RUNNING")
        print("INITIALIZING EDGE SHORTEST PATH COUNTS")
        for e in self.G.edges:
            u                   = min(e[0], e[1])
            v                   = max(e[0], e[1])
            ekey                = (u,v)
            self.edgeSP[ekey]   = 0
        
        random.seed(1)
    
        print("ROUTE VALIDATION INITIALIZED")
        
    def coordsToId(self,x,xp):
        assert(xp < self.jnrSize)
        return x*self.jnrSize + xp

    def idToCoords(self,n):
        assert(n < self.V)
        return n//self.jnrSize, n%self.jnrSize

    def buildPFAdjList(self):
        print("BUILDING PolarFly ADJACENCY LIST")
        for i in range(self.pfV):
            self.pfAdjList[i]    = [n for n in self.pfG.neighbors(i)]
            assert(len(self.pfAdjList[i])==self.pfq+1)

    def build2HopTable(self):
        print("BUILDING 2-HOP TABLE FOR POLARFLY")
        for i in range(self.pfV):
            neighs  = [n for n in self.pfG.neighbors(i)]
            for neigh in neighs:
                neighOfNeighs   = [n for n in self.pfG.neighbors(neigh)]
                for n in neighOfNeighs:
                    self.pfCommNeigh[i][n]   = neigh

        print("VALIDATING 2-HOP TABLE")
        for i in range(self.pfV):
            for j in range(self.pfV):
                if (i==j):
                    continue
                assert(self.pfCommNeigh[i][j] >= 0)
                assert(self.pfCommNeigh[i][j] == self.pfCommNeigh[j][i])


    #src = (x,xp), dst = (y,yp) are adjacent to each other
    def route_adjacent(self,x,xp,y,yp,hops):
        pfm3x       = self.coordsToId(x,xp)
        pfm3y       = self.coordsToId(y,yp)
        assert(hops <= 3)
        if (pfm3x==pfm3y):
            return hops
        assert(self.G.has_edge(pfm3x, pfm3y))
        e               = (min(pfm3x,pfm3y), max(pfm3x,pfm3y))
        self.edgeSP[e]  += 1
        return hops + 1

    #src = (x,xp), dst = (y,yp) are in the same supernode
    def route_within_sn(self,x,xp,y,yp,hops):
        assert(hops <= 3)
        assert(x==y)
        pfm3x       = self.coordsToId(x,xp)
        pfm3y       = self.coordsToId(y,yp)
        z,zp        = x,xp
        #same node
        if (yp == xp):
            return hops
        #adjacent nodes
        if (self.jnrG.has_edge(xp,yp)):
            return self.route_adjacent(x,xp,y,yp,hops)
        #quadric
        elif (self.pfG.has_edge(x,y)):
            #yp=f(xp), adjacent nodes
            if (yp==self.phi[xp]):
                return self.route_adjacent(x,xp,y,yp,hops)
            #yp \in f(N(x)), jump local first and then pseudo-global
            if (self.jnrG.has_edge(xp,self.phi[yp])):
                z,zp    = x,self.phi[yp]
            #yp \in N(f(x)), jump pseudo-global first and then local
            else:
                z,zp    = y,self.phi[xp]
        #else jump to any neighboring supernode
        else:
            z,zp    = self.pfAdjList[x][random.randint(0,self.pfq)], self.phi[xp] 
        hops    = self.route_adjacent(x,xp,z,zp,hops)
        return self.route(self.coordsToId(z,zp),self.coordsToId(y,yp),hops)

    #src = (x,xp), dst = (y,yp) are in adjacent supernodes
    def route_adj_sn(self,x,xp,y,yp,hops):
        assert(hops <= 3)
        assert(self.pfG.has_edge(x,y))
        #yp=f(xp), adjacent nodes
        if (yp==self.phi[xp]):
            return self.route_adjacent(x,xp,y,yp,hops)
        z,zp        = self.pfCommNeigh[x][y], self.phi[xp]
        #yp=xp, find a 2-hop path from x->y in PolarFly 
        if (yp==xp):
            pass
        #yp \in f(N(x)), jump local first and then global
        elif (self.jnrG.has_edge(xp,self.phi[yp])):
            z,zp    = x,self.phi[yp]
        #yp \in N(f(x)), jump global first and then local
        else:
            z,zp    = y,self.phi[xp]
        hops    = self.route_adjacent(x,xp,z,zp,hops)
        return self.route(self.coordsToId(z,zp),self.coordsToId(y,yp),hops)

    #src = (x,xp), dst = (y,yp) are in adjacent supernodes
    def route_non_adj_sn(self,x,xp,y,yp,hops):
        assert(hops <= 3)
        z,zp    = self.pfCommNeigh[x][y], self.phi[xp]
        if (yp==self.phi[xp]):
            z   = self.pfAdjList[x][random.randint(0,self.pfq)]
        hops    = self.route_adjacent(x,xp,z,zp,hops)
        return self.route(self.coordsToId(z,zp),self.coordsToId(y,yp),hops) 

    def route(self,pfm3x,pfm3y,hops):
        x,xp    = self.idToCoords(pfm3x)
        y,yp    = self.idToCoords(pfm3y)
        if (x==y):
            return self.route_within_sn(x,xp,y,yp,hops)
        elif (self.pfG.has_edge(x,y)):
            return self.route_adj_sn(x,xp,y,yp,hops)
        else:
            return self.route_non_adj_sn(x,xp,y,yp,hops)

    def edgeSPStats(self):
        vals    = list(self.edgeSP.values())
        return max(vals), min(vals), statistics.mean(vals), statistics.stdev(vals)


            
