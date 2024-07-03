# general imports, basic globals

import io
import sys
import subprocess 
import pandas as pd
import numpy as np
import pyvista as pv


# make sure the user has at least Python 3.7, which we need for some capture_output
assert sys.version_info.major == 3, "This requires at least Python 3.7"
assert sys.version_info.minor >= 7, "This requires at least Python 3.7"



#####################################################
#
#     a general graph visualizer
#
#####################################################


# Define some colors, for the vertices and edges
RED = '#FF0000'
DK_RED = '#990000'
LT_GREEN = '#44FF44'
DK_GREEN = '#009900'
LT_BLUE = '#0088FF'

def visualize_graph(graph, layout, 
                    edgelists_to_display, 
                    camera_pos, camera_rot , 
                    show_labels, fname, caption):
# lighting
    BACKGROUND_COLOR = 'white'
    LIGHT_COLOR = 'white'
    pl = pv.Plotter(lighting=None, window_size=(2000, 2000))
    light1 = pv.Light(position=(10, 10., -5.0), focal_point=(0, 0, 0), color=LIGHT_COLOR, intensity=1.5)
    light2 = pv.Light(position=(-10, 10.0, -5.0), focal_point=(0, 0, 0), color=LIGHT_COLOR, intensity=0.75)
#     pl.add_light(light1)  # Lighting effect to be cast onto the object
#     pl.add_light(light2)  # Second Lighting effect to be cast onto the object
    hlight = pv.Light(light_type='headlight')
    pl.add_light(hlight)  # headlight effect to be cast onto the object
    pl.set_background(BACKGROUND_COLOR)  # Set the background     
    
    try:
        layout_num = graph.layouts.layout_names.index(layout)
    except ValueError:
        print(layout, " is not in the list of layouts.")

# vertices
# Sort by color then pl.add_mesh much faster than pl.add_points! 
# also (for now) more general than sorting by cluster set
    colorset = []
    color_vertices = []
    for vertex in graph.vertex_list:
        try:
            c = colorset.index(vertex.color)
            color_vertices[c].append(vertex.pos[layout_num])
        except ValueError:
            colorset.append(vertex.color)
            color_vertices.append([vertex.pos[layout_num]])
    for c, arg in enumerate(colorset):
        cloud = pv.PolyData(color_vertices[c])
        pl.add_mesh(cloud, 
                color=arg, 
                point_size=graph.vertex_list[0].size, # making them all the same size
                render_points_as_spheres=True
               )
# this adds point labels of vector values -- but placed on top of the points
    if (show_labels):
        point_labels = []
        for i in range(len(graph.vertex_list)):
            point_labels.append(graph.vertex_list[i].value)        
        pl.add_point_labels(cloud, point_labels, italic=False, bold=False, font_size=30,
                            point_color='black', point_size=0, text_color='black', 
                            shape=None, 
                            render_points_as_spheres=True,
                            always_visible=True, shadow=False)  

# edge sets
    vpos = []
    for v in graph.vertex_list:
        vpos.append(v.pos[layout_num])
    vertices = np.array(vpos)
    for el in edgelists_to_display:
        try:
            i = graph.edges_list.names.index(el)
        except ValueError:
            print(el, " is not in the list of edgesets.")            
        num_edges = len(graph.edges_list.list[i].edges)
        elist = []
        for j in range(num_edges):
            elist.append(graph.edges_list.list[i].edges[j].edge)
        if elist:
            estack = np.hstack(elist)
            edge_mesh = pv.PolyData(vertices, lines=estack, n_lines = num_edges)
            pl.add_mesh(edge_mesh, color = graph.edges_list.list[i].color, opacity = graph.edges_list.list[i].opacity, line_width = graph.edges_list.list[i].line_width, point_size=0)        
        else:
            print('No edges in this graph')

# camera views: xy, xz, yz, yx, zx, zy, iso 
    pl.camera_position = camera_pos
    pl.camera.roll = camera_rot[0]
    pl.camera.azimuth = camera_rot[1]
    pl.camera.elevation = camera_rot[2]
    pl.camera.zoom(1)      
# screenshot
    pl.screenshot(fname, window_size=[2000,2000])
    #pl.show_axes()    
    print(caption)
    pl.show()



