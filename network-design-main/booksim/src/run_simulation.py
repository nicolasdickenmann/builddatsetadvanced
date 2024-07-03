import subprocess
import sys
import time

def run_loads(loads):
	processes = []
	latencies = []
	# Launch processes
	for load in loads:
		# Configure load:
		with open(cfg_file_name, "r") as cfg_file:
			lines = cfg_file.readlines()
		lines[0] = "injection_rate = " + str(load) + ";\n"
		with open(cfg_file_name, "w") as cfg_file:
			cfg_file.writelines(lines)
		# Start thread:
		processes.append(subprocess.Popen(['./booksim', cfg_file_name], stdout=subprocess.PIPE))
		time.sleep(3)

	# Collect processes
	for i in range(len(processes)):
		load = loads[i]
		# Read results
		out = processes[i].stdout.read()
		out_list = str(out)[1:-1].split("\\n")[-50:]
		out_str = ""
		for line in out_list:
			out_str += line + "\n"	
		# Write logfile
		with open(log_file_name, "a") as log_file:
			log_file.write("\n\n********** %s - %s - %s - %s - %f **********\n\n" % (graph, traffic, routing, adaptive_th, load))	
			log_file.write(out_str)
		# Write result file 
		break_flag = False
		if "unstable" in out_str:
			with open(res_file_name, "a") as res_file:
				res_file.write("%f, %f, %f, %f, %f, %f, %f, %f\n" % tuple([load] + [500] + [0] * 6))
			print("Load = %f \t=> Unstable" % (load, ))
			latencies.append(500)
			break_flag = True
		else:
			vals = [-1,-1,-1,-1,-1,-1,-1]
			lines = [-34,-3,-4,-5,-6,-7,-8]
			try:
				for j in range(len(lines)):	
					tmp = out_list[lines[j]].split(" ")	
					for k in range(len(tmp)-1):
						if tmp[k] == "=":
							vals[j] = float(tmp[k+1])
							break
				with open(res_file_name, "a") as res_file:
					res_file.write("%f, %f, %f, %f, %f, %f, %f, %f\n" % tuple([load] + vals))
				print("Load = %f \t=> Latency = %f" % (load, vals[0]))
				latencies.append(vals[0])
				if vals[0] > 50:
					break_flag = True
			#except:
			except Exception as e: 
				print("Load = %f \t=> Exception" % (load, ))
				latencies.append(-1)
				break_flag = True
		if break_flag:
			for j in range(i+1,len(loads)):
				processes[j].terminate()	
			return latencies
	return latencies
	

def simulate(initial_loads):
	loads = initial_loads
	latencies = run_loads(loads)
	all_loads = [x for x in loads]
	all_latencies = [x for x in latencies]
	while True:
		new_loads = []
		for i in range(len(all_loads)-1):
			if all_latencies[i] * 1.5 < all_latencies[i+1] \
				and abs(all_loads[i] - all_loads[i+1]) > 0.01 \
				and all_latencies[i] < 50:
				new_loads.append((all_loads[i] + all_loads[i+1]) / 2.0)
		if len(new_loads) > 0:
			loads = new_loads	
			latencies = run_loads(loads)
			all_loads = all_loads + loads
			all_latencies = all_latencies + latencies
			all_latencies = [x for _, x in sorted(zip(all_loads, all_latencies))]
			all_loads = sorted(all_loads)
			
		else:
			return

#loads = [0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95]
loads = [0.1,0.9]

# Read arguments
if len(sys.argv) < 4:
	print("Usage: run_simulation.py <graph> <traffic> <routing> [adaptive-th] [load]")
	sys.exit()

graph = sys.argv[1]
traffic = sys.argv[2]
routing = sys.argv[3]

adaptive_th = sys.argv[4] if len(sys.argv) > 4 else "4"
one_load = sys.argv[5] if len(sys.argv) > 5 else None
po2 = "yes" if traffic in ["bitrev","shuffle"] else "no"

loads = loads if one_load == None else [float(one_load)]
load_txt = "" if one_load == None else ("-" + str(one_load))

# Prepare files
cfg_file_name = graph + ".conf"
res_file_name = "results/results-%s-%s-%s-%s%s.csv" % (graph, traffic, routing, adaptive_th, load_txt)
log_file_name = "logs/log-%s-%s-%s-%s%s.log" % (graph, traffic, routing, adaptive_th, load_txt)

# Do general configuration:
with open(cfg_file_name, "r") as cfg_file:
	lines = cfg_file.readlines()
lines[1] = "traffic = " + traffic + ";\n"
lines[2] = "routing_function = " + routing + ";\n"
lines[3] = "use_size_power_of_two = " + po2 + ";\n"
lines[4] = "adaptive_threshold = " + adaptive_th + ";\n"
with open(cfg_file_name, "w") as cfg_file:
	cfg_file.writelines(lines)

# Run simulations for different loads:
simulate(loads)



