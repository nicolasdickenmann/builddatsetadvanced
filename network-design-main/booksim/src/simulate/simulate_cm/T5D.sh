#!/bin/bash           

#parameters

logFilesPath="output_torus5d"
pathToT5D="T5D"

mkdir ${logFilesPath}

#injection=( 0.01 0.1 0.2 0.3 0.4 0.5 0.6 0.7)
injection=( 0.01 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 )
routing_fun=( dim_order )
buff_size=( 16 )
scenario=( uniform )

commonContents="topology = mesh;
use_noc_latency = 0;
hold_switch_for_packet=0;

k = 14;
n = 2;

packet_size  = 1;
num_vcs      = 14;
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

					echo "injection_rate = ${j};"		 	> $pathToT5D
					echo "traffic = ${b};"				>> $pathToT5D

                                        if [ "${b}" == "shuffle" -o "${b}" == "bitrev" -o "${b}" == "bitcomp" ]; then
                                                echo "use_size_power_of_two = yes;"     >> $pathToT5D
                                        else
                                                echo "use_size_power_of_two = no;"      >> $pathToT5D
                                        fi

					echo "routing_function = ${i};"			>> $pathToT5D
					echo "vc_buf_size = ${k};"			>> $pathToT5D


					echo "${commonContents}" 			>> $pathToT5D

					../../booksim ./${pathToT5D}			> ./${logFilesPath}"/T5D.output_scen="${b}"_inj="${j}"_fun="${i}"_buff="${k}".log"
				
			done
		done
    	done
done




