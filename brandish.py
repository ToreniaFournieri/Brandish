from map import *
from map_master import *
from entities import *
import curses


def game(stdscr):
    # Set up curses settings
    curses.curs_set(0)  # hide cursor
    stdscr.keypad(1)    # enable special keys
    stdscr.timeout(100) # set getch() non-blocking

    # Generate the maze and find the starting position
    global maze
    
    maze = []
    maze = maze_map
    #for row in maze_map:
    #    maze_row = []
    #    for cell in row:
    #        if cell == "#":
    #            maze_row.append(1)
    #        elif cell in [".", "+", "^", "$", "(", ")", "[", "!"]:
    #            maze_row.append(0)
    #        elif cell == "S":
    #            maze_row.append("S")
    #        else:
    #            maze_row.append(cell)  # For any other characters, add them as-is
    #    maze.append(maze_row)


    # Find the starting position
    start_position = [(x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == "S"][0]
    monsters = []

    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == "M":
                monster = Monster(40,"1d3",0,2,position=(x, y))  # Assuming Monster class has a position attribute
                monsters.append(monster)
                #maze[y][x] = "M"  # This can be changed based on how you want to represent monsters in the maze

    jump_mode = False

    player = Player(start_position)
    while True:
        # Use curses to display
        stdscr.clear()
        # Show player stats and message below the maze
        stats = player.display_stats() # Modify display_stats() to return a string instead of print
        stdscr.addstr(0, 0, stats)

        #display_maze(maze, player.position)
        relative_view = get_relative_view(maze, player)
        view_display = [''.join(["#" if cell == 1 else " " if cell == 0 else cell for cell in row]) for row in relative_view]
        # Display the player's relative view of the maze


        stdscr.addstr(14, 24, f"モンスター {monster.health}/{monster.max_health}" )


        visual_maze = generate_visual_2D_view(view_display)
        for idx, row in enumerate(visual_maze):
            stdscr.addstr(idx +1, 24, ''.join(map(str, row)))

        stdscr.addstr(len(visual_maze) + 2, 0, "方向キーで移動, Pでやめる: ")

        stdscr.addstr(0, 50, f"装備")
        stdscr.addstr(1, 50, f"左手: {player.left_hand}")
        stdscr.addstr(2, 50, f"鎧: {player.armour}")
        stdscr.addstr(3, 50, f"右手: {player.right_hand}")
        stdscr.addstr(4, 50, f"お気に入り: {player.shortcut}")
        stdscr.addstr(5, 50, f"左指輪: {player.left_ring}")
        stdscr.addstr(6, 50, f"右指輪: {player.right_ring}")

        stdscr.addstr(8, 50, f"アイテム")
        stdscr.addstr(9, 50, f"ポーション")
        stdscr.addstr(10, 50, f"合鍵")
        stdscr.addstr(11, 50, f"小石")


        stdscr.refresh()

        # Get user input with curses
        action = stdscr.getch()
        # If 'j' is pressed, set jump_mode to True
        if action == ord('j'):
            jump_mode = True
            continue
        # Translate action into game command
        if action == curses.KEY_UP:
            if jump_mode:
                player.move("jup", maze)
                jump_mode = False
            else:
                player.move("up", maze)
        elif action == curses.KEY_DOWN:
            if jump_mode:
                player.move("jdown", maze)
                jump_mode = False
            else:
                player.move("down", maze)
        elif action == curses.KEY_LEFT:
            if jump_mode:
                player.move("jleft", maze)
                jump_mode = False
            else:
                player.move("left", maze)
        elif action == curses.KEY_RIGHT:
            if jump_mode:
                player.move("jright", maze)
                jump_mode = False
            else:
                player.move("right", maze)
        elif action in [ord('P'), ord('p')]:
            break
        else:
            continue # Skip loop iteration for other keys

        for monster in monsters:
            if is_adjacent(player.position, monster.position):
                battle = Battle(player, monster)
                result = battle.commence_battle()
                print(result)
        
                if monster.health <= 0:
                    monsters.remove(monster)
                    # Update the maze to remove the monster character
                    x, y = monster.position
                    maze[y] = maze[y][:x] + "%" + maze[y][x+1:]



        #player.move(action, maze)
        
        # Check for game over
        if maze[player.position[1]][player.position[0]] == "E":
            stdscr.addstr(len(visual_maze) + 3, 0, "Congratulations! You've reached the end of the maze!")
            stdscr.refresh()
            stdscr.getch() # Wait for a key press before ending
            break

if __name__ == "__main__":
    curses.wrapper(game)