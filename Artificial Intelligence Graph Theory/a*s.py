import heapq

class Node:
    def __init__(self, position, parent=None):
        self.position = position  # (x, y) position
        self.parent = parent      # Parent Node
        self.g = 0                # Cost from start to node
        self.h = 0                # Heuristic cost to target
        self.f = 0                # Total cost

    def __lt__(self, other):
        return self.f < other.f

def heuristic(a, b):
    """Calculate the heuristic estimated cost from current to target."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

def a_star(start, target, grid):
    """Perform the A* algorithm to find the shortest path in a grid."""
    open_list = []
    closed_list = set()
    
    # Create the start node
    start_node = Node(start)
    target_node = Node(target)

    # Initialize the open list
    heapq.heappush(open_list, start_node)

    while open_list:
        # Get the node with the lowest f value
        current_node = heapq.heappop(open_list)
        closed_list.add(current_node.position)

        # Check if we reached the target
        if current_node.position == target_node.position:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # Return reversed path

        # Generate children (neighbors)
        neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Up, Right, Down, Left
        for new_position in neighbors:
            node_position = (current_node.position[0] + new_position[0],
                             current_node.position[1] + new_position[1])

            # Check bounds
            if (node_position[0] > (len(grid) - 1) or
                node_position[0] < 0 or
                node_position[1] > (len(grid[len(grid)-1]) - 1) or
                node_position[1] < 0):
                continue

            # Check if the node is walkable (not an obstacle)
            if grid[node_position[0]][node_position[1]] != 0:
                continue

            # Create new node
            neighbor_node = Node(node_position, current_node)

            if neighbor_node.position in closed_list:
                continue

            # Calculate g, h, and f values
            neighbor_node.g = current_node.g + 1
            neighbor_node.h = heuristic(neighbor_node.position, target_node.position)
            neighbor_node.f = neighbor_node.g + neighbor_node.h

            # Check if this path to neighbor is better
            if add_to_open(open_list, neighbor_node):
                heapq.heappush(open_list, neighbor_node)

    return None  # No path found

def add_to_open(open_list, neighbor):
    """Check if neighbor should be added to the open list."""
    for node in open_list:
        if neighbor.position == node.position and neighbor.g > node.g:
            return False
    return True

if __name__ == "__main__":
    # Define the grid (0 = walkable, 1 = obstacle)
    grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 1],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0]
    ]

    start = (0, 0)  # Starting position
    target = (4, 4)  # Target position
    path = a_star(start, target, grid)

    if path:
        print("Path found:", path)
    else:
        print("No path found.")
