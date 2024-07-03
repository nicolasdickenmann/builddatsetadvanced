package ch.ethz.topobench.graph.subgraphs.generators;

import ch.ethz.topobench.graph.Graph;
import ch.ethz.topobench.graph.SelectorResult;
import ch.ethz.topobench.graph.subgraphs.ImprovedPriorityWeightedAlgorithm;
import ch.ethz.topobench.graph.subgraphs.SubgraphsGenerator;
import ch.ethz.topobench.graph.utility.ArgumentValidator;
import ch.ethz.topobench.graph.utility.CmdAssistant;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.Options;

import static ch.ethz.topobench.graph.utility.CmdAssistant.parseOptions;

public class ImprovedPriorityWeightedAlgorithmGenerator implements SubgraphsGeneratorGenerator {
    @Override
    public SelectorResult<SubgraphsGenerator> generate(Graph graph, String[] args) {

        // Parse the options
        Options options = new Options();
        CmdAssistant.addOption(options, "layers", "number of layers");
        CmdAssistant.addOption(options, "M", "the number of paths in each layer");
        CmdAssistant.addOption(options, "minLength", "the minimum length of paths");
        CmdAssistant.addOption(options, "diam", "the network diameter");
        CmdAssistant.addOption(options, "threads", "number of threads in case of running the program in parallel");
        CmdAssistant.addOption(options, "produce", "produce layers (1) or read them from files (0)");

        CommandLine cmd = parseOptions(options, args, true);

        // Read in parameters
        int layers = ArgumentValidator.retrieveInteger("layers", cmd.getOptionValue("layers"));
        int M = ArgumentValidator.retrieveInteger("M", cmd.getOptionValue("M"));
        int diam = ArgumentValidator.retrieveInteger("diam", cmd.getOptionValue("diam"));
        int minLength = ArgumentValidator.retrieveInteger("minLength", cmd.getOptionValue("minLength"));
        int threads = ArgumentValidator.retrieveInteger("threads", cmd.getOptionValue("threads"));
        boolean produceLayers = ArgumentValidator.retrieveBoolean("produce", cmd.getOptionValue("produce"));

        // Create subgraphs generator
        return new SelectorResult<>(new ImprovedPriorityWeightedAlgorithm(layers, M, minLength, diam, threads, graph, produceLayers), cmd.getArgs());
    }
}
