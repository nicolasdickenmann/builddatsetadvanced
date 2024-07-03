package ch.ethz.topobench.graph.subgraphs.utility;

import edu.asu.emit.algorithm.utils.Pair;
import java.util.*;

public class PairsPriorityQueue {

    // Priority is based upon the number of occurrences of each of the pairs
    private SortedMap<Integer, Set<Pair<Integer,Integer>>> pairsMap;

    public PairsPriorityQueue(int numberOfNodes) {
        pairsMap = new TreeMap<>();

        // create the first element of the pairsMap
        Set<Pair<Integer, Integer>> pairsList = new HashSet<>();

        // create all the pairs of nodes
        for (int i = 0; i < numberOfNodes; i++) {
            for (int j = i + 1; j < numberOfNodes; j++) {
                Pair<Integer, Integer> p1 = new Pair<>(i, j);
                Pair<Integer, Integer> p2 = new Pair<>(j, i);

                pairsList.add(p1);
                pairsList.add(p2);
            }
        }

        pairsMap.put(0, pairsList);
    }

    private int firstKey() {
        int firstKey = -1;

        for (Integer key: pairsMap.keySet()) {
            if (pairsMap.get(key).size() > 0 && (firstKey < 0 || firstKey > key))
                firstKey = key;
        }
        return firstKey;
    }

    synchronized public List<Pair<Integer, Integer>> poll(List<Pair<Integer, Integer>> Q, int numberOfPairs) {
        // poll first numberOfPairs elements

        List<Pair<Integer, Integer>> pairs = new ArrayList<>(numberOfPairs);
        List<Integer> keys = new ArrayList<>(numberOfPairs);

        // sorted iterator
        for(int key: pairsMap.keySet()) {
            if(pairs.size() == numberOfPairs)
                break;
            for(Pair<Integer, Integer> pair: Q) {
                if(pairs.size() == numberOfPairs)
                    break;
                if(pairsMap.get(key).contains(pair)) {
                    pairs.add(pair);
                    keys.add(key);
                }
            }
        }

        for(int i=0; i<keys.size(); i++){
            Q.remove(pairs.get(i));
            increasePriority(pairs.get(i), keys.get(i));
        }
        return pairs;
    }


    synchronized public void decreasePriority(Pair<Integer, Integer> pair) {
        for (int key: pairsMap.keySet()) {
            if (pairsMap.get(key).contains(pair)) {
                if (pairsMap.containsKey(key - 1)) {
                    pairsMap.get(key).remove(pair);
                    pairsMap.get(key - 1).add(pair);
                    break;
                }
            }
        }
    }

    synchronized public void decreasePriority(Pair<Integer, Integer> pair, int key) {
        if(pairsMap.containsKey(key) && pairsMap.get(key).contains(pair)) {
            if (pairsMap.containsKey(key - 1)){
                pairsMap.get(key).remove(pair);
                pairsMap.get(key - 1).add(pair);
            }
        } else
            decreasePriority(pair);
    }

    synchronized public void increasePriority(Pair<Integer, Integer> pair) {
        for (int key: pairsMap.keySet()) {
            if (pairsMap.get(key).contains(pair)) {
                if (!pairsMap.containsKey(key + 1)){
                    pairsMap.put(key + 1, new HashSet<>());
                }
                pairsMap.get(key).remove(pair);
                pairsMap.get(key + 1).add(pair);
                break;
            }
        }
    }

    synchronized public void increasePriority(Pair<Integer, Integer> pair, int key) {
        if(pairsMap.containsKey(key) && pairsMap.get(key).contains(pair)) {
            if (!pairsMap.containsKey(key + 1)){
                pairsMap.put(key + 1, new HashSet<>());
            }
            pairsMap.get(key).remove(pair);
            pairsMap.get(key + 1).add(pair);
        } else
            increasePriority(pair);
    }
}
