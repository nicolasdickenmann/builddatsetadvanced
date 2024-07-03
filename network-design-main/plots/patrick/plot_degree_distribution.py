import matplotlib.pyplot as plt
import math
from matplotlib.patches import Ellipse
import csv
import sys

color_map = {
	"W" : "#000000",
	"V1" : "#990000",
	"V2" : "#000099",
}

marker_map = {
	("PF", "W") :  "s",
	("PF", "V1") : "D",
	("PF", "V2") : "^",
	("PF-M1", "W") :    "+",
	("PF-M1", "V1") :   "x",
	("PF-M1", "V2") :   "1",
	("PF-M2", "W") :    "+",
	("PF-M2", "V1") :   "x",
	("PF-M2", "V2") :   "1",
}


def build_type_map():
	type_map = {}
	with open("graphs/PF.adj.txt", newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=' ', quotechar='"')
		(n, m) = next(reader)
		(n, m) = (int(n), int(m))
		v_id = 0
		for row in reader:
			row = row[:-1]
			if len(row) % 2 == 1:
				type_map[v_id] = "W"
				for n_id in [int(x) for x in row if x != ""]:
					type_map[n_id] = "V1"
			elif v_id not in type_map:
				type_map[v_id] = "V2"
			v_id += 1
	return type_map

def read_graph(filename):
	degree_map = {}
	with open(filename, newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter=' ', quotechar='"')
		(n, m) = next(reader)
		(n, m) = (int(n), int(m))
		v_id = 0
		for row in reader:
			row = row[:-1]
			degree_map[v_id] = len(row)
			v_id += 1
	return (n, m, degree_map)


def add_datapoint_for_one_graph(ax, filename, method, param, typemap, used_labels):
	(n,m,degree_map) = read_graph(filename)	
	data = {}
	for v_id in range(n):
		deg = degree_map[v_id]
		typ = typemap.get(v_id, "W" if method == "PF-M1" else "V1")
		if (deg, typ) in data:
			data[(deg,typ)] += 1
		else:
			data[(deg,typ)] = 1

	for (deg, typ) in data:
		x = deg
		y = data[(deg,typ)]
		color = color_map[typ]
		marker = marker_map[(method, typ)]
		
		label = typ + (" (Expanded)" if method != "PF" else "")
		label = label if label not in used_labels else ""
		used_labels.add(label)
		markersize = (((param if method == "PF-M1" else param / 2) + 15) / 3 if param > 0 else 3)
		ax.plot(x, y, label = label, color = color, marker = marker, markersize = markersize) 

def create_one_plot(ax, method, params):
	ax.grid(which="major", linewidth = 1.0, color = "#666666")
	typemap = build_type_map()

	used_labels = set()

	for param in params:
		if method == "PF-M1":
			filename = "graphs/BrownExt.25.%d.0" % (param,)
		else:
			filename = "graphs/BrownExt.25.0.%d" % (param,)
		add_datapoint_for_one_graph(ax, filename, method, param, typemap, used_labels)

	add_datapoint_for_one_graph(ax, "graphs/PF.adj.txt", "PF", 0, typemap, used_labels)

	ax.set_ylim(0,600)
	ax.set_xlim(20,60)
	ax.set_xlabel("Network radix")
	ax.set_ylabel("#Routers with given network radix")
	ax.set_title("Replicate Quadrics" if method == "PF-M1" else "Round-robin Replication")
	handles, labels = ax.get_legend_handles_labels()
	order = [4,3,5,1,0,2]
	handles = [handles[idx] for idx in order]
	labels = [labels[idx] for idx in order]	
	ax.legend(			handles,
						labels,
						loc='upper left', 
						bbox_to_anchor=(0.0, 1.0), 
						ncol = 2,
						prop={'size': 9},
						handletextpad=0.6,
						labelspacing = 0.3, 
						handlelength = 0.0, 
						columnspacing = 0.8, 
						markerscale = 1.2,
					)


def create_all_plots():
	methods = ["PF-M1", "PF-M2"]
	paramss = [[3,6,9,13], [6,13,19,26]]

	fig, ax = plt.subplots(1,2, figsize = (6,3))
	plt.subplots_adjust(left=0.1, right = 0.98, top = 0.9, bottom = 0.15, wspace = 0.3)

	for i in range(2):
		create_one_plot(ax[i], methods[i], paramss[i])	
	plt.savefig("plots/degree_distribution.pdf")

create_all_plots()


