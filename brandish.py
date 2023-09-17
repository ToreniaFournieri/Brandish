from map import *
from map_master import *
from entities import *



def main():
    # Generate the maze and find the starting position
    global maze
    
    maze = []
    for row in maze_map:
        maze_row = []
        for cell in row:
            if cell == "#":
                maze_row.append(1)
            elif cell in [".", "+", "^", "$", "(", ")", "[", "!"]:
                maze_row.append(0)
            elif cell == "S":
                maze_row.append("S")
            else:
                maze_row.append(cell)  # For any other characters, add them as-is
        maze.append(maze_row)

    # Find the starting position
    start_position = [(x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == "S"][0]


    player = Player(start_position)
    while True:
        display_maze(maze, player.position)
        relative_view = get_relative_view(maze, player)
        view_display = [''.join(["#" if cell == 1 else " " if cell == 0 else cell for cell in row]) for row in relative_view]
        
        # Display the player's relative view of the maze
        print('\n'.join(view_display))
        print()  # Add a newline for separation

        player.display_stats()
        action = input("Enter direction (W/A/S/D), P to quit: ").upper()
        if action == "P":
            break
        player.move(action, maze)
        
        # Check if the player has reached the end
        if maze[player.position[1]][player.position[0]] == "E":
            print("Congratulations! You've reached the end of the maze!")
            break


if __name__ == "__main__":
    main()
