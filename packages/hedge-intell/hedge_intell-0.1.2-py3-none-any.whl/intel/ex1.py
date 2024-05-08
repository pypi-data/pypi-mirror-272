from collections import deque

graph = {
    '5': ['3', '7'],
    '3': ['2', '4'],
    '7': ['8'],
    '2': [],
    '4': ['8'],
    '8': []
}

def bfs(graph, start):
    visited = set()  # Set to keep track of visited nodes
    queue = deque([start])  # Initialize a queue with the start node
    while queue:
        node = queue.popleft()  # Dequeue the first node from the queue
        if node not in visited:
            print(node, end=" ")  # Process the node
            visited.add(node)  # Mark the node as visited
            # Enqueue the unvisited neighbors of the current node
            for neighbour in graph[node]:
                if neighbour not in visited:
                    queue.append(neighbour)

# Driver code
print("Following is the Breadth-First Search:")
bfs(graph, '5')
