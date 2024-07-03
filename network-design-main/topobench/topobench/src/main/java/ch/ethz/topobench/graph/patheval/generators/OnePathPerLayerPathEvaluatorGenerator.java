package ch.ethz.topobench.graph.patheval.generators;

import ch.ethz.topobench.graph.Graph;
import ch.ethz.topobench.graph.SelectorResult;
import ch.ethz.topobench.graph.patheval.OnePathPerLayerPathEvaluator;
import ch.ethz.topobench.graph.patheval.PathEvaluator;

public class OnePathPerLayerPathEvaluatorGenerator implements PathEvaluatorGenerator {
    @Override
    public SelectorResult<PathEvaluator> generate(Graph graph, String[] args) {

        // Create path evaluator
        return new SelectorResult<>(new OnePathPerLayerPathEvaluator(graph), args);
    }
}
