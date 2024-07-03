from cost_model import *
import math
import sys

def sf(q,delta):
	N_r = 2*q*q
	k_r = (3*q - delta)/2.0
	p = int(math.floor(k_r/2.0)+1)
	#p = int(math.ceil(k_r/2.0)+1)
	k = p+k_r
	N = p*N_r
	return [k_r,p,k,N_r,N]







########## HOTI ANALYSIS IN San Francisco
########## WITH ENDPOINT cables

def get_nr_switches_in_rack___TOR(p):
	nr = math.floor( nr_elems_in_rack() / ( 1.0*(1 + p) ) )
	assert(nr >= 1)
	return nr

def get_nr_servers_in_rack___TOR(p, N_sw_in_rack):
	nr = N_sw_in_rack * p
	assert (nr >= 1)
	return nr

def get_nr_racks_in_sf_gr___TOR(a, p, N_sw_in_rack, N_sv_in_rack):
	N_racks_in_gr = math.ceil( (1.0*a) / N_sw_in_rack )
	assert(N_racks_in_gr == math.ceil( (1.0*a*p) / N_sv_in_rack) )
	assert(N_racks_in_gr == math.ceil( (1.0*a*p + a) / (N_sv_in_rack + N_sw_in_rack) ) )
	return N_racks_in_gr

def get_gr_el_cables_in_sf___TOR(N_racks_in_gr, a, g, N, dims_gr, N_r, k_r_l_gr):
	avg_el_gr_sw_c_len = max(dims_gr[0]*x_rack_dim_length(), dims_gr[1]*y_rack_dim_length()) / 2.0
	
	max_cab_len = math.sqrt(x_rack_dim_length() * x_rack_dim_length() * dims_gr[0] * dims_gr[0] + y_rack_dim_length() * y_rack_dim_length() * dims_gr[1] * dims_gr[1])

	N_gr_el_c_sw = N_r * k_r_l_gr / 2.0
	C_gr_el_c_sw = N_gr_el_c_sw * el(avg_el_gr_sw_c_len)
	
	avg_el_gr_sv_c_len = 1
	N_gr_el_c_sv = N
	C_gr_el_c_sv = N_gr_el_c_sv * el(avg_el_gr_sv_c_len)
	
	return [N_gr_el_c_sw,C_gr_el_c_sw, N_gr_el_c_sv,C_gr_el_c_sv, max_cab_len]



def get_nr_switches_in_rack___C_ROW(p):
	nr = nr_elems_in_rack() 
	assert(nr >= 1)
	return nr

def get_nr_servers_in_rack___C_ROW(p, N_sw_in_rack):
	nr = nr_elems_in_rack() 
	assert (nr >= 1)
	return nr

def get_nr_racks_in_sf_gr_sw___C_ROW(a, p, N_sw_in_rack, N_sv_in_rack):
	N_racks_in_gr = math.ceil( (1.0*a) / get_nr_switches_in_rack___C_ROW(p) )
	return N_racks_in_gr

#def get_nr_racks_in_sf_gr_sv___C_ROW(a, p, N_sw_in_rack, N_sv_in_rack):
#	N_racks_in_gr = math.ceil( (1.0*a*p) / get_nr_servers_in_rack___C_ROW(p, N_sw_in_rack) )
#	return N_racks_in_gr

def get_gr_el_cables_in_sf___C_ROW(N_racks_in_gr, a, g, N, dims_gr, N_r, k_r_l_gr):
	avg_el_gr_sw_c_len = max(dims_gr[0] * x_rack_dim_length(), dims_gr[1]*y_rack_dim_length()) / 2.0
	
	max_cab_len = math.sqrt(x_rack_dim_length() * x_rack_dim_length() * dims_gr[0] * dims_gr[0] + y_rack_dim_length()*y_rack_dim_length()*dims_gr[1]*dims_gr[1])

	N_gr_el_c_sw = N_r * k_r_l_gr / 2.0
	C_gr_el_c_sw = N_gr_el_c_sw * el(avg_el_gr_sw_c_len)
	
	return [N_gr_el_c_sw,C_gr_el_c_sw, max_cab_len]




def get_group_dims_sf(g):
	dimensions = [0,0]
	edge = int(math.floor(math.sqrt(g)))
	rest = g - edge*edge
	dimensions[0] = edge
	dimensions[1] = edge

	if(rest < edge):
		dimensions[1] += 1
	elif(rest == edge):
		dimensions[1] += 1
	elif(rest > edge):
		new_rows = math.floor( (1.0 * rest) / edge )
		if(rest % edge != 0):
			new_rows += 1
		dimensions[1] += new_rows
		assert(new_rows <= 2)

	return dimensions


def ___get_group_dims_sf(N_racks):
	print N_racks
	if(N_racks == 1):
		d = [1,1]
	elif(N_racks == 2):
		d = [1,2]
	elif(N_racks == 3):
		d = [1,3]
	elif(N_racks == 4):
		d = [2,2]
	elif(N_racks == 5):
		d = [2,3]
	elif(N_racks == 6):
		d = [2,3]
	elif(N_racks == 7):
		d = [2,4]
	elif(N_racks == 8):
		d = [2,4]
	elif(N_racks == 9):
		d = [3,3]
	elif(N_racks == 10):
		d = [2,5]
	elif(N_racks == 11):
		d = [3,4]
	elif(N_racks == 12):
		d = [3,4]
	elif(N_racks == 13):
		d = [3,5]
	elif(N_racks == 14):
		d = [3,5]
	elif(N_racks == 15):
		d = [3,5]
	elif(N_racks == 16):
		d = [4,4]
	elif(N_racks == 17):
		d = [3,6]
	elif(N_racks == 18):
		d = [3,6]
	elif(N_racks == 19):
		d = [4,5]
	elif(N_racks == 20):
		d = [4,5]
	elif(N_racks == 21):
		d = [3,7]
	elif(N_racks == 22):
		d = [4,6]
	elif(N_racks == 23):
		d = [4,6]
	elif(N_racks == 24):
		d = [4,6]
	elif(N_racks == 25):
		d = [5,5]
	elif(N_racks == 26):
		d = [4,7]
	elif(N_racks == 27):
		d = [4,7]
	elif(N_racks == 28):
		d = [4,7]
	elif(N_racks == 29):
		d = [5,6]
	elif(N_racks == 30):
		d = [5,6]
	elif(N_racks == 31):
		d = [4,8]
	elif(N_racks == 32):
		d = [4,8]
	elif(N_racks == 33):
		d = [5,7]
	elif(N_racks == 34):
		d = [5,7]
	elif(N_racks == 35):
		d = [5,7]
	elif(N_racks == 36):
		d = [6,6]
	elif(N_racks == 37):
		d = [5,8]
	elif(N_racks == 38):
		d = [5,8]
	else:
		assert False

	return d



def sf_group_2q_cost___HOTI_SF_tor_switches(k,N,q,delta, N_1, N_2, k_1, k_2):
	k = int(k)
	N = int(N)

	if((N < N_1 or N > N_2) or (k < k_1 or k > k_2)):
		return [-1, -1, -1]

	[k_r,p,k,N_r,N] = sf(q,delta)

	a = 2*q
	g = int(N_r / (1.0*a))

	assert(q == g)

	_N_c_theory = (N_r * k_r) / 2;
	k_r_l_sub = (q - delta)/2
	k_r_g_sub = q
	assert(k_r == (k_r_g_sub + k_r_l_sub))
	
	####### First, derive and verify the subgroup numbers
	N_l_c_sub = (N_r * k_r_l_sub) / 2
	N_g_c_sub = (N_r * k_r_g_sub) / 2
	assert(_N_c_theory == (N_g_c_sub + N_l_c_sub))

	####### Verify the group decomposition
	k_r_l_gr = k_r_l_sub + 1
	k_r_g_gr = k_r_g_sub - 1
	N_l_c_gr = (N_r * k_r_l_gr) / 2
	N_g_c_gr = (N_r * k_r_g_gr) / 2
	assert(_N_c_theory == (N_g_c_gr + N_l_c_gr))
	assert(N_l_c_gr == ( N_l_c_sub + q*q ))
	assert(N_g_c_gr == ( N_g_c_sub - q*q ))
	assert(N_g_c_gr == ( (q * (q - 1) / 2) * (2*(q)) ))
	assert(N_g_c_gr == ( (g * (g - 1) / 2) * (2*(q)) ))

	##get the cost of local cables
	#N_l_c = _N_c_theory - N_g_c
	#C_el = N_l_c*el(1)

	N_l_c_2 = ( (((q-delta)/2)*N_r)/2 + q*q )
	assert((N_l_c_gr + N_g_c_gr) == _N_c_theory)
	assert(N_l_c_gr == N_l_c_2)

	#get the cost of routers
	C_r = N_r*rt(k)

	#get the number of switches in a rack
	N_sw_in_rack = get_nr_switches_in_rack___TOR(p)

	#get the number of servers in a rack
	N_sv_in_rack = get_nr_servers_in_rack___TOR(p, N_sw_in_rack)

	#get the number of racks in a SF group
	N_racks_in_gr = get_nr_racks_in_sf_gr___TOR(a, p, N_sw_in_rack, N_sv_in_rack)
	
	#get the size of one SF group (in meters) and thus the distance to be used in a global cable cost computations
	SF_gr_dims = get_group_dims_sf(N_racks_in_gr)

	#get the cost of electric cables inside groups 
	[N_gr_el_c_sw,C_gr_el_c_sw, N_gr_el_c_sv,C_gr_el_c_sv, max_cab_len] = get_gr_el_cables_in_sf___TOR(N_racks_in_gr, a, g, N, SF_gr_dims, N_r, k_r_l_gr)

	#get the total cost of electric cables in SF groups
	N_gr_el_c = N_gr_el_c_sw + N_gr_el_c_sv
	C_gr_el_c = C_gr_el_c_sw + C_gr_el_c_sv

	#get the cost of global cables
	dims = get_decomposition(g)
	#[C_op,N_g_c] = get_global_cables_cost_sf_a_2q(dims,q)
	[C_g_op_c,N_g_op_c] = get_global_cables_cost_df___dims_of_df_gr___optical(dims,2*q,SF_gr_dims)
	assert(N_g_c_gr == N_g_op_c)

	fdr = [ dims[0] * SF_gr_dims[0], dims[1] * SF_gr_dims[1], dims[2] * SF_gr_dims[0] ]
	fdm = [ dims[0] * SF_gr_dims[0] * x_rack_dim_length(), dims[1] * SF_gr_dims[1] * y_rack_dim_length(), dims[2] * SF_gr_dims[0] ]

	final_cost = C_r + C_gr_el_c + C_g_op_c
	final_power = N*nic_power() + N_r*router_power(k)

	#assert(N_g_op_c == ( (N_r*h)/2 ))
	assert(N_g_op_c == ( (N_r*k_r)/2 - N_gr_el_c_sw) )
	assert((N_gr_el_c_sw + N_g_op_c) == ((N_r*k_r)/2))

	if((N >= N_1 and N <= N_2) and (k >= k_1 and k <= k_2)):
		print(">>>>>>>>>>>> SF (fixed p, fully balanced, standard: TOR, switches and serves together)")
		print("\t*** N: %d, N_r: %d, k: %d, k': %d, p: %d" % (N, N_r, k, k_r, p))
		print("\ta: %d, g: %d" % (a, g))
		print("\tcables: in groups (electric): %d (to switches: %d, to servers: %d), global optic: %d" % (N_gr_el_c, N_gr_el_c_sw, N_gr_el_c_sv, N_g_op_c))
		print("\tswitches in one rack (group): %d, servers in one rack (group): %d, racks in one group: %d" % (N_sw_in_rack, N_sv_in_rack, N_racks_in_gr))
		print("\tgroup dims (racks): [%d,%d], group physical dims (meters): [%f,%f]" % (SF_gr_dims[0], SF_gr_dims[1], SF_gr_dims[0] * x_rack_dim_length(), SF_gr_dims[1]*y_rack_dim_length()))
		print("\tmax_cab_len in a SF group: %f" % (max_cab_len))
		print("\tFinal DC dims (racks): [%d,%d,%d], final DC physical dims (meters): [%f,%f,%f]" % (fdr[0],fdr[1],fdr[2], fdm[0], fdm[1], fdm[2]))
		print("\tTotal: cost: %f, cost of routers: %f, cost of electric cables: %f, cost of optic cables: %f" % (final_cost, C_r, C_gr_el_c, C_g_op_c))
		print("\tCost per endpoint: %f, Power per endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))
		print 

	return [final_cost,final_power,N_r]






def sf_group_2q_cost___HOTI_SF_central_row_switches(k,N,q,delta, N_1, N_2, k_1, k_2):
	k = int(k)
	N = int(N)

	if((N < N_1 or N > N_2) or (k < k_1 or k > k_2)):
		return [-1, -1, -1]

	[k_r,p,k,N_r,N] = sf(q,delta)

	a = 2*q
	g = int(N_r / (1.0*a))

	assert(q == g)

	_N_c_theory = (N_r * k_r) / 2;
	k_r_l_sub = (q - delta)/2
	k_r_g_sub = q
	assert(k_r == (k_r_g_sub + k_r_l_sub))
	
	####### First, derive and verify the subgroup numbers
	N_l_c_sub = (N_r * k_r_l_sub) / 2
	N_g_c_sub = (N_r * k_r_g_sub) / 2
	assert(_N_c_theory == (N_g_c_sub + N_l_c_sub))

	####### Verify the group decomposition
	k_r_l_gr = k_r_l_sub + 1
	k_r_g_gr = k_r_g_sub - 1
	N_l_c_gr = (N_r * k_r_l_gr) / 2
	N_g_c_gr = (N_r * k_r_g_gr) / 2
	assert(_N_c_theory == (N_g_c_gr + N_l_c_gr))
	assert(N_l_c_gr == ( N_l_c_sub + q*q ))
	assert(N_g_c_gr == ( N_g_c_sub - q*q ))
	assert(N_g_c_gr == ( (q * (q - 1) / 2) * (2*(q)) ))
	assert(N_g_c_gr == ( (g * (g - 1) / 2) * (2*(q)) ))

	##get the cost of local cables
	#N_l_c = _N_c_theory - N_g_c
	#C_el = N_l_c*el(1)

	N_l_c_2 = ( (((q-delta)/2)*N_r)/2 + q*q )
	assert((N_l_c_gr + N_g_c_gr) == _N_c_theory)
	assert(N_l_c_gr == N_l_c_2)

	#get the cost of routers
	C_r = N_r*rt(k)

	#get the number of switches in a rack
	N_sw_in_rack = get_nr_switches_in_rack___C_ROW(p)

	#get the number of servers in a rack
	N_sv_in_rack = get_nr_servers_in_rack___C_ROW(p, N_sw_in_rack)

	#get the number of racks in a SF group
	N_racks_in_gr = get_nr_racks_in_sf_gr_sw___C_ROW(a, p, N_sw_in_rack, N_sv_in_rack)
	
	#get the size of one SF group (in meters) and thus the distance to be used in a global cable cost computations
	SF_gr_dims = get_group_dims_sf(N_racks_in_gr)

	#get the cost of electric cables inside groups 
	[N_gr_el_c_sw,C_gr_el_c_sw, max_cab_len] = get_gr_el_cables_in_sf___C_ROW(N_racks_in_gr, a, g, N, SF_gr_dims, N_r, k_r_l_gr)

	#get the cost of global cables
	dims = get_decomposition(g)

	# !!!!!!!!!!! hack
	dims = [1,g,0]
	[C_g_op_c_sw,N_g_op_c_sw] = get_global_cables_cost_df___dims_of_df_gr___optical(dims,2*q,SF_gr_dims)

	N_racks_in_row = g * SF_gr_dims[1]

	# now, finally, cables for servers...
	N_full_racks_for_servers = math.floor( (1.0*N) / nr_elems_in_rack() )

	N_partial_racks_for_servers = 0
	N_servers_in_last_rack = N % nr_elems_in_rack()

	if(N % nr_elems_in_rack() != 0):
		N_partial_racks_for_servers = 1
		N_servers_in_last_rack = N % nr_elems_in_rack()

	N_full_rows_of_servers = math.floor( (1.0*N_full_racks_for_servers) / N_racks_in_row )
	N_full_racks_in_last_row = (N_full_racks_for_servers) % N_racks_in_row 
	N_servers_in_full_row = N_racks_in_row * nr_elems_in_rack()
	N_servers_in_last_row = N_full_racks_in_last_row * nr_elems_in_rack()

	N_el_c_sv = 0
	C_el_c_sv = 0

	N_op_c_sv = 0
	C_op_c_sv = 0

	if(N_full_rows_of_servers % 2 == 0):
		for i in range(0,int(N_full_rows_of_servers/2)):
			length = i + 1
			if(length < max_el_cable_len):
				C_el_c_sv += 2 * N_servers_in_full_row * el(2 + length)
				N_el_c_sv += 2 * N_servers_in_full_row
			else:
				C_op_c_sv += 2 * N_servers_in_full_row * op(2 + length)
				N_op_c_sv += 2 * N_servers_in_full_row

		length = (N_full_rows_of_servers/2) + 1
		C_op_c_sv += N_servers_in_last_row * op(2 + length)
		N_op_c_sv += N_servers_in_last_row 

	else:
		for i in range(0,int(N_full_rows_of_servers/2)):
			length = i + 1
			if(length < max_el_cable_len):
				C_el_c_sv += 2 * N_servers_in_full_row * el(2 + length)
				N_el_c_sv += 2 * N_servers_in_full_row
			else:
				C_op_c_sv += 2 * N_servers_in_full_row * op(2 + length)
				N_op_c_sv += 2 * N_servers_in_full_row

		length = (N_full_rows_of_servers/2) + 1
		C_op_c_sv += N_servers_in_full_row * op(2 + length)
		N_op_c_sv += N_servers_in_full_row

		length = (N_full_rows_of_servers/2) + 2 
		C_op_c_sv += N_servers_in_last_row * op(2 + length)
		N_op_c_sv += N_servers_in_last_row 

	length = (N_full_rows_of_servers/2) + 2 
	C_op_c_sv += N_servers_in_last_rack * op(2 + length)
	N_op_c_sv += N_servers_in_last_rack

	assert(int(N_el_c_sv + N_op_c_sv) == N)

	final_cost = C_r + C_gr_el_c_sw + C_g_op_c_sw + C_el_c_sv + C_op_c_sv
	final_power = N*nic_power() + N_r*router_power(k)

	sw_fdr = [ dims[0] * SF_gr_dims[0], dims[1] * SF_gr_dims[1], dims[2] * SF_gr_dims[0] ]
	sw_fdm = [ dims[0] * SF_gr_dims[0] * x_rack_dim_length(), dims[1] * SF_gr_dims[1] * y_rack_dim_length(), dims[2] * SF_gr_dims[0] ]

	sv_fdr = [ N_full_rows_of_servers, N_racks_in_row, N_full_racks_in_last_row ]
	sv_fdm = [ N_full_rows_of_servers * x_rack_dim_length(), N_racks_in_row * y_rack_dim_length(), N_full_racks_in_last_row * x_rack_dim_length() ]

	N_g_op_c = N_g_op_c_sw

	assert(N_g_op_c == ( (N_r*k_r)/2 - N_gr_el_c_sw) )
	assert((N_gr_el_c_sw + N_g_op_c) == ((N_r*k_r)/2))

	if((N >= N_1 and N <= N_2) and (k >= k_1 and k <= k_2)):
		print(">>>>>>>>>>>> SF (fixed p, fully balanced, standard: CENTRAL ROW, switches and serves separately)")
		print("\t*** N: %d, N_r: %d, k: %d, k': %d, p: %d" % (N, N_r, k, k_r, p))
		print("\ta: %d, g: %d" % (a, g))
		print("\tcables: in groups (electric): %d (to switches: %d), optic (between switches in groups): %d, electric (to servers): %d, optic (to servers): %d" 
			% (N_gr_el_c_sw, N_gr_el_c_sw, N_g_op_c_sw, N_el_c_sv, N_op_c_sv))
		print("\tswitches in one rack (group): %d, servers in one rack (group): %d, racks in one group: %d" % (N_sw_in_rack, N_sv_in_rack, N_racks_in_gr))
		print("\tgroup dims (switches in racks): [%d,%d], group physical dims (meters): [%f,%f]" % (SF_gr_dims[0], SF_gr_dims[1], SF_gr_dims[0] * x_rack_dim_length(), SF_gr_dims[1]*y_rack_dim_length()))
		print("\tmax_cab_len in a SF group: %f" % (max_cab_len))
		print("\tCentral row dims (racks): [%d,%d], central row physical dims (meters): [%f,%f]" % (sw_fdr[0],sw_fdr[1], sw_fdm[0], sw_fdm[1]))
		print("\tServers dims (racks): [%d,%d], servers physical dims (meters): [%f,%f]" % (sv_fdr[0],sv_fdr[1], sv_fdm[0], sv_fdm[1]))
		# print("\tFinal DC dims (racks): [%d,%d,%d], final DC physical dims (meters): [%f,%f,%f]" % (fdr[0],fdr[1],fdr[2], fdm[0], fdm[1], fdm[2]))
		print("\tTotal: cost: %f, cost of routers: %f, cost of electric cables: %f, cost of optic cables: %f" % (final_cost, C_r, C_gr_el_c_sw + C_el_c_sv, C_g_op_c_sw + C_op_c_sv))
		print("\tCost per endpoint: %f, Power per endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))
		print 

	return [final_cost,final_power,N_r]













def sf_a_2q_cost_single_rack_simple(k,N,q,delta, N_1, N_2, k_1, k_2):
	k = int(k)
	N = int(N)

	[k_r,p,k,N_r,N] = sf(q,delta)

	a = 2*q
	g = int(N_r / (1.0*a))

	_N_e_theory = (N_r * k_r) / 2;
	
	#get the cost of routers
	C_r = N_r*rt(k)

	N_g_c = (q*N_r / 2) - q*q
	assert(N_g_c == ( (q*(q-1)/2) * (2*q) ))

	N_l_c = _N_e_theory - N_g_c
	assert((N_l_c+N_g_c) == _N_e_theory)

	N_c = N_g_c + N_l_c
	C_c = N_c * el(1)

	final_cost = C_r + C_c
	final_power = N*nic_power() + N_r*router_power(k)

	if((N >= N_1 and N <= N_2) and (k >= k_1 and k <= k_2)):
		print(">>>>>>>>>>>> SF (N = %d, k = %d)" % (N,k))
		print("\tN: %d, N_r: %d, k: %d, k': %d, p: %d, N_c: %d" % (N, N_r, k, k_r, p, N_c))
		print("\tC-per_endpoint: %d, P-per_endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))

	return [final_cost,final_power,N_r]


def sf_a_2q_cost(k,N,q,delta, N_1, N_2, k_1, k_2):
	k = int(k)
	N = int(N)

	[k_r,p,k,N_r,N] = sf(q,delta)

	a = 2*q
	g = int(N_r / (1.0*a))

	assert(q == g)

	_N_e_theory = (N_r * k_r) / 2;
	k_r_l_sub = (q - delta)/2
	k_r_g_sub = q
	assert(k_r == (k_r_g_sub + k_r_l_sub))
	
	#get the cost of routers
	C_r = N_r*rt(k)

	####### First, derive and verify the subgroup numbers
	N_l_c_sub = (N_r * k_r_l_sub) / 2
	N_g_c_sub = (N_r * k_r_g_sub) / 2
	assert(_N_e_theory == (N_g_c_sub + N_l_c_sub))

	####### Verify the group decomposition
	#_N_g_c_gr = (q * (q - 1) / 2) * (2*(q - 1))
	#_N_l_c_gr = ( (((q - delta) / 2)*N_r)/2 + q*q )
	k_r_l_gr = k_r_l_sub + 1
	k_r_g_gr = k_r_g_sub - 1
	N_l_c_gr = (N_r * k_r_l_gr) / 2
	N_g_c_gr = (N_r * k_r_g_gr) / 2
	assert(_N_e_theory == (N_g_c_gr + N_l_c_gr))
	assert(N_l_c_gr == ( N_l_c_sub + q*q ))
	assert(N_g_c_gr == ( N_g_c_sub - q*q ))
	# print "-----"
	# print q
	# print N_g_c_gr / (q*(q-1)/2)
	assert(N_g_c_gr == ( (q * (q - 1) / 2) * (2*(q)) ))

	#get the cost of global cables
	dims = get_decomposition(g)
	[C_op,N_g_c] = get_global_cables_cost_sf_a_2q(dims,q)

	# assert(N_g_c == ( (q*N_r / 2) - q*q ))
	# assert(N_g_c == ( (q*(q-1)/2) * (2*q) ))
	assert(N_g_c == N_g_c_gr)

	#get the cost of local cables
	N_l_c = _N_e_theory - N_g_c
	C_el = N_l_c*el(1)

	N_l_c_2 = ( (((q-delta)/2)*N_r)/2 + q*q )
	
	#N_l_c_2 = (((q - delta)/2)*N_r)/2 

	assert((N_l_c + N_g_c) == _N_e_theory)
	#print N_l_c
	#print N_l_c_2
	assert(N_l_c == N_l_c_2)
	# assert(N_l_c == ( (((q-delta)/2)*N_r)/2 + q*q ))

	final_cost = C_r + C_el + C_op
	final_power = N*nic_power() + N_r*router_power(k)

	N_el = N_l_c
	N_op = N_g_c

	if((N >= N_1 and N <= N_2) and (k >= k_1 and k <= k_2)):
		print(">>>>>>>>>>>> SF (N = %d, k = %d)" % (N,k))
		print("\tN: %d, N_r: %d, k: %d, k': %d, p: %d" % (N, N_r, k, k_r, p))
		print("\tN_el: %d, N_op: %d, N_l_c: %d, N_g_c: %d" % (N_el, N_op, N_l_c, N_g_c))
		print("\ta: %d, g: %d" % (a, g))
		print("\tC-per_endpoint: %d, P-per_endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))

	return [final_cost,final_power,N_r]

def sf_a_2q_cost_CENTRAL(k,N,q,delta, N_1, N_2, k_1, k_2):
	k = int(k)
	N = int(N)

	[k_r,p,k,N_r,N] = sf(q,delta)

	a = 2*q
	g = int(N_r / (1.0*a))

	_N_e_theory = (N_r * k_r) / 2;
	
	#get the cost of routers
	C_r = N_r*rt(k)

	#get the cost of global cables
	dims = get_decomposition(g)
	[C_op,N_g_c] = get_global_cables_cost_sf_a_2q(dims,q)

	assert(N_g_c == ( (q*N_r / 2) - q*q ))
	assert(N_g_c == ( (q*(q-1)/2) * (2*q) ))

	#get the cost of local cables
	N_l_c = _N_e_theory - N_g_c
	C_el = N_l_c*el(1)

	assert(N_l_c == ( (((q-delta)/2)*N_r)/2 + q*q ))
	assert((N_l_c+N_g_c) == _N_e_theory)

	final_cost = C_r + C_el + C_op
	final_power = N*nic_power() + N_r*router_power(k)

	N_el = N_l_c
	N_op = N_g_c

	if((N >= N_1 and N <= N_2) and (k >= k_1 and k <= k_2)):
		print(">>>>>>>>>>>> SF (N = %d, k = %d)" % (N,k))
		print("\tN: %d, N_r: %d, k: %d, k': %d, p: %d" % (N, N_r, k, k_r, p))
		print("\tN_el: %d, N_op: %d, N_l_c: %d, N_g_c: %d" % (N_el, N_op, N_l_c, N_g_c))
		print("\ta: %d, g: %d" % (a, g))
		print("\tC-per_endpoint: %d, P-per_endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))

	return [final_cost,final_power,N_r]







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

