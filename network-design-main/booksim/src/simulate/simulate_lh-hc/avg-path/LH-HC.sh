#!/bin/bash           

#parameters

logFilesPath="output_lh_hc"
pathToLHHC="LH-HC.conf"

mkdir ${logFilesPath}

injection=( 0.01 )
routing_fun=( min )
buff_size=( 16 )
scenario=( uniform )

pathToLHHCStructure="LH-HC.12.bsconf"
pathToLHHCRoutingTable="LH-HC.12.route"

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

					echo "injection_rate = ${j};"		 	>> $pathToLHHC
					echo "traffic = ${b};"				>> $pathToLHHC

					if [ "${b}" == "shuffle" -o "${b}" == "bitrev" -o "${b}" == "bitcomp" ]; then
						echo "use_size_power_of_two = yes;" 	>> $pathToLHHC
					else
						echo "use_size_power_of_two = no;"	>> $pathToLHHC
					fi

					echo "routing_function = ${i};"			>> $pathToLHHC
					echo "vc_buf_size = ${k};"			>> $pathToLHHC

					echo "network_file = ${pathToLHHCStructure};"	>> $pathToLHHC

					echo "load_routing_file = no;"			>> $pathToLHHC
					echo "routing_table_file = ${pathToLHHCRoutingTable};"	>> $pathToLHHC

					echo "${commonContents}" 			>> $pathToLHHC

					../../../booksim ./${pathToLHHC}			> ./${logFilesPath}"/"${pathToLHHCStructure}".output_fun_"${i}"_scen_"${b}"_inj_"${j}"_buff_"${k}".log" 
			done
		done
    	done
done

wait


