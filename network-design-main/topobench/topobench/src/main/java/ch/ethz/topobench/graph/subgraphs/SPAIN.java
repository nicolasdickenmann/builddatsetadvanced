package ch.ethz.topobench.graph.subgraphs;

import ch.ethz.topobench.graph.Graph;
import ch.ethz.topobench.graph.subgraphs.utility.ColoredGraph;
import ch.ethz.topobench.graph.subgraphs.utility.Path;

import javax.annotation.processing.SupportedSourceVersion;
import java.util.*;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

public class SPAIN extends SubgraphsGenerator {

    private int k; // path diversity
    private int threads;


    public SPAIN(int k, int threads, Graph graph, boolean produceLayers) {
        super(graph, produceLayers);
        this.threads = threads;
        this.k = k;
    }

    @Override
    public List<Graph> generateLayers() {
        List<Graph> subgraphs = Collections.synchronizedList(new ArrayList<>());

        // Compute all destinations (the per destination VLAN computation)
        if (threads > 1) {
            // In case of running the program in parallel
            ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(threads);

            // Compute per destination subgraphs
            for (int dst = 0; dst < graph.getNumNodes(); dst++){
                if (graph.getNodeWeight(dst) > 0) {
                    int finalDst = dst;
                    executor.submit(() -> {
                        Set<Graph> subgraphsPerDestination = perDestinationVLANComputation(finalDst);
                        if (subgraphsPerDestination != null)
                            subgraphs.addAll(subgraphsPerDestination);
                        return null;
                    });
                }
            }

            executor.shutdown();
            try {
                executor.awaitTermination(Long.MAX_VALUE, TimeUnit.NANOSECONDS);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

        } else {
            // Compute per destination subgraphs
            for (int dst = 0; dst < graph.getNumNodes(); dst++){
                if (graph.getNodeWeight(dst) > 0) {

                    Set<Graph> subgraphsPerDestination = perDestinationVLANComputation(dst);
                    //System.out.println(subgraphsPerDestination.size());

                    if (subgraphsPerDestination != null)
                        subgraphs.addAll(subgraphsPerDestination);
                }
            }
        }

        /* Algorithm for merging VLANs */

        List<Graph> finalSubgraphs = new ArrayList<Graph>();

        /* Algorithm for Merging VLANs */
        List<Graph> subgraphsCopy = new ArrayList<>();
        subgraphsCopy.addAll(subgraphs);

        Collections.shuffle(subgraphs);

        Iterator<Graph> iterator = subgraphs.iterator();
        Set<Graph> removed = new HashSet<>();


        while (iterator.hasNext()) {
            Graph Gi = iterator.next();

            if (removed.contains(Gi)) {
                iterator.remove();
                removed.remove(Gi);
                continue;
            }

            Graph Gtemp = new Graph("Subgraph", graph.getNumNodes());
            mergeGraphs(Gtemp, Gi);

            iterator.remove();

            Collections.shuffle(subgraphs);

            for (Graph Gj : subgraphs) {
                if (removed.contains(Gj)) continue;

                Graph Gm = new Graph("Subgraph", graph.getNumNodes());
                mergeGraphs(Gm, Gj);
                mergeGraphs(Gm, Gtemp);

                if (Gm.isAcyclic()) {
                    removed.add(Gj);
                    mergeGraphs(Gtemp, Gm);
                }

            }

            finalSubgraphs.add(Gtemp);
        }


        // In case of running the program in parallel
        ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(threads);


        for (int N = 0; N < 10; N++) {

            executor.submit(() -> {

                List<Graph> newFinalSubgraphs = new ArrayList<>();
                newFinalSubgraphs.add(graph);
                List<Graph> newSubgraphs = new ArrayList<>();
                Set<Graph> newremoved = new HashSet<>();

                newSubgraphs.addAll(subgraphsCopy);

                Collections.shuffle(newSubgraphs);

                Iterator<Graph> newIterator = newSubgraphs.iterator();

                while (newIterator.hasNext()) {
                    Graph Gi = newIterator.next();

                    if (newremoved.contains(Gi)) {
                        newIterator.remove();
                        newremoved.remove(Gi);
                        continue;
                    }

                    newIterator.remove();

                    Graph Gtemp = new Graph("Subgraph", graph.getNumNodes());
                    mergeGraphs(Gtemp, Gi);

                    Collections.shuffle(newSubgraphs);

                    for (Graph Gj : newSubgraphs) {
                        if (newremoved.contains(Gj)) continue;

                        Graph Gm = new Graph("Subgraph", graph.getNumNodes());
                        mergeGraphs(Gm, Gj);
                        mergeGraphs(Gm, Gtemp);

                        if (Gm.isAcyclic()) {
                            newremoved.add(Gj);
                            mergeGraphs(Gtemp, Gm);

                        }

                    }

                    newFinalSubgraphs.add(Gtemp);
                }

                synchronized (this) {
                    if (newFinalSubgraphs.size() < finalSubgraphs.size()) {
                        System.out.println(" > Old: " +  finalSubgraphs.size() + " New: " + newFinalSubgraphs.size());
                        finalSubgraphs.clear();
                        finalSubgraphs.addAll(newFinalSubgraphs);
                    } else {
                        System.out.println(" > Old: " +  finalSubgraphs.size() + " New: " + newFinalSubgraphs.size());
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


        System.out.println(" > Layers created " + finalSubgraphs.size());


        for (Graph g: finalSubgraphs){
            System.out.println("Layer size " + g.getNumberBidirEdges());
        }

        return finalSubgraphs;
    }

    private void mergeGraphs (Graph Gm, Graph Gj) {

        for (int u = 0; u < graph.getNumNodes(); u++) {
            for (int i = 0; i < Gj.getAdjacencyList()[u].size(); i++){
                int v = Gj.getAdjacencyList()[u].get(i).getLinkTo();

                if (Gm.findNeighborIdx(u, v) == -1){
                    Gm.addNeighbor(u, v);
                }
            }
        }

    }

    /**
     * Given topology graph, number of paths k and destination d, compute the set of graphs
     * for d (SPAIN_old - Algorithm 3).
     * @param d - destination
     * @return
     */
    private Set<Graph> perDestinationVLANComputation(int d) {

        List<Path> Pathset = new ArrayList<>();

        for (int v = 0; v < graph.getNumNodes(); v++) {
            if (graph.getNodeWeight(v) > 0 && v != d)
                Pathset.addAll(computePaths(v, d));
        }


        Pathset.sort((p1, p2) -> {
            List<Integer> l1 = p1.getPath();
            List<Integer> l2 = p2.getPath();

            int i1 = l1.size() - 1;
            int i2 = l2.size() - 1;

            while (i1 >= 0 && i2 >= 0) {

                if (l1.get(i1) > l2.get(i2))
                    return 1;
                else if (l1.get(i1) < l2.get(i2))
                    return -1;
                else {
                    i1--;
                    i2--;
                }
            }

            if (i1 > 0)
                return 1;
            else return 0;

        });


        // Graph coloring
        ColoredGraph coloredGraph = new ColoredGraph(Pathset.size());

        // For every two paths from the Pathset, which are not vlan-compatible
        // add an edge between them in the colored graph
        for (int i = 0; i < Pathset.size(); i++) {
            for (int j = i + 1; j < Pathset.size(); j++) {

                if (!vlanCompatible(Pathset.get(i), Pathset.get(j))) {
                    coloredGraph.addBidirNeighbour(i, j);

                }

            }
        }


        // Color the graph
        int colorsNumber  = coloredGraph.graphColoring();

        // verticesColors maps each vertex v_i (and hence Pathset.get(i)) to one of
        // colorsNumber colors
        int[] verticesColors = coloredGraph.getVerticesColors();


        HashSet<Graph> vlansPerDesination = new HashSet<>();

        if (verticesColors != null) {

            for (int i = 0; i < colorsNumber; i++) {
                Graph g = new Graph("Subgraph", graph.getNumNodes());

                /* Merge all paths with color i */
                for (int j = 0; j < Pathset.size(); j++) {

                    if (verticesColors[j] == i) {
                        // Add path j to the graph
                        addPathToGraph(Pathset.get(j), g);
                    }
                }

                vlansPerDesination.add(g);
            }
        }


        return vlansPerDesination;
    }

    /**
     * Check if pi and pj are vlan-compatible. We define
     * two paths to be vlan-compatible if and only if any common
     * node on those two paths have the same next hop.
     * @param pi
     * @param pj
     * @return
     */
    private boolean vlanCompatible(Path pi, Path pj ){

        for (int i = 0; i < pi.length() - 1; i++) {
            int ui = pi.getPath().get(i);

            // Check if pj contains the same node as pi
            for (int j = 0; j < pj.length() - 1; j++) {
                int uj = pj.getPath().get(j);

                if (ui == uj) {

                    if (!pi.getPath().get(i + 1).equals(pj.getPath().get(j + 1)))
                        return false;
                }
            }
        }

        return true;
    }

    /**
     * Function that adds an undirected path p to graph g
     * @param p
     * @param g
     */
    private void addPathToGraph(Path p, Graph g) {
        for (int i = 0; i < p.length() - 1; i++) {

            // Check if the edge between i-th and (i+1)-th vertex exist in the graph already
            if (g.findNeighborIdx(p.getPath().get(i), p.getPath().get(i + 1)) == -1){
                g.addNeighbor(p.getPath().get(i), p.getPath().get(i+1));
            }

            if (g.findNeighborIdx(p.getPath().get(i+1), p.getPath().get(i)) == -1){
                g.addNeighbor(p.getPath().get(i+1), p.getPath().get(i));
            }
        }

    }

    /**
     * Algorithm 1 (SPAIN) Algorithm for Path Computation.
     *
     * TODO: Compact the graph in the first step, before paths computation
     * @param src
     * @param dst
     * @return
     */
    private Set<Path> computePaths(int src, int dst) {

        Set<Path> Pathset = new HashSet<>();

        // Initialize the edge weights array
        long [][] weights = new long[graph.getNumNodes()][graph.getNumNodes()];
        for (int i = 0; i < graph.getNumNodes(); i++)
            Arrays.fill(weights[i], 1);

        while (Pathset.size() < k) {

            // shortest computes weighted shortest path
            Path p = shortest(src, dst, weights);


            if (Pathset.contains(p) || p == null) {
                // No more useful paths
                break;
            }

            Pathset.add(p);

            // For each edge in the path, add |E| to weight of this edge
            for (int i = 0; i < p.length() - 1; i++) {
                weights[p.getPath().get(i)][p.getPath().get(i+1)] += graph.getNumberBidirEdges()*2;
                weights[p.getPath().get(i+1)][p.getPath().get(i)] += graph.getNumberBidirEdges()*2;
            }

        }

        return Pathset;
    }

    /**
     * shortest computes weighted shortest path using Dijkstra algorithm
     * @param src
     * @param dst
     * @param weights
     * @return
     */
    private Path shortest(int src, int dst, long [][] weights) {


        long [] distance = new long[graph.getNumNodes()];
        int[] previous = new int[graph.getNumNodes()];

        for (int vertex = 0; vertex < graph.getNumNodes(); vertex++) {
            distance[vertex] = 9999;
            previous[vertex] = -1;
        }

        distance[src] = 0;

        PriorityQueue<Integer> Q = new PriorityQueue<>((left, right) -> {
            if (distance[left] < distance[right]) {
                return -1;
            } else if (distance[left] > distance[right]) {
                return 1;
            } else if (left < right){
                return -1;
            } else if (left > right) {
                return 1;
            } else return 0;
        });

        for (int vertex = 0; vertex < graph.getNumNodes(); vertex++)
            Q.add(vertex);


        while (!Q.isEmpty()) {
            int u = Q.poll();

            if (u == dst) {
                // The shortest path was found
                List<Integer> path = new LinkedList<>();
                if (previous[u] >= 0 || u == src) {
                    while (u != src) {
                        ((LinkedList<Integer>) path).offerFirst(u);

                        u = previous[u];
                    }
                }
                ((LinkedList<Integer>) path).offerFirst(u);
                return new Path(path);
            }

            for (int i = 0; i < graph.getAdjacencyList()[u].size(); i++){
                int neighbour = graph.getAdjacencyList()[u].get(i).getLinkTo();

                long alt = distance[u] + weights[u][neighbour];
                if (alt < distance[neighbour]) {
                    distance[neighbour] = alt;
                    previous[neighbour] = u;
                    Q.remove(neighbour);
                    Q.add(neighbour);
                }

            }
        }

        return null;
    }
}
