from cost_model import *
import math
import sys

def ft3_cost_radix_single_rack_simple(k,N_1,N_2, k_1, k_2):
	k = int(k)

	N_r = (5*k*k)/4.0
	N = k*k*k/4.0

	C_r = N_r*rt(k)

	final_cost = 0

	pods = k	
	N_in_pod = N / k
	k_r = k / 2.0
	p = k / 2.0

	assert(k % 2 == 0)

	N_c_c = k*k*k/2.0
	C_c_c = N_c_c * el(1)

	final_cost = C_r + C_c_c
	final_power = N*nic_power() + N_r*router_power(k)

	if((N >= N_1 and N <= N_2) and (k >= k_1 and k <= k_2)):
		print(">>>>>>>>>>>> FT-3 (N = %d, k = %d)" % (N,k))
		print("\tN: %d, N_r: %d, k: %d, k': %d, p: %d, N_c: %d" % (N, N_r, k, k_r, p, N_c_c))
		print("\tpods %d" % (pods))
		print("\tC-per_endpoint: %d, P-per_endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))

	return [final_cost,final_power,N_r,N]


def ft3_cost_radix(k,N_1,N_2, k_1, k_2):
	k = int(k)

	N_r = (5*k*k)/4.0
	N = k*k*k/4.0

	C_r = N_r*rt(k)

	final_cost = 0

	C_el = 0
	C_op = 0
	N_l_c = 0
	N_g_c = 0

	pods = k	
	N_in_pod = N / k
	k_r = k / 2.0
	p = k / 2.0

	assert(k % 2 == 0)

	dims = get_decomposition(pods)

	x = dims[0]
	y = dims[1]
	z = dims[2]

	if(y % 2 == 0):
		for i in range(0,y/2):
			length = i*2
			if(length < 6):
				C_el += x * 2*N_in_pod * el(2 + length)
				N_l_c += x * 2*N_in_pod
			else:
				C_op += x * 2*N_in_pod * op(2 + length)
				N_g_c += x * 2*N_in_pod
		length = (y/2)*2
		C_op += z * N_in_pod * op(2 + length)
		N_g_c += z * N_in_pod
	else:
		for i in range(0,int(y/2)):
			length = i*2
			if(length < 6):
				C_el += x * 2*N_in_pod * el(2 + length)
				N_l_c += x * 2*N_in_pod
			else:
				C_op += x * 2*N_in_pod * op(2 + length)
				N_g_c += x * 2*N_in_pod
		length = (y/2)*2
		C_op += x * 1*N_in_pod * el(2 + length)
		N_g_c += x * 1*N_in_pod
		C_op += z * N_in_pod * el(2 + length)
		N_g_c += z * N_in_pod

	assert(int(N_g_c + N_l_c) == int(k*k*k/4.0))

	N_c_c = k*k*k/2.0
	C_op += N_c_c * op(x/2)

	N_el = N_l_c
	N_op = N_g_c + N_c_c

	final_cost = C_r + C_el + C_op
	final_power = N*nic_power() + N_r*router_power(k)

	if((N >= N_1 and N <= N_2) and (k >= k_1 and k <= k_2)):
		print(">>>>>>>>>>>> FT-3 (N = %d, k = %d)" % (N,k))
		print("\tN: %d, N_r: %d, k: %d, k': %d, p: %d" % (N, N_r, k, k_r, p))
		print("\tN_el: %d, N_op: %d, N_l_c: %d, N_g_c: %d" % (N_el, N_op, N_l_c, N_g_c))
		print("\tpods %d" % (pods))
		print("\tC-per_endpoint: %d, P-per_endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))

	return [final_cost,final_power,N_r,N]


