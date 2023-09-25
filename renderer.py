import blessed
from map_master import *
from player import *
from monster import *
from brandish import *
from wcwidth import wcswidth

def ljust_for_display(s, width):
    """Left-justify string `s` to a display width of `width`."""
    return s + ' ' * (width - wcswidth(s))

class Renderer:
    def __init__(self):
        pass
    

    def render(self,term, player, maze, logs, monsters):
        # Clear screen
        print(term.clear)
       
        # Show player stats and message below the maze
        start_y = 0
        start_x = 0
        # Define colors
        health_style = term.white_on_green
        mana_style = term.white_on_cyan

        print(term.move(start_y, start_x) + f"{player.name}")

        # Display Health
        health_text = f"体力: {player.health}/{player.max_health}".ljust(20)
        filled_length = int(20 * (player.health / player.max_health))

        current_pos = start_x  # Initialize the position counter
        for char in health_text:
            if current_pos < start_x + filled_length:
                print(term.move(start_y + 1, current_pos) + health_style(char) + char, end='')
            else:
                print(term.move(start_y + 1, current_pos) + char, end='')
            current_pos += wcswidth(char)

        # Display Mana
        mana_text = f"気力: {player.mana}/{player.max_mana}".ljust(20)
        filled_length = int(20 * (player.mana / player.max_mana))

        current_pos = start_x  # Reset the position counter for the mana display
        for char in mana_text:
            if current_pos < start_x + filled_length:
                print(term.move(start_y + 2, current_pos) + mana_style(char) + char, end='')
            else:
                print(term.move(start_y + 2, current_pos) + char, end='')
            current_pos += wcswidth(char)


        # Other stats
        print(term.move(start_y + 3, start_x) + f"攻撃力: {player.attack_power}".ljust(20))
        print(term.move(start_y + 4, start_x) + f"防御力: {player.defense}".ljust(20))
        print(term.move(start_y + 5, start_x) + " ".ljust(20))  # Empty line
        print(term.move(start_y + 6, start_x) + f"レベル: {player.level}".ljust(20))
        print(term.move(start_y + 7, start_x) + f"お金: {player.gold}円".ljust(20))
        print(term.move(start_y + 8, start_x) + f"位置: {player.position}".ljust(20))
    

        #display_maze(maze, player.position)
        relative_view = get_relative_view(maze, player)
        view_display = [''.join(["　" if cell == 1 else " " if cell == 0 else cell for cell in row]) for row in relative_view]
        # Display the player's relative view of the maze

        monsterLine = 12
        # Sort the monsters by distance from the player
        visible_monsters = [monster for monster in monsters if monster.isInSight]
        sorted_monsters = sorted(visible_monsters, key=lambda monster: monster.distance)

        # Display only the first 5 monsters from the sorted list
        for monster in sorted_monsters[:5]:
            filled_length = int(20 * (monster.health / monster.max_health))
            unfilled_length = 20 - filled_length

            filled_segment = " " * filled_length
            unfilled_segment = " " * unfilled_length

            health_text = ljust_for_display(f"{monster.name} {monster.health}/{monster.max_health}", 20)

            # Determine the style based on the isAdjacent attribute
            style = term.bold if monster.isAdjacent else term.normal
            white_on_magenta = style + term.color(7) + term.on_color(5)

            current_pos = 0
            for char in health_text:
                if current_pos < filled_length:
                    print(term.move_xy(current_pos, monsterLine) + white_on_magenta + char, end='')
                else:
                    print(term.move_xy(current_pos, monsterLine) + term.normal + style + char, end='')
                current_pos += wcswidth(char)

            monsterLine += 1



        print(term.move(0, 26) + term.normal + f"{player.current_map}")
        #stdscr.addstr(0, 26, f"{player.current_map}")
        generate_visual_2D_view(term, view_display, 1,26)
 
        print(term.move(23, 0) + "方向キーで移動, Pでやめる: ")
        #stdscr.addstr(18+ 5, 0, "方向キーで移動, Pでやめる: ")

        # Check for game over
        if  player.isDead:
            logs.append(f"{player.name}は死んでしまった！おしまい")
            return False

        # Keep only the latest 5 logs
        while len(logs) > 5:
            logs.pop(0)

        pos = 0
        for log in reversed(logs):
            print(term.move(24 + pos, 0) + term.clear_eol + f"{log}")
            pos += 1


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
