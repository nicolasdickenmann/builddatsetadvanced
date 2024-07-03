package ch.ethz.topobench.graph.patheval.generators;

import ch.ethz.topobench.graph.Graph;
import ch.ethz.topobench.graph.LFT;
import ch.ethz.topobench.graph.SelectorResult;
import ch.ethz.topobench.graph.patheval.LFTPathEvaluator;
import ch.ethz.topobench.graph.patheval.PathEvaluator;

public class LFTPathEvaluatorGenerator implements PathEvaluatorGenerator {

    @Override
    public SelectorResult<PathEvaluator> generate(Graph graph, String[] args) {
        return new SelectorResult<>(new LFTPathEvaluator(graph), args);
    }

    public SelectorResult<PathEvaluator> generate(Graph graph, LFT lft, String[] args) {
        return new SelectorResult<>(new LFTPathEvaluator(graph, lft), args);
    }
}
