from cost_model import *
import math
import sys

def lower_power_of_two(r):
	n = 1
	dim = 0
	while(n <= r):
		n *= 2
		dim += 1
	n /= 2
	dim -= 1
	return [n,dim]



def lh_hc_cost_single_rack(N,a):
	N = int(N)
	N_origin = N

	a = 256
	p = 1 #maybe change it?

	E_i = 0
	E_o = 0

	N_l_c = 0
	N_g_c = 0

	[max_hypercube,max_dim] = lower_power_of_two(N)

	if(N == 250):
		max_hypercube = max_hypercube*2
		max_dim += 1

	N_r = max_hypercube
	N = max_hypercube
	N_r_level = N_origin

	k = max_dim + p

	L = -1

	if(max_dim >= 3 and max_dim <= 4):
		L = 3
	elif(max_dim >= 5 and max_dim <= 11):
		L = 4
	elif(max_dim >= 12 and max_dim <= 26):
		L = 5
	else:
		L = 6

	assert(L >= 3)
	k += L

	k_r = max_dim + L

	#get the cost of routers
	E_r = N_r*rt(k)

	if 1==1:
	# this I use when adding "small" parts of the LH-HC
	#while(max_hypercube > 1):
		N_r_rest = N_r_level - max_hypercube	#correct assuming p=1

		group_size = max_hypercube
		nr_groups = 1
		group_dim = max_dim
		while(group_size > a):
			group_size /= 2
			nr_groups *= 2
			group_dim -= 1

		_N_l_c = nr_groups * ((group_size / 2) * group_dim + group_size * L / 2.0)
		E_i += _N_l_c * el(1)
		N_l_c += _N_l_c

		optical_length = 1

		max_length = -1

		if(isinstance(math.sqrt(nr_groups),int)):
			max_length = math.floor(math.sqrt(nr_groups))
		else:
			max_length = math.floor(math.sqrt(nr_groups/2)*2)

		while(optical_length < max_length):
			_N_g_c = max_hypercube / 2 #TODO
			#N_g_c = (max_hypercube / 2)*max_dim - N_l_c
			#####################E_o += _N_g_c * op(optical_length + 2)
			E_o += _N_g_c * el(1)
			N_g_c += _N_g_c
			optical_length *= 2

		N_r_level = N_r_rest
		[max_hypercube,max_dim] = lower_power_of_two(N_r_level)

	N_el = N_l_c+N_g_c
	N_op = 0#N_g_c
	E_l = E_i
	E_g = E_o

	final_cost = E_r+E_i+E_o
	final_power = N*nic_power() + N_r*router_power(k)

	if(N >= 60 and N <= 2000):
		print(">>>>>>>>>>>> LH-HC")
		print("\tN: %d, N_r: %d, k: %d, k': %d, p: %d" % (N, N_r, k, k_r, p))
		print("\tN_el: %d, N_op: %d, N_l: %d, N_g: %d" % (N_el, N_op, N_l_c, N_g_c))
		print("\tN_r_rest: %d" % (N_r_rest))
		print("\tC-per_endpoint: %d, P-per_endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))
		print("\tC_r: %d, C_el: %d, C_o: %d, C_c: %d" % (int(E_r), int(E_l), int(E_g), int(final_cost)))

	#print(">>>> LH-HC: N_r: %d, N_l_c: %d, k: %d, p: %d" % (N_r, N_l_c, k, p))
	#print("\t E_r: %d, E_i: %d, E_o: %d,\t\tE_c: %d, E-per_endpoint: %d, P-per_endpoint: %f" % (int(E_r), int(N_l_c), int(N_g_c), int(final_cost),int(final_cost/(1.0*N)), float(final_power/(1.0*N))))


	return [final_cost,final_power,N_r,N]





def lh_hc_cost(N,N_1,N_2):
	N = int(N)
	N_origin = N

	a = 256
	p = 1 #maybe change it?

	C_el = 0
	C_op = 0

	N_l_c = 0
	N_g_c = 0

	[max_hypercube,max_dim] = lower_power_of_two(N)
	N_r = max_hypercube
	N = max_hypercube
	N_r_level = N_origin

	k = max_dim + p

	L = -1
	if(max_dim >= 3 and max_dim <= 4):
		L = 3
	elif(max_dim >= 5 and max_dim <= 11):
		L = 4
	elif(max_dim >= 12 and max_dim <= 26):
		L = 5
	else:
		L = 6

	assert(L >= 3)
	k += L

	k_r = max_dim + L

	#get the cost of routers
	C_r = N_r*rt(k)

	N_r_rest = N_r_level - max_hypercube	#correct assuming p=1

	group_size = max_hypercube
	nr_groups = 1
	group_dim = max_dim

	while(group_size > a):
		group_size /= 2
		nr_groups *= 2
		group_dim -= 1

	_N_l_c = nr_groups * ((group_size / 2) * group_dim + group_size * L / 2.0)
	C_el += _N_l_c * el(1)
	N_l_c += _N_l_c

	optical_length = 1
	max_length = -1

	if(isinstance(math.sqrt(nr_groups),int)):
		max_length = math.floor(math.sqrt(nr_groups))
	else:
		max_length = math.floor(math.sqrt(nr_groups/2)*2)

	while(optical_length < max_length):
		_N_g_c = max_hypercube / 2 #TODO
		C_op += _N_g_c * op(optical_length + 2)
		N_g_c += _N_g_c
		optical_length *= 2

	N_r_level = N_r_rest
	[max_hypercube,max_dim] = lower_power_of_two(N_r_level)

	N_el = N_l_c
	N_op = N_g_c

	final_cost = C_r + C_el + C_op
	final_power = N*nic_power() + N_r*router_power(k)

	if(N >= N_1 and N <= N_2):
		print(">>>>>>>>>>>> LH-HC (N = %d, k = %d)" % (N,k))
		print("\tN: %d, N_r: %d, k: %d, k': %d, p: %d" % (N, N_r, k, k_r, p))
		print("\tN_el: %d, N_op: %d, N_l_c: %d, N_g_c: %d" % (N_el, N_op, N_l_c, N_g_c))
		print("\tC-per_endpoint: %d, P-per_endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))

	return [final_cost,final_power,N_r,N]

