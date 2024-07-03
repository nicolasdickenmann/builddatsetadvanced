import sys
import math
from sf_cost import *
from pf_cost import *
from del_cost import *
from fbf3_cost import *
from df_cost import *
from t3d_cost import *
from t5d_cost import *
from dln_cost import *
from ft3_cost import *
from lh2_cost import *
from lh_hc_cost import *
from hc_cost import *
from cost_model import *

def compute_cost_power():
  #dir_path="../SC_2014/results/cost_power_cables-eth10-elpeus"
  dir_path="./results/cost_power_cables-qdr56"

  sf_mms_a_2q = open(dir_path+"/sf_a-2q.txt","w")
  pf = open(dir_path+"/pf.txt","w")
  df_full = open(dir_path+"/df_full.txt","w")
  fbf3 = open(dir_path+"/fbf3_relaxed.txt","w")
  del3 = open(dir_path+"/del3.txt","w")
  prod3 = open(dir_path+"/prod3.txt","w")
  ft3 = open(dir_path+"/ft3.txt","w")
  dln = open(dir_path+"/dln.txt","w")
  t3d = open(dir_path+"/t3d.txt","w")
  t5d = open(dir_path+"/t5d.txt","w")
  lh2 = open(dir_path+"/lh2.txt","w")
  lh_hc = open(dir_path+"/lh_hc.txt","w")
  hc = open(dir_path+"/hc.txt","w")
  
  sf_mms_a_2q.write("endpoints radix k_r p routers total_cost total_power cost_per_endpoint_indir power_per_endpoint_indir cost_per_endpoint_dir power_per_endpoint_dir\n") 
  df_full.write("endpoints radix k_r p routers total_cost total_power cost_per_endpoint_indir power_per_endpoint_indir cost_per_endpoint_dir power_per_endpoint_dir\n")  
  pf.write("endpoints radix k_r p routers total_cost total_power cost_per_endpoint_indir power_per_endpoint_indir cost_per_endpoint_dir power_per_endpoint_dir\n")  
  fbf3.write("endpoints radix k_r p routers total_cost total_power cost_per_endpoint_indir power_per_endpoint_indir cost_per_endpoint_dir power_per_endpoint_dir\n")  
  ft3.write("endpoints radix k_r p routers total_cost total_power cost_per_endpoint_indir power_per_endpoint_indir cost_per_endpoint_dir power_per_endpoint_dir\n")  
  del3.write("endpoints radix k_r p routers total_cost total_power cost_per_endpoint_indir power_per_endpoint_indir cost_per_endpoint_dir power_per_endpoint_dir\n")  
  prod3.write("endpoints radix k_r p routers total_cost total_power cost_per_endpoint_indir power_per_endpoint_indir cost_per_endpoint_dir power_per_endpoint_dir\n")  
  dln.write("endpoints radix k_r p routers total_cost total_power cost_per_endpoint_indir power_per_endpoint_indir cost_per_endpoint_dir power_per_endpoint_dir\n")  
  t3d.write("endpoints radix k_r p routers total_cost total_power cost_per_endpoint_indir power_per_endpoint_indir cost_per_endpoint_dir power_per_endpoint_dir\n")  
  t5d.write("endpoints radix k_r p routers total_cost total_power cost_per_endpoint_indir power_per_endpoint_indir cost_per_endpoint_dir power_per_endpoint_dir\n")  
  lh2.write("endpoints radix k_r p routers total_cost total_power cost_per_endpoint_indir power_per_endpoint_indir cost_per_endpoint_dir power_per_endpoint_dir\n")  
  lh_hc.write("endpoints radix k_r p routers total_cost total_power cost_per_endpoint_indir power_per_endpoint_indir cost_per_endpoint_dir power_per_endpoint_dir\n")  
  hc.write("endpoints radix k_r p routers total_cost total_power cost_per_endpoint_indir power_per_endpoint_indir cost_per_endpoint_dir power_per_endpoint_dir\n")  

  compute_SF_MMS = True
  compute_DF_balanced = True
  compute_DF_relaxed = False 
  compute_DEL3 = True
  compute_PF = True
  compute_PROD3 = True
  compute_FT3 = True
  compute_FBF3_relaxed = False
  compute_FBF3 = False
  compute_T3D = False
  compute_T5D = False
  compute_DLN = False
  compute_HC = False
  compute_LH_HC = False
  
  N_1 = 10
  N_2 = 1000000
  k_1 = 1
  k_2 = sys.maxint
  
  if compute_DF_balanced == True:
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DF - fully balanced <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    ps = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    for i in range(0, len(ps)):
      p = ps[i]

      [k_r,p,k,N_r,N] = df_params(p)
    
      [final_cost,final_power,routers,endpoints] = df_cost_conc_fully_balanced(p, N_1, N_2, k_1, k_2)

      df_full.write(str(endpoints) + ' ' + 
        str(int(k)) + ' ' + str(int(k_r)) + ' ' + str(int(p)) + ' ' +
        str(int(routers)) + ' ' + 
        str(int(final_cost)) + ' ' + 
        str(int(final_power)) + ' ' + 
        str(float(float(final_cost) / float(endpoints))) + ' ' + 
        str(float(float(final_power) / float(endpoints))) + ' ' +
        str(float(float(final_cost) / float(routers))) + ' ' + 
        str(float(float(final_power) / float(routers))) + '\n')


  if compute_DEL3 == True:
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DEL3 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    qs = [2, 8, 32, 128]

    for i in range(0, len(qs)):
      q = qs[i]

      [k_r,p,k,N_r,N] = del3_params(q)

      [final_cost,final_power,routers,endpoints] = del3_cost(k, N, q, N_1, N_2, k_1, k_2)

      del3.write(str(endpoints) + ' ' + 
        str(int(k)) + ' ' + str(int(k_r)) + ' ' + str(int(p)) + ' ' +
        str(int(routers)) + ' ' + 
        str(int(final_cost)) + ' ' + 
        str(int(final_power)) + ' ' + 
        str(float(float(final_cost) / float(endpoints))) + ' ' + 
        str(float(float(final_power) / float(endpoints))) + ' ' +
        str(float(float(final_cost) / float(routers))) + ' ' + 
        str(float(float(final_power) / float(routers))) + '\n')


  if compute_PROD3 == True:
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DEL3 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    qs = [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64]

    for i in range(0, len(qs)):
      q = qs[i]

      [k_r,p,k,N_r,N] = prod3_params(q)

      [final_cost,final_power,routers,endpoints] = prod3_cost(k, N, q, N_1, N_2, k_1, k_2)

      prod3.write(str(endpoints) + ' ' + 
        str(int(k)) + ' ' + str(int(k_r)) + ' ' + str(int(p)) + ' ' +
        str(int(routers)) + ' ' + 
        str(int(final_cost)) + ' ' + 
        str(int(final_power)) + ' ' + 
        str(float(float(final_cost) / float(endpoints))) + ' ' + 
        str(float(float(final_power) / float(endpoints))) + ' ' +
        str(float(float(final_cost) / float(routers))) + ' ' + 
        str(float(float(final_power) / float(routers))) + '\n')



  if compute_FT3 == True:
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> FT-3 - full BB <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

    ks = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50]

    for i in range(0,len(ks)):
      k = ks[i]
      k_r = k / 2
      p = k / 2

      [final_cost,final_power,routers,endpoints] = ft3_cost_radix(k, N_1, N_2, k_1, k_2)

      ft3.write(str(endpoints) + ' ' + 
        str(int(k)) + ' ' + str(int(k_r)) + ' ' + str(int(p)) + ' ' +
        str(int(routers)) + ' ' + 
        str(int(final_cost)) + ' ' + 
        str(int(final_power)) + ' ' + 
        str(float(float(final_cost) / float(endpoints))) + ' ' + 
        str(float(float(final_power) / float(endpoints))) + ' ' +
        str(float(float(final_cost) / float(routers))) + ' ' + 
        str(float(float(final_power) / float(routers))) + '\n')

  if compute_FBF3_relaxed == True:
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> FBF-3 relaxed <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    assert(False)
  
    for i in range(0,len(ks)):
      k = ks[i]
      k_r = -1
      p = -1

      [final_cost,final_power,routers,endpoints] = fbf3_cost_radix_relaxed(k)

      fbf3.write(str(endpoints) + ' ' + 
        str(int(k)) + ' ' + str(int(k_r)) + ' ' + str(int(p)) + ' ' +
        str(int(routers)) + ' ' + 
        str(int(final_cost)) + ' ' + 
        str(int(final_power)) + ' ' + 
        str(float(float(final_cost) / float(endpoints))) + ' ' + 
        str(float(float(final_power) / float(endpoints))) + ' ' +
        str(float(float(final_cost) / float(routers))) + ' ' + 
        str(float(float(final_power) / float(routers))) + '\n')


  qs =       [3,4,5, 7, 8, 9, 11, 13, 16, 17, 19, 23, 25, 27, 29, 31, 32, 37, 41, 43]
  deltas =   [-1,0,1,-1, 0, 1, -1,  1,  0,  1, -1, -1,  1, -1,  1, -1,  0,  1,  1, -1]

  assert(len(qs) == len(deltas))

  for i in range(0,len(qs)):
    q = qs[i]
    delta = deltas[i]

    if compute_SF_MMS == True:
      print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> SF MMS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

      [k_r,p,k,N_r,N] = sf(q,delta)

      [final_cost,final_power,routers] = sf_a_2q_cost(k,N,q,delta, N_1, N_2, k_1, k_2)

      sf_mms_a_2q.write(str(N) + ' ' + 
        str(int(k)) + ' ' + str(int(k_r)) + ' ' + str(int(p)) + ' ' +
        str(int(routers)) + ' ' + 
        str(int(final_cost)) + ' ' + 
        str(int(final_power)) + ' ' + 
        str(float(float(final_cost) / float(N))) + ' ' + 
        str(float(float(final_power) / float(N))) + ' ' +
        str(float(float(final_cost) / float(routers))) + ' ' + 
        str(float(float(final_power) / float(routers))) + '\n')

    if compute_PF == True:
      print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> PF <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

      [k_r,p,k,N_r,N] = pf_conf(q)

      [final_cost,final_power,routers] = pf_cost(k,N,q, N_1, N_2, k_1, k_2)

      pf.write(str(N) + ' ' + 
        str(int(k)) + ' ' + str(int(k_r)) + ' ' + str(int(p)) + ' ' +
        str(int(routers)) + ' ' + 
        str(int(final_cost)) + ' ' + 
        str(int(final_power)) + ' ' + 
        str(float(float(final_cost) / float(N))) + ' ' + 
        str(float(float(final_power) / float(N))) + ' ' +
        str(float(float(final_cost) / float(routers))) + ' ' + 
        str(float(float(final_power) / float(routers))) + '\n')

    if compute_DLN == True:
      print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DLN <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

      [final_cost,final_power,routers,endpoints] = dln_cost(k,N,q, N_1, N_2, k_1, k_2)

      dln.write(str(endpoints) + ' ' + 
        str(int(k)) + ' ' + str(int(k_r)) + ' ' + str(int(p)) + ' ' +
        str(int(routers)) + ' ' + 
        str(int(final_cost)) + ' ' + 
        str(int(final_power)) + ' ' + 
        str(float(float(final_cost) / float(endpoints))) + ' ' + 
        str(float(float(final_power) / float(endpoints))) + ' ' +
        str(float(float(final_cost) / float(routers))) + ' ' + 
        str(float(float(final_power) / float(routers))) + '\n')

    if compute_T3D == True:
      print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> T3D <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

      [final_cost,final_power,routers,endpoints] = t3d_cost(N, N_1, N_2)

      p = 1
      k = p + 3*2
      k_r = k - p

      t3d.write(str(endpoints) + ' ' + 
        str(int(k)) + ' ' + str(int(k_r)) + ' ' + str(int(p)) + ' ' +
        str(int(routers)) + ' ' + 
        str(int(final_cost)) + ' ' + 
        str(int(final_power)) + ' ' + 
        str(float(float(final_cost) / float(endpoints))) + ' ' + 
        str(float(float(final_power) / float(endpoints))) + ' ' +
        str(float(float(final_cost) / float(routers))) + ' ' + 
        str(float(float(final_power) / float(routers))) + '\n')

    if compute_T5D == True:
      print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> T5D <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

      [final_cost,final_power,routers,endpoints] = t5d_cost_balanced(N, N_1, N_2)

      k_r = 2*5
      p = 1
      k = k_r + p

      t5d.write(str(endpoints) + ' ' + 
        str(int(k)) + ' ' + str(int(k_r)) + ' ' + str(int(p)) + ' ' +
        str(int(routers)) + ' ' + 
        str(int(final_cost)) + ' ' + 
        str(int(final_power)) + ' ' + 
        str(float(float(final_cost) / float(endpoints))) + ' ' + 
        str(float(float(final_power) / float(endpoints))) + ' ' +
        str(float(float(final_cost) / float(routers))) + ' ' + 
        str(float(float(final_power) / float(routers))) + '\n')

    if compute_HC == True:
      print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> HC <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

      [final_cost,final_power,routers,endpoints] = hc_cost(N,2*q, N_1, N_2)

      hc.write(str(endpoints) + ' ' + 
        str(int(k)) + ' ' + str(int(k_r)) + ' ' + str(int(p)) + ' ' +
        str(int(routers)) + ' ' + 
        str(int(final_cost)) + ' ' + 
        str(int(final_power)) + ' ' + 
        str(float(float(final_cost) / float(endpoints))) + ' ' + 
        str(float(float(final_power) / float(endpoints))) + ' ' +
        str(float(float(final_cost) / float(routers))) + ' ' + 
        str(float(float(final_power) / float(routers))) + '\n')

    if compute_LH_HC == True:
      print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> LH-HC <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

      [final_cost,final_power,routers,endpoints] = lh_hc_cost(N, 2*q, N_1, N_2)

      lh_hc.write(str(endpoints) + ' ' + 
        str(int(k)) + ' ' + str(int(k_r)) + ' ' + str(int(p)) + ' ' +
        str(int(routers)) + ' ' + 
        str(int(final_cost)) + ' ' + 
        str(int(final_power)) + ' ' + 
        str(float(float(final_cost) / float(endpoints))) + ' ' + 
        str(float(float(final_power) / float(endpoints))) + ' ' +
        str(float(float(final_cost) / float(routers))) + ' ' + 
        str(float(float(final_power) / float(routers))) + '\n')

  sf_mms_a_2q.close()
  df_full.close()
  pf.close()
  fbf3.close()
  ft3.close()
  dln.close()
  del3.close()
  prod3.close()
  t3d.close()
  t5d.close()
  hc.close()
  lh2.close()
  lh_hc.close()


compute_cost_power()
