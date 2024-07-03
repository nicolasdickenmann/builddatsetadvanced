package ch.ethz.topobench.graph.subgraphs;

import ch.ethz.topobench.graph.Graph;
import ch.ethz.topobench.graph.subgraphs.utility.Path;

import java.util.*;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;


// The k shortest simple paths merging algorithm
public class kSSPMA extends SubgraphsGenerator {

    private int k;
    private int K = k + 3; // layersNumber of paths found for every nodes pair in kShortestSimplePaths
    private int minLength;
    private int maxLength;
    private int layersNumber;
    private int threads;

    public kSSPMA(int layersNumber, int k, int minLength, int threads, Graph graph, boolean produceLayers) {
        super(graph, produceLayers);
        this.k = k;
        this.minLength = minLength;
        this.maxLength = minLength + 3;
        this.threads = threads;

        // Number of all layers that will be created
        this.layersNumber = layersNumber;
    }

    @Override
    public List<Graph> generateLayers() {

        // Define the list of all-pairs k-shortest simple paths
        List<Path>[][] paths = kShortestSimplePaths();
        List<Graph> subgraphs = mergePaths(paths);
        subgraphs.add(graph);
        return subgraphs;
    }

    /**
     * The function finds all-pairs k-shortest simple paths.
     * The function may be parallelised.
     *
     * @return List for every pair of nodes, containing a List of k shortest
     * simple paths between these nodes, of length >= minLength
     */
    private List<Path>[][] kShortestSimplePaths() {

        List<Path>[][] pathsArray = new List[graph.getNumNodes()][graph.getNumNodes()];

        if (threads > 1){

            // In case of running the program in parallel
            ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(threads);

            // Run BFS from each of the vertices
            for (int u = 0; u < graph.getNumNodes(); u++) {

                int finalU = u;
                executor.submit(() -> {
                    pathsArray[finalU] = pathsPerPair(finalU);
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

            // Run BFS from each of the vertices
            for (int u = 0; u < graph.getNumNodes(); u++) {
                pathsArray[u] = pathsPerPair(u);
            }
        }
        System.out.println(" > Paths calculated");
        return pathsArray;
    }

    /**
     * The function uses BFS algorithm to find K shortest simple paths between
     * selected node u and any other node in the network. All of the paths should
     * be greater or equal minLength.
     *
     * @u The node used as a root for the BFS search
     * @return List of k-shortest simple paths between u and all other nodes,
     * of length >= minLength
     */
    private List<Path>[] pathsPerPair(int u) {

        // Allocate the array of paths lists
        List<Path>[] pathsArray = new List[graph.getNumNodes()];

        for (int i = 0; i < graph.getNumNodes(); i++) {
            pathsArray[i] = new ArrayList();
        }

        // Queue used for the purpose of BFS algorithm
        Queue<Path> Q = new LinkedList<>();

        // Add the path containing only root node to the queue Q
        Q.add(new Path(u));

        while(!Q.isEmpty()){

            Path p = Q.poll();

            // Get the last vertex from the path
            Integer last = p.last();

            if (p.length() - 1 < maxLength) {

                // Get all neighbours of the last vertex
                for (int i = 0; i < graph.getAdjacencyList()[last].size(); i++){
                    int neighbour = graph.getAdjacencyList()[last].elementAt(i).getLinkTo();

                    // Check if the path does not contain neighbour node already,
                    // as the paths should be simple
                    if (p.contains(neighbour)) continue;

                    List<Integer> newPath = new ArrayList<>(p.getPath());
                    newPath.add(neighbour);

                    Q.add(new Path(newPath));

                }

            }
            if (p.length() - 1 >= minLength) {

                boolean disjoint;

                // Check if there exist already k shortest paths from u to last
                if (pathsArray[last].size() >= K){

                    disjoint = true;

                    for (Path path: pathsArray[p.last()]){
                        if (!p.disjoint(path))
                            disjoint = false;
                    }

                    if (disjoint) {

                        // Delete random path from the paths already found
                        pathsArray[last].add(p);
                        Collections.shuffle(pathsArray[last]);
                        pathsArray[last].remove(0);
                    }

                } else {
                    // Check if path p is disjoint with the paths in the list
                    disjoint = true;

                    for (Path path: pathsArray[last]){
                        if (!p.disjoint(path))
                            disjoint = false;
                    }

                    if (disjoint) {
                        pathsArray[last].add(p);
                    }
                }

            }
        }

        return pathsArray;
    }

    /**
     * The main goal of mergePaths function is to assemble the obtained k shortest paths for each pair of vertices
     * into a minimum layersNumber of layers, without reducing the overall throughput.
     * @return List of created layers
     */
    private List<Graph> mergePaths(List<Path> [][] paths) {
        List<Graph> subgraphs = new ArrayList<>();
        for (int i = 0; i < layersNumber; i++) {
            subgraphs.add(new Graph("Subgraph " + i, graph.getNumNodes()));
        }

        for (int i = 0; i < graph.getNumNodes(); i++) {
            for (int j = 0; j < graph.getNumNodes(); j++) {

                if (i == j) continue;

                List<Path> pathsForVerticesPair = paths[i][j];

                // Process the paths in a random order
                Collections.shuffle(pathsForVerticesPair);

                // Set of these paths, that were already placed in any of the layers
                Set<Path> usedPaths = new HashSet<>();

                Collections.shuffle(subgraphs);

                for (Graph g : subgraphs) {
                    // If already k paths for the given pair was analyzed - break the loop
                    if (usedPaths.size() >= k) break;

                    for (Path path: pathsForVerticesPair) {
                        if (usedPaths.size() >= k) break;

                        // Check if the path can be merged into graph g
                        if (compatible(path, g)) {
                            addPathToGraph(path, g);
                            usedPaths.add(path);
                        }

                    }
                    pathsForVerticesPair.removeAll(usedPaths);
                }

            }
        }

        return subgraphs;
    }



    /**
     * Enhanced version of the mergePaths function, which does not allow one pair of nodes to
     * have multiple paths between them within a single layer.
     * Moreover, the number of layers is not bounded from the beginning - at the end, the layers
     * are shuffled and a certain number is chosen randomly and returned to the main function.
     * @param paths
     * @return
     */
    private List<Graph> mergePathsEnhanced(List<Path> [][] paths) {
        List<Graph> subgraphs = new ArrayList<>();
        for (int i = 0; i < layersNumber; i++) {
            subgraphs.add(new Graph("Subgraph " + i, graph.getNumNodes()));
        }

        for (int i = 0; i < graph.getNumNodes(); i++) {
            for (int j = 0; j < graph.getNumNodes(); j++) {

                if (i == j) continue;

                List<Path> pathsForVerticesPair = paths[i][j];

                // Process the paths in a random order
                Collections.shuffle(pathsForVerticesPair);

                // Set of these paths, that were already placed in any of the layers
                Set<Path> usedPaths = new HashSet<>();

                Collections.shuffle(subgraphs);

                for (Graph g : subgraphs) {
                    // If already k paths for the given pair was analyzed - break the loop
                    if (usedPaths.size() >= k) break;

                    for (Path path: pathsForVerticesPair) {
                        if (usedPaths.size() >= k) break;

                        // Check if the path can be merged into graph g
                        if (compatible(path, g)) {
                            addPathToGraph(path, g);
                            usedPaths.add(path);
                            break;
                        }

                    }
                    pathsForVerticesPair.removeAll(usedPaths);
                }


                if (usedPaths.size() < k) {
                    for (Path path: pathsForVerticesPair) {
                        if (usedPaths.size() >= k) break;

                        Graph g = new Graph("Subgraph", graph.getNumNodes());
                        addPathToGraph(path, g);
                        usedPaths.add(path);

                    }
                }
            }
        }

        Collections.shuffle(subgraphs);
        while (subgraphs.size() > layersNumber) {
            subgraphs.remove(subgraphs.size() - 1);
        }

        return subgraphs;
    }

    /**
     * Function that verifies whether graph G with the new path p is loop free or not.
     */
    private boolean compatible (Path p, Graph g) {
        Graph temp = new Graph("Temporary graph", g.getNumNodes());

        // Add all the links from g to temp
        for (int u = 0; u < g.getNumNodes(); u++) {
            for (int i = 0; i < g.getAdjacencyList()[u].size(); i++) {
                int v = g.getAdjacencyList()[u].elementAt(i).getLinkTo();
                temp.addNeighbor(u, v);
            }
        }

        // Append the edges from the path to the graph temp
        addPathToGraph(p, temp);

        // Return whether the graph g is acyclic
        return temp.isAcyclic();
    }

    private void addPathToGraph(Path p, Graph g) {
        for (int i = 0; i < p.length() - 1; i++ ) {

            // Check if the edge between i-th and (i+1)-th vertex exist in the graph already
            if (g.findNeighborIdx(p.getPath().get(i), p.getPath().get(i + 1)) == -1){
                g.addNeighbor(p.getPath().get(i), p.getPath().get(i+1));
            }
        }

    }

}
