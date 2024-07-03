package ch.ethz.topobench.graph.subgraphs;

import ch.ethz.topobench.Main;
import ch.ethz.topobench.graph.Graph;
import ch.ethz.topobench.graph.LFT;
import ch.ethz.topobench.graph.print.PrinterGraph;
import ch.ethz.topobench.graph.print.PrinterLFT;
import ch.ethz.topobench.graph.subgraphs.utility.PairsPriorityQueue;
import ch.ethz.topobench.graph.subgraphs.utility.Path;
import edu.asu.emit.algorithm.utils.Pair;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.*;

public class ImprovedPriorityWeightedAlgorithm extends SubgraphsGenerator{

    private int M;
    private int number;
    private int minLength;
    private int maxLength;
    private int networkDiameter;
    //private int threads;

    public ImprovedPriorityWeightedAlgorithm(int layersNumber, int M, int minLength, int networkDiameter, int threads, Graph graph, boolean produceLayers) {
        super(graph, produceLayers);

        this.number = layersNumber;
        this.M = M;
        this.minLength = minLength;
        this.networkDiameter = networkDiameter;
        if(threads > 1) {
            System.out.println("Can only use a single thread with the improved priority weighted algorithm");
        }
        //this.threads = 1;
        this.maxLength = minLength + 2;
    }

    @Override
    protected List<Graph> getSampledLayers(List<Graph> subgraphs){
        // The full layer is not included in this, it will be added later on
        Collections.shuffle(subgraphs);
        while (subgraphs.size() > number)
            subgraphs.remove(0);

        return subgraphs;
    }

    protected List<Pair<Graph, LFT>> getSampledLayersLFT(List<Pair<Graph, LFT>> subgraphs){
        // The full layer is not included in this, it will be added later on
        Collections.shuffle(subgraphs);
        while (subgraphs.size() > number)
            subgraphs.remove(0);

        return subgraphs;
    }
    @Override
    public List<Graph> generateLayers() {
        List<Graph> subgraphs = new ArrayList<>(number);
        for(Pair<Graph, LFT> pair: generateLayersLFT())
            subgraphs.add(pair.first());
        return subgraphs;
    }

    public List<Pair<Graph, LFT>> generateLayersLFT() {
        List<Pair<Graph, LFT>> subgraphs = new ArrayList<>(number);
        // Compute number of nodes, that takes part in paths creation
        int numberOfNodes = 0;
        for (int i = 0; i < graph.getNumNodes(); i++){
            if (graph.getNodeWeight(i) > 0)
                numberOfNodes++;
        }

        PairsPriorityQueue priorityQueue = new PairsPriorityQueue(numberOfNodes);

        // Matrix containing all the weights
        int [][] weights = new int[graph.getNumNodes()][graph.getNumNodes()];

        for(int i = 0; i < number; i++) {
            subgraphs.add(generateGraphRandomizedWeights(priorityQueue, weights));
        }

        System.out.println("Created subgraphs " + subgraphs.size());

        return subgraphs;

    }

    private Pair<Graph, LFT> generateGraphRandomizedWeights(PairsPriorityQueue priorityQueue, int [][] weights){
        Graph subgraph = new Graph("Subgraph", graph.getNumNodes());

        int batchSize = (M > 0) ? Math.min(10, M) : 10;

        List<Pair<Integer, Integer>> Q = new ArrayList<>();
        Set<Pair<Integer, Integer>> edges = new HashSet<>();

        for (int i = 0; i < graph.getNumNodes(); i++){
            if (graph.getNodeWeight(i) > 0) {
                for (int j = i+1; j < graph.getNumNodes(); j++) {
                    if (graph.getNodeWeight(j) > 0) {
                        Pair<Integer, Integer> p1 = new Pair<>(i, j);
                        Pair<Integer, Integer> p2 = new Pair<>(j, i);
                        Q.add(p1);
                        Q.add(p2);
                    }
                }
            }
        }

        Collections.shuffle(Q, Main.universalRand);
        // Map from destination to vertex to nextHop (the nextHow on the path from vertex to destination)
        Map<Integer, Map<Integer, Integer>> forwardingTable = new HashMap<>();
        int addedPaths = 0;
        // m < 0 indicates that we want all the paths
        while(Q.size() > 0  && (M < 0 || addedPaths < M)) {

            // poll batch of pairs

            List<Pair<Integer, Integer>> batch = priorityQueue.poll(Q, batchSize);

            if (batch.size() == 0) {
                // This should actually never be triggered
                continue;
            }

            for (Pair<Integer, Integer> pair : batch){

                // search for the path for this pair in the graph
                Path path = findShortestPathWeights(pair.first(), pair.second(), weights, forwardingTable);

                // if no directed path was found - generate another pair of vertices
                if (path == null) {
                    priorityQueue.decreasePriority(pair);
                    continue;
                }

                addedPaths++;

                forwardingTable.putIfAbsent(pair.second(), new HashMap<>());
                for (int i = 0; i < path.length() - 1; i++) {
                    int u = path.getPath().get(i);
                    int v = path.getPath().get(i+1);

                    edges.add(new Pair<>(u, v));
                    forwardingTable.get(pair.second()).put(u, v);
                    // remove node pairs that already have a path now
                    Q.remove(new Pair<>(u, pair.second()));
                }

                for (int i = 0; i < path.length() - 1; i++) {
                    int u = path.getPath().get(i);

                    for (int j = i + networkDiameter + 1; j < path.length(); j++){
                        int v = path.getPath().get(j);

                        if (! (u == path.getPath().get(0) && (v == path.getPath().get(path.length() - 1)))) {
                            priorityQueue.increasePriority(new Pair<>(u, v));
                            priorityQueue.increasePriority(new Pair<>(v, u));
                        }
                    }
                }
            }
        }
        Set<Pair<Integer, Integer>> bidirEdges = new HashSet<>();
        for (Pair<Integer, Integer> pair: edges){
            bidirEdges.add(new Pair<>(pair.second(), pair.first()));
            bidirEdges.add(pair);
        }
        for(Pair<Integer, Integer> pair: bidirEdges) {
            subgraph.addNeighbor(pair.first(), pair.second());
        }

        System.out.println("Layers size " + bidirEdges.size()/2);
        LFT subgraphLFT = generateLFT(forwardingTable, subgraph);
        Pair<Graph, LFT> pair = new Pair<>(subgraph, subgraphLFT);

        return pair;
    }

    /**
     *
      * @param forwardingTable should be from destination to vertex to next-hop
     * @return a LFT with all paths inserted from the forwardinTable
     */
    private LFT generateLFT(Map<Integer, Map<Integer, Integer>> forwardingTable, Graph graph) {
        LFT lft = new LFT(graph);
        boolean success = lft.insertMapFT(forwardingTable);
        assert success;
        return lft;
    }

    private long getPathWeight(Path path, int[][] weights) {
        long pathWeight = 0;
        // Compute the pathWeight
        for (int i = 0; i < path.length() - 1; i++) {
            // For each edge in the path - increase the weights of edges
            pathWeight += weights[path.getPath().get(i)][path.getPath().get(i + 1)];

        }
        return pathWeight;
    }

    synchronized private Path findShortestPathWeights(int src, int dst, int [][] weights, Map<Integer, Map<Integer, Integer>> forwardingTable){
        Queue<Path> Q = new LinkedList<>();

        Q.add(new Path(src));

        // Run BFS to find the shortest path from src to dst
        // with edges according to permutation order
        // with length >= minlength

        long bestPathWeight = Long.MAX_VALUE; // set path weight to "infinity"
        Path bestPath = null;

        while(!Q.isEmpty()) {
            Path p = Q.poll();

            // Get the last vertex from the path
            int last = p.last();

            if (last == dst) {

                // This will not produce any path to dst longer than minimum without loops
                if (p.length() < minLength + 1 || p.length() > maxLength + 1){
                    continue;
                }

                // The path was found -- check if its weights is smaller than actual
                long pathWeight = getPathWeight(p, weights);
                if (pathWeight < bestPathWeight) {
                    bestPathWeight = pathWeight;
                    bestPath = p;
                }

            } else {

                if (p.length() < maxLength + 1)  {

                    // Add to Q all neighbours of last

                    List<Integer> neighbours = new ArrayList<>();

                    if(forwardingTable.containsKey(dst) && forwardingTable.get(dst).containsKey(last))
                        neighbours.add(forwardingTable.get(dst).get(last));
                    else {
                        for (int i = 0; i < graph.getAdjacencyList()[last].size(); i++) {
                            int neighbour = graph.getAdjacencyList()[last].elementAt(i).getLinkTo();
                            if (!p.contains(neighbour))
                                neighbours.add(neighbour);
                        }
                    }

                    // For each neighbour from neighbours

                    for (int neighbour : neighbours) {
                        List<Integer> newPath = new ArrayList<>(p.getPath());
                        newPath.add(neighbour);
                        Path path = new Path(newPath);

                        long pathWeight = getPathWeight(path, weights);
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
                // TODO make this a factory and test different approaches
                weights[bestPath.getPath().get(i)][bestPath.getPath().get(i + 1)] += (i + 1) * (bestPath.length() - 1 - i);

            }
        }

        return bestPath;

    }
    public List<Pair<Graph, LFT>> divideGraphLFT() {
        List<Pair<Graph,LFT>> subgraphsLFT;

        if (this.produceLayers) {

            subgraphsLFT = generateLayersLFT();
            writeLayersToFileLFT(subgraphsLFT);

        } else {
            subgraphsLFT = readLayersFromFileLFT();
        }

        subgraphsLFT.add(new Pair<>(graph, new LFT(graph)));

        return subgraphsLFT;
    }

    private void writeLayersToFileLFT(List<Pair<Graph, LFT>> subgraphsLFT) {
        long startTime = System.currentTimeMillis();

        File folder = new File(DIRECTORY_NAME);
        File[] files = folder.listFiles();
        if (files != null) {
            for (File f : files) {
                if (f.isFile()) {
                    f.delete();
                }
            }
        }
        int i = 0;
        for (Pair<Graph, LFT> pair: subgraphsLFT) {
            i++;
            new PrinterGraph(pair.first()).print(DIRECTORY_NAME + "/layer_" + i + ".txt");
            new PrinterLFT(pair.second()).print(DIRECTORY_NAME + "/lft_" + i + ".txt");
        }
        long estimatedTime = System.currentTimeMillis() - startTime;
        System.out.println("> Writing layers to files time: " + estimatedTime);

    }

    private List<Pair<Graph, LFT>> readLayersFromFileLFT() {
        long startTime = System.currentTimeMillis();

        List<Pair<Graph, LFT>> subgraphs = new ArrayList<>();

        File folder = new File(DIRECTORY_NAME);
        File[] files = folder.listFiles();
        List<File> graphs = new LinkedList<>();
        for(File f: files) {
            if(f.isFile() && f.getName().contains("layer_"))
                graphs.add(f);
        }
        if(graphs.size() > 0) {
            for (File fGraph : graphs) {
                String filenameGraph = fGraph.getName();
                String filenameLFT = filenameGraph.replace("layer_", "lft_");

                Graph g = new Graph("Subgraph", graph.getNumNodes());
                LFT lft = new LFT(graph);
                try {
                    // Open input streams
                    FileInputStream fileStreamGraph = new FileInputStream(DIRECTORY_NAME + "/" + filenameGraph);
                    BufferedReader brGraph = new BufferedReader(new InputStreamReader(fileStreamGraph));
                    FileInputStream fileStreamLFT = new FileInputStream(DIRECTORY_NAME + "/" + filenameLFT);
                    BufferedReader brLFT = new BufferedReader(new InputStreamReader(fileStreamLFT));

                    // Simply read in the server pairs
                    String strLine;
                    while ((strLine = brGraph.readLine()) != null) {

                        // Split line
                        String[] match = strLine.split(" ");
                        int n1 = Integer.parseInt(match[0]);
                        int n2 = Integer.parseInt(match[1]);

                        // Check bounds
                        if (n1 < 0 || n2 < 0 || n1 >= graph.getNumNodes() || n2 >= graph.getNumNodes()) {
                            throw new RuntimeException("Out of bounds link indexes (n=" +  graph.getNumNodes() + "), link: " + n1 + " - " + n2);
                        }

                        if (g.findNeighborIdx(n1, n2) == -1){
                            g.addNeighbor(n1, n2);
                        }
                    }

                    assert lft.putGraph(g);
                    int[][] ft = new int[g.getNumNodes()][g.getNumNodes()];
                    int index = 0;
                    while ((strLine = brLFT.readLine()) != null) {

                        // Split line
                        String[] match = strLine.split(" ");
                        assert match.length == g.getNumNodes();
                        for(int j = 0; j < match.length; j++) {
                            ft[index][j] = Integer.parseInt(match[j]);
                        }
                        index++;
                    }
                    assert index >= g.getNumNodes();
                    boolean success = lft.insertFT(ft);
                    if(!success)
                        throw new RuntimeException("Incompatible graph with lft (filename: " + filenameGraph + ")");

                    // Close input streams
                    brGraph.close();
                    brLFT.close();
                } catch (Exception e) {
                    e.printStackTrace();
                    throw new RuntimeException("FileGraph: I/O exception thrown, graph could not be generated. " + filenameGraph);
                }

                subgraphs.add(new Pair<Graph, LFT>(g, lft));
            }
        }

        long estimatedTime = System.currentTimeMillis() - startTime;
        System.out.println("> Reading files time: " + estimatedTime);


        return getSampledLayersLFT(subgraphs);
    }
}
