#!/bin/bash           

#parameters

logFilesPath="output_fbf3-anynet"
pathToFBF="FBF3-ANYNET.conf"

mkdir ${logFilesPath}

injection=( 0.01 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8)
routing_fun=( min )
buff_size=( 16 )
scenario=( uniform )

pathToFBFStructure="FBF3-ANYNET.bsconf"
pathToFBFRoutingTable="FBF3-ANYNET.route"

commonContents="topology = anynet;
use_noc_latency = 0;
hold_switch_for_packet=0;

k = 10;

packet_size  = 1;
num_vcs      = 2;
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

					echo "injection_rate = ${j};"		 	> $pathToFBF
					echo "traffic = ${b};"				>> $pathToFBF


					echo "routing_function = ${i};"			>> $pathToFBF
					echo "vc_buf_size = ${k};"			>> $pathToFBF

					 echo "use_size_power_of_two = no;"      >> $pathToFBF

					echo "network_file = ${pathToFBFStructure};"   >> $pathToFBF

                                        echo "load_routing_file = no;"                  >> $pathToFBF
                                        echo "routing_table_file = ${pathToFBFRoutingTable};"  >> $pathToFBF

					echo "${commonContents}" 			>> $pathToFBF

					../../booksim ./${pathToFBF}			> ./${logFilesPath}"/FBF3-ANYNET.output_scen="${b}"_inj="${j}"_fun="${i}"_buff="${k}".log"
				
			done
		done
    	done
done




