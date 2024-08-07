#!/bin/bash           

#parameters

logFilesPath="output_rand"
pathToHC="HC.conf"

mkdir ${logFilesPath}

#injection=( 0.01 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 )
injection=( 0.5 )
routing_fun=( min )
buff_size=( 16 )
scenario=( uniform )

pathToHCStructure="HC.7.bsconf"
pathToHCRoutingTable="HC.7.bsconf.route"

commonContents="topology = anynet;
use_noc_latency = 0;
hold_switch_for_packet=0;

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
				echo ">>>>>>>>>>>>>>>> Simulation for injection rate ${j} and routing function ${i} and scenario ${b} and buff size ${k}"

					echo "injection_rate = ${j};"		 	>> $pathToHC
					echo "traffic = ${b};"				>> $pathToHC

					if [ "${b}" == "shuffle" -o "${b}" == "bitrev" -o "${b}" == "bitcomp" ]; then
						echo "use_size_power_of_two = yes;" 	>> $pathToHC
					else
						echo "use_size_power_of_two = no;"	>> $pathToHC
					fi

					echo "routing_function = ${i};"			>> $pathToHC
					echo "vc_buf_size = ${k};"			>> $pathToHC

					echo "network_file = ${pathToHCStructure};"	>> $pathToHC

					echo "load_routing_file = no;"			>> $pathToHC
					echo "routing_table_file = ${pathToHCRoutingTable};"	>> $pathToHC

					echo "${commonContents}" 			>> $pathToHC

					../../booksim ./${pathToHC}			> ./${logFilesPath}"/HC.output_fun_"${i}"_scen_"${b}"_inj_"${j}"_buff_"${k}".log" 
			done
		done
    	done
done

wait


