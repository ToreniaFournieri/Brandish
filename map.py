import random
import os
from visual_renderer import *

def display_maze(maze, player_position):
    for y, row in enumerate(maze):
        display_row = []
        for x, cell in enumerate(row):
            if (x, y) == player_position:
                display_row.append("P")  # Representing the player with "P"
            else:
                if cell == 0:
                    display_row.append(".")
                elif cell == 1:
                    display_row.append("#")
                else:
                    display_row.append(cell)
        print(''.join(display_row))

'''        
def rotate_maze(maze, new_direction):
    """Rotate the maze based on the new player's direction."""
    if new_direction == "N":
        return maze
    elif new_direction == "W":
        return [list(row) for row in zip(*maze[::-1])]
    elif new_direction == "S":
        return [row[::-1] for row in maze[::-1]]
    elif new_direction == "E":
        return [list(reversed(row)) for row in zip(*maze)]


return maze
    elif new_direction == "W":
        return [list(row) for row in zip(*maze[::-1])]
    elif new_direction == "S":
        return [row[::-1] for row in maze[::-1]]
    elif new_direction == "E":
        return [list(reversed(row)) for row in zip(*maze)]
        #return [list(row) for row in zip(*maze)]

def get_rotated_position(position, new_direction, maze_width, maze_height):
    x, y = position
    if new_direction == "N":
        return x, y
    elif new_direction == "E":
        return x, maze_width - y -1

        #return y, maze_width - x - 1 
    elif new_direction == "S":
        return maze_width - x - 1, maze_height - y - 1
    elif new_direction == "W":
        return maze_height - y - 1, x


'''
def pad_relative_view(view, up, down, left, right):
    """Pad the player's view with walls to ensure a consistent size."""
    # Calculate the number of rows and columns to pad
    pad_top = up - len(view) if len(view) < up else 0
    pad_bottom = down + 1 - len(view) + pad_top if len(view) + pad_top < up + down + 1 else 0
    pad_left = left - len(view[0]) if len(view[0]) < left else 0
    pad_right = right + 1 - len(view[0]) + pad_left if len(view[0]) + pad_left < left + right + 1 else 0
    
    # Pad rows
    for _ in range(pad_top):
        view.insert(0, [1] * (len(view[0]) + pad_left + pad_right))
    for _ in range(pad_bottom):
        view.append([1] * (len(view[0]) + pad_left + pad_right))
    
    # Pad columns
    for row in view:
        for _ in range(pad_left):
            row.insert(0, 1)
        for _ in range(pad_right):
            row.append(1)
    
    return view



def get_relative_view(maze, player):
    """Get the maze view based on the player's position and direction."""
    #rotated_maze = rotate_maze(maze, player.direction)
    #rotated_position = get_rotated_position(player.position, player.direction, len(maze[0]), len(maze))
    #px, py = rotated_position
    px, py = player.position

    
    # Define the vision limits
    up = 6
    down = 1
    left = 3
    right = 3
    
    # Define the vision limits
    up = 10
    down = 10
    left = 10
    right = 10

    # Rotate the maze based on direction
    if player.direction == "N":
        rotated_maze = maze
    elif player.direction == "W":
        rotated_maze = [list(row) for row in zip(*maze)]
        px, py = py, len(maze[0]) - px - 1
    elif player.direction == "S":
        rotated_maze = [row[::-1] for row in maze[::-1]]
        px, py = len(maze[0]) - px - 1, len(maze) - py - 1
    elif player.direction == "E":
        rotated_maze = [list(row)[::-1] for row in zip(*maze)]
        px, py = len(maze) - py - 1, px

    # Slice the maze to get the player's view
    start_y = max(0, py - up)
    end_y = min(len(rotated_maze), py + down + 1)
    start_x = max(0, px - left)
    end_x = min(len(rotated_maze[0]), px + right + 1)
    
    view = [row[start_x:end_x] for row in rotated_maze[start_y:end_y]]
    view = pad_relative_view(view, up, down, left, right)
    
    # Place the player in the relative view
    view[up][left] = "P"



    return view

