from cost_model import *
import math
import sys

def get_global_cables_cost_fbf3_old(dims, bunch):
	X = dims[0]
	Y = dims[1]
	Z = dims[2]
	cost = 0
	N_g_c = 0
	for i in range(0,X):
		for j in range(0,Y):
			for m in range(0,X):
			 	dist = manh_dist(i,j,m,j)
				c_el = el(dist+2)
				c_op = op(dist+2)
				cost += min(c_el, c_op)*bunch
				N_g_c += bunch
			for n in range(0,Y):
				dist = manh_dist(i,j,i,n)
				c_el = el(dist+2)
				c_op = op(dist+2)
				cost += min(c_el, c_op)*bunch
				N_g_c += bunch

	cost /= 2
	N_g_c /= 2

	for u in range(0,Z):
		for n in range(0,Y):
			dist = manh_dist(u,n,u,-1)
			c_el = el(dist+2)
			c_op = op(dist+2)
			cost += min(c_el, c_op)*bunch
			N_g_c += bunch

	remainder_cost = 0
	remainder_cables = 0
	for i in range(0,Z):
		for j in range(0,Z):
			dist = manh_dist(i,0,j,0)
			c_el = el(dist+2)
			c_op = op(dist+2)

			remainder_cost += min(c_el,c_op)*bunch
			remainder_cables += bunch

	remainder_cost /= 2
	remainder_cables /= 2
	cost += remainder_cost
	N_g_c += remainder_cables

	return [cost,N_g_c]

def get_global_cables_cost_fbf3(dims, bunch):
	X = dims[0]
	Y = dims[1]
	Z = dims[2]
	cost = 0
	N_g_c = 0
	for i in range(0,X):
		for j in range(0,Y):
			for m in range(0,X):
			 	dist = manh_dist(i,j,m,j)
				c_op = op(dist+2)
				cost += c_op*bunch
				N_g_c += bunch
			for n in range(0,Y):
				dist = manh_dist(i,j,i,n)
				c_op = op(dist+2)
				cost += c_op*bunch
				N_g_c += bunch

	cost /= 2
	N_g_c /= 2

	for u in range(0,Z):
		for n in range(0,Y):
			dist = manh_dist(u,n,u,-1)
			c_op = op(dist+2)
			cost += c_op*bunch
			N_g_c += bunch

	remainder_cost = 0
	remainder_cables = 0
	for i in range(0,Z):
		for j in range(0,Z):
			dist = manh_dist(i,0,j,0)
			c_op = op(dist+2)

			remainder_cost += c_op*bunch
			remainder_cables += bunch

	remainder_cost /= 2
	remainder_cables /= 2
	cost += remainder_cost
	N_g_c += remainder_cables

	return [cost,N_g_c]

def fbf3_cost_kary(kary): #k - radix
	n = 4
	kary = int(kary)

	k = n*(kary-1) + 1
	N = kary**n
	p = kary

	N_r = int(math.ceil(N / kary))
	g = int(math.ceil(N_r / kary))
	assert(N % kary == 0 and N_r % kary == 0)

	k_r = k - p
	bunch = kary

	#get the cost of routers
	E_r = N_r*rt(k)

	#get the cost of electric cables inside groups
	N_l_c = g*(p*(p-1)/2)
	E_i = N_l_c * el(1)

	#get the cost of global cables
	dims = get_decomposition(g)

	[E_o,N_g_c] = get_global_cables_cost_fbf3(dims,bunch)

	final_cost = E_r+E_i+E_o
	final_power = N*nic_power() + N_r*router_power(k)

	N_el = N_l_c
	N_op = N_g_c
	E_l = E_i
	E_g = E_o

	if((N >= 8000 and N <= 12000) or (k >= 41 and k <= 46)):
		print(">>>>>>>>>>>> FBF-3 (fixed_radix)")
		print("\tN: %d, N_r: %d, k: %d, k': %d, p: %d" % (N, N_r, k, k_r, p))
		print("\tN_el: %d, N_op: %d, N_l: %d, N_g: %d" % (N_el, N_op, N_l_c, N_g_c))
		print("\tg: %d, kary: %d, n: %d, bunch: %d" % (g, kary, n, bunch))
		print("\tC-per_endpoint: %d, P-per_endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))
		print("\tC_r: %d, C_el: %d, C_o: %d, C_c: %d" % (int(E_r), int(E_l), int(E_g), int(final_cost)))
	
	#print("\t E_r: %d, E_i: %d, E_o: %d,\t\tE_c: %d" % (int(E_r), int(E_i), int(E_o), int(final_cost)))
	#print("\t E_r: %d, E_i: %d, E_o: %d,\t\tE_c: %d, E-per_endpoint: %d, P-per_endpoint: %f" % (int(E_r), int(N_l_c), int(N_g_c), int(final_cost),int(final_cost/(1.0*N)), float(final_power/(1.0*N))))

	#final_power = N_r*k*4*0.7

	return [final_cost,final_power,N_r,N]





def fbf3_cost_radix_relaxed_single_rack(k): #k - radix
	n = 4
	k = int(k)

	#kary = int(math.floor( (k-1)/(n*1.0) + 1 ))
	kary = int(math.floor( (k-1)/(n*1.0) + 1 ))
	p = kary

	if((k-1) % n != 0):
		if(k % n == 0):
			#print 'p'
			k = k+1
			p = p+1
		elif((k+1) % n == 0):
			#print 'pp'
			k = k+2
			p = p+2
		elif((k-2) % n == 0):
			#print 'm'
			k = k-1
			p = p-1
		else:
			print 'radix error'
			return [-1,-1,-1,-1]
	
	#kary = (k-1)/n + 1
	
	N = p**n
	#k_new = n*(kary-1) + 1

	'''

	if(k_new != k):
		print("k_new: %d, k: %d" % (k_new, k))
		return [-1,-1,-1,-1]
		#assert(k_new == k)

	'''

	N_r = int(math.ceil(N / p))
	g = int(math.ceil(N_r / p))
	assert(N % p == 0)

	k_r = k - p
	bunch = p

	#get the cost of routers
	E_r = N_r*rt(k)

	#get the cost of electric cables inside groups
	N_l_c = g*(p*(p-1)/2)
	E_i = N_l_c * el(1)

	#get the cost of global cables
	dims = get_decomposition(g)

	[E_o,N_g_c] = get_global_cables_cost_fbf3(dims,bunch)

	E_o = N_g_c*el(1) # hack, we just oversubscribe the above

	final_cost = E_r+E_i+E_o
	final_power = N*nic_power() + N_r*router_power(k)

	N_el = N_l_c+N_g_c
	N_op = 0#N_g_c
	E_l = E_i
	E_g = E_o

	if((N >= 60 and N <= 2000)):# or (k >= 41 and k <= 46)):
		print(">>>>>>>>>>>> FBF-3 (fixed_radix)")
		print("\tN: %d, N_r: %d, k: %d, k': %d, p: %d" % (N, N_r, k, k_r, p))
		print("\tN_el: %d, N_op: %d, N_l: %d, N_g: %d" % (N_el, N_op, N_l_c, N_g_c))
		print("\tg: %d, kary: %d, n: %d, bunch: %d" % (g, kary, n, bunch))
		print("\tC-per_endpoint: %d, P-per_endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))
		print("\tC_r: %d, C_el: %d, C_o: %d, C_c: %d" % (int(E_r), int(E_l), int(E_g), int(final_cost)))
	
	#print("\t E_r: %d, E_i: %d, E_o: %d,\t\tE_c: %d" % (int(E_r), int(E_i), int(E_o), int(final_cost)))
	#print("\t E_r: %d, E_i: %d, E_o: %d,\t\tE_c: %d, E-per_endpoint: %d, P-per_endpoint: %f" % (int(E_r), int(N_l_c), int(N_g_c), int(final_cost),int(final_cost/(1.0*N)), float(final_power/(1.0*N))))

	#final_power = N_r*k*4*0.7

	return [final_cost,final_power,N_r,N]







def fbf3_cost_radix_relaxed(k): #k - radix
	n = 4
	k = int(k)

	#kary = int(math.floor( (k-1)/(n*1.0) + 1 ))
	kary = int(math.floor( (k-1)/(n*1.0) + 1 ))
	p = kary

	if((k-1) % n != 0):
		if(k % n == 0):
			k = k+1
			p = p+1
		elif((k+1) % n == 0):
			k = k+2
			p = p+2
		elif((k-2) % n == 0):
			k = k-1
			p = p-1
		else:
			print 'radix error'
			return [-1,-1,-1,-1]
	
	#kary = (k-1)/n + 1
	
	N = p**n
	#k_new = n*(kary-1) + 1

	'''

	if(k_new != k):
		print("k_new: %d, k: %d" % (k_new, k))
		return [-1,-1,-1,-1]
		#assert(k_new == k)

	'''

	N_r = int(math.ceil(N / p))
	g = int(math.ceil(N_r / p))
	assert(N % p == 0)

	k_r = k - p
	bunch = p

	#get the cost of routers
	E_r = N_r*rt(k)

	#get the cost of electric cables inside groups
	N_l_c = g*(p*(p-1)/2)
	E_i = N_l_c * el(1)

	#get the cost of global cables
	dims = get_decomposition(g)

	[E_o,N_g_c] = get_global_cables_cost_fbf3(dims,bunch)

	final_cost = E_r+E_i+E_o
	final_power = N*nic_power() + N_r*router_power(k)

	N_el = N_l_c
	N_op = N_g_c
	E_l = E_i
	E_g = E_o

	if((N >= 8000 and N <= 12000) or (k >= 41 and k <= 46)):
		print(">>>>>>>>>>>> FBF-3 (fixed_radix)")
		print("\tN: %d, N_r: %d, k: %d, k': %d, p: %d" % (N, N_r, k, k_r, p))
		print("\tN_el: %d, N_op: %d, N_l: %d, N_g: %d" % (N_el, N_op, N_l_c, N_g_c))
		print("\tg: %d, kary: %d, n: %d, bunch: %d" % (g, kary, n, bunch))
		print("\tC-per_endpoint: %d, P-per_endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))
		print("\tC_r: %d, C_el: %d, C_o: %d, C_c: %d" % (int(E_r), int(E_l), int(E_g), int(final_cost)))
	
	#print("\t E_r: %d, E_i: %d, E_o: %d,\t\tE_c: %d" % (int(E_r), int(E_i), int(E_o), int(final_cost)))
	#print("\t E_r: %d, E_i: %d, E_o: %d,\t\tE_c: %d, E-per_endpoint: %d, P-per_endpoint: %f" % (int(E_r), int(N_l_c), int(N_g_c), int(final_cost),int(final_cost/(1.0*N)), float(final_power/(1.0*N))))

	#final_power = N_r*k*4*0.7

	return [final_cost,final_power,N_r,N]





def fbf3_cost_radix(k): #k - radix
	n = 4
	k = int(k)

	#kary = int(math.floor( (k-1)/(n*1.0) + 1 ))
	kary = int(math.floor( (k-1)/(n*1.0) + 1 ))

	if((k-1) % n != 0):
		if(k % n == 0):
			k = k+1
		elif((k+1) % n == 0):
			k = k+2
		elif((k-2) % n == 0):
			k = k-1
		else:
			print 'radix error'
			return [-1,-1,-1,-1]
	
	kary = (k-1)/n + 1
	
	N = kary**n
	p = kary
	k_new = n*(kary-1) + 1

	if(k_new != k):
		print("k_new: %d, k: %d" % (k_new, k))
		return [-1,-1,-1,-1]
		#assert(k_new == k)

	N_r = int(math.ceil(N / kary))
	g = int(math.ceil(N_r / kary))
	assert(N % kary == 0)

	k_r = k - p
	bunch = kary

	#get the cost of routers
	E_r = N_r*rt(k)

	#get the cost of electric cables inside groups
	N_l_c = g*(p*(p-1)/2)
	E_i = N_l_c * el(1)

	#get the cost of global cables
	dims = get_decomposition(g)

	[E_o,N_g_c] = get_global_cables_cost_fbf3(dims,bunch)

	final_cost = E_r+E_i+E_o
	final_power = N*nic_power() + N_r*router_power(k)

	N_el = N_l_c
	N_op = N_g_c
	E_l = E_i
	E_g = E_o

	if((N >= 8000 and N <= 12000) or (k >= 41 and k <= 46)):
		print(">>>>>>>>>>>> FBF-3 (fixed_radix)")
		print("\tN: %d, N_r: %d, k: %d, k': %d, p: %d" % (N, N_r, k, k_r, p))
		print("\tN_el: %d, N_op: %d, N_l: %d, N_g: %d" % (N_el, N_op, N_l_c, N_g_c))
		print("\tg: %d, kary: %d, n: %d, bunch: %d" % (g, kary, n, bunch))
		print("\tC-per_endpoint: %d, P-per_endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))
		print("\tC_r: %d, C_el: %d, C_o: %d, C_c: %d" % (int(E_r), int(E_l), int(E_g), int(final_cost)))
	
	#print("\t E_r: %d, E_i: %d, E_o: %d,\t\tE_c: %d" % (int(E_r), int(E_i), int(E_o), int(final_cost)))
	#print("\t E_r: %d, E_i: %d, E_o: %d,\t\tE_c: %d, E-per_endpoint: %d, P-per_endpoint: %f" % (int(E_r), int(N_l_c), int(N_g_c), int(final_cost),int(final_cost/(1.0*N)), float(final_power/(1.0*N))))

	#final_power = N_r*k*4*0.7

	return [final_cost,final_power,N_r,N]






def fbf3_cost_old_single_rack(k,N): #k - radix
	n = 4
	k = int(k)
	N = int(N)

	kary = int(math.floor((k+3)/n))
	p = kary+0#hack for 10000 network  TODO: fix...
	kary -= 0

	#if((k+3) % n != 0 and (k+4) % n != 0 and (k+5) % n != 0):
	#	print 'Error! radix does not compatible with n\n'
	#	return

	#if(N % kary != 0):
	#	print 'Error! N does not fit with kary\n'
	#	return		

	N_r = int(math.ceil(N / kary))

	#if(N_r % kary != 0):
	#	print 'Error! N_r does not fit with kary\n'
	#	return		

	g = int(math.ceil(N_r / kary))

	router_ports = k - p
	#if(router_ports % 3 != 0):
	#	print 'Error! router_ports does not fit with 3\n'
	#	return

	bunch = kary

	print(">>>> FBF3: %d routers, %d groups; group size: %d, endpoints (computed): %d, k (computed): %d" % (N_r, g, kary, p*N_r, 4*kary-3))

	#get the cost of routers

	E_r = N_r*rt(k)

	#get the cost of electric cables inside groups

	E_i = g * (p*(p-1)/2) * el(1)
	N_l_c = g*(p*(p-1)/2)

	#get the cost of global cables

	dims = get_decomposition(g)
	#print 'Decomposing ' + str(g) + ' groups. Dimensions: X: ' + str(dims[0]) + ', Y: ' + str(dims[1]) + ', Z: ' + str(dims[2]) + '\n'

	[E_o,N_g_c] = get_global_cables_cost_fbf3(dims,bunch)

	E_o = N_g_c*el(1)

	final_cost = E_r+E_i+E_o
	final_power = N*nic_power() + N_r*k*4*0.7

	print("\t E_r: %d, E_i: %d, E_o: %d,\t\tE_c: %d" % (int(E_r), int(E_i), int(E_o), int(final_cost)))
	print("\t E_r: %d, E_i: %d, E_o: %d,\t\tE_c: %d, E-per_endpoint: %d, P-per_endpoint: %f" % (int(E_r), int(N_l_c), int(N_g_c), int(final_cost),int(final_cost/(1.0*N)), float(final_power/(1.0*N))))

	#final_power = N_r*k*4*0.7

	return [final_cost,final_power,N_r,N]









def fbf3_cost_old(k,N): #k - radix
	n = 4
	k = int(k)
	N = int(N)

	kary = int(math.floor((k+3)/n))
	p = kary+0#hack for 10000 network
	kary -= 0

	#if((k+3) % n != 0 and (k+4) % n != 0 and (k+5) % n != 0):
	#	print 'Error! radix does not compatible with n\n'
	#	return

	#if(N % kary != 0):
	#	print 'Error! N does not fit with kary\n'
	#	return		

	N_r = int(math.ceil(N / kary))

	#if(N_r % kary != 0):
	#	print 'Error! N_r does not fit with kary\n'
	#	return		

	g = int(math.ceil(N_r / kary))

	router_ports = k - p
	#if(router_ports % 3 != 0):
	#	print 'Error! router_ports does not fit with 3\n'
	#	return

	bunch = kary

	print(">>>> FBF3: %d routers, %d groups; group size: %d, endpoints (computed): %d, k (computed): %d" % (N_r, g, kary, p*N_r, 4*kary-3))

	#get the cost of routers

	E_r = N_r*rt(k)

	#get the cost of electric cables inside groups

	E_i = g * (p*(p-1)/2) * el(1)
	N_l_c = g*(p*(p-1)/2)

	#get the cost of global cables

	dims = get_decomposition(g)
	#print 'Decomposing ' + str(g) + ' groups. Dimensions: X: ' + str(dims[0]) + ', Y: ' + str(dims[1]) + ', Z: ' + str(dims[2]) + '\n'

	[E_o,N_g_c] = get_global_cables_cost_fbf3(dims,bunch)

	final_cost = E_r+E_i+E_o
	final_power = N*nic_power() + N_r*k*4*0.7

	print("\t E_r: %d, E_i: %d, E_o: %d,\t\tE_c: %d" % (int(E_r), int(E_i), int(E_o), int(final_cost)))
	print("\t E_r: %d, E_i: %d, E_o: %d,\t\tE_c: %d, E-per_endpoint: %d, P-per_endpoint: %f" % (int(E_r), int(N_l_c), int(N_g_c), int(final_cost),int(final_cost/(1.0*N)), float(final_power/(1.0*N))))

	#final_power = N_r*k*4*0.7

	return [final_cost,final_power,N_r,N]

if(len(sys.argv) > 1):
	k = int(sys.argv[1])
	N = int(sys.argv[2])
	cost = fbf3_cost(k,N)
	print 'FBF3 cost (k = ' + str(k) + ', N = ' + str(N) + ') is: ' + str(int(cost)) + ' $\n'

	
	
	
