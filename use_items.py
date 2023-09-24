import random


def use_wand_of_strike(player, direction, maze, monsters):
    # The distance the shockwave travels
    DISTANCE = 8

    # Coordinates for direction
    dx, dy = 0, 0
    if direction == "up":
        dx, dy = 0, -1
    elif direction == "down":
        dx, dy = 0, 1
    elif direction == "left":
        dx, dy = -1, 0
    elif direction == "right":
        dx, dy = 1, 0

    # Check each tile in the direction of the shockwave
    for i in range(1, DISTANCE + 1):
        x, y = player.position[0] + dx * i, player.position[1] + dy * i

        # Check for monsters and deal damage
        for monster in monsters:
            if monster.position == (x, y):
                damage = random.randint(1, 10)  # 1d10 damage
                monster.health -= damage
                if monster.health <= 0:
                    pass # remove the monster, add death logic, etc.

        # Change the tile texture
        if maze[y][x] == "・":
            maze[y] = maze[y][:x] + "、" + maze[y][x+1:]

        # Stop the shockwave if it hits a wall or goes out of bounds
        if maze[y][x] == "＃":
            break

