from cost_model import *
import math
import sys

def prod3_params(q):
  N_r = (q+1)*(q+1)*(q*q + 1) 
  k_r = (q+1)*(q+1) 
  p = int(math.floor(k_r/3.0)+1)
  k = p+k_r
  N = p*N_r
  return [k_r,p,k,N_r,N]

def prod3_cost(k,N,q, N_1, N_2, k_1, k_2):
  k = int(k)
  N = int(N)

  [k_r,p,k,N_r,N] = prod3_params(q)

  N_e_theory = N_r * k_r / 2

  #get the cost of routers
  C_r = N_r*rt(k)

  #get the cost of cables
  C_el = N_e_theory * el(8)
  C_op = 0

  final_cost = C_r + C_el + C_op
  final_power = N*nic_power() + N_r*router_power(k)

  if((N >= N_1 and N <= N_2) and (k >= k_1 and k <= k_2)):
    print(">>>>>>>>>>>> PROD (N = %d, k = %d)" % (N,k))
    print("\tN: %d, N_r: %d, k: %d, k': %d, p: %d" % (N, N_r, k, k_r, p))
    # print("\tN_el: %d, N_op: %d, N_l_c: %d, N_g_c: %d" % (N_el, N_op, N_l_c, N_g_c))
    print("\tC-per_endpoint: %d, P-per_endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))

  return [final_cost,final_power,N_r,N]


def del3_params(q):
  N_r = (q+1)*(q*q + 1) 
  k_r = (q+1) 
  p = int(math.floor(k_r/3.0)+1)
  k = p+k_r
  N = p*N_r
  return [k_r,p,k,N_r,N]

def del3_cost(k,N,q, N_1, N_2, k_1, k_2):
  k = int(k)
  N = int(N)

  [k_r,p,k,N_r,N] = del3_params(q)

  g = int(q*q + 1)

  N_e_theory = (g * 1 * q + g * q * (q + 1)) / 2    #(N_r * k_r) / 2;

  #get the cost of routers
  C_r = N_r*rt(k)

  #get the cost of global cables
  N_g_c = g * (g - 1) / 2
  avg_g_len = int(0.5 * 2.0 * math.ceil(math.sqrt(g)))
  C_op = op(avg_g_len)

  #get the cost of local cables
  N_l_c = g * q
  C_el = N_l_c * el(1)

  #print N_e_theory
  #print N_l_c + N_g_c
  assert(N_e_theory == N_l_c + N_g_c)

  final_cost = C_r + C_el + C_op
  final_power = N*nic_power() + N_r*router_power(k)

  N_el = N_l_c
  N_op = N_g_c

  if((N >= N_1 and N <= N_2) and (k >= k_1 and k <= k_2)):
    print(">>>>>>>>>>>> DEL3 (N = %d, k = %d)" % (N,k))
    print("\tN: %d, N_r: %d, k: %d, k': %d, p: %d" % (N, N_r, k, k_r, p))
    print("\tN_el: %d, N_op: %d, N_l_c: %d, N_g_c: %d" % (N_el, N_op, N_l_c, N_g_c))
    print("\tC-per_endpoint: %d, P-per_endpoint: %f" % (int(final_cost/(1.0*N)), float(final_power/(1.0*N))))

  return [final_cost,final_power,N_r,N]

