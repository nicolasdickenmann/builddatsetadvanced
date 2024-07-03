import os
import re

def parse_adjacency_list(file_path):
    with open(file_path, 'r') as file:
        # Read the number of nodes and edges
        num_nodes, num_edges = map(int, file.readline().strip().split())
        
        # Initialize adjacency list
        adjacency_list = []
        
        # Read the adjacency list
        for i in range(num_nodes):
            connected_nodes = list(map(int, file.readline().strip().split()))
            for node in connected_nodes:
                if (node + 1, i + 1) not in adjacency_list:
                    adjacency_list.append((node + 1, i + 1))
                    
    return num_nodes, num_edges, adjacency_list

def create_dataset_files(adjacency_list, output_dir, graph_id, runningedge, graph_indicator, node_labels):
    # Prepare data for the dataset
    edge_list = []
    max_edge = 0

    for edge in adjacency_list:
        # Adjust node IDs for the combined dataset
        adjusted_edge = (edge[0] + runningedge, edge[1] + runningedge)
        edge_list.append(adjusted_edge)
        max_edge = max(max_edge, max(edge))

    # Extend graph_indicator and node_labels for the new nodes
    graph_indicator.extend([graph_id] * (max_edge + runningedge - len(graph_indicator)))
    node_labels.extend([1] * (max_edge + runningedge - len(node_labels)))

    # Write DD_A.txt
    with open(os.path.join(output_dir, 'dia3moore_A.txt'), 'a') as file:
        for edge in edge_list:
            file.write(f'         {edge[0]},         {edge[1]}\n')
    
    return max_edge + runningedge   # Return the next starting edge number

    
def main():
    input_base_dir = 'topologies/data/'
    output_dir = 'dataset'
    print("hello")
    
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Helper function to extract the numeric part from the filename
    def extract_number(filename):
        match = re.search(r'\d+', filename)
        return int(match.group()) if match else float('inf')

    # Initialize lists to accumulate data across all files
    graph_indicator = []
    graph_labels = []
    node_labels = []
    runningedge = 0    
    graph_id = 1
    totnodes = 0
    totedges = 0
    
    # Clear or create output files
    open(os.path.join(output_dir, 'dia3moore_A.txt'), 'w').close()
    open(os.path.join(output_dir, 'dia3moore_graph_indicator.txt'), 'w').close()
    open(os.path.join(output_dir, 'dia3moore_graph_labels.txt'), 'w').close()
    open(os.path.join(output_dir, 'dia3moore_node_labels.txt'), 'w').close()
    
    # Iterate through each subdirectory in the input base directory
    for subdir in os.listdir(input_base_dir):
        input_dir = os.path.join(input_base_dir, subdir)
        if os.path.isdir(input_dir):
            # Get and sort all adjacency list files in the input directory
            filenames = sorted([f for f in os.listdir(input_dir) if f.endswith('.adj.txt')],
                               key=extract_number)
            for filename in filenames:
                if filename.endswith('.adj.txt'):
                    file_path = os.path.join(input_dir, filename)
                    num_nodes, num_edges, adjacency_list = parse_adjacency_list(file_path)
                    runningedge = create_dataset_files(adjacency_list, output_dir, graph_id, runningedge, graph_indicator, node_labels)
                    totedges += num_edges
                    totnodes += num_nodes
                    graph_labels.append(1)
                    graph_id += 1
    
    # Write graph indicator, graph labels, and node labels files
    with open(os.path.join(output_dir, 'dia3moore_graph_indicator.txt'), 'a') as file:
        for indicator in graph_indicator:
            file.write(f'{indicator}\n')

    with open(os.path.join(output_dir, 'dia3moore_graph_labels.txt'), 'a') as file:
        for label in graph_labels:
            file.write(f'{label}\n')

    with open(os.path.join(output_dir, 'dia3moore_node_labels.txt'), 'a') as file:
        for label in node_labels:
            file.write(f'{label}\n')
    
    print(f'Total number of nodes: {totnodes}')
    print(f'Total number of edges: {totedges}')
    print(f'Dataset files created in directory: {output_dir}')

if __name__ == '__main__':
    main()
