package ch.ethz.topobench.graph.subgraphs.generators;

import ch.ethz.topobench.graph.Graph;
import ch.ethz.topobench.graph.SelectorResult;
import ch.ethz.topobench.graph.subgraphs.SubgraphsGenerator;
import ch.ethz.topobench.graph.subgraphs.kSSPMA;
import ch.ethz.topobench.graph.utility.ArgumentValidator;
import ch.ethz.topobench.graph.utility.CmdAssistant;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.Options;

import static ch.ethz.topobench.graph.utility.CmdAssistant.parseOptions;

public class kSSPMAGenerator implements SubgraphsGeneratorGenerator {

    public SelectorResult<SubgraphsGenerator> generate(Graph graph, String[] args) {

        // Parse the options
        Options options = new Options();
        CmdAssistant.addOption(options, "layers", "number of layers");
        CmdAssistant.addOption(options, "k", "the number of k-shortest simple paths");
        CmdAssistant.addOption(options, "minLength", "the minimum length of paths");

        CmdAssistant.addOption(options, "threads", "number of threads in case of running the program in parallel");
        CmdAssistant.addOption(options, "produce", "produce layers (1) or read them from files (0)");

        CommandLine cmd = parseOptions(options, args, true);

        // Read in parameters
        int layers = ArgumentValidator.retrieveInteger("layers", cmd.getOptionValue("layers"));
        int k = ArgumentValidator.retrieveInteger("k", cmd.getOptionValue("k"));
        int minLength = ArgumentValidator.retrieveInteger("minLength", cmd.getOptionValue("minLength"));

        int threads = ArgumentValidator.retrieveInteger("threads", cmd.getOptionValue("threads"));
        boolean produceLayers = ArgumentValidator.retrieveBoolean("produce", cmd.getOptionValue("produce"));


        // Create subgraphs generator
        return new SelectorResult<>(new kSSPMA(layers, k, minLength, threads, graph, produceLayers), cmd.getArgs());
    }
}
