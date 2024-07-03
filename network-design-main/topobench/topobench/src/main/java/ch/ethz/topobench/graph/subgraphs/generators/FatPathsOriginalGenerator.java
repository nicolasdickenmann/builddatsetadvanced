package ch.ethz.topobench.graph.subgraphs.generators;

import ch.ethz.topobench.graph.Graph;
import ch.ethz.topobench.graph.SelectorResult;
import ch.ethz.topobench.graph.subgraphs.FatPathsOriginal;
import ch.ethz.topobench.graph.subgraphs.SubgraphsGenerator;
import ch.ethz.topobench.graph.utility.ArgumentValidator;
import ch.ethz.topobench.graph.utility.CmdAssistant;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.Options;

import static ch.ethz.topobench.graph.utility.CmdAssistant.parseOptions;

public class FatPathsOriginalGenerator  implements SubgraphsGeneratorGenerator {

    @Override
    public SelectorResult<SubgraphsGenerator> generate(Graph graph, String[] args) {

        // Parse the options
        Options options = new Options();
        CmdAssistant.addOption(options, "number", "number of layers");
        CmdAssistant.addOption(options, "fraction", "fraction of paths, that should be removed in each of new layers");
        CmdAssistant.addOption(options, "produce", "produce layers (1) or read them from files (0)");

        CommandLine cmd = parseOptions(options, args, true);

        // Read in parameters
        int number = ArgumentValidator.retrieveInteger("number", cmd.getOptionValue("number"));
        double fraction = ArgumentValidator.retrieveDouble("fraction", cmd.getOptionValue("fraction"));
        boolean produceLayers = ArgumentValidator.retrieveBoolean("produce", cmd.getOptionValue("produce"));

        return new SelectorResult<>(new FatPathsOriginal(graph, number, fraction, produceLayers), cmd.getArgs());
    }
}
