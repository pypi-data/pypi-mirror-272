import heapq

def heuristic(a, b): 
    # Assume a mapping between nodes and coordinates 
    coordinates = { 
        'A': (0, 0), 'B': (1, 0), 'C': (2, 0), 
        'D': (0, 1), 'E': (1, 1), 'F': (2, 1), 
        'G': (0, 2), 'H': (1, 2), 'I': (2, 2) 
    } 
    (x1, y1) = coordinates[a] 
    (x2, y2) = coordinates[b] 
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def memory_bounded_a_star_search(start, goal, max_memory): 
    graph = { 
        'A': [('B', 1), ('D', 1)], 
        'B': [('C', 1), ('E', 1), ('A', 1)], 
        'C': [('F', 1), ('B', 1)], 
        'D': [('E', 1), ('G', 1), ('A', 1)], 
        'E': [('F', 1), ('H', 1), ('B', 1), ('D', 1)], 
        'F': [('I', 1), ('C', 1), ('E', 1)], 
        'G': [('H', 1), ('D', 1)], 
        'H': [('I', 1), ('E', 1), ('G', 1)], 
        'I': [('F', 1), ('H', 1)] 
    } 
    frontier = [(0, start)] # Priority queue sorted by cost + heuristic 
    came_from = {} 
    cost_so_far = {start: 0} 
    in_memory = {start} # Set of nodes in memory 
    
    while frontier: 
        _, current = heapq.heappop(frontier) 
        if current == goal: 
            break
        for next, weight in graph.get(current, []): 
            new_cost = cost_so_far[current] + weight 
            if next not in cost_so_far or new_cost < cost_so_far[next]: 
                cost_so_far[next] = new_cost 
                priority = new_cost + heuristic(next, goal) 
                heapq.heappush(frontier, (priority, next)) 
                came_from[next] = current 
                if len(in_memory) >= max_memory: 
                    to_remove = min(in_memory, key=lambda n: cost_so_far[n] + heuristic(n, goal)) 
                    in_memory.remove(to_remove) 
                in_memory.add(next) 
    if goal not in cost_so_far: 
        return None 
    path = [] 
    node = goal 
    while node != start: 
        path.append(node) 
        node = came_from[node] 
    path.append(start) 
    path.reverse() 
    return path 

# Example usage 
start = 'A' 
goal = 'I' 
max_memory = 5 
path = memory_bounded_a_star_search(start, goal, max_memory) 
print(f"Shortest path from {start} to {goal}: {path}")
