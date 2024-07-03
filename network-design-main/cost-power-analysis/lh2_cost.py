from cost_model import *
import math
import sys

def lh2_cost(k,N):
	N = int(N)

	p = int(0.5*math.sqrt(N))

	k_r = 2*p
	k = k_r + p

	N_r = int(math.ceil(N/(1.0*p)))
	
	E_r = N_r*rt(k)
	
	a = 2*p
	g = int(math.ceil(N/(1.0*a)))
	
	print(">>>> LH2: %d routers, %d groups; group size: %d, endpoints (computed): %d, p: %d, k: %d" % (N_r, g, a, p*N_r, p, k))
	
	#get the cost of routers
	
	E_r = N_r*rt(k)

	#get the cost of electric cables inside groups

	E_i = g * ( k_r * 0.5 * a )/2.0 * el(1)
	
	#get the cost of global cables
	
	dims = get_decomposition(g)
	#print 'Decomposing ' + str(g) + ' groups. Dimensions: X: ' + str(dims[0]) + ', Y: ' + str(dims[1]) + ', Z: ' + str(dims[2]) + '\n'
	
	E_o = ((k_r * 0.5 * N_r) / 2.0) * op(2 + dims[0]/2.0)

	final_cost = E_r+E_i+E_o

	print("\t E_r: %d, E_i: %d, E_o: %d,\t\tE_c: %d" % (int(E_r), int(E_i), int(E_o), int(final_cost)))

	final_power = N*nic_power() + N_r*k*4*0.7

	return [final_cost,final_power,N_r,N]

if(len(sys.argv) > 1):
	k = int(sys.argv[1])
	N = int(sys.argv[2])
	cost = df_cost(k,N)
	print 'DF cost (k = ' + str(k) + ', N = ' + str(N) + ') is: ' + str(int(cost)) + ' $\n'




