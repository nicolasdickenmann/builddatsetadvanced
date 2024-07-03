package ch.ethz.topobench.graph.patheval;

import ch.ethz.topobench.graph.Graph;
import ch.ethz.topobench.graph.Link;
import ch.ethz.topobench.graph.graphs.FatTreeSigcomm;
import edu.asu.emit.algorithm.utils.Pair;

import java.util.*;

public class PASTPathEvaluator extends PathEvaluator {

    public enum Type {
        PAST {
            @Override
            public void initLayers(Graph graph){
                layers = new HashMap<>();

                // Using BFS, for each of the vertices, define a new spanning tree
                // rooted in this certain vertex
                for (int v = 0; v < graph.getNumNodes(); v++) {
                    layers.put(v, new HashSet<>());
                    for (int i = 0; i < pathDiversity; i++) {
                        layers.get(v).add(BFS_ST(v, graph));
                    }
                }
            }
        },
        PAST_R {
            @Override
            public void initLayers(Graph graph){
                layers = new HashMap<>();

                // Using BFS, for each of the vertices, define a new spanning tree
                // rooted in this certain vertex
                for (int v = 0; v < graph.getNumNodes(); v++) {
                    layers.put(v, new HashSet<>());
                    for (int i = 0; i < pathDiversity; i++) {
                        layers.get(v).add(BFS_ST_RAND(v, graph));
                    }
                }
            }
        },
        NM_PAST {
            @Override
            public void initLayers(Graph graph){
                layers = new HashMap<>();

                // Using BFS, for each of the vertices, define a new spanning tree
                for (int v = 0; v < graph.getNumNodes(); v++) {

                    layers.put(v, new HashSet<>());
                    for (int k = 0; k < pathDiversity; k++) {

                        // Let i denote an intermediate switch, which would be chosen as
                        // the root for BFS spanning tree
                        int i = v;
                        while (i == v) {
                            i = new Random().nextInt(graph.getNumNodes());
                        }

                        layers.get(v).add(BFS_ST(i, graph));
                    }
                }
            }
        },
        NM_PAST_R {
            public void initLayers(Graph graph){
                layers = new HashMap<>();

                // Using BFS, for each of the vertices, define a new spanning tree
                for (int v = 0; v < graph.getNumNodes(); v++) {

                    layers.put(v, new HashSet<>());
                    for (int k = 0; k < pathDiversity; k++) {
                        // Let i denote an intermediate switch, which would be chosen as
                        // the root for BFS spanning tree
                        int i = v;
                        while (i == v) {
                            i = new Random().nextInt(graph.getNumNodes());
                        }

                        layers.get(v).add(BFS_ST_RAND(i, graph));
                    }
                }
            }
        }
        ;

        public abstract void initLayers(Graph graph);

    }

    private static Type getPASTAlgorithm(String s) {
        switch (s) {
            case "BASELINE":        return Type.PAST;
            case "RANDOM":          return Type.PAST_R;
            case "NM_BASELINE":     return Type.NM_PAST;
            case "NM_RANDOM":       return Type.NM_PAST_R;
            default:                return null;
        }
    }

    private static Map<Integer, Set<Graph>> layers;
    private static int pathDiversity; // The pathDiversity could be changed, by assigning multiple addresses per destination

    public PASTPathEvaluator(Graph graph, String type, int pathDiversity) {
        super(graph);

        Type algorithmSelectorType = getPASTAlgorithm(type);
        if (algorithmSelectorType == null) {
            throw new RuntimeException("FATAL: argument encoding the algorithm type does not encode to a " +
                    "valid algorithm generator " + type);
        }

        PASTPathEvaluator.pathDiversity = pathDiversity;

        // Generate the layers
        algorithmSelectorType.initLayers(graph);
    }

    /**
     * Function generating a spanning tree, using the BFS algorithm
     * rooted in the provided root node.
     * @param root - the root of the newly created spanning tree
     * @param graph - the initial graph topology
     * @return graph representing the tree
     */
    private static Graph BFS_ST(int root, Graph graph) {
        Graph subgraph = new Graph("Subgraph", graph.getNumNodes());

        boolean [] visited = new boolean[graph.getNumNodes()];
        Arrays.fill(visited, false);

        Queue<Pair<Integer, Integer>> Q = new LinkedList<>();

        // Add all of the neighbours of the root to the queue
        for (int i = 0; i < graph.getAdjacencyList()[root].size(); i++) {
            int u = graph.getAdjacencyList()[root].elementAt(i).getLinkTo();
            if (!visited[u])
                Q.add(new Pair<>(root, u));
        }

        while (!Q.isEmpty()) {
            Pair<Integer, Integer> pair = Q.poll();
            int src = pair.first();
            int dst = pair.second();

            // Check if the destination node was already visited by the BFS algorithm
            if (visited[dst]) continue;
            visited[dst] = true;

            // Add the edge from src to dst to the graph (reversed as the root should be
            // treated as a global destination node in PAST)
            subgraph.addBidirNeighbor(dst, src);

            // Add to the queue all univisited neighbours of the destination node
            for (int i = 0; i < graph.getAdjacencyList()[dst].size(); i++) {
                int u = graph.getAdjacencyList()[dst].elementAt(i).getLinkTo();
                if (!visited[u])
                    Q.add(new Pair<>(dst, u));
            }

        }

        return subgraph;
    }

    /**
     * BFS with random tie breaking.
     * @param root - the root of the newly created spanning tree
     * @param graph - the initial graph topology
     * @return
     */
    private static Graph BFS_ST_RAND(int root, Graph graph) {
        Graph subgraph = new Graph("Subgraph", graph.getNumNodes());

        boolean [] visited = new boolean[graph.getNumNodes()];
        Arrays.fill(visited, false);

        Queue<Pair<Integer, Integer>> Q = new LinkedList<>();

        // Add all of the neighbours of the root to the queue (in
        // random order)

        List<Link> neighbours = graph.getAdjacencyList()[root];
        Collections.shuffle(neighbours);

        for (int i = 0; i < neighbours.size(); i++) {
            int u = neighbours.get(i).getLinkTo();
            if (!visited[u])
                Q.add(new Pair<>(root, u));
        }

        while (!Q.isEmpty()) {
            Pair<Integer, Integer> pair = Q.poll();
            int src = pair.first();
            int dst = pair.second();

            // Check if the destination node was already visited by the BFS algorithm
            if (visited[dst]) continue;
            visited[dst] = true;

            // Add the edge from src to dst to the graph
            subgraph.addBidirNeighbor(dst, src);

            // Add to the queue all unvisited neighbours of the destination node
            neighbours = graph.getAdjacencyList()[dst];
            Collections.shuffle(neighbours);

            for (int i = 0; i < neighbours.size(); i++) {
                int u = neighbours.get(i).getLinkTo();
                if (!visited[u])
                    Q.add(new Pair<>(dst, u));
            }

        }
        return subgraph;
    }


    @Override
    public boolean isFlowZero(int src, int dst, int linkFrom, int linkTo) {

        // Check if the edge from linkFrom to linkTo exists in the graph defined for the dst node
        for (Graph g : layers.get(dst)){
            for (int i = 0; i < g.getAdjacencyList()[linkFrom].size(); i++) {
                int u = g.getAdjacencyList()[linkFrom].elementAt(i).getLinkTo();
                if (u == linkTo) {

                    return false;
                }
            }
        }


        return true;
    }
}
