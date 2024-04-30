import heapq
import networkx as nx
import matplotlib.pyplot as plt
import readCsv

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, weight):
        self.edges.setdefault(from_node, []).append((to_node, weight))
        self.edges.setdefault(to_node, []).append((from_node, weight))

    def dijkstra(self, start):
        distances = {node: float('inf') for node in self.nodes}
        distances[start] = 0
        queue = [(0, start)]
        while queue:
            current_distance, current_node = heapq.heappop(queue)
            if current_distance > distances[current_node]:
                continue
            for neighbor, weight in self.edges.get(current_node, []):
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(queue, (distance, neighbor))
        return distances

def visualize_graph(graph):
    G = nx.Graph()
    for node in graph.nodes:
        G.add_node(node)
    for from_node, neighbors in graph.edges.items():
        for to_node, weight in neighbors:
            G.add_edge(from_node, to_node, weight=weight)
    pos = nx.spring_layout(G, scale=2)
    # pos = {1: (0, 0), 2: (-1, 0.3), 3: (2, 0.17), 4: (4, 0.255), 5: (5, 0.03)}
    nx.draw(G, pos, with_labels=True, node_size=600, node_color='skyblue', font_size=12, font_weight='bold', arrows=True)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Map of a Placeholder Area")
    plt.show(block=False)  #Set to 'False' to proceed to User Input Prompts
    plt.ion()
    plt.figure(1).canvas.manager.set_window_title("Map of a Placeholder Area")
    plt.draw()

def main():
    graph = Graph()
    # nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    nodes = readCsv.get_nodes()
    for node in nodes:
        graph.add_node(node)

    # edges = [('A', 'B', 2), ('A', 'C', 5), ('B', 'D', 3), ('B', 'E', 7),
    #          ('C', 'F', 4), ('D', 'G', 2), ('E', 'H', 1), ('F', 'H', 6),
    #          ('G', 'H', 3), ('A', 'F', 1), ('C', 'D', 2), ('E', 'G', 5)]
    edges = readCsv.get_edges()
    for edge in edges:
        graph.add_edge(*edge)

    visualize_graph(graph)

    start = input("Enter the Starting Node: ").strip().upper()
    end = input("Enter the End Node: ").strip().upper()

    if start not in graph.nodes or end not in graph.nodes:
        print("Invalid Input!")
        return

    distances = graph.dijkstra(start)
    path = [end]
    current_node = end
    while current_node != start:
        for neighbor, weight in graph.edges.get(current_node, []):
            if distances[current_node] == distances[neighbor] + weight:
                path.append(neighbor)
                current_node = neighbor
                break

    path.reverse()
    print("Shortest Path:", ' -> '.join(path))
    print("Total Distance:", distances[end])

if __name__ == "__main__":
    main()
