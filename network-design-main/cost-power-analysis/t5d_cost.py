from cost_model import *
import math
import sys


def t5d_cost_balanced_single_rack(N):
	N = int(N)
	N_origin = N

	k_r = 2*5
	p = 1
	k = k_r + p

	e = int(math.floor(math.pow(N,1/5.0)))
	N_rest = N - e*e*e*e*e
	nr_of_add_4d_layers = int(math.floor(N_rest/(1.0*e*e*e*e)))
	N_4d_rest = N_rest - nr_of_add_4d_layers * e*e*e*e
	assert(N_4d_rest >= 0 and N_4d_rest < e*e*e*e)

	dims = e
	dim5 = e + nr_of_add_4d_layers

	N = dims * dims * dims * dims * dim5

	N_r = N

	#get the cost of routers
	E_r = N_r*rt(k)

	#get the number of short cables

	N_l_c = 0
	N_l_c += 5*(e-1)*e*e*e*e
	N_l_c += nr_of_add_4d_layers*(e*e*e*e + 4*(e-1)*e*e*e)
	
	#N_l_c = (e+nr_of_add_layers)*(e-1)*e*e*e + (e+nr_of_add_layers-1)*e*e*e*e + (e+nr_of_add_layers)*(e-1)*e*e*e //OLd version

	#get the cost of short cables
	E_l  = N_l_c * el(1)
	
	#get the number and cost of global cables
	
	N_g_c = 4 * (e-1)*e*e*(e+nr_of_add_4d_layers) + e*e*e*e
	E_g = N_g_c*el(1)

	#N_g_c = 3*(e*e) + (e+nr_of_add_4d_layers)*e + (e+nr_of_add_4d_layers)*e
	#E_o = 3*(e*e)*op(2 + e+nr_of_add_4d_layers) + (e+nr_of_add_4d_layers)*e*op(2+e) + (e+nr_of_add_4d_layers)*e*op(2+e)
	
	N_el = N_l_c+N_g_c
	N_op = 0

	final_cost = E_r+E_l+E_g
	final_power = N*nic_power() + N_r*router_power(k)

	if(N >= 60 and N <= 2000):	
		print(">>>>>>>>>>>> T5D")
		print("\tN: %d, N_r: %d, k: %d, k': %d, p: %d" % (N, N_r, k, k_r, p))
		print("\tN_el: %d, N_op: %d, N_l: %d, N_g: %d" % (N_el, N_op, N_l_c, N_g_c))
		print("\tdims: %d, dim5: %d" % (dims, dim5))
		print("\tN_rest: %d, nr_add_layers: %d, N_4d_rest: %d" % (N_rest, nr_of_add_4d_layers, N_4d_rest))
		print("\tC-per_endpoint: %d, P-per_endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))
		print("\tC_r: %d, C_el: %d, C_o: %d, C_c: %d" % (int(E_r), int(E_l+E_g), int(0), int(final_cost)))
	
	#print(">>>> T5D: N_r: %d, N_l_c: %d, N_g_c: %d, , N_el: %d, N_r_rest: %d, nr_add_layers: %d, endpoints (computed): %d, k: %d, p: %d" % (N_r, N_l_c, N_g_c, N_l_c+N_g_c,N_r_rest, nr_of_add_4d_layers, N_r*p, k_r+p, p))

	##print("\t E_r: %d, E_el: %d, E_o: %d,\t\tE_c: %d" % (int(E_r), int(E_l+E_g), int(0), int(final_cost)))
	#print("\t E_r: %d, E_el: %d, E_o: %d,\t\tE_c: %d, E-per_endpoint: %d, P-per_endpoint: %f" % (int(E_r), int(N_l_c+N_g_c), int(0), int(final_cost), int(final_cost/(1.0*N)), float(final_power/(1.0*N))))

	return [final_cost,final_power,N_r,N]






def t5d_cost_balanced(N):
	N = int(N)
	N_origin = N

	k_r = 2*5
	p = 1
	k = k_r + p

	e = int(math.floor(math.pow(N,1/5.0)))
	N_rest = N - e*e*e*e*e
	nr_of_add_4d_layers = int(math.floor(N_rest/(1.0*e*e*e*e)))
	N_4d_rest = N_rest - nr_of_add_4d_layers * e*e*e*e
	assert(N_4d_rest >= 0 and N_4d_rest < e*e*e*e)

	dims = e
	dim5 = e + nr_of_add_4d_layers

	N = dims * dims * dims * dims * dim5

	N_r = N

	#get the cost of routers
	E_r = N_r*rt(k)

	#get the number of short cables

	N_l_c = 0
	N_l_c += 5*(e-1)*e*e*e*e
	N_l_c += nr_of_add_4d_layers*(e*e*e*e + 4*(e-1)*e*e*e)
	
	#N_l_c = (e+nr_of_add_layers)*(e-1)*e*e*e + (e+nr_of_add_layers-1)*e*e*e*e + (e+nr_of_add_layers)*(e-1)*e*e*e //OLd version

	#get the cost of short cables
	E_l  = N_l_c * el(1)
	
	#get the number and cost of global cables
	
	N_g_c = 4 * (e-1)*e*e*(e+nr_of_add_4d_layers) + e*e*e*e
	E_g = N_g_c*el(3)

	#N_g_c = 3*(e*e) + (e+nr_of_add_4d_layers)*e + (e+nr_of_add_4d_layers)*e
	#E_o = 3*(e*e)*op(2 + e+nr_of_add_4d_layers) + (e+nr_of_add_4d_layers)*e*op(2+e) + (e+nr_of_add_4d_layers)*e*op(2+e)
	
	N_el = N_l_c+N_g_c
	N_op = 0

	final_cost = E_r+E_l+E_g
	final_power = N*nic_power() + N_r*router_power(k)

	if(N >= 8000 and N <= 12000):	
		print(">>>>>>>>>>>> T5D")
		print("\tN: %d, N_r: %d, k: %d, k': %d, p: %d" % (N, N_r, k, k_r, p))
		print("\tN_el: %d, N_op: %d, N_l: %d, N_g: %d" % (N_el, N_op, N_l_c, N_g_c))
		print("\tdims: %d, dim5: %d" % (dims, dim5))
		print("\tN_rest: %d, nr_add_layers: %d, N_4d_rest: %d" % (N_rest, nr_of_add_4d_layers, N_4d_rest))
		print("\tC-per_endpoint: %d, P-per_endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))
		print("\tC_r: %d, C_el: %d, C_o: %d, C_c: %d" % (int(E_r), int(E_l+E_g), int(0), int(final_cost)))
	
	#print(">>>> T5D: N_r: %d, N_l_c: %d, N_g_c: %d, , N_el: %d, N_r_rest: %d, nr_add_layers: %d, endpoints (computed): %d, k: %d, p: %d" % (N_r, N_l_c, N_g_c, N_l_c+N_g_c,N_r_rest, nr_of_add_4d_layers, N_r*p, k_r+p, p))

	##print("\t E_r: %d, E_el: %d, E_o: %d,\t\tE_c: %d" % (int(E_r), int(E_l+E_g), int(0), int(final_cost)))
	#print("\t E_r: %d, E_el: %d, E_o: %d,\t\tE_c: %d, E-per_endpoint: %d, P-per_endpoint: %f" % (int(E_r), int(N_l_c+N_g_c), int(0), int(final_cost), int(final_cost/(1.0*N)), float(final_power/(1.0*N))))

	return [final_cost,final_power,N_r,N]

def t5d_cost_single_rack_simple(N, N_1, N_2):
	N = int(N)
	N_origin = N

	k_r = 5*2
	p = 1
	k = k_r + p

	e = int(math.floor(math.pow(N,1/5.0)))
	N_rest = N - e*e*e*e*e
	nr_of_add_4d_layers = int(math.floor(N_rest/(1.0*e*e*e*e)))
	N_4d_rest = N_rest - nr_of_add_4d_layers * e*e*e*e
	assert(N_4d_rest >= 0 and N_4d_rest < e*e*e*e)

	dims = e
	dim5 = e + nr_of_add_4d_layers
	N = dims * dims * dims * dims * dim5
	N_r = N

	#get the cost of routers
	C_r = N_r*rt(k)

	N_c = (N_r * k_r)/2
	C_c = N_c * el(1)

	final_cost = C_r + C_c
	final_power = N*nic_power() + N_r*router_power(k)

	if(N >= N_1 and N <= N_2):	
		print(">>>>>>>>>>>> T5D (N = %d, k = %d)" % (N, k))
		print("\tN: %d, N_r: %d, k: %d, k': %d, p: %d, N_c: %d" % (N, N_r, k, k_r, p, N_c))
		print("\tdims: %d, dim5: %d" % (dims, dim5))
		print("\tC-per_endpoint: %d, P-per_endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))
	
	return [final_cost,final_power,N_r,N]


def t5d_cost(N, N_1, N_2):
	N = int(N)
	N_origin = N

	k_r = 5*2
	p = 1
	k = k_r + p

	e = int(math.floor(math.pow(N,1/5.0)))
	N_rest = N - e*e*e*e*e
	nr_of_add_4d_layers = int(math.floor(N_rest/(1.0*e*e*e*e)))
	N_4d_rest = N_rest - nr_of_add_4d_layers * e*e*e*e
	assert(N_4d_rest >= 0 and N_4d_rest < e*e*e*e)

	dims = e
	dim5 = e + nr_of_add_4d_layers
	N = dims * dims * dims * dims * dim5
	N_r = N

	#get the cost of routers
	C_r = N_r*rt(k)

	#get the number of short cables
	N_l_c = 0
	N_l_c += 5*(e-1)*e*e*e*e
	N_l_c += nr_of_add_4d_layers*(e*e*e*e + 5*(e-1)*e*e*e)
	
	#get the cost of short cables
	C_l_c  = N_l_c * el(1)
	
	#get the number and cost of global cables
	N_g_c = 5 * (e-1)*e*e*(e+nr_of_add_4d_layers) + e*e*e*e
	C_g_c = N_g_c * el(1 + 2)

	N_el = N_l_c + N_g_c
	N_op = 0

	assert(N_origin == N + N_4d_rest)
	print N_el, " ", ((N*k_r)/2)
	assert(N_el == ((N*k_r)/2))

	final_cost = C_r + C_l_c + C_g_c
	final_power = N*nic_power() + N_r*router_power(k)

	if(N >= N_1 and N <= N_2):	
		print(">>>>>>>>>>>> T5D (N = %d, k = %d)" % (N, k))
		print("\tN: %d, N_r: %d, k: %d, k': %d, p: %d" % (N, N_r, k, k_r, p))
		print("\tN_el: %d, N_op: %d, N_l_c: %d, N_g_c: %d" % (N_el, N_op, N_l_c, N_g_c))
		print("\tdims: %d, dim5: %d" % (dims, dim5))
		print("\tC-per_endpoint: %d, P-per_endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))
	
	return [final_cost,final_power,N_r,N]

