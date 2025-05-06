# Goal is to find reachable cities from a source node via BFS (e.g. Trip Planner App)
from collections import deque
def bfs(graph, start):
    visited = set() # Set to track visited cities
    queue = deque([start]) # Queue for BFS starting from the given city
    
    print("\nBFS Traversal Order:")
    while queue:
        city = queue.popleft() #Dequeue a city
        if city not in visited:
            print(city, end=" ") #printing visited cities
            visited.add(city) #marking as a visited city
            for neighbor in graph.get(city, []): #traverse neighbors
                if neighbor not in visited:
                    queue.append(neighbor)
                    
if __name__ == "__main__":
    graph = {}
    print("Enter number of Connections:")
    edges = int(input())
    
    print("Enter each connection (city1 city2):")
    for _ in range(edges):
        u, v = input().split()
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append(v)
        graph[v].append(u)
        
    print("Enter starting city for BFS:")
    start_city = input()
    bfs(graph, start_city)
    