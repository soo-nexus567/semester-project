# Define the DFS function using recursion
def dfs(graph, node, visited =None):
    if visited is None:
        visited = set()
        
    if node not in visited:
        print(node)
        visited.add(node)
        
        for neighbor in graph.get(node, []):
            dfs(graph, neighbor, visited) #Recursive DFS call for the neighbor

#main block of code
if __name__ == "__main__":
    graph = {}
    
    print("Enter number of connection in the graph(edges):")
    edges = int(input())
    
    print("now enter each connection in the format: node1 node 2")
    print("This will assume the graph is undirected (2 way connections)")
    
    for _ in range(edges):
        u, v = input().split()
        
        if u not in graph:
            graph[u] = []
        graph[u].append(v)
        
        if v not in graph:
            graph[v] = []
        graph[v].append(u)
        
    print("Enter the starting node for DFS Traversal:")
    start_node = input()
    
    print("\nDFS Traversal Order:")
    dfs(graph, start_node)