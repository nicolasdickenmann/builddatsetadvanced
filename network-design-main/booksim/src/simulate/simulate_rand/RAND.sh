#!/bin/bash           

#parameters

logFilesPath="output_rand"
pathToRAND="RAND.conf"

mkdir ${logFilesPath}

injection=( 0.4 )
#injection=( 0.6 0.05 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 )
routing_fun=( ugallnew )
buff_size=( 16 )
scenario=( uniform )

pathToRANDStructure="RAND.98.11.5.bsconf"
pathToRANDRoutingTable="RAND.98.11.5.route"

commonContents="topology = anynet;
use_noc_latency = 0;
//KURWAhold_switch_for_packet=0;

k = 16;

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
				echo ">>>>>>>>>>>>>>>> Simulation for injection rate ${j} and routing function ${i} and scenario ${b} and buff size ${k}"

					echo "injection_rate = ${j};"		 	> $pathToRAND
					echo "traffic = ${b};"				>> $pathToRAND

					if [ "${b}" == "shuffle" -o "${b}" == "bitrev" -o "${b}" == "bitcomp" ]; then
						echo "use_size_power_of_two = yes;" 	>> $pathToRAND
					else
						echo "use_size_power_of_two = no;"	>> $pathToRAND
					fi

					echo "routing_function = ${i};"			>> $pathToRAND
					echo "vc_buf_size = ${k};"			>> $pathToRAND

					echo "network_file = ${pathToRANDStructure};"	>> $pathToRAND

					echo "load_routing_file = no;"			>> $pathToRAND
					echo "routing_table_file = ${pathToRANDRoutingTable};"	>> $pathToRAND

					echo "${commonContents}" 			>> $pathToRAND

					../../booksim ./${pathToRAND}			> ./${logFilesPath}"/"${pathToRANDStructure}".output_fun_"${i}"_scen_"${b}"_inj_"${j}"_buff_"${k}".log" 
			done
		done
  done
done

wait


