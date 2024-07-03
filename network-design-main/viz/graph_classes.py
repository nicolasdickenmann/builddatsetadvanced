# general imports, basic globals

import io
import sys
import subprocess 
import copy
import pandas as pd
import numpy as np
import pyvista as pv


#####################################################
#
#     some graph support classes
#
#####################################################

    
class Vertex:
    def __init__(self, value):
        self.value = value
        self.adj = []  # vertices that are adjacent to self
        self.pos = []  # a set of positions for self. self.pos[i] is self position in the ith layout
        self.color = 'black'   # what color do you want the default vertex to be
        self.size = 20   # what size do you want the default vertex to be
        
    def __getitem__(self, key):
        return self.__dict__[key]

    def __str__(self):
        return str(self.value)
        
class VertexList:
    def __init__(self):
        self.list = []

    def __getitem__(self, key):
        return self.__dict__[key]

    def __str__(self):
        string = ''
        for l in self.list:
            string += str(l)
        string += '\n'
        return string

class Position: # cartesian
    def __init__self(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        
    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __str__(self):
        return str('(' + self.x +', ' + self.y +', ' + self.z +')')

class Value:  # 3-vectors
    def __init__self(self, a,b,c):
        self.v0 = a
        self.v1 = b
        self.v2 = c  
                        
    def __getitem__(self, key):
        return self.__dict__[key]

    def __str__(self):
        return str('(' + self.v0 +', ' + self.v1 +', ' + self.v2 +')')
        
class Edge:
    def __init__(self, v1, v2):
        self.edge = [2, v1, v2]
        
    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __str__(self):
        string = '['+ str(self.edge[0]) +','+ str(self.edge[1]) +',' + str(self.edge[2]) +']'
        return string


class Edgeset:
    # this is a set of edges. Color, opacity, line_width defined per Edgeset, not per Edge
    def __init__(self, color, opacity, line_width):
        self.edges = []
        self.opacity = opacity
        self.color = color
        self.line_width = line_width
        
    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __str__(self):
        string = '['
        for i in range(len(self.edges)-1):
            string += str(self.edges[i])+','
        string += str(self.edges[len(self.edges)-1])+']'
        return string
    
    def append_edge(self, edge):
        self.edgeset.append(edge)
        
    def concatenate_edgesets(self, edgeset):
        new_edgeset = self
        for e in edgeset:
            new_edgeset.edges.append(e)
        new_edgeset.color = self.color
        new_edgeset.opacity = self.opacity
        new_edgeset.line_width = self.line_width
        return new_edgeset
            
    def num_edges(self):
        return len(self.edges)

    
class EdgesList:
    # this is a list of edge sets
    def __init__(self, edgeset, name):
        self.list = [edgeset]
        self.names = [name]
        
    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __str__(self):
        string = '['
        for i in range(len(self.list)-1):
            string += str(self.list[i])+','
        string += str(self.list[len(self.list)-1]) + ']'
        return string
    
    def append_edgeset(self, edgeset):
    # append a set of edges to the current edge_sets list, along with their positions and drawing details
        self.list.append(edgeset)  
        
    def num_lists(self):
        return len(self.list)


#####################################################
#
#     graph base class
#
#####################################################

    

class Graph:

    def __init__(self, num):
        self.vertex_list, self.num_vertices = self.set_vertex_list(num) # should be set by child class 
        num_vlist = len(self.vertex_list)
        self.adj_matrix = self.set_adjacency_matrix() # must be set by child class
        self.num_edge, self.num_loops = self.set_num_edges()
        self.set_adj_lists()  
        self.SA = self.get_self_adj_vertices()
        self.indices = [i for i in range(self.num_vertices)]
        # default for self.edges_list is a list with all of the edges of the graph. self.edges_list is for viz purposes.
        self.edges_list = EdgesList(self.get_edges_within_indexset(self.indices, 'black', 0.2, 1), 'all_edges')
        self.num_edge = self.edges_list.list[0].num_edges()
        self.inc_matrix = self.set_incidence_matrix()
        # default for self.layouts is a circular layout with a clockwise ordering as per self.indices
        self.set_layouts()
        self.init_stuff()

    def __getitem__(self, key):
        return self.__dict__[key]
    
    def set_vertex_list(self, num):
        vertex_list = []
        for i in range(0,num):
            vertex_list.append(Vertex(i))
        return vertex_list, len(vertex_list)
        pass
    
    def set_adjacency_matrix(self):
        # adj_matrix[i][j]=1 when i is adjacent to j
        adj_matrix = []
        for i in range(self.num_vertices):
            row = [0]*self.num_vertices
            adj_matrix.append(row)
        return adj_matrix
    
    def get_self_adj_vertices(self):
        SA_color = 'red'
        SA = []
        for i in range(self.num_vertices):
            if self.adj_matrix[i][i]==1:
                SA.append(i)
                self.vertex_list[i].color = SA_color
        return SA
    
    def set_num_edges(self):    
        num_loops = 0
        num_non_loops = 0
        for i in range(self.num_vertices):
            num_non_loops += self.adj_matrix[i].count(1)
            if self.adj_matrix[i][i] == 1:
                num_loops += 1
                num_non_loops -= 1
        num_edges = int(num_non_loops/2)
        return num_edges, num_loops
    
    def set_incidence_matrix(self):
    # includes self-adjacent vertices, and they are accounted for in the first columns
        inc_matrix = []
        for i in range(self.num_vertices):
            row = [0]*(self.num_edge+self.num_loops)
            inc_matrix.append(row)
        adj_num = 0
        for i in range(self.num_vertices):
            if self.adj_matrix[i][i]==1:
                inc_matrix[i][adj_num] = 1
                adj_num += 1                
        for i in range(self.num_vertices):
            for j in range(i+1,self.num_vertices):
                if self.adj_matrix[i][j]==1:
                    inc_matrix[i][adj_num] = 1
                    inc_matrix[j][adj_num] = 1
                    adj_num +=1
        return inc_matrix
        
    def set_adj_lists(self):
    # includes self-adjacent vertices
        num_vlist = len(self.vertex_list)
        for i in range(self.num_vertices):
            if self.adj_matrix[i][i]==1:
                self.vertex_list[i].adj.append(i)
            for j in range(i, self.num_vertices):
                if self.adj_matrix[i][j]==1:
                    self.vertex_list[i].adj.append(j)
                    self.vertex_list[j].adj.append(i)
    
    def set_layouts(self):
        self.layouts = Layouts(self)
    
    def init_stuff(self):
        pass
    
    def get_layout(self,layoutnum):
        layout = []
        for i in range(self.num_vertices):
            layout.append(self.vertex_list.pos[layoutnum])
        return layout
    
    def get_subgraph(self):
        pass
    
    def induced_subgraph(self, iset):
        subgraph = Graph(len(iset))
        subgraph.vertex_list = []
        for i in iset:
            subgraph.vertex_list.append(self.vertex_list[i])
        subgraph.adj_matrix = []
        for i in range(subgraph.num_vertices):
            row = [0]*subgraph.num_vertices
            subgraph.adj_matrix.append(row)
            if self.adj_matrix[iset[i]][iset[i]] == 1:
                subgraph.adj_matrix[i][i] = 1
        for i in range(subgraph.num_vertices):
            for j in range(i, subgraph.num_vertices):
                if self.adj_matrix[iset[i]][iset[j]] == 1:
                    subgraph.adj_matrix[i][j] = 1
                    subgraph.adj_matrix[j][i] = 1                    
        for i in range(subgraph.num_vertices):
            subgraph.vertex_list[i].adj = []
        subgraph.set_adj_lists()  
        subgraph.indices = [i for i in range(subgraph.num_vertices)]
        subgraph.edges_list = EdgesList(subgraph.get_edges_within_indexset(subgraph.indices, 'black', 0.2, 1), 'all_edges' )  
        subgraph.layouts = copy.deepcopy(self.layouts)
        return subgraph

    def get_positions_from_indexset(self, iset):
    # this grabs a bunch of positions corresponding to the pointers
        vpos = []
        for i in range(len(ptrset)):
            vpos.append(self.vertex_list[ptrset[i]].pos)
        return vpos

    def get_edges_between_indexsets(self, iset0, iset1, color, opacity, line_width):
    # get all of the edges between two disjoint pointer_sets, for viz purposes
        edgeset = Edgeset(color, opacity, line_width)
        for i in range(len(iset0)):
            for j in range(len(iset1)):
                if self.adj_matrix[iset0[i]][iset1[j]]==1:
                    edgeset.edges.append(Edge(iset0[i],iset1[j]))
        return edgeset
    
    def get_edges_within_indexset(self, iset, color, opacity, line_width):
    # get all of the non-loop edges within a pointer_set, for viz purposes
        edgeset = Edgeset(color, opacity, line_width)
        for i in range(len(iset)):
            for j in range(i+1,len(iset)):
                if self.adj_matrix[iset[i]][iset[j]]==1:
                    edgeset.edges.append(Edge(iset[i],iset[j]))
        return edgeset
    
    
#####################################################
#
#     layout base class
#
#####################################################

    
class Layouts:
    def __init__(self, graph):
    # bare minimum
        self.graph = graph
        self.layout_list = [] 
        self.layout_names = []
        self.set_layouts()
        
    def __getitem__(self, key):
        return self.__dict__[key]
    
    def set_layouts(self):
        self.add_layout(self.clockwise_layout(), 'default')
        return self.layout_list, self.layout_names
    
    def add_layout(self,position_list, name):
    # position_list must have num_vertices elements
        for i in range(self.graph.num_vertices):
            self.graph.vertex_list[i].pos.append(position_list[i])
        self.layout_list.append(position_list)
        self.layout_names.append(name)
    
    def clockwise_layout(self):
        vpos_list = []
        angle_increment = 2*np.pi/self.graph.num_vertices    
        for i in range(self.graph.num_vertices):
            vpos_list.append([np.sin(i*angle_increment), np.cos(i*angle_increment), 0])
        return vpos_list

    def get_layouts(self):
        return self.layout_list, self.layout_names

########## helper functions for layouts  #################

    def circle_pos(self, i):
    # gives the ith position around the num_vertices-step unit circle clockwise
        angle_increment = 2*np.pi/self.graph.num_vertices    
        position = [np.sin(i*angle_increment), np.cos(i*angle_increment), 0]
        return position

    def all_circle_positions(self, ptr_list, starting_angle, radius, height):
    # gives equi-spaced positions on a circle of radius and height
        num_ptrs = len(ptr_list)
        angle = -2*np.pi/(num_ptrs)
        pos_list = []
        for i in range(num_ptrs):
            pos_list.append([radius*np.sin(i*angle+starting_angle), radius*np.cos(i*angle+starting_angle), height])
        return pos_list

    def permute_pos(self, vpos_list, permutation):
    # takes a permutation of the form [[x00, x01, ... x0n], ... , [xs0, xs1, ... xsm]]
    # s+1 self-contained permutations, moving however many elements
    # permutes the positions of K as per the permutation
        num_vpos_list = len(vpos_list)
        num_perms = len(permutation)
        #save original positions of vpos_list out
        new_vpos_list = copy.deepcopy(vpos_list)
        for k in range(num_perms):
            num_perm_k = len(permutation[k])
            # move src element position to dest element position, for each move in the permutation
            for i in range(num_perm_k):
                src = permutation[k][i]
                dest = permutation[k][(i+1)%num_perm_k]
                new_vpos_list[dest] = vpos_list[src]
        return new_vpos_list


