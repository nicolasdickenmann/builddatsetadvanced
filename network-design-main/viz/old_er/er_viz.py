import io
import sys
import subprocess 
import copy

import numpy as np
import pyvista as pv

# make sure the user has at least Python 3.7, which we need for some capture_output
assert sys.version_info.major == 3, "This requires at least Python 3.7"
assert sys.version_info.minor >= 7, "This requires at least Python 3.7"# viz stuff

def visualize_graph(layout, vertex_list, edges_list, edge_displaylist, 
                    fname, camera_pos, camera_rot , show_labels, caption):

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
    
# extract the layout
    if layout == 'lex':
        layout_num = 0
    elif layout == 'good':
        layout_num = 1
    elif layout == 'cake':
        layout_num = 2  
        
# vertices
    for v in vertex_list:
        pt = pv.PolyData(v.pos[layout_num])
        pl.add_points(pt, color=v.color, point_size=v.size, render_points_as_spheres=True)
        if (show_labels):
            pt_label = [v.value]
            pl.add_point_labels(pt, pt_label, italic=False, bold=True, font_size=30, 
                                text_color='black', always_visible=True, shape=None) 
            
# edge sets
    vpos = []
    for v in vertex_list:
        vpos.append(v.pos[layout_num])
    vertices = np.array(vpos)
    for i in edge_displaylist:
        num_edges = len(edges_list.list[i].edges)
        elist = []
        for j in range(num_edges):
            elist.append(edges_list.list[i].edges[j])
        edges = np.hstack(elist)
        edge_mesh = pv.PolyData(vertices, lines=edges)
#         edge_mesh = pv.PolyData(vertices, lines=edges, n_lines = num_edges)
        pl.add_mesh(edge_mesh, color = edges_list[i].color, opacity = edges_list[i].opacity, line_width = edgelist_list[i].line_width, point_size=0)        
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
