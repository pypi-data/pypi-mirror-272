def aStarAlgo(start_node, stop_node):
    open_set = {start_node}  # Initialize open_set correctly
    closed_set = set()
    g = {start_node: 0}  # Initialize g with start_node's cost
    parents = {start_node: start_node}  # Initialize parents with start_node

    while open_set:
        n = None
        for v in open_set:
            if n is None or g[v] + heuristic(v) < g.get(n, float('inf')) + heuristic(n):
                n = v

        if n is None:
            print('Path does not exist!')
            return None

        if n == stop_node:
            path = []
            while parents[n] != n:
                path.append(n)
                n = parents[n]
            path.append(start_node)
            path.reverse()
            print('Path found:', path)
            return path

        open_set.remove(n)
        closed_set.add(n)

        if n in Graph_nodes:
            for m, weight in get_neighbors(n):
                tentative_g = g.get(n, float('inf')) + weight
                if m not in closed_set or tentative_g < g.get(m, float('inf')):
                    open_set.add(m)
                    parents[m] = n
                    g[m] = tentative_g

    print('Path does not exist!')
    return None

def get_neighbors(v):
    return Graph_nodes.get(v, [])

def heuristic(n):
    H_dist = {
        'A': 11,
        'B': 6,
        'C': 5,
        'D': 7,
        'E': 3,
        'F': 6,
        'G': 5,
        'H': 3,
        'I': 1,
        'J': 0
    }
    return H_dist.get(n, float('inf'))

Graph_nodes = {
    'A': [('B', 6), ('F', 3)],
    'B': [('A', 6), ('C', 3), ('D', 2)],
    'C': [('B', 3), ('D', 1), ('E', 5)],
    'D': [('B', 2), ('C', 1), ('E', 8)],
    'E': [('C', 5), ('D', 8), ('I', 5), ('J', 5)],
    'F': [('A', 3), ('G', 1), ('H', 7)],
    'G': [('F', 1), ('I', 3)],
    'H': [('F', 7), ('I', 2)],
    'I': [('E', 5), ('G', 3), ('H', 2), ('J', 3)],
}

aStarAlgo('A', 'J')  # Corrected stop_node to 'J'
