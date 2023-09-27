import random
import curses
from collections import defaultdict
from use_items import *
from monster import *

# Player class and any other game entities
class Player:
    def __init__(self, start_position):
        self.name ="🚶主人公"
        self.level = 1
        self.health = 76
        self.isDead = False
        self.max_health = 100
        self.mana = 32
        self.max_mana = 100
        self.attack_power = "1d6"
        self.defense = 1
        self.gold = 0
        self.position = start_position
        self.left_hand = "Shield"
        self.armour = "Armour"
        self.right_hand = "Short sowrd"
        self.left_ring = "None"
        self.right_ring = "None"
        self.current_map = ""
        self.inventory = defaultdict(int)  # Using defaultdict from collections module
        self.display_full_map = False  # Add this outside the game loop
        self.directionSkillOrItem = ""

    def add_item(self, item_name):
        self.inventory[item_name] += 1

    def use_item(self, item_index):
        log = ""
        items = list(self.inventory.keys())
        if item_index < len(items):
            item_name = items[item_index]
            if self.inventory[item_name] > 0:
                self.inventory[item_name] -= 1
                # If item count reaches 0, remove it from the inventory
                if self.inventory[item_name] == 0:
                    del self.inventory[item_name]
                # apply item effects here, e.g.:
                if item_name == "🍾ポーション":
                    potential_new_health = self.health + 50
                    actual_restore = min(self.max_health, potential_new_health) - self.health
                    self.health += actual_restore
                    log = f"ポーションを使い体力が{actual_restore}回復した!"
                if item_name == "🪄衝撃の杖":
                    self.directionSkillOrItem = "🪄衝撃の杖"
                    log = f"🪄衝撃の杖を使う、どの方向に？矢印で選択"
            else:
                log = "そのアイテムを持っていない"
        else:
            log = "そのアイテムは存在しない"
        return log

    def move_rock(self, rock_position, direction, maze):
        x, y = rock_position # position

        # Define movement deltas
        dx, dy = 0, 0
        if direction == "up":
            dx, dy = 0, -1
        elif direction == "down":
            dx, dy = 0, 1
        elif direction == "left":
            dx, dy = -1, 0
        elif direction == "right":
            dx, dy = 1, 0

        # Check the tile beyond the rock in the direction of movement
        if maze[y + dy][x + dx] == '・':  # Empty space
            # Update the maze to reflect the rock's new position
            maze[y] = maze[y][:x] + "・" + maze[y][x+1:]
            # Place the rock in its new position
            new_y = y + dy
            new_x = x + dx
            maze[new_y] = maze[new_y][:new_x] + "🪨" + maze[new_y][new_x+1:]
            return True

        elif maze[y + dy][x + dx]  == '🕳':  # Hole
            # Update the maze to reflect the rock's new position
            maze[y] = maze[y][:x] + "・" + maze[y][x+1:]
            # Place the rock in its new position
            new_y = y + dy
            new_x = x + dx
            maze[new_y] = maze[new_y][:new_x] + "・" + maze[new_y][new_x+1:]
            return True


        #Faild to move the lock
        return False

    def snatch_object(self, direction, maze):
        log = ""
        # Define movement deltas
        dx, dy = 0, 0
        if direction == "up":
            dx, dy = 0, -1
        elif direction == "down":
            dx, dy = 0, 1
        elif direction == "left":
            dx, dy = -1, 0
        elif direction == "right":
            dx, dy = 1, 0

        x, y = self.position

        # Check each tile in the direction up to 5 tiles away
        for i in range(1, 6):
            target_x, target_y = x + i * dx, y + i * dy
        
            # Check if we're out of bounds
            if target_x < 0 or target_y < 0 or target_x >= len(maze[0]) or target_y >= len(maze):
                break
        
            # Check if the tile contains the object (rock)
            target =maze[target_y][target_x]
            if target not in {"・", "、"}:
                # Move the object to the tile next to the player
                maze[target_y] = maze[target_y][:target_x] + "・" + maze[target_y][target_x+1:]
                maze[y + dy] = maze[y + dy][:x + dx] + target + maze[y + dy][x + dx + 1:]
                log = f"{maze[target_y][target_x]}　を引き寄せた"
                break

        return log


    def move(self, action, maze):
        x, y = self.position
        dx, dy = 0, 0

               
        MOVEABLE_TILES = {"Ｓ","・","、", "％", "🚪", "🕳", "💰", "🗡","🪄", "🛡", "🍾", "💎","🔽", "🔼", "🪨"}

        text = ""
        if action == "up" and y-1 >= 0 and maze[y-1][x] in MOVEABLE_TILES:  # Added boundary check
            if maze[y-1][x] == "🪨":
                if self.move_rock((x, y-1), action, maze):
                    self.position = (x, y-1)                    
                else:
                    return "岩を動かせられない！"
            else:
                self.position = (x, y-1)
        elif action == "jup" and y-2 >= 0 and maze[y-2][x] in MOVEABLE_TILES:
            self.position = (x, y-2)

        elif action == "down" and y+1 < len(maze) and maze[y+1][x] in MOVEABLE_TILES:
            if maze[y+1][x] == "🪨":
                if self.move_rock((x, y+1), action, maze):
                    self.position = (x, y+1)
                else:
                    return "岩を動かせられない！"
            else:
                self.position = (x, y+1)
        elif action == "jdown" and y+2 < len(maze) and maze[y+2][x] in MOVEABLE_TILES:
            self.position = (x, y+2)

        elif action == "right" and x+1 < len(maze[0]) and maze[y][x+1] in MOVEABLE_TILES:  # Added boundary check
            if maze[y][x+1] == "🪨":
                if self.move_rock((x+1, y), action, maze):
                    self.position = (x+1, y)
                else:
                    return "岩を動かせられない！"
            else:
                self.position = (x+1, y)
        elif action == "jright" and x+2 < len(maze[0]) and maze[y][x+2] in MOVEABLE_TILES:
            self.position = (x+2, y)

        elif action == "left" and x-1 >= 0 and maze[y][x-1] and maze[y][x-1] in MOVEABLE_TILES:
            if maze[y][x-1] == "🪨":
                if self.move_rock((x-1, y), action, maze):
                    self.position = (x-1, y)
                else:
                    return "岩を動かせられない！"
            else:
                self.position = (x-1, y)
        elif action == "jleft" and x-2 >= 0 and maze[y][x-1] and maze[y][x-2] in MOVEABLE_TILES:
            self.position = (x-2, y)

        else:
            text = "移動できない！"


        return text



