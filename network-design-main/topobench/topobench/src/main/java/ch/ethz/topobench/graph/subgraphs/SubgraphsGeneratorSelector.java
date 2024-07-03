package ch.ethz.topobench.graph.subgraphs;

import ch.ethz.topobench.graph.Graph;
import ch.ethz.topobench.graph.SelectorResult;
import ch.ethz.topobench.graph.subgraphs.generators.*;

import static ch.ethz.topobench.graph.subgraphs.SubgraphsGeneratorSelector.Type.*;

public class SubgraphsGeneratorSelector {

    public enum Type {
        SPAIN,
        RANDOM_DAGS,
        FAT_PATHS,
        KSSPMA,
        PRIORITY_WEIGHTED,
        IMPROVED_PRIORITY_WEIGHTED
    }

    /**
     * Map subgraphs generators type to its string representation.
     *
     * @param sg   Subgraph generator type
     *
     * @return String representation
     */
    private static String getSubgraphsGeneratorsRepresentation(Type sg) {
        switch(sg) {
            case SPAIN:                     return "SPAIN";
            case RANDOM_DAGS:               return "RANDOM_DAGS";
            case FAT_PATHS:                 return "FAT_PATHS";
            case KSSPMA:                    return "KSSPMA";
            case PRIORITY_WEIGHTED:         return "PRIORITY_WEIGHTED";
            case IMPROVED_PRIORITY_WEIGHTED: return "IMPROVED_PRIORITY_WEIGHTED";
            default:                        throw new RuntimeException("SubgraphsGeneratorSelector: getTrafficModeRepresentation: cannot select illegal subgraph generator type");
        }
    }

    /**
     * Get the correct subgraph generator
     *
     * @param i     Subgraph generator encoding string
     *
     * @return  Subgraph generator type
     */
    public static SubgraphsGeneratorSelector.Type getSubgraphGenerator(String i) {
        switch (i) {
            case "SPAIN":                     return SPAIN;
            case "RANDOM_DAGS":               return RANDOM_DAGS;
            case "FAT_PATHS":                 return FAT_PATHS;
            case "KSSPMA":                    return KSSPMA;
            case "PRIORITY_WEIGHTED":         return PRIORITY_WEIGHTED;
            case "IMPROVED_PRIORITY_WEIGHTED": return IMPROVED_PRIORITY_WEIGHTED;
            default:                          return null;
        }
    }

    /**
     * Generate the subgraph generator for the given graph.
     *
     * @param sgType            Subgraphs generator type
     * @param graph             Graph over which to generate subgraph generator
     * @param remainingArgs     Arguments
     *
     * @return  Selection result (passes on trailing unused parameters)
     */
    public static SelectorResult<SubgraphsGenerator> select(SubgraphsGeneratorSelector.Type sgType, Graph graph, String[] remainingArgs) {

        switch(sgType) {
            case SPAIN:                     return new SPAINGenerator().generate(graph, remainingArgs);
            case RANDOM_DAGS:               return new RandomDAGsGenerator().generate(graph, remainingArgs);
            case FAT_PATHS:                 return new FatPathsOriginalGenerator().generate(graph, remainingArgs);
            case KSSPMA:                    return new kSSPMAGenerator().generate(graph, remainingArgs);
            case PRIORITY_WEIGHTED:         return new PriorityWeightedAlgorithmGenerator().generate(graph, remainingArgs);
            case IMPROVED_PRIORITY_WEIGHTED: return new ImprovedPriorityWeightedAlgorithmGenerator().generate(graph, remainingArgs);
            default:                        throw new RuntimeException("SubgraphsGeneratorSelector: select: cannot select illegal subgraphs generator type");
        }

    }

    /**
     * Retrieve the list of all subgraph generators.
     *
     * @return  String of all subgraphs generators algorithms (e.g. "SPAIN")
     */
    public static String getSubgraphsGenerators() {
        StringBuilder res = new StringBuilder();
        boolean first = true;
        for (Type sg : Type.values()) {
            if (first) {
                first = false;
            } else {
                res.append(", ");
            }
            res.append(getSubgraphsGeneratorsRepresentation(sg));
        }
        return res.toString();
    }

}