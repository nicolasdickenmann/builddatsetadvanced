package ch.ethz.topobench.graph.subgraphs.utility;

import java.util.ArrayList;
import java.util.List;

public class Path {

    // List of integers representing a path in the graph
    private List<Integer> path;

    public Path(List <Integer> path) {
        this.path = path;
    }

    public Path(Integer v) {
        this.path = new ArrayList<>();
        this.path.add(v);
    }

    public List<Integer> getPath() {
        return path;
    }

    public Integer last(){
        return this.path.get(this.path.size() - 1);
    }

    /**
     * @return The length of the path in the graph (number of vertices - 1)
     */
    public int length() {
        if (path != null)
            return path.size();
        else
            return 0;
    }

    public boolean equals(Object o) {
        if (o == this)
            return true;
        if (o instanceof Path){
            return ((Path) o).getPath().equals(this.getPath());
        } else return false;

    }

    public boolean disjoint(Path p){
        // Check if there exist 2 consecutive vertices in paths
        for (int i = 0; i < this.path.size()-1; i++){
            int pos = p.getPath().indexOf(path.get(i));
            if (pos > -1){
                if (p.getPath().get(pos + 1).equals(path.get(i + 1)))
                    return false;
            }
        }
        return true;
    }

    @Override
    public int hashCode() {
        return path.hashCode();
    }

    public boolean contains(Integer node){
        if (path != null)
            return path.contains(node);
        else
            return false;
    }
}
