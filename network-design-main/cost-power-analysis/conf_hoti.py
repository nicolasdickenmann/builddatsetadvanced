import sys
import math
from sf_cost import *
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

def sf_generate():
	#dir_path="../SC_2014/results/cost_power_cables-eth10-elpeus"
	dir_path="./results/cost_power_cables-qdr56"
	sf_a_2q = open(dir_path+"/sf_a-2q.txt","w")

	df_full_p = open(dir_path+"/df_full_p.txt","w")
	df_k_N = open(dir_path+"/df_k_N.txt","w")

	fbf3_k = open(dir_path+"/fbf3_k_relaxed.txt","w")
	ft3_k = open(dir_path+"/ft3_k.txt","w")
	dln_k = open(dir_path+"/dln_k.txt","w")

	fbf3_N = open(dir_path+"/fbf3_N.txt","w")
	ft3_N = open(dir_path+"/ft3_N.txt","w")
	dln_N = open(dir_path+"/dln_N.txt","w")

	t3d = open(dir_path+"/t3d.txt","w")
	t5d = open(dir_path+"/t5d.txt","w")
	lh2 = open(dir_path+"/lh2.txt","w")
	lh_hc = open(dir_path+"/lh_hc.txt","w")
	hc = open(dir_path+"/hc.txt","w")


	
	sf_a_2q_power = open(dir_path+"/sf_a-2q_power.txt","w")
	fbf3_power = open(dir_path+"/fbf3_power.txt","w")
	df_power = open(dir_path+"/df_power.txt","w")
	t3d_power = open(dir_path+"/t3d_power.txt","w")
	t5d_power = open(dir_path+"/t5d_power.txt","w")
	ft3_power = open(dir_path+"/ft3_power.txt","w")
	lh2_power = open(dir_path+"/lh2_power.txt","w")
	lh_hc_power = open(dir_path+"/lh_hc_power.txt","w")
	hc_power = open(dir_path+"/hc_power.txt","w")
	dln_power = open(dir_path+"/dln_power.txt","w")

	sf_a_2q_routers = open(dir_path+"/sf_a-2q_routers.txt","w")
	fbf3_routers = open(dir_path+"/fbf3_routers.txt","w")
	df_routers = open(dir_path+"/df_routers.txt","w")
	t3d_routers = open(dir_path+"/t3d_routers.txt","w")
	t5d_routers = open(dir_path+"/t5d_routers.txt","w")
	ft3_routers = open(dir_path+"/ft3_routers.txt","w")
	lh2_routers = open(dir_path+"/lh2_routers.txt","w")
	lh_hc_routers = open(dir_path+"/lh_hc_routers.txt","w")
	hc_routers = open(dir_path+"/hc_routers.txt","w")
	dln_routers = open(dir_path+"/dln_routers.txt","w")
	
	N_1 = 100
	N_2 = 200000
	k_1 = 1
	k_2 = sys.maxint
	
	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> DF - fully balanced <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

	ps = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

	for i in range(0, len(ps)):
		p = ps[i]
		
		[df_final_cost,df_final_power,routers,endpoints] = df_cost_conc_fully_balanced___HOTI_DF_tor_switches(p, N_1, N_2, k_1, k_2)

		if(df_final_cost > 0):
			df_full_p.write(str(endpoints) + ' ' + str(int(df_final_cost)) + '\n')
		
		if(df_final_power > 0):
			df_power.write(str(endpoints) + ' ' + str(int(df_final_power)) + '\n')
	
		if(routers > 0):
			df_routers.write(str(endpoints) + ' ' + str(int(routers)) + '\n')



		[df_final_cost,df_final_power,routers,endpoints] = df_cost_conc_fully_balanced___HOTI_DF_switches_central_row(p, N_1, N_2, k_1, k_2)

		if(df_final_cost > 0):
			df_full_p.write(str(endpoints) + ' ' + str(int(df_final_cost)) + '\n')
		
		if(df_final_power > 0):
			df_power.write(str(endpoints) + ' ' + str(int(df_final_power)) + '\n')
	
		if(routers > 0):
			df_routers.write(str(endpoints) + ' ' + str(int(routers)) + '\n')


	'''

	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> FT-3 - full BB <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

	#ks = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51,52,53,54,55,56,57,58,59,60]
	#ks = [5, 6, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51,53,55,57,59]
	ks = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50]

	for i in range(0,len(ks)):
		k = ks[i]
			
		[ft3_final_cost,ft3_final_power,routers,endpoints] = ft3_cost_radix(k, N_1, N_2, k_1, k_2)

		if(ft3_final_cost > 0):
			ft3_k.write(str(endpoints) + ' ' + str(int(ft3_final_cost)) + '\n')

		if(ft3_final_power > 0):
			ft3_power.write(str(endpoints) + ' ' + str(int(ft3_final_power)) + '\n')

		if(routers > 0):
			ft3_routers.write(str(endpoints) + ' ' + str(int(routers)) + '\n')


	'''

	'''

	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> FBF-3 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
	
	for i in range(0,len(ks)):
		k = ks[i]

		[fbf3_final_cost,fbf3_final_power,routers,endpoints] = fbf3_cost_radix_relaxed(k)

		if(fbf3_final_cost > 0):
			fbf3_k.write(str(endpoints) + ' ' + str(int(fbf3_final_cost)) + '\n')

		if(fbf3_final_power > 0):
			fbf3_power.write(str(endpoints) + ' ' + str(int(fbf3_final_power)) + '\n')

		if(routers > 0):
			fbf3_routers.write(str(endpoints) + ' ' + str(int(routers)) + '\n')

	'''


	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> OTHER TOPOLOGIES <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

	qs = 			[3,5, 7, 8, 9, 11, 13, 16, 17, 19, 23, 25, 27, 29, 31, 32, 37, 41, 43, 47, 49, 53, 59, 61, 64]
	deltas = 	[-1,1,-1, 0, 1, -1, 1, 0, 1, -1, -1, 1, -1, 1, -1, 0, 1, 1, -1, -1, 1, 1, -1, 1, 0]

	assert(len(qs) == len(deltas))

	for i in range(0,len(qs)):
		q = qs[i]
		delta = deltas[i]

		[k_r,p,k,N_r,N] = sf(q,delta)

		#[sf_cost,sf_power,routers] = sf_a_2q_cost(k,N,q,delta, N_1, N_2, k_1, k_2)
		[sf_cost,sf_power,routers] = sf_group_2q_cost___HOTI_SF_tor_switches(k,N,q,delta, N_1, N_2, k_1, k_2)

		sf_a_2q.write(str(N) + ' ' + str(int(sf_cost)) + '\n')
		sf_a_2q_power.write(str(N) + ' ' + str(int(sf_power)) + '\n')

		if(routers > 0):
			sf_a_2q_routers.write(str(N) + ' ' + str(int(routers)) + '\n')




		[sf_cost,sf_power,routers] = sf_group_2q_cost___HOTI_SF_central_row_switches(k,N,q,delta, N_1, N_2, k_1, k_2)

		sf_a_2q.write(str(N) + ' ' + str(int(sf_cost)) + '\n')
		sf_a_2q_power.write(str(N) + ' ' + str(int(sf_power)) + '\n')

		if(routers > 0):
			sf_a_2q_routers.write(str(N) + ' ' + str(int(routers)) + '\n')



		'''

		#FBF costs

		[fbf3_final_cost,fbf3_final_power,routers,endpoints] = fbf3_cost_old(k,N)

		if(fbf3_final_cost > 0):
			fbf3_k.write(str(endpoints) + ' ' + str(int(fbf3_final_cost)) + '\n')

		if(fbf3_final_power > 0):
			fbf3_power.write(str(endpoints) + ' ' + str(int(fbf3_final_power)) + '\n')

		if(routers > 0):
			fbf3_routers.write(str(endpoints) + ' ' + str(int(routers)) + '\n')

		'''

		'''

		#DF costs

		[df_final_cost,df_final_power,routers,endpoints] = df_cost_relaxed(k,N, N_1, N_2, k_1, k_2)

		if(df_final_cost > 0):
			df_k_N.write(str(endpoints) + ' ' + str(int(df_final_cost)) + '\n')
		
		if(df_final_power > 0):
			df_power.write(str(endpoints) + ' ' + str(int(df_final_power)) + '\n')
	
		if(routers > 0):
			df_routers.write(str(endpoints) + ' ' + str(int(routers)) + '\n')

		'''

		#DLN costs
		
		# [dln_final_cost,dln_final_power,routers,endpoints] = dln_cost(k,N,q, N_1, N_2, k_1, k_2)

		# if(dln_final_cost > 0):
		# 	dln_k.write(str(endpoints) + ' ' + str(int(dln_final_cost)) + '\n')

		# if(dln_final_power > 0):
		# 	dln_power.write(str(endpoints) + ' ' + str(int(dln_final_power)) + '\n')

		# if(routers > 0):
		# 	dln_routers.write(str(endpoints) + ' ' + str(int(routers)) + '\n')

		'''

		#T3D costs
		
		[t3d_final_cost,t3d_final_power,routers,endpoints] = t3d_cost(N, N_1, N_2)

		if(t3d_final_cost > 0):
			t3d.write(str(endpoints) + ' ' + str(int(t3d_final_cost)) + '\n')
		
		if(t3d_final_power > 0):
			t3d_power.write(str(endpoints) + ' ' + str(int(t3d_final_power)) + '\n')
	
		if(routers > 0):
			t3d_routers.write(str(endpoints) + ' ' + str(int(routers)) + '\n')

		'''

		#T5D costs
		
		# [t5d_final_cost,t5d_final_power,routers,endpoints] = t5d_cost_balanced(N, N_1, N_2)

		# if(t5d_final_cost > 0):
		# 	t5d.write(str(endpoints) + ' ' + str(int(t5d_final_cost)) + '\n')

		# if(t5d_final_power > 0):
		# 	t5d_power.write(str(endpoints) + ' ' + str(int(t5d_final_power)) + '\n')

		# if(routers > 0):
		# 	t5d_routers.write(str(endpoints) + ' ' + str(int(routers)) + '\n')

	
		#HC costs
		
		# [hc_final_cost,hc_final_power,routers,endpoints] = hc_cost(N,2*q, N_1, N_2)

		# if(hc_final_cost > 0):
		# 	hc.write(str(endpoints) + ' ' + str(int(hc_final_cost)) + '\n')

		# if(hc_final_power > 0):
		# 	hc_power.write(str(endpoints) + ' ' + str(int(hc_final_power)) + '\n')

		# if(routers > 0):
		# 	hc_routers.write(str(endpoints) + ' ' + str(int(routers)) + '\n')

	
		# #LH-HC costs
		# 
		# [lh_hc_final_cost,lh_hc_final_power,routers,endpoints] = lh_hc_cost(N, 2*q, N_1, N_2)

		# if(lh_hc_final_cost > 0):
		# 	lh_hc.write(str(endpoints) + ' ' + str(int(lh_hc_final_cost)) + '\n')

		# if(lh_hc_final_power > 0):
		# 	lh_hc_power.write(str(endpoints) + ' ' + str(int(lh_hc_final_power)) + '\n')

		# if(routers > 0):
		# 	lh_hc_routers.write(str(endpoints) + ' ' + str(int(routers)) + '\n')


	sf_a_2q.close()

	df_full_p.close()
	df_k_N.close()

	fbf3_k.close()
	ft3_k.close()
	dln_k.close()

	fbf3_N.close()
	ft3_N.close()
	dln_N.close()

	t3d.close()
	t5d.close()
	hc.close()
	lh2.close()
	lh_hc.close()



	sf_a_2q_power.close()
	fbf3_power.close()
	df_power.close()
	t3d_power.close()
	t5d_power.close()
	dln_power.close()
	ft3_power.close()
	lh2_power.close()
	lh_hc_power.close()
	hc_power.close()

	sf_a_2q_routers.close()
	fbf3_routers.close()
	df_routers.close()
	t3d_routers.close()
	t5d_routers.close()
	dln_routers.close()
	ft3_routers.close()
	lh2_routers.close()
	lh_hc_routers.close()
	hc_routers.close()


sf_generate()
