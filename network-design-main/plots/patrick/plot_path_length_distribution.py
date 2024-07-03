import matplotlib.pyplot as plt
from os.path import exists
import csv

global_markers = ["o","^","x","d","*","h","s","D","2",">","<","^","o","o","o","o","o","o","o","o","o"]

global_colors = ["#000000","#000099","#009900","#990000","#990099","#009999","#999900",
                 "#555555","#5555CC","#55CC55","#CC5555","#CC55CC","#55CCCC","#CCCC55",
                 "#777777","#7777FF","#77FF77","#FF7777","#FF77FF","#77FFFF","#FFFF77",
                ]

def read_data(filename):
	print("Reading File: " + filename)
	path_length_counts = [{} for i in range(6)]
	with open("results/" + filename, newline = '') as csvfile:
		reader =csv.reader(csvfile, delimiter=',', quotechar = '"')
		headers = [x.replace(' ','') for x in next(reader)]
		for row in reader:
			for i in range(5):
				load = float(row[headers.index("input_inj_rate")])
				if (load * 10) % 1 == 0:
					path_count = int(row[headers.index("num_"+str(i+1)+"_hops")])
					path_length_counts[i][load] = path_count
	return path_length_counts

def create_one_plot(configs, plotname):
	fig, ax = plt.subplots(1,1, figsize = (4,4))
	plt.subplots_adjust(left=0.15, right = 0.97, top = 0.92, bottom = 0.125)
	n = len(configs)
	i = 0
	for i_ in range(len(configs)):
		(graph, traffic, routing) = configs[i_]
		filename = "results-%s-%s-%s.csv" % (graph, traffic, routing)
		if not exists("results/" + filename):
			print("File not found: " + filename)
			continue
		i += 1
		path_length_counts = read_data(filename)
		marker = global_markers[i]
		color = global_colors[i]
		label = graph + "-" + routing	
		first = True
		for j in range(6):
			x = (n+1) * j + i + 1
			for load in path_length_counts[j].keys():
				if sum([path_length_counts[k][load] for k in range(5)]) == 0:
					continue
				y = path_length_counts[j][load] / sum([path_length_counts[k][load] for k in range(5)])
				ms = 2 + (load * 7)
				ax.plot(x, y, label = (label if first else ""), 
						marker = marker , color = color, 
						markersize = ms, markeredgewidth = 1, 
						markerfacecolor = "None", linestyle = "None")
				first = False
	ax.set_ylim(-0.05,1.05)
	ax.set_xlim(0,6)
	ax.set_xticklabels('')
	ax.set_xticks([(n+1) * i for i in range(6)], minor = False)
	ax.set_xticks([(n+1) * (i + 0.5) for i in range(5)],minor = True)
	ax.set_xticklabels([str(i) for i in range(5)], minor = True)
	ax.tick_params(axis='x', which='minor',length=0)
	ax.set_xlabel("Number of hops")
	ax.set_ylabel("Fraction of paths with a given number of hops")
	plt.legend(
		loc='upper left', bbox_to_anchor=(0.0, 1.0),				# Position of legend
		prop={'size': 10}, markerscale = 1.5,				   		# Text and marker size
		handletextpad=0.1, handlelength = 0.7,
		columnspacing = 1, labelspacing = 0.2)
	ax.grid()
	plt.savefig("plots/" + plotname + ".pdf")

def create_all_plots():
	n = 3
	graphs = ["Brown.11"] * n
	traffics = ["uniform"] * n
	routings = ["min","ugall4_pf","ugall3_pf"]
	create_one_plot(n, graphs, traffics, routings, "hist-uniform")
	n = 3
	graphs = ["Brown.11"] * n
	traffics = ["shuffle"] * n
	routings = ["min","ugall4_pf","ugall3_pf"]
	create_one_plot(n, graphs, traffics, routings, "hist-shuffle")

def create_all_plots():	
	# Create topology comparison
	traffics = ["uniform","goodpf","badpf","shuffle","randperm"]
	graphs = ["pf","sf","df","ft"]
	routings = ["min","ugall4_pf","ugallnew","ugal","ugalgnew","nca"]
	for traffic in traffics:
		configs = []
		for graph in graphs:
			for routing in routings:
				configs.append((graph, traffic, routing))
		create_one_plot(configs, "pl_" + traffic)
	# Create comparison of expanded PFs
	expansion_methods = ["m0","m1"]
	expansion_numbers = ["3","6","9","12"]
	routings = ["ugall4_pf","ugallnew"]
	for em in expansion_methods:
		configs = []
		for en in expansion_numbers:
			for routing in routings:
				configs.append(("pf_" + em + "_" + en, "uniform", routing))
		create_one_plot(configs, "pl_expansion_" + em)


		
create_all_plots()
