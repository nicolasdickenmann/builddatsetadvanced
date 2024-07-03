# Author: Alessandro Maissen
# Two-Level Orthogonal Fat-Tree
# Implemented based on Paper: Cost-Effective Diameter-Two Topologies: Analysis and Evaluation (2.2.4)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#    Basic strucutre of k-OFT                                                       #
#                                                                                   #
#    -------------------------                                                      #
#   |         LAYER 2         |                                                     #
#    -------------------------                                                      #
#       |               |                                                           #
#       |               |       Layer2 connects with Layer1 based on ML3B           #
#    -------------------------                                                      #
#   |         LAYER 1         |                                                     #
#    -------------------------                                                      #
#       |               |                                                           #
#       |               |       Layer0 connects with Layer1 based on ML3B           #
#    -------------------------                                                      #
#   |         LAYER 0         |                                                     #
#    -------------------------                                                      #
#                                                                                   #
#   Only Layer 0 and Layer 2 have end-nodes!                                        #
#                                                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# PARAMETERS
# k: degree of routers/nodes in Layer 0 and Layer 2 (k:= q + 1 where q is prime)

# VARIABLES
# R: total number of routers/nodes
# Rl: total numbers of routers/nodes per level

# ADDITIONAL NOTES
# The first 2*Rl (0...2*Rl-1) nodes/routers are edge routers. All Layer 0 and Layer 2 routers are edge routers.
# Only edge routers can have hosts attached.

import random
from .TopologyGenerator import TopologyGenerator
from .validate_oft import validate
from .common import is_prime

class OFTGenerator(TopologyGenerator):

    def __init(self):
        super(OFTGenerator,self).__init__()
    
    def make(self, k: int) -> [[int]]:
        assert(is_prime(k-1))

        R = 3*k**2 - 3*k + 3
        Rl = 1 + k*(k-1)

        graph = [[] for _ in range(R)]
        ml3btabluar = get_ML3B(k)

        # connect layers (L1 routers have the highest numbers)
        for i in range(0, Rl):
            for elem in ml3btabluar[i]:
                # connect L0 with L1
                graph[i].append(Rl*2 + elem)
                graph[Rl*2 + elem].append(i)
                # connect L2 with L1
                graph[Rl*1 + i].append(Rl*2 + elem)
                graph[Rl*2 + elem].append(Rl*1 + i)

        return graph

    def validate(self, topo : [[int]], k : int) -> bool:
        return validate(topo,k)
    
    def get_folder_path(self):
        return super(OFTGenerator,self).get_folder_path() + "ofts/"
    
    def get_file_name(self, k : int) -> str:
        return "OFT." + str(k) + ".adj.txt"

## ------------------ helper functions ------------------ ##

# n has to be prime
# source: https://math.stackexchange.com/questions/1624841/algorithms-for-mutually-orthogonal-latin-squares-a-correct-one
# --> I had to swap i, j to get same results for 4-ML3B as in the paper
def get_MOLS(n : int) -> [[[int]]]:

    mols = []
    for k in range(1,n):
        ols = []
        for j in range(0,n):
            row = []
            for i in range(0,n):
                row.append((k*i + j) % n)
            ols.append(row)
        mols.append(ols)
    return mols

# k := p + 1 where p i prime
def get_ML3B(k : int) -> [[int]]:
    Rl = 1 + k*(k-1)

    tabular = [[] for _ in range(0,Rl)]

    # step 1: fill first row
    for i in range(0,k):
        tabular[0].append(Rl + i - k)
    
    # step 2: fill remaining entires of first column
    for i in range(0,k):
        for j in range(1, k):
            tabular[i*(k-1) + j].append(Rl - k + i)

    # step 3.1: insert 1st block in tabular
    # bulding (k-1) x (k-1) block filled with numbers 0 to (k-1)^2 - 1
    # order from left to right, top to bottom
    block = []
    for i in range(0,k-1):
        row = []
        for j in range(0,k-1):
            row.append(i*(k-1) + j)
        block.append(row)
    
    # insert block in tabular
    tabular = fill_in_block(tabular, block, 1, k-1)
    
    # step 3.2: insert 2nd block in tabular, which is the transposed from the 1st block
    trasnposed_block = list(map(list, zip(*block))) # assumes quadratic matrix
    tabular = fill_in_block(tabular,trasnposed_block, k, k-1)
    
    # step 3.3: insert MOLS in the remaining k-2 blocks
    mols = get_MOLS(k-1) # k-1 is prime
    # modfy mols
    for o in range(0,k-2):
        for i in range(0,k-1):
            for j in range(0, k-1):
                mols[o][i][j] +=j*(k - 1)

    for i in range(0,k-2):
        tabular = fill_in_block(tabular, mols[i], (i+2)*(k-1) + 1, k-1)
    
    return tabular

def fill_in_block(matrix : [[int]], submatrix : [[int]], start_row : int , sub_rows : int):
    
    for i in range(0,sub_rows):
            matrix[start_row + i] += submatrix[i]
    return matrix