# general imports, basic globals

import io
import sys
import subprocess 
import copy
import pandas as pd
import numpy as np
import pyvista as pv

import galois
import json



#####################################################
#
#     GF(q) arithmetic class
#
#####################################################

    
class GFq:
    # finite field arithmetic tables and 3-D dot product calculation
    def __init__(self, q):
        self.q = q
        self.add, self.mul = self.make_GF_q_arith_table()
        self.prim_elts = self.get_prim_elts()
        
    def __getitem__(self, key):
        return self.__dict__[key]
    
    def make_GF_q_arith_table(self):
    # addition and multiplication tables in GF(q)
        add = []
        mul = []
        GF = galois.GF(self.q)
        for i in range(self.q):
            x_vec = self.q*[i]
            y_vec = [j for j in range(self.q)]
            x = GF(x_vec)
            y = GF(y_vec)
            add.append(json.loads(str(x+y)))
            mul.append(json.loads(str(x*y)))
        return add, mul    
    
    def get_prim_elts(self):
        prim_elts = galois.GF(self.q).primitive_elements
        return prim_elts


    def dot_product_3d(self,v,w):
        mul0 = self.mul[v[0]][w[0]]
        mul1 = self.mul[v[1]][w[1]]
        mul2 = self.mul[v[2]][w[2]]
        return self.add[ self.add[mul0][mul1]][mul2]
    
    

