package ch.ethz.topobench.graph.patheval;

import ch.ethz.topobench.graph.Graph;
import java.util.*;


public class LayerPathEvaluator extends PathEvaluator {

    private List<PathEvaluator> layers;

    public LayerPathEvaluator(Graph graph, List<PathEvaluator> layers) {
        super(graph);
        this.layers = layers;
    }

    public List<PathEvaluator> getLayers() {
        return layers;
    }


    @Override
    public boolean isFlowZero(int src, int dst, int linkFrom, int linkTo) {
        return false;
    }


}
