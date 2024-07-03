package ch.ethz.topobench.graph.subgraphs.utility;

import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

/**
 * Purpose of this class is the implementation of coloring of the vertices in the graph,
 * used in SPAIN_old algorithm to further minimize the overall number of VLANs (subgraphs / layers).
 */
public class ColoredGraph {

    private int numNodes;  // number of nodes in the graph
    private List<Integer>[] adjacencyList; // adjacency List of each of the vertices
    private int verticesColors[]; // array containing the color of each vertex

    public ColoredGraph (int numNodes) {
        this.numNodes = numNodes;
        adjacencyList = new LinkedList[this.numNodes];

        for (int i = 0; i < this.numNodes; i++)
            adjacencyList[i] = new LinkedList<>();

        verticesColors = new int[this.numNodes];
    }

    /**
     *  Add a bidirectional neighborhood between the two given nodes.
     * @param v
     * @param u
     */
    public void addBidirNeighbour(int v, int u) {
        if (u < numNodes && v < numNodes){
            adjacencyList[v].add(u);
            adjacencyList[u].add(v);
        }
    }

    /**
     * Function which aims at coloring the graph with minimum number of colors.
     * The colors are represented by consecutive integer numbers.
     *
     * @return Number of used colors
     */
    public int graphColoring() {

        if (numNodes < 1) return 0;

        // Initialize the array of vertices colors to -1 (undefined color) and
        // set the color of first vertex to 0
        Arrays.fill(verticesColors, -1);
        verticesColors[0] = 0;

        // availableColors is used to store the still available colors
        // availableColors[i] = false iff the i-th color is already in use
        boolean availableColors [] = new boolean[numNodes];
        Arrays.fill(availableColors, true);

        int color = 0;

        // Assign colors to other vertices
        for (int v = 1; v < numNodes; v++) {

            for (Integer i : adjacencyList[v]) {
                if (verticesColors[i] != -1)
                    availableColors[verticesColors[i]] = false;
            }

            for (color = 0; color < numNodes; color++){
                if (availableColors[color]) break;
            }

            verticesColors[v] = color;
            Arrays.fill(availableColors, true);
        }

        color = 0;

        for (int i = 0; i < numNodes; i++){
            if(verticesColors[i] > color){
                color = verticesColors[i];
            }
        }

        return color+1;
    }

    public int[] getVerticesColors() {
        return verticesColors;
    }
}
