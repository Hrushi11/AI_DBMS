from collections import namedtuple

# Define a named tuple to represent a state in the game
State = namedtuple('State', ['x', 'y'])

# Define the grid size
GRID_SIZE = 5

# Define the start and goal coordinates
start_state = State(0, 0)
goal_state = State(4, 4)

# Define the grid with blocked cells represented by 'X'
grid = [
    [' ', ' ', ' ', ' ', ' '],
    [' ', 'X', ' ', 'X', ' '],
    [' ', ' ', ' ', ' ', ' '],
    [' ', 'X', ' ', 'X', ' '],
    [' ', ' ', ' ', ' ', ' ']
]

def generate_neighbors(state):
    neighbors = []

    # Define the possible movement directions: up, down, left, right
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for direction in directions:
        new_x = state.x + direction[0]
        new_y = state.y + direction[1]

        # Check if the new coordinates are within the grid bounds
        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            # Check if the new cell is not blocked
            if grid[new_x][new_y] != 'X':
                neighbors.append(State(new_x, new_y))

    return neighbors

def cost(state, neighbor):
    # Assume a cost of 1 to move from any state to its neighbor
    return 1

def heuristic(state):
    # Use the Manhattan distance as the heuristic function
    return abs(state.x - goal_state.x) + abs(state.y - goal_state.y)

def astar(start_state, goal_state, heuristic):
    open_set = {start_state}
    closed_set = set()

    g_score = {start_state: 0}
    f_score = {start_state: heuristic(start_state)}

    while open_set:
        current_state = min(open_set, key=lambda state: f_score[state])

        if current_state == goal_state:
            return reconstruct_path(current_state)

        open_set.remove(current_state)
        closed_set.add(current_state)

        neighbors = generate_neighbors(current_state)

        for neighbor in neighbors:
            g = g_score[current_state] + cost(current_state, neighbor)

            if neighbor in closed_set and g >= g_score.get(neighbor, float('inf')):
                continue

            if neighbor not in open_set or g < g_score.get(neighbor, float('inf')):
                g_score[neighbor] = g
                f_score[neighbor] = g + heuristic(neighbor)
                neighbor.parent = current_state
                open_set.add(neighbor)

    return None

def reconstruct_path(state):
    path = [state]
    while hasattr(state, 'parent') and state.parent is not None:
        state = state.parent
        path.append(state)
    return list(reversed(path))

# Call the A* algorithm with the given parameters
path = astar(start_state, goal_state, heuristic)

if path is not None:
    print("Path found:")
    for state in path:
        print(f"({state.x}, {state.y})")
else:
    print("No path found.")
