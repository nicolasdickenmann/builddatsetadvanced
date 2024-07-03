import networkx as nx
import matplotlib.pyplot as plt

V=18

def DFS(graph, marked, n, vert, start, count):
    # mark the vertex vert as visited
    marked[vert] = True

    # if the path of length (n-1) is found
    if n == 0:

        # mark vert as un-visited to make
        # it usable again.
        marked[vert] = False

        # Check if vertex vert can end with
        # vertex start
        if graph[vert][start] == 1:
            count = count + 1
            return count
        else:
            return count

            # For searching every possible path of
    # length (n-1)
    for i in range(V):
        if marked[i] == False and graph[vert][i] == 1:
            # DFS for searching path by decreasing
            # length by 1
            count = DFS(graph, marked, n - 1, i, start, count)

            # marking vert as unvisited to make it
    # usable again.
    marked[vert] = False
    return count


# Counts cycles of length
# N in an undirected
# and connected graph.
def countCycles(graph, n):
    # all vertex are marked un-visited intially.
    marked = [False] * V

    # Searching for cycle by using v-n+1 vertices
    count = 0
    for i in range(V - (n - 1)):
        count = DFS(graph, marked, n - 1, i, i, count)

        # ith vertex is marked as visited and
        # will not be visited again.
        marked[i] = True

    return int(count / 2)

def draw_graph(file_name, nodes, edges):
    G = nx.DiGraph()

    with open(file_name, "r") as file:
        lines = file.readlines()
        for line in lines:
            f, t = line.rstrip('\n').split()
            G.add_edge(f, t)

    nx.draw(G)
    plt.show()

def print_incidence_matrix(file_name, numNodes):

    graph = [ [0 for i in range(numNodes)] for j in range(numNodes)]
    with open(file_name, "r") as file:
        lines = file.readlines()
        for line in lines:
            f, t = line.rstrip('\n').split()
            fint = int(f)
            tint = int(t)
            graph[fint][tint] = 1
            graph[tint][fint] = 1

    n = 4
    print("Total cycles of length ", n, " are ", countCycles(graph, n))
    for row in graph:
        print(str(row).rstrip("]").lstrip("["))

if __name__ == '__main__':
    numNodes = V
    numEdges = {18:45, 50:175, 98:539, 242: 2057, 338:3211}
    file_name = "slimfly_" + str(numNodes) + ".txt"
    draw_graph(file_name, numNodes, numEdges)
    print_incidence_matrix(file_name, numNodes)
