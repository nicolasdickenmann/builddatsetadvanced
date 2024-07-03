from cost_model import *
import math
import sys

def t3d_cost_single_rack_simple(N, N_1, N_2):
	N = int(N)
	N_origin = N
	p = 1

	e = int(math.floor(math.pow(N,1/3.0)))

	N_rest = N - e*e*e
	nr_of_add_2d_layers = int(math.floor(N_rest/(1.0*e*e)))
	N_2d_rest = N_rest - nr_of_add_2d_layers * e*e
	assert(N_2d_rest >= 0 and N_2d_rest < e*e)

	dimX = e
	dimY = e
	dimZ = e + nr_of_add_2d_layers
	N = dimX * dimY * dimZ 

	assert(N_origin == N + N_2d_rest)
	assert(N_origin == e*e*e + nr_of_add_2d_layers*e*e + N_2d_rest)

	N_r = N
	k = p + 3*2
	k_r = k - p

	#get the cost of routers
	C_r = N_r*rt(k)

	N_c = (N_r*k_r)/2
	C_c = N_c * el(1)

	final_cost = C_r + C_c
	final_power = N*nic_power() + N_r*router_power(k)

	if(N >= N_1 and N <= N_2):
		print(">>>>>>>>>>>> T3D (N = %d, k = %d)" % (N, k))
		print("\tN: %d, N_r: %d, k: %d, k': %d, p: %d, N_c: %d" % (N, N_r, k, k_r, p, N_c))
		print("\tdimX: %d, dimY: %d, dimZ: %d" % (dimX, dimY, dimZ))
		print("\tC-per_endpoint: %d, P-per_endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))

	return [final_cost,final_power,N_r,N]


def t3d_cost(N, N_1, N_2):
	N = int(N)
	N_origin = N
	p = 1

	e = int(math.floor(math.pow(N,1/3.0)))

	N_rest = N - e*e*e
	nr_of_add_2d_layers = int(math.floor(N_rest/(1.0*e*e)))
	N_2d_rest = N_rest - nr_of_add_2d_layers * e*e
	assert(N_2d_rest >= 0 and N_2d_rest < e*e)

	dimX = e
	dimY = e
	dimZ = e + nr_of_add_2d_layers
	N = dimX * dimY * dimZ 

	assert(N_origin == N + N_2d_rest)
	assert(N_origin == e*e*e + nr_of_add_2d_layers*e*e + N_2d_rest)

	N_r = N
	k = p + 3*2
	k_r = k - p

	#get the cost of routers
	C_r = N_r*rt(k)

	#get the number of short cables
	N_l_c = 0
	N_l_c += 3*(e-1)*e*e
	N_l_c += nr_of_add_2d_layers*(e*e + (e-1)*e + e*(e-1)) 

	#get the cost of short cables
	C_l_c = N_l_c * el(1)

	#get the number of global (also electric, we assume folding)
	N_g_c = 3 * (e-1)*(e+nr_of_add_2d_layers) + e*e  
	C_g_c = N_g_c * el(1 + 2)  

	N_el = N_l_c + N_g_c
	N_op = 0

	#### !!! fix assert(N_el == ((N*k_r)/2))

	final_cost = C_r + C_l_c + C_g_c
	final_power = N*nic_power() + N_r*router_power(k)

	if(N >= N_1 and N <= N_2):
		print(">>>>>>>>>>>> T3D (N = %d, k = %d)" % (N, k))
		print("\tN: %d, N_r: %d, k: %d, k': %d, p: %d" % (N, N_r, k, k_r, p))
		print("\tN_el: %d, N_op: %d, N_l_c: %d, N_g_c: %d" % (N_el, N_op, N_l_c, N_g_c))
		print("\tdimX: %d, dimY: %d, dimZ: %d" % (dimX, dimY, dimZ))
		print("\tC-per_endpoint: %d, P-per_endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))

	return [final_cost,final_power,N_r,N]

