package ch.ethz.topobench.graph.subgraphs.generators;

import ch.ethz.topobench.graph.Graph;
import ch.ethz.topobench.graph.SelectorResult;
import ch.ethz.topobench.graph.subgraphs.SubgraphsGenerator;

interface SubgraphsGeneratorGenerator {
    SelectorResult<SubgraphsGenerator> generate(Graph graph, String[] args);
}
