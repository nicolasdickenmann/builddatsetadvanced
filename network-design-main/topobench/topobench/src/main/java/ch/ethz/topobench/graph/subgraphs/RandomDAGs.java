package ch.ethz.topobench.graph.subgraphs;

import ch.ethz.topobench.graph.Graph;

import java.util.*;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class RandomDAGs extends SubgraphsGenerator {

    private int layersNumber;
    private int threads;

    private double epsilon = 0.9;  // Fraction of edges, that should not be deleted randomly

    public RandomDAGs(int layersNumber, int threads, Graph graph, boolean produceLayers, double epsilon) {
        super(graph, produceLayers);
        this.layersNumber = layersNumber;
        this.threads = threads;
        this.epsilon = epsilon;
        System.out.println("* Number of layers: " + layersNumber);
        System.out.println("* Epsilon: " + epsilon);
    }

    /**
     * Divide the graph randomly into subgraphs, where each of them is a directed acyclic graph.
     * The function may be parallelized.
     * @return List of subgraphs.
     */
    @Override
    public List<Graph> generateLayers() {
        List<Graph> subgraphs = Collections.synchronizedList(new ArrayList<>());

        // permutationsSet is the set of all vertices permutations, that would be further mapped into graph layers
        Set<List<Integer>> permutationSet = Collections.synchronizedSet(new HashSet<>());

        if (threads > 1) {

            // In case of running the program in parallel
            ThreadPoolExecutor executor =
                    (ThreadPoolExecutor) Executors.newFixedThreadPool(threads);

            for (int i = 0; i < layersNumber; i++) {
                executor.submit(() -> {
                    while (true) {
                        List<Integer> vertices = IntStream.rangeClosed(0, graph.getNumNodes()).boxed().collect(Collectors.toList());
                        Collections.shuffle(vertices);
                        if (permutationSet.add(vertices)) {
                            Graph subgraph = permutationToGraph(vertices);
                            subgraphs.add(subgraph);
                            break;
                        }
                    }
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

            // In case of using only one thread

            while (permutationSet.size() < layersNumber){
                List<Integer> vertices = IntStream.rangeClosed(0, graph.getNumNodes()).boxed().collect(Collectors.toList());
                Collections.shuffle(vertices);
                permutationSet.add(vertices);
            }

            for (List<Integer> permutation : permutationSet) {
                subgraphs.add(permutationToGraph(permutation));
            }
        }

        return subgraphs;
    }

    /**
     *
     * @param verticesOrder Permutation of vertices, defining the direction of each of edges.
     * @return Directed acyclic graph, being a subgraph of the initialGraph, compliant with
     * the given permutation.
     */
    private Graph permutationToGraph(List<Integer> verticesOrder) {
        Graph subgraph = new Graph("Subgraph", graph.getNumNodes());

        for (int u = 0; u < graph.getNumNodes(); u++) {
            for (int j = 0; j < graph.getAdjacencyList()[u].size(); j++) {
                int v = graph.getAdjacencyList()[u].get(j).getLinkTo();

                // Check if label of u < label of v -> if so, add the link to the graph
                if (verticesOrder.get(u) < verticesOrder.get(v)) {
                    if (new Random().nextDouble() < epsilon)
                        subgraph.addNeighbor(u, v);
                }
            }
        }

        return subgraph;
    }
}
