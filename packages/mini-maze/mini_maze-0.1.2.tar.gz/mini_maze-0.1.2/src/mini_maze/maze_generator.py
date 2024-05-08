import random
from heapq import heappush, heappop


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def init_maze(width, height):
    """Initialize the maze grid with walls (1) and set the start position."""
    maze = [[1 for _ in range(width)] for _ in range(height)]
    return maze


def carve_passages_from(x, y, maze):
    """Carve passages using DFS algorithm."""
    dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Directions: right, down, left, up
    random.shuffle(dir)  # Shuffle directions to ensure randomness

    for dx, dy in dir:
        nx, ny = x + dx * 2, y + dy * 2
        if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] == 1:
            maze[y + dy][x + dx] = 0  # Remove wall between cells
            maze[ny][nx] = 0  # Mark the new cell as a path
            carve_passages_from(nx, ny, maze)

def pad_matrix(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    # Create a new matrix with additional padding
    padded_matrix = [[1] * (cols + 2) for _ in range(rows + 2)]

    # Copy the original matrix into the padded matrix
    for i in range(rows):
        for j in range(cols):
            padded_matrix[i + 1][j + 1] = matrix[i][j]

    return padded_matrix
def generate_random_maze(size):
    """Generate a random maze."""
    if size[0] % 2 == 0 or size[1] % 2 == 0:
        raise ValueError("The size tuple must be odd numbers.")
    width, height = size
    maze = init_maze(width, height)
    start_x, start_y = (0, 0)  # Starting from the top-left corner
    maze[start_y][start_x] = 0  # Mark the starting cell as a path

    carve_passages_from(start_x, start_y, maze)
    maze[0][0] = 0  # Entrance
    maze[-1][-1] = 0  # Exit

    # Check if the end point is reachable:
    if find_shortest_path(pad_matrix(maze), (1, 1), (width, height)) is None:
        return generate_random_maze(size)
    return pad_matrix(maze), (1, 1), (width, height)

def find_shortest_path(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    visited = set()
    heap = []
    heappush(heap, (0, start, [start]))  # Initialize the path with the starting position

    while heap:
        _, current, path = heappop(heap)
        if current == goal:
            return path  # Return the complete path

        if current in visited:
            continue
        visited.add(current)

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 0:
                new_path = path + [(nx, ny)]  # Create a new path by appending the current position
                heappush(heap, (manhattan_distance((nx, ny), goal), (nx, ny), new_path))

    return []  # Return an empty list if no path is found

def find_next_state(maze, start, goal):
    path = find_shortest_path(maze, start, goal)
    if len(path) > 1:
        return path[1]  # Return the next state in the path
    else:
        return None  # Return None if there is no valid path or the agent is already at the goal


if __name__ == "__main__":
    def print_maze(maze):
        """Print the maze to the console."""
        for row in maze:
            print(' '.join(['#' if cell == 1 else ' ' for cell in row]))

    width, height = 9, 9  # Maze dimensions (should be odd numbers)
    maze, start, goal = generate_random_maze((width, height))
    current = start

    next_state = find_next_state(maze, current, goal)
    if next_state is None:
        print("No path found to reach the goal.")
    print_maze(maze)
    print(f"Start: {start}")
    print(f"Goal: {goal}")
    print(f"Next state: {next_state}")
    print(f"Current: {current}")