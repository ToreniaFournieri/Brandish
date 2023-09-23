from map import *
from map_master import *
from entities import *
import curses
from renderer import *

def game(stdscr):
    # Set up curses settings
    curses.curs_set(0)  # hide cursor
    stdscr.keypad(1)    # enable special keys
    stdscr.timeout(100) # set getch() non-blocking
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_MAGENTA)  # Foreground: White, Background: Blue for current health
    renderer = Renderer(stdscr)
    # Generate the maze and find the starting position
    global maze    
    maze = Yuya_map1

    # Find the starting position
    start_position = [(x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == "S"][0]
    monsters = []

    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == "M":
                monster = Monster("大鼠",40,"1d3",0,2,position=(x, y))  # Assuming Monster class has a position attribute
                monsters.append(monster)
                #maze[y][x] = "M"  # This can be changed based on how you want to represent monsters in the maze

    renderer = Renderer(stdscr)
    logs = []

    player = Player(start_position)
    player.current_map = find_map_name(maze)

    while True:

        renderer.render(stdscr,player , maze, logs, monsters)

        # Get user input with curses
        action = stdscr.getch()
        key_to_inventory_index = {
            ord('a'): 0 if len(player.inventory) > 0 else None,
            ord('s'): 1 if len(player.inventory) > 1 else None,
            ord('d'): 1 if len(player.inventory) > 2 else None,
            ord('f'): 1 if len(player.inventory) > 3 else None,
            ord('g'): 1 if len(player.inventory) > 4 else None,
            ord('h'): 1 if len(player.inventory) > 5 else None,
            # ... and so on, but make sure to check if the item exists before accessing!
        }

        # If 'j' is pressed, set jump_mode to True
        if action == ord('z'):
            player.jump_mode = True
            continue
        # Translate action into game command
        if action == curses.KEY_UP:
            if player.jump_mode:
                logs.append(player.move("jup", maze))
                player.jump_mode = False
            else:
                player.move("up", maze)
        elif action == curses.KEY_DOWN:
            if player.jump_mode:
                player.move("jdown", maze)
                player.jump_mode = False
            else:
                player.move("down", maze)
        elif action == curses.KEY_LEFT:
            if player.jump_mode:
                player.move("jleft", maze)
                player.jump_mode = False
            else:
                player.move("left", maze)
        elif action == curses.KEY_RIGHT:
            if player.jump_mode:
                player.move("jright", maze)
                player.jump_mode = False
            else:
                player.move("right", maze)
        elif action in [ord('.')]:
            pass
            #one turn rest.
        elif action in key_to_inventory_index and key_to_inventory_index[action] is not None:
            item_index = key_to_inventory_index[action]
            logs.append(player.use_item(item_index))

        elif action in [ord('P'), ord('p')]:
            break
        elif action == ord('m'):
            player.display_full_map = not player.display_full_map

        else:
            continue # Skip loop iteration for other keys

        #Check the tile under the player
        x, y = player.position
        if maze[y][x] == "!":
            player.add_item("ポーション")
            maze[y] = maze[y][:x] + "." + maze[y][x+1:]
            logs.append("ポーションを手に入れた!")
        elif maze[y][x] == "*":
            player.inventory["黄色の宝石"] += 1
            maze[y] = maze[y][:x] + "." + maze[y][x+1:]
            logs.append("黄色の宝石を拾った!")

        elif maze[y][x] in ['>', '<']:
            logs.append("階段にいる！")
            # Check if this stair exists in the master mapping
            if (player.current_map, player.position) in stairs_master:
                destination_map, destination_position = stairs_master[(player.current_map, player.position)]
                # Now move the player to destination_map and destination_position
                player.current_map = destination_map
                maze = all_maps[player.current_map]
                player.position = destination_position
                logs.append("階段を登った/降った")

        for monster in monsters:
            if is_adjacent(player.position, monster.position):
                monster.isAdjacent = True
                battle = Battle(player, monster)
                logs.append(battle.commence_battle())
        
                if monster.health <= 0:
                    monsters.remove(monster)
                    # Update the maze to remove the monster character
                    x, y = monster.position
                    maze[y] = maze[y][:x] + "%" + maze[y][x+1:]
            else:
                monster.isAdjacent = False

        

if __name__ == "__main__":
    curses.wrapper(game)