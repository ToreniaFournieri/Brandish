# Player class and any other game entities
class Player:
    def __init__(self, start_position):
        self.health = 100
        self.attack_power = 10
        self.defense = 5
        self.gold = 0
        self.position = start_position
        self.direction = "N"

    def move(self, direction, maze):
        x, y = self.position
        if direction == "W" and maze[y-1][x] != 1:
            self.position = (x, y-1)
        elif direction == "S" and maze[y+1][x] != 1:
            self.position = (x, y+1)
        elif direction == "D" and maze[y][x+1] != 1:
            self.position = (x+1, y)
        elif direction == "A" and maze[y][x-1] != 1:
            self.position = (x-1, y)
        else:
            print("Invalid direction or there's a wall!")

    def display_stats(self):
        print(f"Health: {self.health}")
        print(f"Attack Power: {self.attack_power}")
        print(f"Defense: {self.defense}")
        print(f"Gold: {self.gold}")
        print(f"Position: {self.position}")

