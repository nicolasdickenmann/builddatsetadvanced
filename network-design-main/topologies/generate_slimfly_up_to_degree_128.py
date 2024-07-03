import subprocess
import math
import sys
import os

from translate_topogen_to_bs import *

prime_powers = [3,4,5,7,8,9,11,13,16,17,19,23,25,27,29,31,32,37,41,43,47,49,53,59,61,64,67,71,73,79,81,83,89,97]

for q in prime_powers:
	if q % 4 == 0:
		delta = 0
	elif (q - 1) % 4 == 0:
		delta = 1
	elif (q + 1) % 4 == 0:
		delta = -1
	else:
		print("\tFailed to find delta in [-1,0,1] such that q = 4w + delta => SKIP q = %d" % q)
		continue
	concentration = int(math.ceil((3 * q - delta) / 4))
	routers = 2 * q**2
	nodes = concentration * routers
	network_radix = int(math.ceil((3 * q - delta) / 2))
	router_radix = network_radix + concentration

	if network_radix > 128:
		break

	print("===========================================================")
	print("q = %d" % q)
	print("===========================================================")
	print("--> Routers:\t\t\t\t%d" % routers)
	print("--> Concentration (nodes per router):\t%d" % concentration)
	print("--> Nodes:\t\t\t\t%d" % nodes)
	print("--> Network Radix:\t\t\t%d" % network_radix)
	print("--> Router Radix:\t\t\t%d" % router_radix)
	os.system("python tool.py generate slimfly %d" % q)
	print("--> Translating topology from adjacency list to BookSim format")
	topogen_file = "data/slimflies/SlimFly.%d.adj.txt" % q
	bs_file = "data/slimflies/SlimFly.%d.bsconf" % q
	translate_topogen_to_bs(topogen_file, bs_file, concentration)
	print("--> Saving to %s" % bs_file)
	print()

