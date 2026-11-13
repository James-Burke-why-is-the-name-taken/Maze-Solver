from collections import deque
from heapq import heappop, heappush
import random

def heuristic(position, end):
    return abs(position[0] - end[0]) + abs(position[1] - end[1])

def solve_maze(maze):
    return search_maze(maze, algorithm="bfs")

def solve_maze_dfs(maze):
    return search_maze(maze, algorithm="dfs")

def solve_maze_astar(maze):
    return search_maze(maze, algorithm="astar")

def search_maze(maze, algorithm):
    rows, cols = len(maze), len(maze[0])
    start = None
    end = None

    # Assigns the starts and end.
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 'S':
                start = (r, c)
            elif maze[r][c] == 'E':
                end = (r, c)

    if start is None or end is None:
        print("Error, no start and end point found.")
        return None  # Start or end not found


    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    if algorithm == "astar":
        frontier = [(heuristic(start, end), 0, start)]
        costs = {start: 0}
    else:
        frontier = deque([start])
    visited = {start}
    explored = set()
    parent = {start: None}

    while frontier:
        if algorithm == "astar":
            _, current_cost, current = heappop(frontier)
            if current_cost != costs[current]:
                continue
        else:
            current = frontier.pop() if algorithm == "dfs" else frontier.popleft()
        explored.add(current)

        if current == end:
            break

        for dr, dc in directions:
            neighbor = (current[0] + dr, current[1] + dc)

            if (0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor[0]][neighbor[1]] != '#'):
                if algorithm == "astar":
                    new_cost = current_cost + 1
                    if new_cost < costs.get(neighbor, float("inf")):
                        costs[neighbor] = new_cost
                        parent[neighbor] = current
                        priority = new_cost + heuristic(neighbor, end)
                        heappush(frontier, (priority, new_cost, neighbor))
                elif neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    frontier.append(neighbor)

    
    path = None
    if end in parent:
        path = []
        step = end
        while step is not None:
            path.append(step)
            step = parent[step]
        path.reverse()

    if algorithm == "dfs":
        print("DFS search: . = explored, * = found path")
    elif algorithm == "astar":
        print("A* search: . = explored, * = shortest path")
    else:
        print("BFS search: . = explored, * = shortest path")
    print_maze(maze, explored, path)
    return path

def generate_random_maze(rows, cols):
    if rows < 4 or cols < 4:
        raise ValueError("Maze dimensions must be at least 4 rows by 4 columns.")

    # Keep the outer border as walls and randomly fill the interior.
    maze = [['#' for _ in range(cols)] for _ in range(rows)]

    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            maze[r][c] = ' ' if random.random() < 0.45 else '#'

    # Carve a randomized route so the end is always reachable from the start.
    r, c = 1, 1
    while (r, c) != (rows - 2, cols - 2):
        moves = []
        if r < rows - 2:
            moves.append((r + 1, c))
        if c < cols - 2:
            moves.append((r, c + 1))
        r, c = random.choice(moves)
        maze[r][c] = ' '

    maze[1][1] = 'S'
    maze[rows - 2][cols - 2] = 'E'

    return maze

def print_maze(maze, explored=None, path=None):
    display = [row.copy() for row in maze]

    if explored:
        for r, c in explored:
            if display[r][c] == ' ':
                display[r][c] = '.'

    if path:
        for r, c in path:
            if display[r][c] == ' ' or display[r][c] == '.':
                display[r][c] = '*'

    for row in display:
        print(' '.join(row))

    if explored is not None and path is None:
        print("No possible Solve")

r = int(input("How many rows do you want the maze to be (minimum of 4): "))
c = int(input("How many columns do you want the maze to be (minimum of 4): "))

maze = generate_random_maze(r, c)
print_maze(maze)
search_type = input("Choose search type (0 for BFS, 1 for DFS, 2 for A*): ")
while search_type not in {"0", "1", "2"}:
    print("Please enter 0, 1, or 2.")
    search_type = input("Choose search type (0/1/2): ")

if search_type == "0":
    solve_maze(maze)
elif search_type == "1":
    solve_maze_dfs(maze)
else:
    solve_maze_astar(maze)