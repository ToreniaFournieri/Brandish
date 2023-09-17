# Player class and any other game entities
class Player:
    def __init__(self, start_position):
        self.health = 100
        self.attack_power = 10
        self.defense = 5
        self.gold = 0
        self.position = start_position
        self.direction = "N"
        self.previous_direction = "N"

    def move(self, action, maze):
        x, y = self.position
        self.previous_direction = self.direction
        dx, dy = 0, 0

        if action == "W":  # Move forward
            if self.direction == "N":
                dx, dy = 0, -1
            elif self.direction == "E":
                dx, dy = 1, 0
            elif self.direction == "S":
                dx, dy = 0, 1
            elif self.direction == "W":
                dx, dy = -1, 0

        elif action == "S":  # Move backward
            if self.direction == "N":
                dx, dy = 0, 1
            elif self.direction == "E":
                dx, dy = -1, 0
            elif self.direction == "S":
                dx, dy = 0, -1
            elif self.direction == "W":
                dx, dy = 1, 0

        elif action == "D":  # Move right
            if self.direction == "N":
                dx, dy = 1, 0
            elif self.direction == "E":
                dx, dy = 0, 1
            elif self.direction == "S":
                dx, dy = -1, 0
            elif self.direction == "W":
                dx, dy = 0, -1

        elif action == "A":  # Move left
            if self.direction == "N":
                dx, dy = -1, 0
            elif self.direction == "E":
                dx, dy = 0, -1
            elif self.direction == "S":
                dx, dy = 1, 0
            elif self.direction == "W":
                dx, dy = 0, 1
        elif action == "Q":
            self.rotate_left()
        elif action == "E":
            self.rotate_right()
        else:
            print("Invalid direction or there's a wall!")

        # If the movement is valid, update the player's position
        if 0 <= x + dx < len(maze[0]) and 0 <= y + dy < len(maze) and maze[y + dy][x + dx] != 1:
            self.position = (x + dx, y + dy)


    def rotate_left(self):
        directions = ["N", "E", "S", "W"]
        idx = directions.index(self.direction)
        self.direction = directions[(idx - 1) % 4]

    def rotate_right(self):
        directions = ["N", "W", "S", "E"]
        idx = directions.index(self.direction)
        self.direction = directions[(idx - 1) % 4]

    def display_stats(self):
        print(f"Health: {self.health}")
        print(f"Attack Power: {self.attack_power}")
        print(f"Defense: {self.defense}")
        print(f"Gold: {self.gold}")
        print(f"Position: {self.position} {self.direction} ({self.previous_direction})")

