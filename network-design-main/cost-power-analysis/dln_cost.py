from cost_model import *
from random import *
import math
import sys
import random

def get_max_free_ports(adj,k_r):
	max_nr = 0
	i = 1
	for s,lst in sorted(adj.iteritems()):
		if(k_r - len(lst) > max_nr):
			max_nr = k_r - len(lst)
			i = s
	return [max_nr,i]

def get_single_free_ports(adj,k_r):
	switches = list()
	for s,lst in sorted(adj.iteritems()):
		if(k_r - len(lst) == 1):
			switches.append(s)
	return switches

def verify_correctness(adj,N_r,k_r):
	assert len(adj) == N_r

	switches = {}
	for s in range(1,N_r+1):
		switches[s] = {}
		for r in range(1,N_r+1):
			switches[s][r] = False

	for s,lst in sorted(adj.iteritems()):
		assert(len(lst) > 0)
		assert(len(lst) <= k_r)
		for r in lst:
			assert(r > 0)
			assert(r <= N_r)
			assert switches[s][r] == False
			switches[s][r] = True

def dln_cost_single_rack_simple(k,N,g, N_1, N_2, k_1, k_2):
	k = int(k)
	N = int(N)
	N_origin = N

	g = int(g)
	p = int((k+1)/4.0) #similar to DF
	k_r = k - p

	N_r = int(math.ceil(N/(1.0*p)))
	a = int(math.ceil(N_r/(1.0*g)))

	'''

	#assert((a*g + N_r % g) == N_r)
	switches_adj = {}
	switches_gr = {}
	gr_nr = 0
	cables = 0

	finished = False
	while not finished:
		repeated = 0
		thresh = 10
		
		switches_adj = {}
		switches_gr = {}
		gr_nr = 0
		cables = 0

		for s in range(1,N_r+1):
			switches_gr[s] = gr_nr
			if((s-1) % a == 0):
				gr_nr += 1

			switches_adj[s] = list()
			switches_adj[s].append((s % N_r) + 1)
			cables += 1
			if(s > 1):
				switches_adj[s].append(((s-1) % N_r))
				cables += 1
			else:
				switches_adj[s].append(N_r)
				cables += 1
		
		assert(gr_nr == g)

		print "XXXXXXXXXXXXXXXXXXX"
		completed = False
		while not completed:
			s_A = random.randrange(N_r)+1
			while len(switches_adj[s_A]) == k_r:
				s_A = random.randrange(N_r)+1
	
			s_B = random.randrange(N_r)+1
			while len(switches_adj[s_B]) == k_r:
				s_B = random.randrange(N_r)+1

			if(s_A in switches_adj[s_B]) or (s_B in switches_adj[s_A]) or (s_A == s_B):
				repeated += 1
				if(repeated > thresh):
					break
				continue

			switches_adj[s_A].append(s_B) 
			switches_adj[s_B].append(s_A) 
			cables += 2
	
			#print "A new edge selected: (" + str(s_A) + "," + str(s_B) + ")"
	
			[max_free_ports,s] = get_max_free_ports(switches_adj,k_r)
			#print ">>> Max free ports: " + str(max_free_ports) + " at switch " + str(s)
	
			sw = get_single_free_ports(switches_adj,k_r)
			#print ">>> Switches with single free ports: " + str(sw)

			if(max_free_ports <= 1):
				completed = True
				finished = True

	cables /= 2

	verify_correctness(switches_adj, N_r, k_r)

	dims = get_decomposition(g)

	C_r = N_r*rt(k)

	avg_local = 1
	N_l_c = 0
	N_g_c = 0
	C_l_c = 0
	C_g_c = 0

	for router in range(1, N_r+1):
		for neigh in switches_adj[router]:
			if(switches_gr[router] == switches_gr[neigh]):
				N_l_c += 1
				C_g_c += el(1)
			else:
				N_g_c += 1
				dist = get_manh_dist(switches_gr[router], switches_gr[neigh], dims)
				C_g_c += op(2 + dist)

	N_l_c /= 2
	N_g_c /= 2
	C_l_c /= 2
	C_g_c /= 2

	assert(cables == (N_l_c + N_g_c))

	'''

	C_r = N_r*rt(k)

	N_c = (N_r * k_r)/2
	C_c = N_c * el(1)

	final_cost = C_r + C_c
	final_power = N*nic_power() + N_r*router_power(k)

	if((N >= N_1 and N <= N_2) or (k >= k_1 and k <= k_2)):
		print(">>>>>>>>>>>> DLN (N = %d, k = %d)" % (N, k))
		print("\tN: %d, N_r: %d, k: %d, k': %d, p: %d, N_c: %d" % (N, N_r, k, k_r, p, N_c))
		print("\tC-per_endpoint: %d, P-per_endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))

	return [final_cost,final_power,N_r,N]



def dln_cost(k,N,g, N_1, N_2, k_1, k_2):
	k = int(k)
	N = int(N)
	N_origin = N

	g = int(g)
	p = int((k+1)/4.0) #similar to DF
	k_r = k - p

	N_r = int(math.ceil(N/(1.0*p)))
	a = int(math.ceil(N_r/(1.0*g)))

	assert(a*g + N_r % g == N_r)

	switches_adj = {}
	switches_gr = {}
	gr_nr = 0

	cables = 0

	for s in range(1,N_r+1):
		switches_gr[s] = gr_nr
		if(s % a == 0):
			gr_nr += 1

		switches_adj[s] = list()
		switches_adj[s].append((s % N_r) + 1)
		cables += 1
		if(s > 1):
			switches_adj[s].append(((s-1) % N_r))
			cables += 1
		else:
			switches_adj[s].append(N_r)
			cables += 1
		
	assert(gr_nr == g)

	completed = False
	while not completed:
		s_A = random.randrange(N_r)+1
		while len(switches_adj[s_A]) == k_r:
			s_A = random.randrange(N_r)+1
	
		s_B = random.randrange(N_r)+1
		while len(switches_adj[s_B]) == k_r:
			s_B = random.randrange(N_r)+1

		if(s_A in switches_adj[s_B]) or (s_B in switches_adj[s_A]) or (s_A == s_B):
			continue

		switches_adj[s_A].append(s_B) 
		switches_adj[s_B].append(s_A) 
		cables += 2

		#print "A new edge selected: (" + str(s_A) + "," + str(s_B) + ")"

		[max_free_ports,s] = get_max_free_ports(switches_adj,k_r)
		#print ">>> Max free ports: " + str(max_free_ports) + " at switch " + str(s)

		sw = get_single_free_ports(switches_adj,k_r)
		#print ">>> Switches with single free ports: " + str(sw)

		if(max_free_ports <= 1):
			completed = True

	cables /= 2

	verify_correctness(switches_adj, N_r, k_r)

	dims = get_decomposition(g)

	C_r = N_r*rt(k)

	avg_local = 1
	N_l_c = 0
	N_g_c = 0
	C_el = 0
	C_op = 0

	for router in range(1, N_r+1):
		for neigh in switches_adj[router]:
			if(switches_gr[router] == switches_gr[neigh]):
				N_l_c += 1
				C_el += el(1)
			else:
				N_g_c += 1
				dist = get_manh_dist(switches_gr[router], switches_gr[neigh], dims)
				C_op += op(2 + dist)

	N_l_c /= 2
	N_g_c /= 2
	C_el /= 2
	C_op /= 2

	assert(cables == (N_l_c + N_g_c))

	final_cost = C_r + C_el + C_op
	final_power = N*nic_power() + N_r*router_power(k)

	N_el = N_l_c
	N_op = N_g_c
	
	if((N >= N_1 and N <= N_2) or (k >= k_1 and k <= k_2)):
		print(">>>>>>>>>>>> DLN (N = %d, k = %d)" % (N, k))
		print("\tN: %d, N_r: %d, k: %d, k': %d, p: %d" % (N, N_r, k, k_r, p))
		print("\tN_el: %d, N_op: %d, N_l_c: %d, N_g_c: %d" % (N_el, N_op, N_l_c, N_g_c))
		print("\tC-per_endpoint: %d, P-per_endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))

	return [final_cost,final_power,N_r,N]

