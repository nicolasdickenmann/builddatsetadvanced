def translate_topogen_to_bs(in_file, out_file, concentration):
	# Read topogen format
	with open(in_file, "r") as file:
		next(file)
		data = file.readlines()
	# Transform and write data
	node_id = 0
	with open(out_file, "w") as file:
		# Transform
		for (router_id, line) in enumerate(data):	
			line_bs = "router %d" % router_id
			# Add router-to-router connections
			for other_router_id in line.split(" "):
				if other_router_id != "\n":
					line_bs += " router %d" % int(other_router_id)
			# Add router-to-node connections
			for i in range(concentration):
				line_bs += " node %d" % int(node_id)
				node_id += 1
			line_bs += "\n"
			# Write
			file.write(line_bs)
		
