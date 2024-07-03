import networkx as nx
import os

def parse_adjacency_list(file_path):
    with open(file_path, 'r') as file:
        # Read the number of nodes and edges
        num_nodes, num_edges = map(int, file.readline().strip().split())
        
        # Initialize adjacency list
        adjacency_list = []
        
        # Read the adjacency list
        for i in range(num_nodes):
            connected_nodes = list(map(int, file.readline().strip().split()))
            adjacency_list.append((i, connected_nodes))
                    
    return num_nodes, num_edges, adjacency_list

def create_graph_from_adjacency_list(adjacency_list):
    G = nx.Graph()
    
    for node, neighbors in adjacency_list:
        for neighbor in neighbors:
            G.add_edge(node, neighbor)
    
    return G

def compute_graph_properties(G):
    max_diameter = nx.diameter(G)
    max_degree = max(dict(G.degree()).values())
    
    return max_diameter, max_degree

def main():
    input_file = '/home/nicolas/Documents/network-design-new/network-design-main/topologies/data/flatbutterflies/3DFlatButterfly.10.adj.txt'  # Replace with your file path
    
    # Parse the adjacency list
    num_nodes, num_edges, adjacency_list = parse_adjacency_list(input_file)
    
    # Create graph from adjacency list
    G = create_graph_from_adjacency_list(adjacency_list)
    
    # Compute graph properties
    max_diameter, max_degree = compute_graph_properties(G)
    
    print(f'Max Diameter: {max_diameter}')
    print(f'Max Degree: {max_degree}')

if __name__ == '__main__':
    main()


