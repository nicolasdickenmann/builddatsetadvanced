package ch.ethz.topobench.graph.patheval;

import ch.ethz.topobench.graph.Graph;
import ch.ethz.topobench.graph.LFT;

import java.util.ArrayList;
import java.util.List;

public class LFTPathEvaluator extends PathEvaluator {

    private LFT forwardingTable;

    public LFTPathEvaluator(Graph graph) {
        super(graph);
        this.forwardingTable = new LFT(graph);
        forwardingTable.fillRemainingEntries();
    }

    public LFTPathEvaluator(Graph graph, LFT forwardingTable) {
        super(graph);
        assert forwardingTable.putGraph(graph);
        this.forwardingTable = forwardingTable;
        forwardingTable.fillRemainingEntries();
    }

    public List<Integer> getPath(int u, int v) {
        List<Integer> path = forwardingTable.getPath(u, v);
        if (path == null) {
            path = new ArrayList<>();
        }
        return path;
    }

    @Override
    public boolean isFlowZero(int src, int dst, int linkFrom, int linkTo) {

        // Restore the shortest path from src to dst and check if it contains the edge (linkFrom, linkTo)
        List<Integer> path = getPath(src, dst);
        if (path.size() <= 0){
            return true;
        }
        int start = path.get(0);
        for (int i = 1; i < path.size(); i++) {
            if(start == linkFrom && path.get(i) == linkTo)
                return false;
            start = path.get(i);
        }
        return true;
    }
}
