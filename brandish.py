from map import *
from map_master import *
from entities import *
import curses


def game(stdscr):
    # Set up curses settings
    curses.curs_set(0)  # hide cursor
    stdscr.keypad(1)    # enable special keys
    stdscr.timeout(100) # set getch() non-blocking
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_MAGENTA)  # Foreground: White, Background: Blue for current health

    # Generate the maze and find the starting position
    global maze    
    maze = maze_map

    # Find the starting position
    start_position = [(x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == "S"][0]
    monsters = []

    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == "M":
                monster = Monster("大鼠",40,"1d3",0,2,position=(x, y))  # Assuming Monster class has a position attribute
                monsters.append(monster)
                #maze[y][x] = "M"  # This can be changed based on how you want to represent monsters in the maze

    jump_mode = False
    display_full_map = False  # Add this outside the game loop

    logs = []

    player = Player(start_position)
    while True:
        # Use curses to display
        stdscr.clear()

        

        # Show player stats and message below the maze
        player.display_stats(stdscr, 0, 0)




        #display_maze(maze, player.position)
        relative_view = get_relative_view(maze, player)
        view_display = [''.join(["#" if cell == 1 else " " if cell == 0 else cell for cell in row]) for row in relative_view]
        # Display the player's relative view of the maze



        monsterLine = 12
        for monster in monsters:
            if monster.isAdjacent:
                filled_length = int(20 * (monster.health / monster.max_health))
                unfilled_length = 20 - filled_length
    
                filled_segment = " " * filled_length
                unfilled_segment = " " * unfilled_length

                health_text = f"{monster.name} {monster.health}/{monster.max_health}".ljust(20)

                for i, char in enumerate(health_text):
                    if i < filled_length:
                        stdscr.addstr(monsterLine, 0 + i, char, curses.color_pair(1) | curses.A_BOLD)
                    else:
                        stdscr.addstr(monsterLine, 0 + i, char, curses.A_BOLD)




                monsterLine += 1


        visual_maze = generate_visual_2D_view(view_display)
        for idx, row in enumerate(visual_maze):
            stdscr.addstr(idx +1, 26, ''.join(map(str, row)))

        stdscr.addstr(len(visual_maze) + 5, 0, "方向キーで移動, Pでやめる: ")

        # Check for game over
        if maze[player.position[1]][player.position[0]] == "E":
            logs.append("おめでとう！ゲームクリア")
            break
        elif player.isDead:
            logs.append(f"{player.name}は死んでしまった！おしまい")
            break

        pos = 0
        for log in logs:
            stdscr.addstr(len(visual_maze) + 6 + pos, 0, f"{log}")
            pos += 1


        stdscr.refresh()

        # Keep only the latest 5 logs
        if len(logs) > 5:
            logs.pop(0)

        stdscr.addstr(0, 50, f"装備")
        stdscr.addstr(1, 50, f"左手: {player.left_hand}")
        stdscr.addstr(2, 50, f"鎧: {player.armour}")
        stdscr.addstr(3, 50, f"右手: {player.right_hand}")

        stdscr.addstr(5, 50, f"左指輪: {player.left_ring}")
        stdscr.addstr(6, 50, f"右指輪: {player.right_ring}")

        stdscr.addstr(0, 70, f"スキル")
        stdscr.addstr(1, 70, f"z: ジャンプ {jump_mode}")
        stdscr.addstr(2, 70, f"m: 大きい地図表示 {display_full_map}")

        # Display inventory somewhere on the screen
        inventory_display_position = (8, 50)  # Or wherever you want it
        stdscr.addstr(inventory_display_position[0], inventory_display_position[1], "アイテム:")
        shortcut_keys = ['a', 's', 'd', 'f', 'g', 'h']  # ... extend this list if needed
        for idx, (item, count) in enumerate(player.inventory.items()):
            stdscr.addstr(inventory_display_position[0] + idx + 1, inventory_display_position[1], f"{shortcut_keys[idx]}: {item}: {count}")

        # Then, conditionally display the map:
        if display_full_map:
            for idx, row in enumerate(maze):
                for jdx, cell in enumerate(row):
                    if (jdx, idx) == player.position:
                        stdscr.addstr(idx, jdx +18, "@")  # Display player with '@' character
                    else:
                        stdscr.addstr(idx, jdx + 18, cell)
                

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
            jump_mode = True
            continue
        # Translate action into game command
        if action == curses.KEY_UP:
            if jump_mode:
                logs.append(player.move("jup", maze))
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
        elif action in [ord('.')]:
            pass
            #one turn rest.
        elif action in key_to_inventory_index and key_to_inventory_index[action] is not None:
            item_index = key_to_inventory_index[action]
            logs.append(player.use_item(item_index))

        elif action in [ord('P'), ord('p')]:
            break
        elif action == ord('m'):
            display_full_map = not display_full_map

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