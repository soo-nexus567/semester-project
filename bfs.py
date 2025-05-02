# Goal is to find recheable cities from a source node via BFS (e.g. Trip Planner App)
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

def bfs(graph, start):
    visited = set() # Set to track visited cities
    queue = deque([start]) # Queue for BFS starting from the given city
    visited.add(start)
    G = nx.Graph(graph)
    pos = nx.spring_layout(G, seed =42)
    print("\nBFS Traversal Order:")
    while queue:
        city = queue.popleft() #Dequeue a city
        nx.draw_networkx_nodes(G, pos, nodelist=[city], node_color='red', node_size=500)
        nx.draw_networkx_labels(G, pos, {city:city}, font_size=12, font_color='black')
        nx.draw_networkx_edges(G, pos, width=1)
        plt.title(f"BFS: Visting {city}")
        plt.pause(0.5)
        plt.clf()
        neighbors = graph.get(city, [])
        for neighbor in neighbors: #traverse neighbors
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=12)
    plt.title("BFS Traversal Complete")
    plt.show()
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': ['F'],
    'F': []
}
bfs(graph, 'A')



            