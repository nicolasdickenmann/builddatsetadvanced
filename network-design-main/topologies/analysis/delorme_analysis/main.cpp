#include <iostream>
#include <cassert>
#include <vector>
#include <fstream>
#include <stdio.h>
#include <stdlib.h>
#include <sstream>
#include <algorithm>
#include <string.h>

int main(int argc, char** argv)
{
    printf("command to run : ./a.out <q> <adj_filename> -o <output_filename>\n");
    int q;
    std::string graphFile;
    std::string opFile;
    bool opExists = false;
    bool helpReq = false; 

    int expected_vertices;

    for (int i = 1; i < argc; i++)
    {  
        if (i + 1 != argc)
        {
            if (strcmp(argv[i], "-q") == 0) // parameter q
            {                 
                q = atoi(argv[i+1]);
                expected_vertices = (q*q + 1)*(q+1);
                i++;    
            }
            if (strcmp(argv[i], "-i") == 0) // input graph filename
            {                 
                graphFile = std::string(argv[i+1]);   
                i++;    
            }
            if (strcmp(argv[i], "-o") == 0) // output file (adjacency list with neighbor, cluster ID, offset tuples)
            {
                opFile = std::string(argv[i+1]);
                opExists = true;
                i++; 
            }
        }
        if (strcmp(argv[i], "-h") == 0)
        {
            helpReq = true;
            break;
        }
    }
    if (helpReq)
    {
        printf("command to run is \n ./analyze -q <q> -i <input_adj_file> -o <output_adj_file>\n\n");
        printf("Example: ./analyze -q 8 -i ../../data/Delormes/Delorme.8.adj.txt -o Delorme.8.tuples.txt \n\n");
        return 0;
    }

    std::ifstream infile(graphFile.c_str());
    if (infile.fail())
    {
        printf("input file does not exists\n");
        exit(0);
    }
    std::string line;
    int line_id = 0;


    int num_vertices;
    int num_edges;
    int num_edges_read = 0;

    std::vector<std::vector<int>> adj;
    std::vector<int> degree;
    std::vector<bool> isCentral;

    //Read the graph
    while(std::getline(infile, line))
    {
        std::istringstream iss(line);
        if (line_id == 0)
        {
            iss >> num_vertices;
            iss >> num_edges;
            assert(num_vertices == expected_vertices);
            assert(num_vertices > 0);
            assert(num_edges >= 0);
            printf("v = %d, e = %d\n", num_vertices, num_edges);
            adj.resize(num_vertices);
            degree.resize(num_vertices);
            isCentral.resize(num_vertices);
        }
        else
        {
            int neigh;
            while(iss >> neigh)
            {
                adj[line_id-1].push_back(neigh);
                num_edges_read++;
            }
            degree[line_id-1] = adj[line_id-1].size();
            assert(degree[line_id-1]==q || degree[line_id-1]==(q+1));
            isCentral[line_id-1] = (degree[line_id-1]==q);
        }
        line_id++;
    }
    printf("graph read\n");
    assert(num_edges_read == (2*num_edges));
    infile.close();

    if (opExists)
    {
        std::ofstream op(opFile.c_str());
        for (int i=0; i<num_vertices; i++)
        {
            for (auto x : adj[i])
                op << "(" << x << "," << x/(q+1) << "," << x%(q+1) << ") ";
            op << "\n";
        }
        op.close();
    }


    int infty = 100000;
    std::vector<int> distance (num_vertices, infty);
    std::vector<int> parent (num_vertices, num_vertices + 1);
    //BFS from all vertices
    for (int i=1; i<num_vertices; i++)
    {
        if (isCentral[i]) 
        {
            printf("central vertex %d\n", i);
            continue;
        }

        std::fill(distance.begin(), distance.end(), infty);
        std::vector<int> frontier; 
        std::vector<int> next_frontier;

        //initialize
        frontier.push_back(i);
        distance[i] = 0;
        parent[i] = i;
        int curr_distance = 0;
        bool central = isCentral[i];

        //number of neighbors at each distance value
        std::vector<int> numNeighAtHops (4, 0);

        //previously discovered vertices and previously discovered distance (overlap)
        std::vector<std::vector<std::pair<int, int>>> prevDiscovered (4);
        while(frontier.size()>0)
        {
            int mooreBoundNeigh = 1;
            for (int j=0; j<curr_distance; j++)
                mooreBoundNeigh = mooreBoundNeigh*(q+1);

            numNeighAtHops[curr_distance] = frontier.size();
            assert(frontier.size() <= mooreBoundNeigh);
            assert(curr_distance < 4);
            int next_distance = curr_distance + 1;
            for (auto v : frontier)
            {
                for (auto neigh : adj[v])
                {
                    if (distance[neigh]==infty)
                    {
                        parent[neigh] = v;
                        next_frontier.push_back(neigh);
                        distance[neigh] = next_distance; 
                    }
                    else if (curr_distance < 3)
                    {
                        if (neigh != parent[v])
                            prevDiscovered[next_distance].push_back(std::make_pair(neigh, distance[neigh]));
                    }
                }           
            }
            curr_distance++;
            frontier.clear();
            frontier.swap(next_frontier);
        }

        //cycle length with previously discovered vertices at distance 3
        int agg_cycle_length = 0;
        for(auto x : prevDiscovered[3])
            agg_cycle_length += (3 + x.second);

        double avg_cycle_length = ((double)agg_cycle_length)/((double)prevDiscovered[3].size());
        printf("vertex %d -> 1-hop neigh = %d, 2-hop = %d, 3-hop = %d, previously discovered 3-hop neighbors = %d, cycle length = %lf\n", i, numNeighAtHops[1], numNeighAtHops[2], numNeighAtHops[3], prevDiscovered[3].size(), avg_cycle_length);
    }
    
    return 0;
}
