import random
import curses
from collections import defaultdict

# Player class and any other game entities
class Player:
    def __init__(self, start_position):
        self.name ="主人公"
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
        self.inventory = defaultdict(int)  # Using defaultdict from collections module
        self.jump_mode = False
        self.display_full_map = False  # Add this outside the game loop



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
                if item_name == "ポーション":
                    restore = 50
                    self.health += restore  # or however much you want to heal
                    log = f"ポーションを使い体力が{restore}回復した!"
            else:
                log = "そのアイテムを持っていない"
        else:
            log = "そのアイテムは存在しない"
        return log



    def move(self, action, maze):
        x, y = self.position
        dx, dy = 0, 0
        MOVEABLE_TILES = {"S",".", "$", "%", "+", "^", "$", "(", ")", "[", "!","*"} 
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


    def display_stats(self, stdscr, start_y, start_x):
        # Define colors
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_GREEN)  # Blue on Black for player
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_CYAN)  # Blue on Black for player


        stdscr.addstr(start_y, start_x, f"{self.name}")

        # Display Health
        health_text = f"体力: {self.health}/{self.max_health}".ljust(20)
        filled_length = int(20 * (self.health / self.max_health))

        for i, char in enumerate(health_text):
            if i < filled_length:
                stdscr.addstr(start_y+1, start_x + i, char, curses.color_pair(2) | curses.A_BOLD)
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
        stdscr.addstr(start_y + 3, start_x, f"攻撃力: {self.attack_power}".ljust(20))
        stdscr.addstr(start_y + 4, start_x, f"防御力: {self.defense}".ljust(20))
        stdscr.addstr(start_y + 5, start_x, " ".ljust(20))  # Empty line
        stdscr.addstr(start_y + 6, start_x, f"レベル: {self.level}".ljust(20))
        stdscr.addstr(start_y + 7, start_x, f"お金: {self.gold}".ljust(20))
        stdscr.addstr(start_y + 8, start_x, f"位置: {self.position}".ljust(20))
    



class Monster:
    def __init__(self, name, health, attack_power, defense, experience_point, position):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack_power = attack_power
        self.defense = defense
        self.experience_point = experience_point
        self.position = position
        self.isAdjacent = False

def roll_dice(dice_notation):
    """
    Roll dice based on the given dice notation (e.g., "1d3", "2d6").
    Returns the total of the dice rolls.
    """
    num_dice, dice_sides = map(int, dice_notation.split('d'))
    return sum([random.randint(1, dice_sides) for _ in range(num_dice)])

def is_adjacent(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return abs(x1 - x2) <= 1 and abs(y1 - y2) <= 1 and (x1 != x2 or y1 != y2)


class Battle:
    def __init__(self, player, monster):
        self.player = player
        self.monster = monster

    def calculate_damage(self, attacker, defender):
        # Calculate damage considering attacker's attack power and defender's defense.
        # This can be enhanced further.
        raw_damage = roll_dice(attacker.attack_power)
        defense = defender.defense
        return max(1, raw_damage - defense)  # Ensure at least 1 damage

    def player_attack(self):
        damage = self.calculate_damage(self.player, self.monster)
        self.monster.health -= damage
        return damage

    def monster_attack(self):
        damage = self.calculate_damage(self.monster, self.player)
        self.player.health -= damage
        return damage

    def commence_battle(self):
        # Player goes first
        player_damage = self.player_attack()

        # Check if monster is still alive
        if self.monster.health <= 0:
            # Player gains experience, etc.
            return f"{self.monster.name}を倒した！"

        # Monster's turn
        monster_damage = self.monster_attack()

        # Check if player is still alive
        if self.player.health <= 0:
            # Game over logic
            self.player.isDead = True
            return f"{self.player.name}はやられてしまった"


        return f"{self.player.name}は {self.monster.name}に{player_damage}のダメージを与え,{monster_damage}ダメージ受けた"
