package ch.ethz.topobench.graph.patheval.generators;

import ch.ethz.topobench.graph.Graph;
import ch.ethz.topobench.graph.SelectorResult;
import ch.ethz.topobench.graph.patheval.PASTPathEvaluator;
import ch.ethz.topobench.graph.patheval.PathEvaluator;
import ch.ethz.topobench.graph.utility.ArgumentValidator;
import ch.ethz.topobench.graph.utility.CmdAssistant;
import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.Options;

import java.util.Arrays;

public class PASTPathEvaluatorGenerator implements PathEvaluatorGenerator {


    @Override
    public SelectorResult<PathEvaluator> generate(Graph graph, String[] args) {

        Options options = new Options();
        CmdAssistant.addOption(options, "type", "Type of algorithm (the default one is the Baseline PAST algorithm)");
        CmdAssistant.addOption(options, "nm", "Non-minimal PAST");
        CmdAssistant.addOption(options, "pd", "Path Diversity");

        // Parse the options
        CommandLine cmd = CmdAssistant.parseOptions(options, args, true);

        String type = cmd.getOptionValue("type");
        boolean nonMinimal = ArgumentValidator.retrieveBoolean("nm", cmd.getOptionValue("nm"));
        int pathDiversity = ArgumentValidator.retrieveInteger("pd", cmd.getOptionValue("pd"));

        if (nonMinimal)
            type = "NM_" + type;

        // Return path evaluator
        return new SelectorResult<>(new PASTPathEvaluator(graph, type.toUpperCase(), pathDiversity), cmd.getArgs());
    }
}

