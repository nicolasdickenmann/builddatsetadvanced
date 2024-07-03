package ch.ethz.topobench.graph.patheval;

import ch.ethz.topobench.graph.Graph;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class OnePathPerLayerPathEvaluator extends PathEvaluator {

    private int[][] successor;
    private int[][] distance;

    private final int infinity = 99999;

    public OnePathPerLayerPathEvaluator(Graph graph) {
        super(graph);

        int numberOfNodes = graph.getNumNodes();
        successor = new int[numberOfNodes][numberOfNodes];
        distance = new int[numberOfNodes][numberOfNodes];

        // determine shortest paths and store the successor nodes (for path reconstruction purposes)
        FloydWarshallAlgorithm(graph);
    }

    public int getDistance(int u, int v){
        return distance[u][v];
    }

    public List<Integer> getPath(int u, int v) {

        List<Integer> path = new ArrayList<>();
        if (getDistance(u, v) < infinity) {

            if (successor[u][v] < 0){
                return path;
            }

            int intermediate = u;
            path.add(intermediate);

            while (intermediate != v) {
                if (successor[u][v] < 0){
                    break;
                }
                intermediate = successor[intermediate][v];
                path.add(intermediate);
            }
        }

        return path;
    }

    @Override
    public boolean isFlowZero(int src, int dst, int linkFrom, int linkTo) {

        // Restore the shortest path from src to dst and check if it contains the edge (linkFrom, linkTo)

        if (successor[src][dst] < 0){
            return true;
        }

        int u = src;
        boolean linkFromFound = false;

        while (u != dst) {
            if (linkFromFound){
                if (u == linkTo)
                    return false;
                else linkFromFound = false;
            } else if (u == linkFrom) {
                linkFromFound = true;
            }

            u = successor[u][dst];
        }

        if (linkFromFound && u == linkTo){
            return false;
        }


        return true;
    }

    private void FloydWarshallAlgorithm(Graph graph) {

        // Initialize the distance and succesor  arrays
        for (int i = 0; i < graph.getNumNodes(); i++){
            Arrays.fill(successor[i], -1);
            Arrays.fill(distance[i], infinity);
        }


        for (int u = 0; u < graph.getNumNodes(); u++){
            for (int i = 0; i < graph.getAdjacencyList()[u].size(); i++){
                int v = graph.getAdjacencyList()[u].elementAt(i).getLinkTo();

                // Set the distance of (u, v) edge equal to 1
                distance[u][v] = 1;
                successor[u][v] = v;

            }
        }

        // Floyd-Washall Algorithm
        for (int k = 0; k < graph.getNumNodes(); k++) {
            for (int i = 0; i < graph.getNumNodes(); i++) {
                for (int j = 0; j < graph.getNumNodes(); j++) {
                    if (distance[i][j] > distance[i][k] + distance[k][j]) {
                        distance[i][j] = distance[i][k] + distance[k][j];
                        successor[i][j] = successor[i][k];
                    }
                }
            }
        }
    }

}
