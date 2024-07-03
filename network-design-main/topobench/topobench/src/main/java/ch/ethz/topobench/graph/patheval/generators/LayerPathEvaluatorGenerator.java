package ch.ethz.topobench.graph.patheval.generators;

import ch.ethz.topobench.graph.Graph;
import ch.ethz.topobench.graph.LFT;
import ch.ethz.topobench.graph.SelectorResult;
import ch.ethz.topobench.graph.patheval.LayerPathEvaluator;
import ch.ethz.topobench.graph.patheval.PathEvaluator;
import ch.ethz.topobench.graph.patheval.PathEvaluatorSelector;
import ch.ethz.topobench.graph.subgraphs.ImprovedPriorityWeightedAlgorithm;
import ch.ethz.topobench.graph.subgraphs.SubgraphsGenerator;
import ch.ethz.topobench.graph.subgraphs.SubgraphsGeneratorSelector;
import ch.ethz.topobench.graph.utility.CmdAssistant;
import edu.asu.emit.algorithm.utils.Pair;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.Options;

import java.util.ArrayList;
import java.util.List;

import static ch.ethz.topobench.graph.utility.CmdAssistant.parseOptions;

public class LayerPathEvaluatorGenerator implements  PathEvaluatorGenerator {

    ArrayList<PathEvaluator> layers;

    @Override
    public SelectorResult<PathEvaluator> generate(Graph graph, String[] args) {

        // Parse the options
        Options options = new Options();
        CmdAssistant.addOption(options, "eval", "evaluator", true,
                "algorithm for the layers path evaluators");
        CmdAssistant.addOption(options, "div", "division", true,
                "algorithm for the division of graph into layers (subgraphs)");
        CommandLine cmd = parseOptions(options, args, true);


        // Read in parameters
        String pathEvaluatorEnc = cmd.getOptionValue("evaluator", "INVALID");
        PathEvaluatorSelector.Type pathEvaluatorType = PathEvaluatorSelector.getPathEvaluator(pathEvaluatorEnc);
        if (pathEvaluatorType == null) {
            throw new RuntimeException("FATAL: argument pathEvaluator does not encode to a valid path evaluator with string " + pathEvaluatorEnc + ".");
        }
        System.out.println(" > Choosing " + pathEvaluatorEnc + " as path evaluator for the layers...");

        String subgraphsGeneratorEnc = cmd.getOptionValue("division", "INVALID");
        SubgraphsGeneratorSelector.Type subgraphsGeneratorType = SubgraphsGeneratorSelector.getSubgraphGenerator(subgraphsGeneratorEnc);
        if (subgraphsGeneratorType == null) {
            throw new RuntimeException("FATAL: argument subgraphGenerator does not encode to a valid subgraph generator with string " + subgraphsGeneratorEnc + ".");
        }
        System.out.println(" > Choosing " + subgraphsGeneratorEnc + " as algorithm of generating the layers...");


        System.out.println(" > Generating layers...");
        SelectorResult<SubgraphsGenerator> subgraphsGeneratorSelectorResult = SubgraphsGeneratorSelector.select(subgraphsGeneratorType, graph, cmd.getArgs());
        SubgraphsGenerator subgraphsGenerator = subgraphsGeneratorSelectorResult.getResult();
        String[] remainingArguments;
        if(subgraphsGenerator instanceof ImprovedPriorityWeightedAlgorithm) {
            assert pathEvaluatorType == PathEvaluatorSelector.Type.LFT;
            List<Pair<Graph, LFT>> subgraphsLFT = ((ImprovedPriorityWeightedAlgorithm) subgraphsGenerator).divideGraphLFT();
            remainingArguments = allocateLayersListLFT(subgraphsLFT, subgraphsGeneratorSelectorResult.getRemainingArgs());

        } else {
            List<Graph> subgraphs = subgraphsGenerator.divideGraph();
            // Allocate the layers list
            remainingArguments = allocateLayersList(subgraphs, pathEvaluatorType, subgraphsGeneratorSelectorResult.getRemainingArgs());
        }

        // Create path evaluator
        return new SelectorResult<>(new LayerPathEvaluator(graph, layers), remainingArguments);
    }

    private String[] allocateLayersList(List<Graph> subgraphs, PathEvaluatorSelector.Type pathEvaluatorType,
                                    String[] layersPathEvaluatorArgs) {

        layers = new ArrayList<>(subgraphs.size());

        String [] remainingArguments = {};

        for (Graph subgraph : subgraphs) {
            SelectorResult<PathEvaluator> pathEvaluatorSelectorResult = PathEvaluatorSelector.select(pathEvaluatorType,
                    subgraph, layersPathEvaluatorArgs);
            layers.add(pathEvaluatorSelectorResult.getResult());

            if (remainingArguments == null || remainingArguments.length == 0) {
                remainingArguments = pathEvaluatorSelectorResult.getRemainingArgs();
            }
        }

        return remainingArguments;
    }

    private String[] allocateLayersListLFT(List<Pair<Graph, LFT>> subgraphsLFT, String[] layersPathEvaluatorArgs) {

        layers = new ArrayList<>(subgraphsLFT.size());

        String [] remainingArguments = {};

        for (Pair<Graph, LFT> pair: subgraphsLFT) {
            SelectorResult<PathEvaluator> pathEvaluatorSelectorResult = new LFTPathEvaluatorGenerator().generate(pair.first(), pair.second(), layersPathEvaluatorArgs);
            layers.add(pathEvaluatorSelectorResult.getResult());

            if (remainingArguments == null || remainingArguments.length == 0) {
                remainingArguments = pathEvaluatorSelectorResult.getRemainingArgs();
            }
        }

        return remainingArguments;
    }

}

