import blessed
from map_master import *
from player import *
from monster import *
from brandish import *

class Renderer:
    def __init__(self):
        pass
    

    def render(self,term, player, maze, logs, monsters):
        # Clear screen
        print(term.clear)
       
        # Show player stats and message below the maze
        player.display_stats(term, 0, 0)

        #display_maze(maze, player.position)
        relative_view = get_relative_view(maze, player)
        view_display = [''.join(["＃" if cell == 1 else " " if cell == 0 else cell for cell in row]) for row in relative_view]
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

        print(term.move(0, 26) + f"{player.current_map}")
        #stdscr.addstr(0, 26, f"{player.current_map}")
        generate_visual_2D_view(term, view_display, 1,26)
 
        print(term.move(23, 0) + "方向キーで移動, Pでやめる: ")
        #stdscr.addstr(18+ 5, 0, "方向キーで移動, Pでやめる: ")

        # Check for game over
        if maze[player.position[1]][player.position[0]] == "E":
            logs.append("おめでとう！ゲームクリア")
            return False
        elif player.isDead:
            logs.append(f"{player.name}は死んでしまった！おしまい")
            return False

        pos = 0
        for log in logs:
            #stdscr.addstr(18 + 6 + pos, 0, f"{log}")
            print(term.move(24 + pos, 0) +  f"{log}")
            pos += 1


        #stdscr.refresh()

        # Keep only the latest 5 logs
        if len(logs) > 5:
            logs.pop(0)

        print(term.move(0, 70) + "装備")
        print(term.move(1, 70) + f"左手: {player.left_hand}")
        print(term.move(2, 70) + f"鎧: {player.armour}")
        print(term.move(3, 70) + f"右手: {player.right_hand}")

        print(term.move(5, 70) + f"左指輪: {player.left_ring}")
        print(term.move(6, 70) + f"右指輪: {player.right_ring}")

        print(term.move(0, 90) + "スキル")
        print(term.move(1, 90) + f"z: ジャンプ {player.jump_mode}")
        # Display inventory somewhere on the screen
        inventory_display_position = (8, 70)  # Or wherever you want it
        print(term.move(inventory_display_position[0], inventory_display_position[1]) + "アイテム:")
        shortcut_keys = ['a', 's', 'd', 'f', 'g', 'h']  # ... extend this list if needed
        for idx, (item, count) in enumerate(player.inventory.items()):
            print(term.move(inventory_display_position[0] + idx + 1, inventory_display_position[1]) + f"{shortcut_keys[idx]}: {item}: {count}")

        # Then, conditionally display the map:
        if player.display_full_map:
            for idx, row in enumerate(maze):
                for jdx, cell in enumerate(row):
                    if (jdx, idx) == player.position:
                        print(term.move(idx, jdx + 18) + "🚶")  # Display player with '🚶' character
                    else:
                        print(term.move(idx, jdx + 18) + cell)
