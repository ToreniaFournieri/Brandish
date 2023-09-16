import random
from collections import deque

def get_neighboring_walls(pos, width, height):
    x, y = pos
    walls = []
    
    # Check the four possible directions for walls two units away
    if x > 2:
        walls.append((x - 2, y))
    if x < width - 3:
        walls.append((x + 2, y))
    if y > 2:
        walls.append((x, y - 2))
    if y < height - 3:
        walls.append((x, y + 2))
        
    return walls

def get_opposite_cell(wall, pos):
    wx, wy = wall
    px, py = pos
    
    # Determine the direction of the wall relative to the position and return the adjacent cell
    if wx > px:
        return wx - 1, wy
    if wx < px:
        return wx + 1, wy
    if wy > py:
        return wx, wy - 1
    if wy < py:
        return wx, wy + 1
    return None, None  # Return (None, None) if no valid opposite cell is found

def generate_maze(width, height):
    # Create a grid of walls
    maze = [[1 for _ in range(width)] for _ in range(height)]
    
    # Starting point
    start = (2 * random.randint(0, (width - 1) // 2), 2 * random.randint(0, (height - 1) // 2))
    maze[start[1]][start[0]] = "S"
    
    # List of visited cells
    visited = [start]
    
    # Walls adjacent to the starting cell
    walls = get_neighboring_walls(start, width, height)
    
    while walls:
        wall = random.choice(walls)
        
        # Get the cell opposite to the current wall relative to the most recently visited cell
        opposite = get_opposite_cell(wall, visited[-1])
        
        # If we have a valid opposite cell, carve the path
        if opposite != (None, None):
            ox, oy = opposite
            if 0 <= ox < width and 0 <= oy < height and maze[oy][ox] == 1:
                maze[wall[1]][wall[0]] = 0
                maze[oy][ox] = 0
                visited.append((ox, oy))
                walls += get_neighboring_walls((ox, oy), width, height)
        
        walls.remove(wall)
    
    # Add an end point
    end = (2 * random.randint(0, (width - 1) // 2), 2 * random.randint(0, (height - 1) // 2))
    maze[end[1]][end[0]] = "E"
    
    return maze

def bfs(maze, start, end):
    """Check if there's a path between start and end using BFS."""
    visited = set()
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        if (x, y) == end:
            return True  # Path found
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and (nx, ny) not in visited:
                if maze[ny][nx] == 0 or maze[ny][nx] == "E":
                    visited.add((nx, ny))
                    queue.append((nx, ny))
    return False  # No path found

def carve_path(maze, start, end):
    """Carve a direct path between start and end."""
    x, y = start
    ex, ey = end
    while (x, y) != (ex, ey):
        if x < ex:
            maze[y][x] = 0
            x += 1
        elif x > ex:
            maze[y][x] = 0
            x -= 1
        elif y < ey:
            maze[y][x] = 0
            y += 1
        elif y > ey:
            maze[y][x] = 0
            y -= 1

def ensure_path_to_end(maze):
    start = [(x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == "S"][0]
    end = [(x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == "E"][0]
    
    if not bfs(maze, start, end):
        carve_path(maze, start, end)



class Player:
    def __init__(self, start_position):
        self.health = 100
        self.attack_power = 10
        self.defense = 5
        self.gold = 0
        self.position = start_position
        self.direction = "N"

    def move(self, direction, maze):
        x, y = self.position
        if direction == "N" and maze[y-1][x] != 1:
            self.position = (x, y-1)
        elif direction == "S" and maze[y+1][x] != 1:
            self.position = (x, y+1)
        elif direction == "E" and maze[y][x+1] != 1:
            self.position = (x+1, y)
        elif direction == "W" and maze[y][x-1] != 1:
            self.position = (x-1, y)
        else:
            print("Invalid direction or there's a wall!")

    def display_stats(self):
        print(f"Health: {self.health}")
        print(f"Attack Power: {self.attack_power}")
        print(f"Defense: {self.defense}")
        print(f"Gold: {self.gold}")
        print(f"Position: {self.position}")

def display_maze(maze, player_position):
    for y, row in enumerate(maze):
        display_row = []
        for x, cell in enumerate(row):
            if (x, y) == player_position:
                display_row.append("P")  # Representing the player with "P"
            else:
                if cell == 0:
                    display_row.append(".")
                elif cell == 1:
                    display_row.append("#")
                else:
                    display_row.append(cell)
        print(''.join(display_row))
        
def rotate_maze(maze, direction):
    """Rotate the maze based on the player's direction."""
    if direction == "N":
        return maze
    elif direction == "E":
        return [list(row) for row in zip(*maze[::-1])]
    elif direction == "S":
        return [row[::-1] for row in maze[::-1]]
    elif direction == "W":
        return [list(row) for row in zip(*maze)]

def pad_relative_view(view, up=6, down=1, left=3, right=3):
    """Pad the view to ensure it has the expected dimensions."""
    
    # Pad rows at the top
    while len(view) < up + down + 1:
        view.insert(0, [1] * len(view[0]))
    
    # Pad columns on the left and right
    for row in view:
        while len(row) < left + right + 1:
            row.insert(0, 1)
            row.append(1)
    
    return view


def get_relative_view(maze, player_position, direction):
    """Get the maze view based on the player's position and direction."""
    rotated_maze = rotate_maze(maze, direction)
    px, py = player_position
    
    # Define the vision limits
    up = 6
    down = 1
    left = 3
    right = 3
    
    # Slice the maze to get the player's view
    start_y = max(0, py - up)
    end_y = min(len(rotated_maze), py + down + 1)
    start_x = max(0, px - left)
    end_x = min(len(rotated_maze[0]), px + right + 1)
    
    view = [row[start_x:end_x] for row in rotated_maze[start_y:end_y]]
    view = pad_relative_view(view, up, down, left, right)
    
    # Place the player in the relative view
    view[up][left] = "P"
    
    return view


def main():
    # Generate the maze and find the starting position
    maze = generate_maze(80, 20)
    ensure_path_to_end(maze)

    start_position = [(x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == "S"][0]

    player = Player(start_position)
    while True:
        relative_view = get_relative_view(maze, player.position, player.direction)
        view_display = [''.join(["#" if cell == 1 else " " if cell == 0 else cell for cell in row]) for row in relative_view]
        
        # Display the player's relative view of the maze
        print('\n'.join(view_display))
        print()  # Add a newline for separation

        player.display_stats()
        direction = input("Enter direction (N/S/E/W) or Q to quit: ").upper()
        if direction == "Q":
            break
        player.move(direction, maze)
        
        # Check if the player has reached the end
        if maze[player.position[1]][player.position[0]] == "E":
            print("Congratulations! You've reached the end of the maze!")
            break


if __name__ == "__main__":
    main()
