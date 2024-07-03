package ch.ethz.topobench.graph;

import ch.ethz.topobench.Main;
import edu.asu.emit.algorithm.utils.Pair;

import java.util.*;

public class LFT {
    private Graph graph;
    private int[][] forwardingTable;
    private boolean immutable;
    private List<Map<Integer, Integer>> edge_weights;


    public LFT(Graph graph) {
        this.graph = graph;
        immutable = false;
        initializeFT();
    }

    public LFT(Graph graph, List<List<Integer>> paths) {
        this.graph = graph;
        immutable = false;
        initializeFT();
        for(List<Integer> path : paths) {
            insertPath(path);
        }
    }

    private void initializeFT() {
        if(!immutable) {
            this.forwardingTable = new int[graph.numNodes][graph.numNodes];
            for (int i = 0; i < graph.getNumNodes(); i++) {
                for (int j = 0; j < graph.getNumNodes(); j++) {
                    forwardingTable[i][j] = -1;
                }
            }
        }

    }

    public boolean putGraph(Graph graph1) {
        if(immutable || !verifyForwardingTable(graph1))
            return false;
        if (!graph1.toString().equals(graph.toString()))
            graph = graph1;
        return true;
    }
    private boolean verifyForwardingTable(Graph graph1) {
        for(int i = 0; i < forwardingTable.length; i ++){
            for(int j = 0; j< forwardingTable[0].length; j++){
                if (forwardingTable[i][j] > -1 && graph1.findNeighborIdx(i, forwardingTable[i][j]) < 0)
                    return false;
            }
        }
        return true;
    }

    public Graph getGraph() {
        return graph;
    }

    public int nextHop(int current, int destination) {
        assert current < forwardingTable.length && destination < forwardingTable[0].length;
        return forwardingTable[current][destination];
    }

    public List<Integer> getPath(int source, int destination) {
        List<Integer> out = new ArrayList<>();
        if (source == destination)
            return out;
        if (forwardingTable[source][destination] == -1)
            return null;
        out.add(source);
        int next = forwardingTable[source][destination];
        while (next != destination) {
            if(next == -1) {
                throw new RuntimeException("The forwarding table is in an inconsistent state");
            }
            out.add(next);
            next = forwardingTable[next][destination];
        }
        out.add(destination);
        return out;
    }

    /**
     * Will reset the forwardingTable to ft (copied) if the graph allows to do so. Very dangerous if FT contains errors.
     * @param ft the new forwarding table
     * @return true iff ft was compatible with the graph and forwardingTable was updated
     */
    public boolean insertFT(int[][] ft) {
        int[][] backup = forwardingTable.clone();
        assert(backup != forwardingTable);
        if(immutable || ft.length != graph.getNumNodes() || ft[0].length != graph.getNumNodes())
            return false;
        for(int i = 0; i < forwardingTable.length; i++) {
            for(int j = 0; j < forwardingTable.length; j++) {
                forwardingTable[i][j] = ft[i][j];
                if((i == j && forwardingTable[i][j] != -1) || (forwardingTable[i][j] != -1 && graph.findNeighborIdx(i,forwardingTable[i][j]) < 0)) {
                    forwardingTable = backup;
                    return false;
                }
            }
        }
        return true;
    }

    /**
     * Will reset the forwardingTable and put values of ft inside. Should be used with caution as all previous values will be resetted.
     * @param ft should be from destination to vertex to next-hop
     * @return Returns true iff the setting of the forwardingTable was successful
     */
    public boolean insertMapFT(Map<Integer, Map<Integer, Integer>> ft) {
        int[][] backup = forwardingTable.clone();
        assert(backup != forwardingTable);
        if (immutable)
            return false;
        initializeFT();
        for(int destination: ft.keySet()) {
            if(ft.get(destination) != null) {
                for(int source: ft.get(destination).keySet()) {
                    if(source == destination)
                        continue;
                    forwardingTable[source][destination] = ft.get(destination).get(source);
                    if(graph.findNeighborIdx(source, forwardingTable[source][destination]) < 0) {
                        forwardingTable = backup;
                        return false;
                    }
                }
            }
        }
        return true;
    }

    /**
     * Adds path to the linear forwarding table
     * @param path List containing the full path, including source and destination.
     * @return Returns a negative number if the path could not be inserted due to missing edges or the number of overwritten entries.
     */
    public int insertPath(List<Integer> path) {
        if (!immutable && verifyPath(path)) {
            int destination = path.get(path.size()-1);
            int count = 0;
            for(int i = 0; i < path.size() -1; i++) {
                if (forwardingTable[path.get(i)][destination] != -1)
                    count++;
                forwardingTable[path.get(i)][destination] = path.get(i+1);
            }
            return count;
        }
        return -1;
    }

    private boolean verifyPath(List<Integer> path) {
        if (path.size() < 2)
            return false;
        Iterator<Integer> itr = path.iterator();
        int current = itr.next();
        while (itr.hasNext()) {
            int next = itr.next();
            if (graph.findNeighborIdx(current, next) < 0) {
                return false;
            }
        }
        return true;
    }
    public void fillRemainingEntries() {
        if(!immutable) {
            int [][] cp = forwardingTable.clone();
            initEdgeWeights();
            establishFixPathsWeights();
            int[] distanceDestination = new int[forwardingTable.length];
            int[] nextHop = new int[forwardingTable.length];

            List<Integer> destinations = new ArrayList<>(forwardingTable.length);
            for(int i = 0; i < forwardingTable.length; i++) {
               destinations.add(i);
            }
            Collections.shuffle(destinations, Main.universalRand);
            for(int destination: destinations) {
                recomputeWeightsDestination(destination, distanceDestination, nextHop);
                fillRemainingEntries(destination, distanceDestination, nextHop);
            }
            for(int i = 0; i < forwardingTable.length; i++) {
                for(int j = 0; j <forwardingTable.length; j++) {
                    assert cp[i][j] == -1 || cp[i][j] == forwardingTable[i][j];
                }
            }
            immutable = true;
        }
    }

    private void fillRemainingEntries(int destination, int[] distanceDestination, int[] nextHop) {
        PriorityQueue<Pair<Integer, Integer>> pq = initPQ(distanceDestination);
        Set<Integer> fixed = new HashSet<>(pq.size());
        for(Pair<Integer, Integer> pair: pq)
            fixed.add(pair.first());
        while(!pq.isEmpty()) {
            Pair<Integer, Integer> pair = pq.poll();
            if(pair.second() > distanceDestination[pair.first()])
                continue;
            for(Link link: graph.getAdjacencyList()[pair.first()]) {
                int node = link.getLinkTo();
                if(!fixed.contains(node) && pair.second() + edge_weights.get(node).get(pair.first()) < distanceDestination[node]) {
                    distanceDestination[node] = pair.second() + edge_weights.get(node).get(pair.first());
                    nextHop[node] = pair.first();
                    pq.add(new Pair<>(node, distanceDestination[node]));
                }
            }
        }

        int[] unused1 = new int[forwardingTable.length];
        int[] unused2 = new int[forwardingTable.length];
        changeFixPathsWeights(destination, unused1, unused2, false);
        for(int node = 0; node < nextHop.length; node++) {
            forwardingTable[node][destination] = nextHop[node];
        }
        changeFixPathsWeights(destination, unused1, unused2, true);

    }

    private void establishFixPathsWeights() {
        int[] nextHop = new int[forwardingTable.length];
        int[] unused = new int[forwardingTable.length];
        for(int destination = 0; destination < edge_weights.size(); destination++) {
            changeFixPathsWeights(destination, nextHop, unused,true);
        }
    }
    private void changeFixPathsWeights(int destination, int[] nextHop, int[] unused, boolean add) {
        recomputeWeightsDestination(destination, unused, nextHop);
        int[] numSenders = numSenders(nextHop, destination);
        for(int sender = 0; sender < nextHop.length; sender++) {
            int inc = 1 + numSenders[sender];
            if(nextHop[sender] > -1)
                edge_weights.get(sender).computeIfPresent(nextHop[sender], (k, a) -> (add) ? a + inc: a - inc);
        }
    }
    private void recomputeWeightsDestination(int destination, int[] distanceDestination, int[] nextHop) {
        Arrays.fill(distanceDestination, Integer.MAX_VALUE);
        distanceDestination[destination] = 0;
        for(int i = 0; i < nextHop.length; i++) {
            nextHop[i] = forwardingTable[i][destination];
        }
        for(int i = 0; i < nextHop.length; i++) {
            if (nextHop[i] != -1)
                computeDistance(i, distanceDestination, nextHop);
        }
    }

    private PriorityQueue<Pair<Integer, Integer>> initPQ(int[] distanceDestination) {
        PriorityQueue<Pair<Integer, Integer>> pq = new PriorityQueue<>(forwardingTable.length / 2, Comparator.comparingInt(Pair::second));
        for(int i = 0; i < distanceDestination.length; i++) {
            if (distanceDestination[i] < Integer.MAX_VALUE) {
                pq.add(new Pair<>(i, distanceDestination[i]));
            }
        }
        return pq;
    }
    private void computeDistance(int node, int[] distanceDestination, int[] nextHop) {
        if(distanceDestination[node] < Integer.MAX_VALUE)
            return;
        assert nextHop[node] != -1;
        computeDistance(nextHop[node], distanceDestination, nextHop);
        distanceDestination[node] = distanceDestination[nextHop[node]] + edge_weights.get(node).get(nextHop[node]);
    }

    private void initEdgeWeights() {
        edge_weights = new ArrayList<>(graph.getNumNodes());
        for(int i = 0; i < graph.getNumNodes(); i++) {
            HashMap<Integer, Integer> map = new HashMap<>();
            edge_weights.add(map);
            for(Link link: graph.getAdjacencyList()[i]) {
                map.put(link.getLinkTo(), graph.getNumNodes() * graph.getNumNodes());
            }
        }
    }
    private int[] numSenders(int[] nextHop, int destination) {
        List<List<Integer>> receivesFrom = new ArrayList<>(nextHop.length);
        for(int i = 0; i < nextHop.length; i++)
            receivesFrom.add(new LinkedList<>());

        for(int sender = 0; sender < nextHop.length; sender++) {
            if(nextHop[sender] > -1) {
                receivesFrom.get(nextHop[sender]).add(sender);
            }
        }

        int[] numSenders = new int[nextHop.length];
        Arrays.fill(numSenders, -1);
        computeSenders(destination, receivesFrom, numSenders);

        return numSenders;
    }

    /**
     * Runs for ever, if the paths are cyclic. Shouldn't not be the case.
     * @param destination
     * @param receivesFrom
     * @param numSenders
     */
    private void computeSenders(int destination, List<List<Integer>> receivesFrom, int[] numSenders) {
        if(numSenders[destination] > -1)
            return;
        numSenders[destination] = 0;
        for(int sender: receivesFrom.get(destination)) {
            computeSenders(sender, receivesFrom, numSenders);
            numSenders[destination] += numSenders[sender] + 1;
        }
    }
}
