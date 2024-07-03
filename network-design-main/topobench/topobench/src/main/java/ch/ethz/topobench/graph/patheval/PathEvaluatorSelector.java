/* *******************************************************
 * Released under the MIT License (MIT) --- see LICENSE
 * Copyright (c) 2014 Ankit Singla, Sangeetha Abdu Jyothi,
 * Chi-Yao Hong, Lucian Popa, P. Brighten Godfrey,
 * Alexandra Kolla, Simon Kassing
 * ******************************************************** */

package ch.ethz.topobench.graph.patheval;

import ch.ethz.topobench.graph.Graph;
import ch.ethz.topobench.graph.SelectorResult;
import ch.ethz.topobench.graph.patheval.generators.*;

import static ch.ethz.topobench.graph.patheval.PathEvaluatorSelector.Type.*;

public class PathEvaluatorSelector {

    public enum Type {
        SLACK,
        NEIGHBOR,
        K_SHORTEST_PATHS,
        VALIANT,
        LAYER,
        ONE_PATH,
        PAST,
        LFT
    }

    /**
     * Map path evaluator type to its string representation.
     *
     * @param pe    Path evaluator type
     *
     * @return String representation
     */
    private static String getPathEvaluatorRepresentation(Type pe) {
        switch(pe) {
            case SLACK:             return "SLACK";
            case NEIGHBOR:          return "NEIGH";
            case K_SHORTEST_PATHS:  return "KSHRT";
            case VALIANT:           return "VALIA";
            case LAYER:             return "LAYER";
            case ONE_PATH:          return "ONE_PATH";
            case PAST:              return "PAST";
            case LFT:               return "LFT";
            default:                throw new RuntimeException("PathEvaluatorSelector: getTrafficModeRepresentation: cannot select illegal path evaluator type");
        }
    }

    /**
     * Get the correct path evaluator
     *
     * @param i     Path evaluator encoding string
     *
     * @return  Path evaluator type
     */
    public static PathEvaluatorSelector.Type getPathEvaluator(String i) {
        switch (i) {
            case "SLACK":       return SLACK;
            case "NEIGH":       return NEIGHBOR;
            case "KSHRT":       return K_SHORTEST_PATHS;
            case "VALIA":       return VALIANT;
            case "LAYER":       return LAYER;
            case "ONE_PATH":    return ONE_PATH;
            case "PAST":        return PAST;
            case "LFT":         return LFT;
            default:            return null;
        }
    }

    /**
     * Generate the path evaluator for the given graph.
     *
     * @param peType            Path evaluator type
     * @param graph             Graph over which to generate path evaluator
     * @param remainingArgs     Arguments
     *
     * @return  Selection result (passes on trailing unused parameters)
     */
    public static SelectorResult<PathEvaluator> select(PathEvaluatorSelector.Type peType, Graph graph, String[] remainingArgs) {

        switch(peType) {
            case SLACK:             return new SlackPathEvaluatorGenerator().generate(graph, remainingArgs);
            case NEIGHBOR:          return new NeighborPathEvaluatorGenerator().generate(graph, remainingArgs);
            case K_SHORTEST_PATHS:  return new KShortestPathEvaluatorGenerator().generate(graph, remainingArgs);
            case VALIANT:           return new ValiantLBPathEvaluatorGenerator().generate(graph, remainingArgs);
            case LAYER:             return new LayerPathEvaluatorGenerator().generate(graph, remainingArgs);
            case ONE_PATH:          return new OnePathPerLayerPathEvaluatorGenerator().generate(graph, remainingArgs);
            case PAST:              return new PASTPathEvaluatorGenerator().generate(graph, remainingArgs);
            case LFT:               return new LFTPathEvaluatorGenerator().generate(graph, remainingArgs);
            default:                throw new RuntimeException("PathEvaluatorSelector: select: cannot select illegal path evaluator type");
        }

    }

    /**
     * Retrieve the list of all path evaluators.
     *
     * @return  String of all traffic modes (e.g. "SLACK, NEIGHBOR")
     */
    public static String getPathEvaluators() {
        StringBuilder res = new StringBuilder();
        boolean first = true;
        for (Type pe : Type.values()) {
            if (first) {
                first = false;
            } else {
                res.append(", ");
            }
            res.append(getPathEvaluatorRepresentation(pe));
        }
        return res.toString();
    }

}