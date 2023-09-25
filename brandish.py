# -*- coding: utf-8 -*-
import blessed
from map import *
from map_master import *
from player import *
from monster import *
from renderer import *

term = blessed.Terminal()

def game():
    with term.cbreak(), term.hidden_cursor():
        # Generate the maze and find the starting position
        global maze    
        maze = Cave_map1

        # Find the starting position
        start_position = [(x, y) for y, row in enumerate(maze) for x, cell in enumerate(row) if cell == "Ｓ"][0]
        monsters = []

        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == "🐀":
                    monster = Monster("🐀大鼠",40,"1d3",0,2,position=(x, y))  # Assuming Monster class has a position attribute
                    monsters.append(monster)

        renderer = Renderer()
        logs = []

        player = Player(start_position)
        player.current_map = find_map_name(maze)

        while True:
            # Clear screen
            print(term.clear)
            renderer.render(term, player , maze, logs, monsters)
            action = term.inkey()

            # Get user input
            key_to_inventory_index = {
                'a': 0 if len(player.inventory) > 0 else None,
                's': 1 if len(player.inventory) > 1 else None,
                'd': 1 if len(player.inventory) > 2 else None,
                'f': 1 if len(player.inventory) > 3 else None,
                'g': 1 if len(player.inventory) > 4 else None,
                'h': 1 if len(player.inventory) > 5 else None,
                # ... and so on, but make sure to check if the item exists before accessing!
            }

            if action == 'z':
                player.jump_mode = True
                continue

            if player.directionSkillOrItem == "🪄衝撃の杖":
                if action == '\x1b[A':
                    use_wand_of_strike(player, "up", maze, monsters)
                    player.directionSkillOrItem = False
                    continue
                elif action == '\x1b[B':
                    use_wand_of_strike(player, "down", maze, monsters)
                    player.directionSkillOrItem = False
                    continue
                elif action == '\x1b[C':
                    use_wand_of_strike(player, "right", maze, monsters)
                    player.directionSkillOrItem = False
                    continue
                elif action == '\x1b[D':
                    use_wand_of_strike(player, "left", maze, monsters)
                    player.directionSkillOrItem = False
                    continue
            

            # Translate action into game command
            if action == '\x1b[A':
                if player.jump_mode:
                    logs.append(player.move("jup", maze))
                    player.jump_mode = False
                else:
                    logs.append(player.move("up", maze))
            elif action == '\x1b[B':
                if player.jump_mode:
                    logs.append(player.move("jdown", maze))
                    player.jump_mode = False
                else:
                    logs.append(player.move("down", maze))
            elif action == '\x1b[C':
                if player.jump_mode:
                    logs.append(player.move("jright", maze))
                    player.jump_mode = False
                else:
                    logs.append(player.move("right", maze))
            elif action == '\x1b[D':
                if player.jump_mode:
                    logs.append(player.move("jleft", maze))
                    player.jump_mode = False
                else:
                    logs.append(player.move("left", maze))
            elif action in ['.']:
                pass
                #one turn rest.
            elif action in key_to_inventory_index and key_to_inventory_index[action] is not None:
                item_index = key_to_inventory_index[action]
                logs.append(player.use_item(item_index))

            elif action in ['P', 'p', term.KEY_ESCAPE]:
                print(term.clear)            
                break

            else:
                continue # Skip loop iteration for other keys

            #Check the tile under the player
            x, y = player.position
            if maze[y][x] == "🍾":
                player.add_item("🍾ポーション")
                maze[y] = maze[y][:x] + "・" + maze[y][x+1:]
                logs.append("🍾ポーションを手に入れた!")
            elif maze[y][x] == "💎":
                player.inventory["💎黄色の宝石"]
                maze[y] = maze[y][:x] + "・" + maze[y][x+1:]
                logs.append("💎黄色の宝石を拾った!")
            elif maze[y][x] == "💰":
                player.gold += 10
                maze[y] = maze[y][:x] + "・" + maze[y][x+1:]  # Replace the gold with an empty tile
                logs.append("💰お金を10円手に入れたぞ！")
            elif maze[y][x] == "🪄":
                player.add_item("🪄衝撃の杖")
                player.add_item("🪄衝撃の杖")
                player.add_item("🪄衝撃の杖")
                player.add_item("🪄衝撃の杖")
                player.add_item("🪄衝撃の杖")
                player.add_item("🪄衝撃の杖")
                maze[y] = maze[y][:x] + "・" + maze[y][x+1:]
                logs.append("🪄衝撃の杖を手に入れたぞ！！")
        

            elif maze[y][x] in ['🔼', '🔽']:
                # Check if this stair exists in the master mapping
                if (player.current_map, player.position) in stairs_master:
                    destination_map, destination_position = stairs_master[(player.current_map, player.position)]
                    # Now move the player to destination_map and destination_position
                    player.current_map = destination_map
                    maze = all_maps[player.current_map]
                    player.position = destination_position
                    logs.append("階段を登った/降った")
            elif maze[y][x] == "🕳":
                player.health -= 12
                player.gold -= 1
                #maze[y] = maze[y][:x] + "・" + maze[y][x+1:]  # Replace the gold with an empty tile
                logs.append("🕳穴に落ちてしまった！痛い！12のダメージを受けた！💰お金を1円無くした！")

            for monster in monsters:
                if is_in_sight(player.position, monster.position):
                    monster.distance = calculate_distance(player.position, monster.position)
                    monster.isInSight =True
                else:
                    monster.distance = 100 # far away 
                    monster.isInSight =False
                    
                if is_adjacent(player.position, monster.position):
                    monster.isAdjacent = True
                    battle = Battle(player, monster)
                    logs.append(battle.commence_battle())
        
                    if monster.health <= 0:
                        monsters.remove(monster)
                        # Update the maze to remove the monster character
                        x, y = monster.position
                        maze[y] = maze[y][:x] + "％" + maze[y][x+1:]
                else:
                    monster.isAdjacent = False

if __name__ == "__main__":
    game()