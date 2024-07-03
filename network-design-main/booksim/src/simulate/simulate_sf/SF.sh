#!/bin/bash           

#parameters

logFilesPath="___NOC"
pathToMMS="MMS-ANYNET-1296.conf"

mkdir ${logFilesPath}

#injection=( 0.01 )
injection=( 0.01 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8)
#injection=( 0.9 )
#routing_fun=( ugallnew )
routing_fun=( min ugallnew ugalgnew )
#routing_fun=( val )
buff_size=( 16 )
scenario=( uniform shuffle asymmetric bitrev )

#pathToMMSStructure="MMS.29.15.bsconf"
#pathToMMSRoutingTable="MMS.29.15.route"

pathToMMSStructure="SF.1296.bsconf"
pathToMMSRoutingTable="SF.1296.route"

commonContents="topology = anynet;
use_noc_latency = 0;
hold_switch_for_packet=0;

k = 8;

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

					echo "injection_rate = ${j};"		 	> $pathToMMS
					echo "traffic = ${b};"				>> $pathToMMS


					echo "routing_function = ${i};"			>> $pathToMMS
					echo "vc_buf_size = ${k};"			>> $pathToMMS

					echo "use_size_power_of_two = no;"      >> $pathToMMS

					echo "network_file = ${pathToMMSStructure};"   >> $pathToMMS

                                        echo "load_routing_file = no;"                  >> $pathToMMS
                                        echo "routing_table_file = ${pathToMMSRoutingTable};"  >> $pathToMMS

					echo "${commonContents}" 			>> $pathToMMS

					../../booksim ./${pathToMMS}			> ./${logFilesPath}"/"${pathToMMSStructure}".output_scen="${b}"_inj="${j}"_fun="${i}"_buff="${k}".log"
				
			done
		done
    	done
done




