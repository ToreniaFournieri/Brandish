import random

def generate_maze(width, height):
    # Create a grid of walls
    maze = [[1 for _ in range(width)] for _ in range(height)]
    # Starting point
    start = (2 * random.randint(0, (width - 1) // 2), 2 * random.randint(0, (height - 1) // 2))
    maze[start[1]][start[0]] = "S"
    walls = get_neighboring_walls(start, width, height)
    
    while walls:
        wall = random.choice(walls)
        opposite = get_opposite_cell(wall, width, height)
        
        if maze[wall[1]][wall[0]] == 1 and (maze[opposite[1]][opposite[0]] == 1 or maze[opposite[1]][opposite[0]] == "E"):
            maze[wall[1]][wall[0]] = 0
            maze[opposite[1]][opposite[0]] = 0
            walls += get_neighboring_walls(opposite, width, height)
        
        walls.remove(wall)
    
    # Add an end point
    end = (2 * random.randint(0, (width - 1) // 2), 2 * random.randint(0, (height - 1) // 2))
    maze[end[1]][end[0]] = "E"
    
    return maze

def get_neighboring_walls(pos, width, height):
    x, y = pos
    walls = []
    if x > 1:
        walls.append((x - 1, y))
    if x < width - 2:
        walls.append((x + 1, y))
    if y > 1:
        walls.append((x, y - 1))
    if y < height - 2:
        walls.append((x, y + 1))
    return walls

def get_opposite_cell(wall, width, height):
    x, y = wall
    if x > 1 and maze[y][x - 1] != 1:
        return x - 2, y
    if x < width - 2 and maze[y][x + 1] != 1:
        return x + 2, y
    if y > 1 and maze[y - 1][x] != 1:
        return x, y - 2
    if y < height - 2 and maze[y + 1][x] != 1:
        return x, y + 2
    return None, None


# Generate a 15x15 maze for demonstration
maze_width = 15
maze_height = 15
maze = generate_maze(maze_width, maze_height)



class Player:
    def __init__(self, start_position):
        self.health = 100
        self.attack_power = 10
        self.defense = 5
        self.gold = 0
        self.position = start_position

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
                    display_row.append(" ")
                elif cell == 1:
                    display_row.append("#")
                else:
                    display_row.append(cell)
        print(''.join(display_row))
        
def main():
    # Generate the maze and find the starting position
    maze = generate_maze(15, 15)
    start_position = [(x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == "S"][0]

    player = Player(start_position)
    while True:
        display_maze(maze, player.position)
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
