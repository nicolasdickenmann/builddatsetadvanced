#!/bin/bash           

#parameters

logFilesPath="output_hc"
pathToHC="HC"

mkdir ${logFilesPath}

injection=( 0.7 0.8 0.9 )
#injection=( 0.8 0.85 0.9 )
routing_fun=( valiant )
buff_size=( 16 )
scenario=( bitrev )

size=13

commonContents="topology = torus;
use_noc_latency = 0;
hold_switch_for_packet=0;

k = 2;
n = 13;

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

					echo "injection_rate = ${j};"		 	> $pathToHC
					echo "traffic = ${b};"				>> $pathToHC


					echo "routing_function = ${i};"			>> $pathToHC
					echo "vc_buf_size = ${k};"			>> $pathToHC


					echo "${commonContents}" 			>> $pathToHC

					../../booksim ./${pathToHC}			> ./${logFilesPath}"/HC.output_scen="${b}"_inj="${j}"_fun="${i}"_buff="${k}"_size="${size}".log"
				
			done
		done
    	done
done




