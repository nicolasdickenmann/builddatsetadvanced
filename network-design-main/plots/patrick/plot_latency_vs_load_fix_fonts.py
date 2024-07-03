import matplotlib
import matplotlib.pyplot as plt
import csv
from os.path import exists

global_markers = ["o","^","x","d","*","h","s","D","2",">","<","^","o","o","o","o","o","o","o","o","o"]

global_colors = ["#000000","#000077","#007700","#770000","#770077","#007777","#777700",
				 "#555555","#5555CC","#55CC55","#CC5555","#CC55CC","#55CCCC","#CCCC55",
				 "#777777","#7777FF","#77FF77","#FF7777","#FF77FF","#77FFFF","#FFFF77",
				]

global_color_and_marker_map = {
	("pf","min") 				:	("#000000","o"),
	("pf","ugall4_pf") 			:	("#000077","^"),
	("pf","ugallnew") 			:	("#770000","d"),

	("sf","min") 				:	("#770077","p"),
	("sf","ugallnew") 			:	("#007777","+"),

	("df17","min") 				: 	("#777700","D"),
	("df17","ugal") 			: 	("#777777","s"),
	("df32","min") 				: 	("#006699","d"), #TODO
	("df32","ugal") 			: 	("#3399FF","."), #TODO

	("jf","min") 				: 	("#009966","X"), #TODO
	("jf","ugal") 				: 	("#33FF66","x"), #TODO
	("jf","ugallnew") 			: 	("#33FF66","x"), #TODO

	("ft","nca") 				:	("#CC7700","*"),

	("pf13","min") 				: 	("#777700","o"),
	("pf19","min") 				: 	("#770077","d"),
	("pf25","min") 				: 	("#007777","x"),
	("pf31","min") 				: 	("#777777","p"),

	("pf13","ugall4_pf") 		: 	("#777700","o"),
	("pf19","ugall4_pf") 		: 	("#770077","d"),
	("pf25","ugall4_pf") 		: 	("#007777","x"),
	("pf31","ugall4_pf") 		: 	("#777777","p"),


	("pf_m0_3","ugall4_pf") 	:	("#777700","o"),
	("pf_m0_6","ugall4_pf") 	:	("#770077","d"),
	("pf_m0_9","ugall4_pf") 	:	("#007777","x"),
	("pf_m0_12","ugall4_pf") 	:	("#777777","p"),

	("pf_m1_3","ugall4_pf") 	:	("#777700","o"),
	("pf_m1_6","ugall4_pf") 	:	("#770077","d"),
	("pf_m1_9","ugall4_pf") 	:	("#007777","x"),
	("pf_m1_12","ugall4_pf") 	:	("#777777","p"),
}

global_graph_label_map = {
	"pf_m0_3" : "PF$_{10}$",
	"pf_m0_6" : "PF$_{19}$",
	"pf_m0_9" : "PF$_{29}$",
	"pf_m0_12" :"PF$_{39}$",
	"pf_m1_3" : "PF$_{10}$",
	"pf_m1_6" : "PF$_{19}$",
	"pf_m1_9" : "PF$_{29}$",
	"pf_m1_12" :"PF$_{39}$",
	"pf" : "PF",
	"sf" : "SF",
	"df" : "DF",
	"df32" : "DF2",
	"df17" : "DF1",
	"ft" : "FT",
	"jf" : "JF",
	"pf13" : "PF$_{13}$",
	"pf19" : "PF$_{19}$",
	"pf25" : "PF$_{25}$",
	"pf31" : "PF$_{31}$",
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
			if "-" not in row[headers.index("avg_latency_str")] and "dl" not in row[headers.index("avg_latency_str")]:
				load = float(row[headers.index("input_inj_rate")])
				latency = float(row[headers.index("avg_latency_str")])
				latencies[load] = latency
	return latencies

def create_one_plot(configs, plotname, legend_pos, ylab, xlim):
	matplotlib.rc('pdf', fonttype=42)
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
	if legend_pos == "ul":
		lpos = ("upper left", (0.0,1.0))
	elif legend_pos == "lr":
		lpos = ("lower right",(1.0,0.0))
	elif legend_pos == "uc":
		lpos = ("upper center",(0.5,1.0))
	plt.legend(
		loc=lpos[0], bbox_to_anchor=lpos[1],        		# Position of legend
		prop={'size': 8.5}, markerscale = 1.7,                   		# Text and marker size
		handletextpad=0.1, handlelength = 1.0,
		columnspacing = 1, labelspacing = 0.2, 
		ncol = 1, framealpha=0.5)
	ax.set_ylim(0,100)
	ax.set_xlim(0,xlim)
	ax.set_xlabel("Offered Load")
	if ylab:
		ax.set_ylabel("Average Latency [cycles]")
	ax.grid()
	plt.savefig("plots_fix_fonts/" + plotname + ".pdf")

def create_all_plots():	
	# Uniform + MIN
	configs = [(g,"uniform",r) for g in ["pf","sf","df17","df32","ft","jf"] for r in ["min","nca"]]
	create_one_plot(configs, "uniform-min", "ul", True, 1.0)
	# Uniform + UGAL
	configs = [(g,"uniform",r) for g in ["pf","sf","df17","df32","ft","jf"] for r in ["ugal","ugallnew","ugall4_pf","nca"]]
	create_one_plot(configs, "uniform-ugal", "ul", False, 1.0)
	# Rand-Perm
	configs = [(g,"randperm",r) for g in ["pf","sf","df17","df32","ft","jf"] for r in ["nca","ugal","ugallnew","ugall4_pf"]]
	create_one_plot(configs, "randperm", "lr", False, 1.0)
	# Tornado 
	configs = [(g,"tornado",r) for g in ["pf","sf","df17","df32","ft","jf"] for r in ["nca","ugal","ugallnew","ugall4_pf"]]
	create_one_plot(configs, "tornado", "lr", False, 1.0)
	# Good-PF 
	configs = [("pf","goodpf",r) for r in ["min","ugallnew","ugall4_pf"]]
	create_one_plot(configs, "goodpf", "lr", True, 0.6)
	# Bad-PF 
	configs = [("pf","badpf",r) for r in ["min","ugallnew","ugall4_pf"]]
	create_one_plot(configs, "bad", "lr", False, 0.6)
	# Uniform + MIN (size evaluation)
	configs = [(g,"uniform","min") for g in ["pf13","pf19","pf25","pf31"]]
	create_one_plot(configs, "size-min", "ul", True, 1.0)
	# Uniform + UGAL (size evaluation)
	configs = [(g,"uniform","ugall4_pf") for g in ["pf13","pf19","pf25","pf31"]]
	create_one_plot(configs, "size-ugal", "ul", False, 1.0)
	# Uniform + UGAL (expanded PFs using M0)
	configs = [(g,"uniform","ugall4_pf") for g in ["pf","pf_m0_3","pf_m0_6","pf_m0_9","pf_m0_12"]]
	create_one_plot(configs, "expand-m0", "ul", True, 1.0)
	# Uniform + UGAL (expanded PFs using M1)
	configs = [(g,"uniform","ugall4_pf") for g in ["pf","pf_m1_3","pf_m1_6","pf_m1_9","pf_m1_12"]]
	create_one_plot(configs, "expand-m1", "ul", False, 1.0)

		
create_all_plots()
