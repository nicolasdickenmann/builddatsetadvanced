{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 72,
   "id": "cd9dd1ab",
   "metadata": {},
   "outputs": [],
   "source": [
    "# general imports\n",
    "\n",
    "import io\n",
    "import sys\n",
    "import subprocess \n",
    "import copy\n",
    "\n",
    "import numpy as np\n",
    "import pyvista as pv\n",
    "\n",
    "# make sure the user has at least Python 3.7, which we need for some capture_output\n",
    "assert sys.version_info.major == 3, \"This requires at least Python 3.7\"\n",
    "assert sys.version_info.minor >= 7, \"This requires at least Python 3.7\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 73,
   "id": "80dc03da",
   "metadata": {},
   "outputs": [],
   "source": [
    "# viz stuff\n",
    "# Let's define some colors\n",
    "RED = '#FF0000'\n",
    "YELLOW = '#CCCC00'\n",
    "GREEN = '#00DD00'\n",
    "CYAN = '#00FFFF'\n",
    "BLUE = '#0000FF'\n",
    "MAGENTA = '#CC00CC'\n",
    "\n",
    "LT_RED = '#FF3333'\n",
    "DK_RED = '#990000'\n",
    "ORANGE = '#FF8400'\n",
    "LT_GREEN = '#44FF44'\n",
    "DK_GREEN = '#009900'\n",
    "NEON_GREEN = '#00FE94'\n",
    "LT_BLUE = '#0088FF'\n",
    "NEON_BLUE = '#7DF9FF'\n",
    "LIGHT_COLOR = 'white'\n",
    "BACKGROUND_COLOR = 'white'\n",
    "GREY = '#AAAAAA'\n",
    "LT_GREY = '#CCCCCC'\n",
    "\n",
    "L_color = RED\n",
    "W_color = DK_RED\n",
    "C_color = LT_GREEN\n",
    "V1_color = DK_GREEN\n",
    "V2_color = LT_BLUE\n",
    "# these next are for the lex display if desired\n",
    "# vertex_size = 70\n",
    "# W_color = RED\n",
    "# C_color = GREEN\n",
    "# V1_color = GREEN\n",
    "\n",
    "\n",
    "def visualize_graph(layout, q, vertex_list, L, W, C, V1, V2, \n",
    "                    edge_sets, edge_opacities, edge_colors, line_widths, \n",
    "                    fname, camera_pos, camera_rot , show_labels, caption):\n",
    "    print(caption)\n",
    "    if q<17:\n",
    "        edge_opacities[0] = 0.08\n",
    "    elif q<27:\n",
    "        edge_opacities[0] = 0.04\n",
    "    elif q<47:\n",
    "        edge_opacities[0] = 0.01\n",
    "    elif q<63:\n",
    "        edge_opacities[0] = 0.005\n",
    "    elif q<129:\n",
    "        edge_opacities[0] = 0.0005\n",
    "    else:\n",
    "        edge_opacities[0] = 0.0001\n",
    "    vertex_size = 25\n",
    "    vertex_size_smaller = vertex_size\n",
    "\n",
    "    # camera_pos views: xy, xz, yz, yx, zx, zy, iso, can also define a camera_pos = (x,y,z) tuple\n",
    "#     camera_pos = 'zx'\n",
    "#     camera_rot = [0,5,15]\n",
    "#     # overhead view\n",
    "#     camera_pos = 'xy'\n",
    "#     camera_rot = [0,0,180]\n",
    "    pl = pv.Plotter(lighting=None, window_size=(2000, 2000))\n",
    "    light1 = pv.Light(position=(10, 10., -5.0),\n",
    "                       focal_point=(0, 0, 0),\n",
    "                       color=LIGHT_COLOR,  # Color temp. 5400 K\n",
    "                       intensity=1.5)\n",
    "    light2 = pv.Light(position=(-10, 10.0, -5.0),\n",
    "                       focal_point=(0, 0, 0),\n",
    "                       color=LIGHT_COLOR,  # Color temp. 2850 K\n",
    "                       intensity=0.75)\n",
    "#     pl.add_light(light1)  # Lighting effect to be cast onto the object\n",
    "#     pl.add_light(light2)  # Second Lighting effect to be cast onto the object\n",
    "    hlight = pv.Light(light_type='headlight')\n",
    "    pl.add_light(hlight)  # Second Lighting effect to be cast onto the object\n",
    "    pl.set_background(BACKGROUND_COLOR)  # Set the background \n",
    "            \n",
    "    # pdata is the basic vertex data positions\n",
    "    vpos = []\n",
    "    for i in range(len(vertex_list)):\n",
    "        if layout == 'lex':\n",
    "            vpos.append(vertex_list[i].pos[0]) \n",
    "        elif layout == 'good':\n",
    "            vpos.append(vertex_list[i].pos[1]) \n",
    "        elif layout == 'cake':\n",
    "            vpos.append(vertex_list[i].pos[2]) \n",
    "    pdata = pv.PolyData(vpos)     \n",
    "# this adds point labels of vector values -- but placed on top of the points\n",
    "    if (show_labels):\n",
    "        point_labels = []\n",
    "        for i in range(len(vertex_list)):\n",
    "            point_labels.append(vertex_list[i].value)        \n",
    "        pl.add_point_labels(pdata, point_labels, italic=False, bold=True, font_size=30,\n",
    "                            point_color='black', point_size=0, text_color='black', \n",
    "                            shape=None, \n",
    "                            render_points_as_spheres=True,\n",
    "                            always_visible=True, shadow=False)  \n",
    "# this adds the other edge sets    \n",
    "    other_pdata = []\n",
    "    for i in range(len(edge_sets)):\n",
    "        other_pdata.append(pv.PolyData(vpos))\n",
    "        other_pdata[i].lines = edge_sets[i]\n",
    "        pl.add_mesh(other_pdata[i],\n",
    "                    color = edge_colors[i],\n",
    "                    opacity = edge_opacities[i],\n",
    "                    point_size=0,\n",
    "                    line_width = line_widths[i],\n",
    "                    render_points_as_spheres=True\n",
    "        )        \n",
    "    L_vertex_position=[]\n",
    "    for i in L:\n",
    "        L_vertex_position.append(vpos[L[0]])\n",
    "    L_cloud = pv.PolyData(L_vertex_position)\n",
    "    pl.add_mesh(L_cloud, \n",
    "                color=L_color, \n",
    "                point_size=vertex_size,\n",
    "                render_points_as_spheres=True\n",
    "               )\n",
    "    W_vertex_position=[]\n",
    "    for i in W:\n",
    "        W_vertex_position.append(vpos[i])\n",
    "    W_cloud = pv.PolyData(W_vertex_position)\n",
    "    pl.add_mesh(W_cloud, \n",
    "                color=W_color, \n",
    "                point_size=vertex_size,\n",
    "                render_points_as_spheres=True\n",
    "               )\n",
    "    C_vertex_position=[]\n",
    "    for i in C:\n",
    "        C_vertex_position.append(vpos[i])\n",
    "    C_cloud = pv.PolyData(C_vertex_position)\n",
    "    pl.add_mesh(C_cloud, \n",
    "                color=C_color, \n",
    "                point_size=vertex_size,\n",
    "                render_points_as_spheres=True\n",
    "               )\n",
    "    V1_vertex_position=[]\n",
    "    for i in V1:\n",
    "        V1_vertex_position.append(vpos[i])\n",
    "    V1_cloud = pv.PolyData(V1_vertex_position)\n",
    "    pl.add_mesh(V1_cloud, \n",
    "                color=V1_color, \n",
    "                point_size=vertex_size_smaller,\n",
    "                render_points_as_spheres=True\n",
    "               )\n",
    "    V2_vertex_position=[]\n",
    "    for i in V2:\n",
    "        V2_vertex_position.append(vpos[i])\n",
    "    V2_cloud = pv.PolyData(V2_vertex_position)\n",
    "    pl.add_mesh(V2_cloud, \n",
    "                color=V2_color, \n",
    "                point_size=vertex_size_smaller,\n",
    "                render_points_as_spheres=True\n",
    "               )    \n",
    "    # Views: xy, xz, yz, yx, zx, zy, iso \n",
    "    pl.camera_position = camera_pos\n",
    "    pl.camera.roll = camera_rot[0]\n",
    "    pl.camera.azimuth = camera_rot[1]\n",
    "    pl.camera.elevation = camera_rot[2]\n",
    "    pl.camera.zoom(1)   \n",
    "    # Save the plot as a screenshot.  We can change the output resolution if desired\n",
    "    pl.screenshot(fname, window_size=[2000,2000])\n",
    "    #pl.add_point_labels(vpos_sets[0], range(len(vpos_sets[0])), font_size=100)\n",
    "    #pl.show_axes()\n",
    "    pl.show()\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
