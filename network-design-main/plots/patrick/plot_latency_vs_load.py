import matplotlib.pyplot as plt
import csv
from os.path import exists

global_markers = ["o","^","x","d","*","h","s","D","2",">","<","^","o","o","o","o","o","o","o","o","o"]

global_colors = ["#000000","#000077","#007700","#770000","#770077","#007777","#777700",
				 "#555555","#5555CC","#55CC55","#CC5555","#CC55CC","#55CCCC","#CCCC55",
				 "#777777","#7777FF","#77FF77","#FF7777","#FF77FF","#77FFFF","#FFFF77",
				]

global_color_and_marker_map = {
	("pf","min") : 			("#000000","o"),
	("pf","ugall4_pf") : 	("#000077","^"),
	("pf","ugallnew") : 	("#770000","d"),
	("pf","ugalgnew") : 	("#007700","x"),

	("sf","min") : 			("#770077","p"),
	("sf","ugallnew") : 	("#007777","+"),

	("df","min") : 			("#777700","D"),
	("df","ugal") : 		("#777777","s"),

	("ft","nca") : 			("#CC7700","*"),

	("pf_m0_3","ugall4_pf") :  ("#777700","o"),
	("pf_m0_6","ugall4_pf") :  ("#770077","d"),
	("pf_m0_9","ugall4_pf") :  ("#007777","x"),
	("pf_m0_12","ugall4_pf") : ("#777777","p"),

	("pf_m1_3","ugall4_pf") :  ("#777700","o"),
	("pf_m1_6","ugall4_pf") :  ("#770077","d"),
	("pf_m1_9","ugall4_pf") :  ("#007777","x"),
	("pf_m1_12","ugall4_pf") : ("#777777","p"),
}

global_graph_label_map = {
	"pf" : "PF",
	"pf_m0_3" : "PF$_{10}$",
	"pf_m0_6" : "PF$_{19}$",
	"pf_m0_9" : "PF$_{29}$",
	"pf_m0_12" :"PF$_{39}$",
	"pf_m1_3" : "PF$_{10}$",
	"pf_m1_6" : "PF$_{19}$",
	"pf_m1_9" : "PF$_{29}$",
	"pf_m1_12" :"PF$_{39}$",
	"pf" : "PF",
	"pf" : "PF",
	"sf" : "SF",
	"df" : "DF",
	"ft" : "FT",
	}

global_routing_label_map = {
	"min" : "MIN",
	"ugallnew" : "UGAL",
	"ugalgnew" : "UGAL-G",
	"ugal" : "UGAL",
	"ugall4_pf" : "UGAL$_{PF}$",
	"nca" : "NCA",
	}



def read_data(filename):
	print("Reading file " + filename)
	latencies = {}
	with open("results/" + filename, newline = '') as csvfile:
		reader =csv.reader(csvfile, delimiter=',', quotechar = '"')
		headers = [x.replace(' ','') for x in next(reader)]
		for row in reader:
			if "-" not in row[headers.index("avg_latency_str")]:
				load = float(row[headers.index("input_inj_rate")])
				latency = float(row[headers.index("avg_latency_str")])
				latencies[load] = latency
	return latencies

def create_one_plot(configs, plotname, legend_pos, ylab):
	if ylab:
		fig, ax = plt.subplots(1,1, figsize = (3.25,3))
		plt.subplots_adjust(left=0.2, right = 0.95, top = 0.95, bottom = 0.15)
	else:
		fig, ax = plt.subplots(1,1, figsize = (3,3))
		plt.subplots_adjust(left=0.125, right = 0.95, top = 0.95, bottom = 0.15)
	i = 0
	for i_ in range(len(configs)):
		(graph, traffic, routing) = configs[i_]	
		filename = "results-%s-%s-%s.csv" % (graph, traffic, routing)
		if not exists("results/" + filename):
			print("File not found: " + filename)
			continue
		i += 1
		latencies = read_data(filename)
		label = global_graph_label_map[graph] + "-" + global_routing_label_map[routing]
		loads = sorted(latencies.keys())
		lats = [latencies[x] for x in loads]
		(color, marker) = global_color_and_marker_map[(graph,routing)]
		ax.plot(	
			loads, lats,linewidth = 1,markersize = 2.5, 
			marker = marker, color = color, label = label) 					# label
	lpos = ("upper left", (0.0,1.0)) if legend_pos == "ul" else ("lower right",(1.0,0.0))
	plt.legend(
		loc=lpos[0], bbox_to_anchor=lpos[1],        		# Position of legend
		prop={'size': 8.5}, markerscale = 1.7,                   		# Text and marker size
		handletextpad=0.1, handlelength = 1.0,
		columnspacing = 1, labelspacing = 0.2, 
		ncol = 1, framealpha=0.5)
	ax.set_ylim(0,100)
	if max(loads) < 0.58:	
		ax.set_xlim(0,0.6)
	else:
		ax.set_xlim(0,1)
	ax.set_xlabel("Offered Load")
	if ylab:
		ax.set_ylabel("Average Latency [cycles]")
	ax.grid()
	plt.savefig("plots/" + plotname + ".pdf")

def create_all_plots():	
	# Create topology comparison
	traffics = ["uniform","goodpf","badpf","shuffle","randperm"]
	graphs = ["pf","sf","df","ft"]
	routings = ["min","ugall4_pf","ugallnew","ugal","nca"]
	lposs = ["ul","lr","lr","ul","lr"]
	first = True
	for (traffic,lpos) in zip(traffics, lposs):
		configs = []
		for graph in graphs:
			for routing in routings:
				configs.append((graph, traffic, routing))
		create_one_plot(configs, traffic, lpos, first)
		first = False
	# Create comparison of expanded PFs
	expansion_methods = ["m0","m1"]
	expansion_numbers = ["3","6","9","12"]
	routings = ["ugall4_pf"]
	first = True
	for em in expansion_methods:
		configs = []
		configs.append(("pf","uniform","ugall4_pf"))
		for en in expansion_numbers:
			for routing in routings:
				configs.append(("pf_" + em + "_" + en, "uniform", routing))
		create_one_plot(configs, "expansion_" + em, "ul", first)
		first = False
	# Create comparison of expanded PFs

		
create_all_plots()
