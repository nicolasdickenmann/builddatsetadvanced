package ch.ethz.topobench.graph.subgraphs;

import ch.ethz.topobench.graph.Graph;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

public class FatPathsOriginal extends SubgraphsGenerator {

    private int layersNumber;
    private double edgesFraction;

    public FatPathsOriginal(Graph graph, int number, double fraction, boolean produceLayers) {
        super(graph, produceLayers);

        this.layersNumber = number;
        this.edgesFraction = fraction;
    }

    @Override
    public List<Graph> generateLayers() {

        List<Graph> subgraphs = Collections.synchronizedList(new ArrayList<>());

        // Add the original graph as layer zero
        subgraphs.add(graph);

        ThreadPoolExecutor executor =
                (ThreadPoolExecutor) Executors.newFixedThreadPool(8);

        int numNodes = graph.getNumNodes();
        int numberOfEdges = 0;

        // Prepare the incidence matrix of the original graph
        int[][] incidenceMatrix = new int[numNodes][numNodes];

        // Initialize the incindence matrix with 0
        for (int i = 0; i < numNodes; i++)
            Arrays.fill(incidenceMatrix[i], 0);

        for (int u = 0; u < numNodes; u++){

            for (int i = 0; i < graph.getAdjacencyList()[u].size(); i++) {
                int v = graph.getAdjacencyList()[u].elementAt(i).getLinkTo();
                incidenceMatrix[u][v] = 1;
                numberOfEdges++;
            }
        }

        int finalNumberOfEdges = numberOfEdges;

        for (int i = 0; i < layersNumber; i++) {
            executor.submit(() -> {
                subgraphs.add(createLayer(finalNumberOfEdges, incidenceMatrix));
            });
        }

        executor.shutdown();
        try {
            executor.awaitTermination(Long.MAX_VALUE, TimeUnit.NANOSECONDS);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        return subgraphs;

    }

    private Graph createLayer(int numberOfEdges, int[][] incidenceMatrix) {

        int numNodes = graph.getNumNodes();

        // create a permutation of the nodes - these would stand for labels for vertices
        int [][] subgraph = new int[numNodes][numNodes];

        // The number of edges that would be not be deleted
        int remainingEdges = (int)(numberOfEdges * edgesFraction);

        List<Integer> values = new ArrayList<>();
        for (int l = 0; l < numberOfEdges - remainingEdges; l++)
            values.add(0);
        for (int l = 0; l < remainingEdges; l++)
            values.add(1);
        Collections.shuffle(values);

        for (int i = 0; i < numNodes; i++) {
            for (int j = 0; j < numNodes; j++) {
                if (incidenceMatrix[i][j] > 0) {
                    subgraph[i][j] = values.remove(0);
                } else {
                    subgraph[i][j] = 0;
                }
            }
        }

        return pathsToGraph(subgraph);
    }

    private Graph pathsToGraph(int [][] adjacencyMatrix) {
        Graph subgraph = new Graph("Subgraph", graph.getNumNodes());

        for (int i = 0; i < graph.getNumNodes(); i++){
            for (int j = 0; j < graph.getNumNodes(); j++){
                if (adjacencyMatrix[i][j] > 0){
                    subgraph.addNeighbor(i, j);
                }
            }
        }
        return subgraph;
    }

}
