package ch.ethz.topobench.graph.subgraphs;

import ch.ethz.topobench.graph.Graph;
import ch.ethz.topobench.graph.print.PrinterGraph;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;


public abstract class SubgraphsGenerator {

    protected Graph graph;
    protected boolean produceLayers;
    protected String DIRECTORY_NAME = "temp_layers";

    public SubgraphsGenerator(Graph graph, boolean produceLayers) {
        this.graph = graph;
        this.produceLayers = produceLayers;
    }

    public List<Graph> divideGraph() {

        List<Graph> subgraphs;

        if (this.produceLayers) {

            subgraphs = generateLayers();
            writeLayersToFile(subgraphs);

        } else {
            subgraphs = readLayersFromFile();
        }

        subgraphs.add(graph);

        return subgraphs;
    }

    protected abstract List<Graph> generateLayers();

    private List<Graph> readLayersFromFile() {

        long startTime = System.currentTimeMillis();

        List<Graph> subgraphs = new ArrayList<>();

        File folder = new File(DIRECTORY_NAME);
        File[] files = folder.listFiles();
        if (files != null) {

            for (File f : files) {
                if (f.isFile()) {

                    String filename = f.getName();
                    Graph g = new Graph("Subgraph", graph.getNumNodes());

                    try {

                        // Open input stream
                        FileInputStream fileStream = new FileInputStream(DIRECTORY_NAME + "/" + filename);
                        BufferedReader br = new BufferedReader(new InputStreamReader(fileStream));

                        // Simply read in the server pairs
                        String strLine;
                        while ((strLine = br.readLine()) != null) {

                            // Split line
                            String[] match = strLine.split(" ");
                            int n1 = Integer.valueOf(match[0]);
                            int n2 = Integer.valueOf(match[1]);

                            // Check bounds
                            if (n1 < 0 || n2 < 0 || n1 >= graph.getNumNodes() || n2 >= graph.getNumNodes()) {
                                throw new RuntimeException("Out of bounds link indexes (n=" +  graph.getNumNodes() + "), link: " + n1 + " - " + n2);
                            }

                            if (g.findNeighborIdx(n1, n2) == -1){
                                g.addNeighbor(n1, n2);
                            }
                        }
                        // Close input stream
                        br.close();

                    } catch (Exception e) {
                        e.printStackTrace();
                        throw new RuntimeException("FileGraph: I/O exception thrown, graph could not be generated. " + filename);
                    }

                    subgraphs.add(g);
                }
            }
        }

        long estimatedTime = System.currentTimeMillis() - startTime;
        System.out.println("> Reading files time: " + estimatedTime);


        return getSampledLayers(subgraphs);
    }

    protected List<Graph> getSampledLayers(List<Graph> subgraphs){
        return subgraphs;
    }

    private void writeLayersToFile(List<Graph> subgraphs) {
        long startTime = System.currentTimeMillis();

        File folder = new File(DIRECTORY_NAME);
        File[] files = folder.listFiles();
        if (files != null) {
            for (File f : files) {
                if (f.isFile()) {
                    f.delete();
                }
            }
        }
        int i = 0;
        for (Graph layer: subgraphs) {
            i++;
            new PrinterGraph(layer).print(DIRECTORY_NAME + "/" + i + ".txt");
        }
        long estimatedTime = System.currentTimeMillis() - startTime;
        System.out.println("> Writing layers to files time: " + estimatedTime);

    }
}
