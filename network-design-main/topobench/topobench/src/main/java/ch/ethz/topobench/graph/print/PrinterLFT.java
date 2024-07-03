package ch.ethz.topobench.graph.print;

import ch.ethz.topobench.graph.LFT;

import java.io.BufferedWriter;
import java.io.FileWriter;

public class PrinterLFT {
    private LFT lft;

    public PrinterLFT(LFT lft) {
       this.lft = lft;
    }

    /**
     * Print the graph to a file.
     *
     * @param fileName  File destination
     */
    public void print(String fileName) {
        try {
            // Open output stream
            FileWriter fileStream = new FileWriter(fileName);
            BufferedWriter out = new BufferedWriter(fileStream);


            for (int i = 0; i < lft.getGraph().getNumNodes(); i++) {
                boolean firstNum = true;
                for (int j = 0; j < lft.getGraph().getNumNodes(); j++) {
                    if (!firstNum) {
                        out.write(" ");
                    } else
                        firstNum = false;
                    out.write("" + lft.nextHop(i, j));
                }
                out.write("\n");
            }

            // Close output stream
            out.close();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}