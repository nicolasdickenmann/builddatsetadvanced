#!/bin/bash           

#parameters

logFilesPath="output_new_rand_test"
pathToRAND="RAND.conf"

mkdir ${logFilesPath}

injection=( 0.01 )
routing_fun=( min )
buff_size=( 16 )
scenario=( uniform )

rnd_struct=( RAND_N.50.7.3.bsconf RAND_N.98.11.5.bsconf RAND_N.242.17.8.bsconf RAND_N.338.19.8.bsconf RAND_N.578.25.11.bsconf )

#pathToRANDStructure="RAND_N.722.29.13.bsconf"
#pathToRANDRoutingTable="RAND_N.722.29.13.bsconf"

#pathToRANDStructure="RAND_N.578.25.11.bsconf"
#pathToRANDRoutingTable="RAND_N.578.25.11.bsconf"

#pathToRANDStructure="RAND_N.338.19.8.bsconf"
#pathToRANDRoutingTable="RAND_N.338.19.8.bsconf"

#pathToRANDStructure="RAND_N.242.17.8.bsconf"
#pathToRANDRoutingTable="RAND_N.242.17.8.bsconf"

#pathToRANDStructure="RAND_N.98.11.5.bsconf"
#pathToRANDRoutingTable="RAND_N.98.11.5.bsconf"

#pathToRANDStructure="RAND_N.50.7.3.bsconf"
#pathToRANDRoutingTable="RAND_N.50.7.3.bsconf"

commonContents="topology = anynet;
//use_noc_latency = 0;
//hold_switch_for_packet=0;

k = 1;

packet_size  = 1;
num_vcs      = 4;
vc_allocator = separable_input_first; 
sw_allocator = separable_input_first;

alloc_iters   = 1;
sample_period = 500;

wait_for_tail_credit = 0;
use_read_write       = 0;

credit_delay   = 2;
routing_delay  = 0;
vc_alloc_delay = 1;
sw_alloc_delay = 1;
st_final_delay = 1;

input_speedup     = 1;
output_speedup    = 1;
internal_speedup  = 2.0;

warmup_periods = 3;
sim_count      = 1;

priority = none;
injection_rate_uses_flits=1;"

for i in "${routing_fun[@]}"
do
	for k in "${buff_size[@]}"
	do
		for b in "${scenario[@]}"
		do
			for j in "${injection[@]}"
			do
        for ff in "${rnd_struct[@]}"
        do
				echo ">>>>>>>>>>>>>>>> Simulation for injection rate ${j} and routing function ${i} and scenario ${b} and buff size ${k} and file ${ff}"

					echo "injection_rate = ${j};"		 	> $pathToRAND
					echo "traffic = ${b};"				>> $pathToRAND

					if [ "${b}" == "shuffle" -o "${b}" == "bitrev" -o "${b}" == "bitcomp" ]; then
						echo "use_size_power_of_two = yes;" 	>> $pathToRAND
					else
						echo "use_size_power_of_two = no;"	>> $pathToRAND
					fi

					echo "routing_function = ${i};"			>> $pathToRAND
					echo "vc_buf_size = ${k};"			>> $pathToRAND

					#echo "network_file = ${pathToRANDStructure};"	>> $pathToRAND
					echo "network_file = ${ff};"	>> $pathToRAND

					echo "load_routing_file = no;"			>> $pathToRAND
					#echo "routing_table_file = ${pathToRANDRoutingTable};"	>> $pathToRAND
					echo "routing_table_file = ${ff}.route;"	>> $pathToRAND

					echo "${commonContents}" 			>> $pathToRAND


					../../../booksim ./${pathToRAND}			> ./${logFilesPath}"/RAND.output_fun_"${i}"_scen_"${b}"_inj_"${j}"_buff_"${k}"_file_"${ff}".log" 

					../../../booksim ./${pathToRAND}			> ./${logFilesPath}"/RAND.output_fun_"${i}"_scen_"${b}"_inj_"${j}"_buff_"${k}".log" 

			done
      done
		done
  done
done

wait


