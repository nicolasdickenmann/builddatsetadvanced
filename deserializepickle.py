import pickle as cp
import networkx as nx
import statistics


def load_graphs(file_path):
    with open(file_path, 'rb') as f:
        graphs = cp.load(f)
    return graphs

def max_diameter_degree(graphs):
    iteration = 0
    
    for graph in graphs:
        iteration += 1
        # Find the largest connected component
        largest_cc = max(nx.connected_components(graph), key=len)
        subgraph = graph.subgraph(largest_cc)
        
        # Calculate the diameter of the largest connected component
        if nx.is_connected(subgraph):
            diameter = nx.diameter(subgraph)
        else:
            diameter = float('inf')  # If the subgraph is not connected, set diameter to infinity
        
        # Calculate the maximum degree in the largest connected component
        degrees = dict(subgraph.degree())
        max_deg = max(degrees.values())
        min_deg = min(degrees.values())
        median_deg = statistics.median(degrees.values())
        average_deg = statistics.mean(degrees.values())

        
        # Get the number of nodes in the largest connected component
        num_nodes = len(largest_cc)
        tot_num_nodes = len(graph)

        # Calculate the average number of hops (average shortest path length)
        if num_nodes > 1 and nx.is_connected(subgraph):
            average_hops = nx.average_shortest_path_length(subgraph)
        else:
            average_hops = float('inf')  # If the subgraph is not connected or has only one node, set to infinity
        
        # Print the results for the current graph
        print(f'Graph: {iteration}')
        print(f'Number of Nodes in Largest Connected Component: {num_nodes}')
        print(f'Tot Number of Nodes: {tot_num_nodes}')
        print(f'Maximum Diameter: {diameter}')
        print(f'Average Number of Hops: {average_hops}')
        print(f'Maximum Degree: {max_deg}')
        print(f'Minimum Degree: {min_deg}')
        print(f'Median Degree: {median_deg}')
        print(f'Average Degree: {average_deg}')

        print('---')
    
if __name__ == "__main__":
    file_path = '/home/nicolas/Documents/DFS-blksize--1-b-1.graphs-0'  # replace with your file path
    graphs = load_graphs(file_path)
    max_diameter_degree(graphs)
