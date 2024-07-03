import math


### rack model 1:

def _nr_elems_in_rack():
	return math.ceil(0.9 * 42)

### rack model 2:

def _nr_elems_in_rack():
	return math.ceil(0.9 * 84)

### rack model 3:

def nr_elems_in_rack():
	return math.ceil(0.9 * 42)

##################

def max_el_cable_len():
	return 2

def x_rack_dim_length():
	return 1.0

def y_rack_dim_length():
	return 0.5

def nic_power():
	return 0

def router_power(k):
	return k*4*0.7

def el(x):
	#our prev
	#result = 120*(0.1409*x + 0.3643)

	#mellanox fdr10/qdr 40Gb, up to 5 meters
	#result = 40*(0.273*x + 1.041)

	#mellanox fdr10/qdr 40Gb, from 2 up to 7 meters
	#OUR STANDARD DEFAULT
	#result = 40*(0.4079*x + 0.5771)

	#mellanox qdr 56Gb
	result = 56*(0.2042*x + 1.2341)

	#elpheus eth10Gb
	#result = 10*(0.8568*x + 2.4791)

	#FBF-model:
	#result = 120*(1.4*x + 2.16)
	return result

def op(x):
	#our
	#result = 120*(0.05429*x + 2.202)
	
	#mellanox fdr10 40Gb
	#OUR STANDARD DEFAULT
	#result = 40*(0.0919*x + 7.2745)
	
	#mellanox qdr 56Gb
	result = 56*(0.1031*x + 6.0464)
	
	#---transceiver:
	#Mellanox VPI FDR QSFP Optical Module - Part ID: MC2207411-SR4L
	#Mellanox optical module, VPI, up to 56Gb/s, QSFP, MPO, 850nm, up to 30m
	result = result + 2*195

	#elpheus eth10Gb
	#result = 10*(0.1768*x + 10.4211)

	#FBF-model
	#result = 120*(0.364*x + 9.7103)
	return result

def rt(k):
	#result = 150.7*k + 928.8
	#result = -959 + 349*k

	#used stuff
	#result = -323 + 340*k

	#fdr-10/qdr
	#result = 350.4*k -892.3

	#Ethernet Mellanox
	result = 225*k + 3353.7

	#result = 1052 + 232*k

	#Mellanox Ethernet 40Gb !!!
	result = 207.80*k + 3531.94
	return result

def manh_dist(i,j,m,n):
	return abs(i - m) + abs(j - n)

def manh_dist___dims_gr(i,j,m,n, dims_gr):
	assert(dims_gr[1] >= dims_gr[0])
	return abs(i - m)*dims_gr[0]*x_rack_dim_length() + abs(j - n)*dims_gr[1]*y_rack_dim_length()

def get_manh_dist(g1, g2, dims):
	X = dims[0]
	Y = dims[1]
	Z = dims[2]

	dist = -1
	dist_X = -1
	dist_Y = -1

	dist_X = abs((g1 % X) - (g2 % X))
	dist_Y = abs((int(g1) / int(X)) - (int(g2) / int(X)))
	
	dist = dist_X + dist_Y
	assert(dist_X >= 0)
	assert(dist_X < X)
	assert(dist_Y >= 0)

	if(Z == 0):
		assert(dist_Y < Y)
	else:
		assert(dist_Y < Y+1)
	
	return dist

def get_group_dims(N_racks):
	if N_racks == 1:
		return [1,1]
	elif N_racks == 2:
		return []

def get_decomposition(g):
	dimensions = [0,0,0] #[x,y,z]
	edge = int(math.floor(math.sqrt(g)))
	rest = g - edge*edge
	dimensions[0] = edge
	dimensions[1] = edge

	if(rest < edge):
		dimensions[2] = rest
	elif(rest == edge):
		dimensions[0] += 1
	elif(rest > edge):
		dimensions[0] += 1
		dimensions[2] = rest - edge

	return dimensions


def get_global_cables_cost_df(dims, bunch):
	nr = 0
	X = dims[0]
	Y = dims[1]
	Z = dims[2]
	cost = 0
	for i in range(0,X):
		for j in range(0,Y):
			for m in range(0,X):
				for n in range(0,Y):
					if((i == m) and (j == n)):
						continue

					dist = manh_dist(i,j,m,n)
					c_el = el(dist+2)
					c_op = op(dist+2)

					nr += bunch
					cost += min(c_el, c_op)*bunch

	cost /= 2
	nr /= 2

	XY = X*Y
	G = XY+Z
	assert(nr == (XY*(XY-1)/2))

	for u in range(0,Z):
		for m in range(0,X):
			for n in range(0,Y):
				dist = manh_dist(m,n,u,-1)
				c_el = el(dist+2)
				c_op = op(dist+2)

				nr += bunch

				cost += min(c_el, c_op)*bunch

	remainder_nr = 0
	remainder_cost = 0
	for i in range(0,Z):
		for j in range(0,Z):
			if(i == j):
				continue

			dist = manh_dist(i,0,j,0)
			c_el = el(dist+2)
			c_op = op(dist+2)

			remainder_nr += bunch

			remainder_cost += min(c_el,c_op)*bunch

	remainder_nr /= 2
	remainder_cost /= 2
	cost += remainder_cost
	nr += remainder_nr

	assert(nr == (G*(G-1)/2))

	return [cost,nr]



def get_global_cables_cost_df___dims_of_df_gr___optical(dims, bunch, dims_gr):
	nr = 0
	X = dims[0]
	Y = dims[1]
	Z = dims[2]
	cost = 0
	for i in range(0,X):
		for j in range(0,Y):
			for m in range(0,X):
				for n in range(0,Y):
					if((i == m) and (j == n)):
						continue

					dist = manh_dist___dims_gr(i,j,m,n,dims_gr)
					c_op = op(dist + 2)

					nr += bunch
					cost += c_op * bunch

	cost /= 2
	nr /= 2

	XY = X*Y
	G = XY+Z
	assert(nr == bunch*(XY*(XY-1)/2))

	for u in range(0,Z):
		for m in range(0,X):
			for n in range(0,Y):
				dist = manh_dist___dims_gr(m,n,u,-1, dims_gr)
				c_op = op(dist+2)

				nr += bunch
				cost += c_op*bunch

	remainder_nr = 0
	remainder_cost = 0
	for i in range(0,Z):
		for j in range(0,Z):
			if(i == j):
				continue

			dist = manh_dist___dims_gr(i,0,j,0,dims_gr)
			c_op = op(dist+2)

			remainder_nr += bunch

			remainder_cost += c_op*bunch

	remainder_nr /= 2
	remainder_cost /= 2
	cost += remainder_cost
	nr += remainder_nr

	assert(nr == bunch*(G*(G-1)/2))

	return [cost,nr]







def get_global_cables_cost_sf_a_2q(dims, q):
	nr = 0
	bunch = 2*q
	X = dims[0]
	Y = dims[1]
	Z = dims[2]
	cost = 0
	for i in range(0,X):
		for j in range(0,Y):
			for m in range(0,X):
				for n in range(0,Y):
					if((i == m) and (j == n)):
						continue

					dist = manh_dist(i,j,m,n)
					c_el = el(dist+2)
					c_op = op(dist+2)

					nr += bunch

					cost += min(c_el, c_op)*bunch

	nr /= 2
	cost /= 2

	for u in range(0,Z):
		for m in range(0,X):
			for n in range(0,Y):
				dist = manh_dist(m,n,u,-1)
				c_el = el(dist+2)
				c_op = op(dist+2)

				nr += bunch

				cost += min(c_el, c_op)*bunch

	remainder_nr = 0
	remainder_cost = 0
	for i in range(0,Z):
		for j in range(0,Z):
			if(i == j):
				continue

			dist = manh_dist(i,0,j,0)
			c_el = el(dist+2)
			c_op = op(dist+2)

			remainder_nr += bunch

			remainder_cost += min(c_el,c_op)*bunch

	remainder_nr /= 2
	remainder_cost /= 2
	cost += remainder_cost
	nr += remainder_nr

	return [cost,nr]




def get_global_cables_cost_pf(dims, q):
	nr = 0
	bunch = q-2
	X = dims[0]
	Y = dims[1]
	Z = dims[2]
	cost = 0
	for i in range(0,X):
		for j in range(0,Y):
			for m in range(0,X):
				for n in range(0,Y):
					if((i == m) and (j == n)):
						continue

					dist = manh_dist(i,j,m,n)
					c_el = el(dist+2)
					c_op = op(dist+2)

					nr += bunch

					cost += min(c_el, c_op)*bunch

	nr /= 2
	cost /= 2

	for u in range(0,Z):
		for m in range(0,X):
			for n in range(0,Y):
				dist = manh_dist(m,n,u,-1)
				c_el = el(dist+2)
				c_op = op(dist+2)

				nr += bunch

				cost += min(c_el, c_op)*bunch

	remainder_nr = 0
	remainder_cost = 0
	for i in range(0,Z):
		for j in range(0,Z):
			if(i == j):
				continue

			dist = manh_dist(i,0,j,0)
			c_el = el(dist+2)
			c_op = op(dist+2)

			remainder_nr += bunch

			remainder_cost += min(c_el,c_op)*bunch

	remainder_nr /= 2
	remainder_cost /= 2
	cost += remainder_cost
	nr += remainder_nr

	return [cost,nr]







