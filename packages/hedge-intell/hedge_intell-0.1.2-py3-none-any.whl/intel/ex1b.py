graph = {
    '5': ['3', '7'],
    '3': ['2', '4'],
    '7': ['8'],
    '2': [],
    '4': ['8'],
    '8': []
}

def dfs(graph, start, visited=None):
    if visited is None:
        visited = set()  # Set to keep track of visited nodes
    if start not in visited:
        print(start, end=" ")  # Process the node
        visited.add(start)  # Mark the node as visited
        # Recursively visit unvisited neighbors of the current node
        for neighbour in graph[start]:
            dfs(graph, neighbour, visited)

# Driver code
print("Following is the Depth-First Search:")
dfs(graph, '5')
