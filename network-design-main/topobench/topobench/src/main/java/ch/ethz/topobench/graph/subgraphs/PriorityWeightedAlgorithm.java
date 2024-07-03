package ch.ethz.topobench.graph.subgraphs;

import ch.ethz.topobench.Main;
import ch.ethz.topobench.graph.Graph;
import ch.ethz.topobench.graph.subgraphs.utility.PairsPriorityQueue;
import ch.ethz.topobench.graph.subgraphs.utility.Path;
import edu.asu.emit.algorithm.utils.Pair;

import java.util.*;
import java.util.concurrent.*;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class PriorityWeightedAlgorithm extends SubgraphsGenerator {

    private int M;
    private int number;
    private int minLength;
    private int maxLength;
    private int networkDiameter;
    private int threads;

    public PriorityWeightedAlgorithm(int layersNumber, int M, int minLength, int networkDiameter, int threads, Graph graph, boolean produceLayers) {
        super(graph, produceLayers);

        this.number = layersNumber;
        this.M = M;
        this.minLength = minLength;
        this.networkDiameter = networkDiameter;
        this.threads = threads;
        this.maxLength = minLength + 2;
    }

    @Override
    protected List<Graph> getSampledLayers(List<Graph> subgraphs){

        Collections.shuffle(subgraphs);
        while (subgraphs.size() > number)
            subgraphs.remove(0);

        return subgraphs;
    }

    @Override
    public List<Graph> generateLayers() {

        List<Graph> subgraphs = new ArrayList<>();

        // Compute number of nodes, that takes part in paths creation
        int numberOfNodes = 0;
        for (int i = 0; i < graph.getNumNodes(); i++){
            if (graph.getNodeWeight(i) > 0)
                numberOfNodes++;
        }

        PairsPriorityQueue priorityQueue = new PairsPriorityQueue(numberOfNodes);

        // Generate random distinct permutations - every permutation is corresponding
        // to one subgraph
        Set<List<Integer>> permutationSet = new HashSet<>();
        while (permutationSet.size() < number) {
            List<Integer> vertices = IntStream.rangeClosed(0, graph.getNumNodes()).boxed().collect(Collectors.toList());
            Collections.shuffle(vertices);
            permutationSet.add(vertices);
        }

        System.out.println("Created permutations " + permutationSet.size());

        // Matrix containing all the weights
        int [][] weights = new int[graph.getNumNodes()][graph.getNumNodes()];
        for (int i = 0; i < graph.getNumNodes(); i++)
            Arrays.fill(weights[i], 0);


        if (threads > 1) {

            // In case of running the program in parallel
            ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(threads);

            for (List<Integer> permutation: permutationSet){
                executor.submit(() -> {
                    Graph subgraph = generateGraphRandomizedWeights(permutation, priorityQueue, weights);
                    subgraphs.add(subgraph);
                    return null;
                });
            }

            executor.shutdown();
            try {
                executor.awaitTermination(Long.MAX_VALUE, TimeUnit.NANOSECONDS);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

        } else {

            for (List<Integer> permutation: permutationSet){
                Graph subgraph = generateGraphRandomizedWeights(permutation, priorityQueue, weights);
                subgraphs.add(subgraph);
            }
        }

        System.out.println("Created subgraphs " + subgraphs.size());

        return subgraphs;
    }


    private Graph generateGraphRandomizedWeights(List<Integer> permutation, PairsPriorityQueue priorityQueue, int [][] weights){
        Graph subgraph = new Graph("Subgraph", graph.getNumNodes());

        int batchSize = 10;

        List<Pair<Integer, Integer>> Q = new ArrayList<>();
        Set<Pair<Integer, Integer>> edges = new HashSet<>();

        int[][] incidenceMatrix = new int[graph.getNumNodes()][graph.getNumNodes()];

        for (int i = 0; i < graph.getNumNodes(); i++)
            Arrays.fill(incidenceMatrix[i], 0);

        for (int u = 0; u < graph.getNumNodes(); u++){
            for (int i = 0; i < graph.getAdjacencyList()[u].size(); i++){
                int v = graph.getAdjacencyList()[u].elementAt(i).getLinkTo();
                if (permutation.get(u) < permutation.get(v))
                    incidenceMatrix[u][v] = 1;
            }
        }

        for (int i = 0; i < graph.getNumNodes(); i++){
            if (graph.getNodeWeight(i) > 0) {
                for (int j = 0; j < graph.getNumNodes(); j++) {
                    if (graph.getNodeWeight(j) > 0) {
                        if (permutation.get(i) < permutation.get(j)) {
                            Pair<Integer, Integer> p1 = new Pair<>(i, j);
                            Q.add(p1);
                        }
                    }
                }
            }
        }

        Collections.shuffle(Q, Main.universalRand);

        int addedPaths = 0;

        while(Q.size() > 0  && (addedPaths < M)) {

            // poll batch of pairs

            List<Pair<Integer, Integer>> batch = priorityQueue.poll(Q, batchSize);

            if (batch.size() == 0) {
                continue;
            }

            for (Pair<Integer, Integer> pair : batch){

                // search for the path for this pair in the graph
                Path path = findDirectedShortestPathWeights(incidenceMatrix, pair.first(), pair.second(), weights);

                // if no directed path was found - generate another pair of vertices
                if (path == null) {
                    priorityQueue.decreasePriority(pair);
                    continue;
                }

                addedPaths++;

                // if in the same time any other path for this pair of vertices
                // wasn't generated - add the path to the graph
                for (int i = 0; i < path.length() - 1; i++) {
                    int u = path.getPath().get(i);
                    int v = path.getPath().get(i+1);

                    edges.add(new Pair<>(u, v));

                }

                for (int i = 0; i < path.length() - 1; i++) {
                    int u = path.getPath().get(i);

                    for (int l = i + networkDiameter + 1; l < path.length(); l++){
                        int v = path.getPath().get(l);

                        if (! (u == path.getPath().get(0) && (v == path.getPath().get(path.length() - 1))))
                            priorityQueue.increasePriority(new Pair<>(u, v));
                    }
                }

                // Remove certain edges from the incidence Matrix in order to avoid using them in future paths
                // finding

                for (int start = 0; start < path.length(); start++) {
                    for (int end = start + 2; end < path.length(); end++) {
                        incidenceMatrix[start][end] = 0;
                    }
                }

                // Remove all pairs from Q that should not be taken into consideration
                for (int i = 0; i < path.length()-1; i++) {
                    int u = path.getPath().get(i);

                    for (int l = 1; l <= Math.min(minLength, path.length() - 1 - i); l++){
                        int v = path.getPath().get(i+l);

                        Q.remove(new Pair<>(u, v));
                    }

                }
            }

        }

        for (Pair<Integer, Integer> pair: edges){
            subgraph.addNeighbor(pair.first(), pair.second());
        }

        System.out.println("Layers size " + edges.size());

        return subgraph;
    }


    synchronized private Path findDirectedShortestPathWeights(int [][] incidenceMatrix, int src, int dst, int [][] weights){
        Queue<Path> Q = new LinkedList<>();

        Q.add(new Path(src));

        // Run BFS to find the shortest path from src to dst
        // with edges according to permutation order
        // with length >= minlength

        long bestPathWeight = 999999; // set path weight to "infinity"
        Path bestPath = null;

        while(!Q.isEmpty()) {
            Path p = Q.poll();

            // Get the last vertex from the path
            Integer last = p.last();

            if (last == dst) {

                // This will not produce any path to dst longer than minimum without loops
                if (p.length() < minLength + 1){
                    continue;
                }

                // The path was found -- check if its weights is smaller than actual
                long pathWeight = 0;

                // Compute the pathWeight
                for (int i = 0; i < p.length() - 1; i++) {
                    // For each edge in the path - increase the weights of edges
                    pathWeight += weights[p.getPath().get(i)][p.getPath().get(i + 1)];

                }

                if (pathWeight < bestPathWeight) {
                    bestPathWeight = pathWeight;
                    bestPath = p;
                }



            } else {

                if (p.length() < maxLength + 1)  {

                    // Add to Q all neighbours of last

                    List<Integer> neighbours = new ArrayList<>();

                    for (int i = 0; i < graph.getAdjacencyList()[last].size(); i++) {
                        int neighbour = graph.getAdjacencyList()[last].elementAt(i).getLinkTo();

                        if (incidenceMatrix[last][neighbour] > 0){
                            neighbours.add(neighbour);
                        }
                    }

                    // Sort the neighbours according to the weights

                                      // For each neighbour from neighbours

                    for (Integer neighbour : neighbours) {
                        List<Integer> newPath = new ArrayList<>(p.getPath());
                        newPath.add(neighbour);
                        Path path = new Path(newPath);

                        long pathWeight = 0;

                        // Compute the pathWeight
                        for (int i = 0; i < path.length() - 1; i++) {
                            // For each edge in the path - increase the weights of edges
                            pathWeight += weights[path.getPath().get(i)][path.getPath().get(i + 1)];

                        }

                        if (pathWeight < bestPathWeight){
                            Q.add(path);
                        }

                    }

                }
            }

        }

        if (bestPath != null) {
            for (int i = 0; i < bestPath.length() - 1; i++) {
                // For each edge in the path - increase the weights of edges
                weights[bestPath.getPath().get(i)][bestPath.getPath().get(i + 1)] += i * (bestPath.length() - 1 - i);

            }
        }

        return bestPath;

    }


}
