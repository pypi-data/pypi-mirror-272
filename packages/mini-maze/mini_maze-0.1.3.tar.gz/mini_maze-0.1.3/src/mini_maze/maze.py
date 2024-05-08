import random
from heapq import heappush, heappop


class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = None
        self.start = None
        self.goal = None
        self.reset()

    def init_maze(self):
        """Initialize the maze grid with walls (1) and set the start position."""
        maze = [[1 for _ in range(self.width)] for _ in range(self.height)]
        return maze

    def carve_passages_from(self, x, y):
        """Carve passages using DFS algorithm."""
        dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Directions: right, down, left, up
        random.shuffle(dir)  # Shuffle directions to ensure randomness

        for dx, dy in dir:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < len(self.maze[0]) and 0 <= ny < len(self.maze) and self.maze[ny][nx] == 1:
                self.maze[y + dy][x + dx] = 0  # Remove wall between cells
                self.maze[ny][nx] = 0  # Mark the new cell as a path
                self.carve_passages_from(nx, ny)

    def pad_matrix(self):
        rows = len(self.maze)
        cols = len(self.maze[0])

        # Create a new matrix with additional padding
        padded_matrix = [[1] * (cols + 2) for _ in range(rows + 2)]

        # Copy the original matrix into the padded matrix
        for i in range(rows):
            for j in range(cols):
                padded_matrix[i + 1][j + 1] = self.maze[i][j]

        self.maze = padded_matrix

    def generate_random_maze(self):
        """Generate a random maze."""
        if self.width % 2 == 0 or self.height % 2 == 0:
            raise ValueError("The size tuple must be odd numbers.")
        start_x, start_y = (0, 0)  # Starting from the top-left corner
        self.maze[start_y][start_x] = 0  # Mark the starting cell as a path

        self.carve_passages_from(start_x, start_y)
        self.maze[0][0] = 0  # Entrance
        self.maze[-1][-1] = 0  # Exit

        self.pad_matrix()

        # Check if the end point is reachable:
        if MazeSolver(self.maze).find_shortest_path((1, 1), (self.width, self.height)) is None:
            return self.generate_random_maze()
        self.start = (1, 1)
        self.goal = (self.width, self.height)

    def reset(self):
        self.maze = self.init_maze()
        self.generate_random_maze()

        end_positions = self.get_end_positions()
        if len(end_positions) < 2:
            self.reset()  # Regenerate the maze if there are not enough end positions
        else:
            start, target = random.sample(end_positions, 2)
            self.start = start
            self.goal = target

    def get_maze(self):
        return self.maze

    def get_start(self):
        return self.start

    def get_target(self):
        return self.goal

    def get_end_positions(self):
        end_positions = []
        rows, cols = len(self.maze), len(self.maze[0])

        for i in range(rows):
            for j in range(cols):
                if self.maze[i][j] == 0:  # Check if the cell is a path
                    neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
                    path_neighbors = [n for n in neighbors if
                                      0 <= n[0] < rows and 0 <= n[1] < cols and self.maze[n[0]][n[1]] == 0]
                    if len(path_neighbors) == 1:  # Check if the cell has only one path neighbor
                        end_positions.append((i, j))

        return end_positions

    def print_maze(self, return_str = False):
        if not return_str:
            """Print the maze to the console."""
            for i in range(len(self.maze)):
                row = []
                for j in range(len(self.maze[0])):
                    if (i, j) == self.start:
                        row.append('S')
                    elif (i, j) == self.goal:
                        row.append('T')
                    else:
                        row.append('#' if self.maze[i][j] == 1 else ' ')
                print(' '.join(row))
        else:
            output = ""
            for i in range(len(self.maze)):
                row = []
                for j in range(len(self.maze[0])):
                    if (i, j) == self.start:
                        row.append('S')
                    elif (i, j) == self.goal:
                        row.append('T')
                    else:
                        row.append('#' if self.maze[i][j] == 1 else ' ')
                output = output + ' '.join(row) + "\n"
            return output


class MazeSolver:
    def __init__(self, maze):
        self.maze = maze

    def manhattan_distance(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def find_shortest_path(self, start, goal):
        rows, cols = len(self.maze), len(self.maze[0])
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
                if 0 <= nx < cols and 0 <= ny < rows and self.maze[ny][nx] == 0:
                    new_path = path + [(nx, ny)]  # Create a new path by appending the current position
                    heappush(heap, (self.manhattan_distance((nx, ny), goal), (nx, ny), new_path))

        return []  # Return an empty list if no path is found

    def find_next_state(self, start, goal):
        path = self.find_shortest_path(start, goal)
        if len(path) > 1:
            return path[1]  # Return the next state in the path
        else:
            return None  # Return None if there is no valid path or the agent is already at the goal