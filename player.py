import random
import curses
from collections import defaultdict
from use_items import *

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
        self.jump_mode = False
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
                    directionSkillOrItem = "🪄衝撃の杖"
                    log = f"🪄衝撃の杖を使う、どの方向に？矢印で選択"
            else:
                log = "そのアイテムを持っていない"
        else:
            log = "そのアイテムは存在しない"
        return log



    def move(self, action, maze):
        x, y = self.position
        dx, dy = 0, 0
        MOVEABLE_TILES = {"Ｓ","・", "％", "🚪", "🕳", "💰", "🗡","🪄", "🛡", "🍾", "💎","🔽", "🔼"} 
        text = ""
        if action == "up" and maze[y-1][x] in MOVEABLE_TILES:
            self.position = (x, y-1)
        elif action == "jup" and maze[y-2][x] in MOVEABLE_TILES:
            self.position = (x, y-2)

        elif action == "down" and maze[y+1][x] in MOVEABLE_TILES:
            self.position = (x, y+1)
        elif action == "jdown" and maze[y+2][x] in MOVEABLE_TILES:
            self.position = (x, y+2)

        elif action == "right" and maze[y][x+1] in MOVEABLE_TILES:
            self.position = (x+1, y)
        elif action == "jright" and maze[y][x+2] in MOVEABLE_TILES:
            self.position = (x+2, y)

        elif action == "left" and maze[y][x-1] in MOVEABLE_TILES:
            self.position = (x-1, y)
        elif action == "jleft" and maze[y][x-2] in MOVEABLE_TILES:
            self.position = (x-2, y)
        else:
            text = "Invalid direction or there's a wall!"


        return text


    def display_stats(self, term, start_y, start_x):
        # Define colors
        health_style = term.white_on_green
        mana_style = term.white_on_cyan


        print(term.move(start_y, start_x) + f"{self.name}")

        # Display Health
        health_text = f"体力: {self.health}/{self.max_health}".ljust(20)
        filled_length = int(20 * (self.health / self.max_health))

        for i, char in enumerate(health_text):
            if i < filled_length:
                print(term.move(start_y+1, start_x + i) + health_style(char)
            else:
                stdscr.addstr(start_y+1, start_x + i, char, curses.A_BOLD)

        # Display Mana
        mana_text = f"気力: {self.mana}/{self.max_mana}".ljust(20)
        filled_length = int(20 * (self.mana / self.max_mana))

        for i, char in enumerate(mana_text):
            if i < filled_length:
                stdscr.addstr(start_y + 2, start_x + i, char, curses.color_pair(3) | curses.A_BOLD)
            else:
                stdscr.addstr(start_y + 2, start_x + i, char, curses.A_BOLD)

        # Other stats
        print(term.move(start_y + 3, start_x) + f"攻撃力: {self.attack_power}".ljust(20))
        print(term.move(start_y + 4, start_x) + f"防御力: {self.defense}".ljust(20))
        print(term.move(start_y + 5, start_x) + " ".ljust(20))  # Empty line
        print(term.move(start_y + 6, start_x) + f"レベル: {self.level}".ljust(20))
        print(term.move(start_y + 7, start_x) + f"お金: {self.gold}円".ljust(20))
        print(term.move(start_y + 8, start_x) + f"位置: {self.position}".ljust(20))
    

