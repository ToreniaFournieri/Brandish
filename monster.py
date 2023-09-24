import random
import curses
from collections import defaultdict
from player import *

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
