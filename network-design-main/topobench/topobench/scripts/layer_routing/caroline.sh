#!/usr/bin/env bash

###################################
### SCRIPT PARAMETERS
###

NRUNS=4       # Reduced for sake of running time
MYMAINPATH="../../"

###################################
### GENERAL PARAMETERS
###

seed=0          # Set to 0 for random
lpt=MCFFC       # SIMPLE is fast for dense traffic matrices
                # MCFFC is fast for sparse traffic matrices

###################################
### TOPOLOGY SPECIFIC PARAMETERS
###

topology=FILE   # JF = JellyFish,
                # FT = fat-tree,
                # XP = Xpander
                # FILE = Readm from file

linkFailRate=0.0    # Link failure rate [0.0, 1.0]

###################################
### PATH EVALUATION PARAMETERS
###

patheval=LAYER                  # SLACK = Use slack such that flow cannot deviate more than SLACK from shortest path src-dst
                                # NEIGH = Use neighbor's shortest path to destination
                                # KSHRT = K-shortest paths
                                # VALIA = K-valiant load balancing
                                # LAYER = Layer routing
                                # PAST


### SUBGRAPHS GENERATOR PARAMETERS
###

division=PRIORITY_WEIGHTED      # SPAIN = Use SPAIN algorithm
                                # RANDOM_DAGS = Use randomly selected DAGs
                                # PRIORITY_WEIGHTED = Use the algorithm, based on Priority Queue

evaluator=ONE_PATH        # Path evaluator for the layers

###################################
### TRAFFIC GENERATOR SPECIFIC PARAMETERS
###

tmode=MAWP              # RPP = Rand. Permutation Pairs,
                        # ATA = All-to-All,
                        # AT1 = All-to-One,
                        # STR = Stride,
                        # MIWP = Min. Weight Pairs
                        # MAWP = Max. Weight Pairs

###################################
### EXECUTE RUNS
###

# Clock start
before="$(date +%s)"
fraction=1

declare -A hashmap
declare -A pmap

hashmap=(["98"]="110" ["242"]="275" ["338"]="359" ["578"]="625" ["722"]="810")
pmap=(["98"]="6" ["242"]="9" ["338"]="10" ["578"]="13" ["722"]="15")

for switches in 9 #18 #242 338 #578 722
do
    for layersNumber in 6 #${hashmap["$switches"]}
do
    for tmode in MAWP #MIWP RPP AT1
do

   for M in 3 #$(($switches * 3 / 2)) $(($switches * 2)) $(($switches *5 / 4 )) $(($switches))
   do

   if [[ $tmode != AT1 ]] && [[ $tmode != ATA ]]; then

   for trafficFrac in 0.55 #0.1 0.3 0.55 0.8 1.0 #0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
    do

        for fraction in 2 #${pmap["$switches"]} 
        do

            # Executing NRUNS times, store each resulting flow into flowtmp_tutorial
            rm -rf flowtmp_layer_routing
            for (( i=0 ; i < NRUNS ; i++ ))
            do
                    cd $MYMAINPATH
                    filename="graph_files/slimfly_"$switches".txt"
                    # Generate linear program and additional information in temp/
                    # There are five parts to the command: general, selectors, topology parameters, path evaluator parameters, and traffic parameters

                    java -jar TopoBench.jar \
                    -mode PRODUCE -seed $seed -lpt $lpt \
                    -gt $topology -pe $patheval -tm $tmode \
                    -switches $switches -partswitches $switches -filename $filename -p $fraction  \
                    -eval $evaluator -div $division -layers $layersNumber -M $M -diam 2 -minLength 3 -threads 10 -produce 1 -tfr $trafficFrac

                    # Execute solver
                    sh scripts/localLpRun.sh        # Local: scripts/localLpRun.sh, Remote: scripts/remoteLpRun.sh

                    # Run analysis (result will be in analysis/<time-specific-folder-name>/)25
                    java -jar TopoBench.jar \
                    -mode ANALYZE -seed $seed -lpt $lpt \
                    -tm $tmode

                    cd -

                    # Add to list of received flow values
                    flowVal=$(cat ../../temp/objective.txt)
                    echo "$flowVal" >> flowtmp_layer_routing

            done

            # Clock end
            after="$(date +%s)"
            time_taken=`expr $after - $before`
            time_taken=`expr $time_taken / 60`

            # Calculate average and standard deviation
            avgstdflow=`cat flowtmp_layer_routing | awk 'BEGIN{sum=0; count=0}{thr=$1; sum+=thr; val[count]=thr; count++}END{mean=sum/count; sq_sum=0; for (i=0; i < count; i++) sq_sum+=(val[i] - mean)*(val[i] - mean); variance=sqrt(sq_sum/count)/mean; rnd_mean=int(mean * 1000000) / 1000000; rnd_variance=int(variance*100000)/100000; print rnd_mean, rnd_variance}'`

            # Write result to file
            echo "Caroline: $patheval $topology $switches $layersNumber $M $fraction $tmode $trafficFrac $avgstdflow $time_taken" >> ../../results/layer_routing/${tmode}_slimfly_pw_tests.txt
        done
    done

    else
        # Executing NRUNS times, store each resulting flow into flowtmp_tutorial
            rm -rf flowtmp_layer_routing
            for (( i=0 ; i < NRUNS ; i++ ))
            do
                    cd $MYMAINPATH
                    filename="graph_files/slimfly_"$switches".txt"
                    # Generate linear program and additional information in temp/
                    # There are five parts to the command: general, selectors, topology parameters, path evaluator parameters, and traffic parameters

                    java -jar TopoBench.jar \
                    -mode PRODUCE -seed $seed -lpt $lpt \
                    -gt $topology -pe $patheval -tm $tmode \
                    -switches $switches -partswitches $switches -filename $filename -p $fraction  \
                    -eval $evaluator -div $division -layers $layersNumber -M $M -diam 2 -minLength 3 -threads 8 -produce 1

                    # Execute solver
                    sh scripts/localLpRun.sh        # Local: scripts/localLpRun.sh, Remote: scripts/remoteLpRun.sh

                    # Run analysis (result will be in analysis/<time-specific-folder-name>/)25
                    java -jar TopoBench.jar \
                    -mode ANALYZE -seed $seed -lpt $lpt \
                    -tm $tmode

                    cd -

                    # Add to list of received flow values
                    flowVal=$(cat ../../temp/objective.txt)
                    echo "$flowVal" >> flowtmp_layer_routing

            done


            # Clock end
            after="$(date +%s)"
            time_taken=`expr $after - $before`
            time_taken=`expr $time_taken / 60`

            # Calculate average and standard deviation
            avgstdflow=`cat flowtmp_layer_routing | awk 'BEGIN{sum=0; count=0}{thr=$1; sum+=thr; val[count]=thr; count++}END{mean=sum/count; sq_sum=0; for (i=0; i < count; i++) sq_sum+=(val[i] - mean)*(val[i] - mean); variance=sqrt(sq_sum/count)/mean; rnd_mean=int(mean * 1000000) / 1000000; rnd_variance=int(variance*100000)/100000; print rnd_mean, rnd_variance}'`

            # Write result to file
            echo "$patheval $topology $switches $layersNumber $fraction $tmode $trafficFrac $avgstdflow $time_taken" >> ../../results/layer_routing/${tmode}_slimfly_pw_2.txt
    fi
done
done
done
done
