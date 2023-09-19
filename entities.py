# Player class and any other game entities
class Player:
    def __init__(self, start_position):
        self.level = 1
        self.health = 76
        self.max_health = 100
        self.mana = 32
        self.max_mana = 100
        self.attack_power = 10
        self.defense = 5
        self.gold = 0
        self.position = start_position
        self.left_hand = "Shield"
        self.armour = "Armour"
        self.right_hand = "Short sowrd"
        self.shortcut = "Potion"
        self.left_ring = "None"
        self.right_ring = "None"

    def move(self, action, maze):
        x, y = self.position
        dx, dy = 0, 0

        if action == "up" and maze[y-1][x] != 1:
            self.position = (x, y-1)

        elif action == "down" and maze[y+1][x] != 1:
            self.position = (x, y+1)

        elif action == "right" and maze[y][x+1] != 1:
            self.position = (x+1, y)

        elif action == "left" and maze[y][x-1] != 1:
            self.position = (x-1, y)


        else:
            print("Invalid direction or there's a wall!")

    
    def generate_bar(self, current, max_value, bar_width=20):
        ratio = current / max_value
        filled_length = int(bar_width * ratio)
        unfilled_length = bar_width - filled_length
    
        # Use Unicode block elements for a more graphical look
        filled_portion = '█' * filled_length
        unfilled_portion = '░' * unfilled_length
    
        return f"{filled_portion}{unfilled_portion}"


    def display_stats(self):
        stats = []
        stats.append(f"ライフ: {self.health}/ {self.max_health}")
        health_bar = self.generate_bar(self.health, self.max_health)
        stats.append(f" {health_bar}")
        stats.append(f"マナ: {self.mana}/ {self.max_mana}")
        Mana_bar = self.generate_bar(self.mana, self.max_mana)
        stats.append(f" {Mana_bar}")

        stats.append(f"攻撃力: {self.attack_power}")
        stats.append(f"防御力: {self.defense}")
        stats.append(f" ")

        stats.append(f"レベル:   {self.level} ")


        stats.append(f"お金: {self.gold}")
        stats.append(f"位置: {self.position}")
        return "\n".join(stats)

