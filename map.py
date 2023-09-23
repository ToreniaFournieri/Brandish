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
    """Get the maze view based on the player's position."""
    px, py = player.position
    
    # Define the vision limits
    up = 10
    down = 10
    left = 10
    right = 10

    # Slice the maze to get the player's view
    start_y = py - up
    end_y = py + down + 1
    start_x = px - left
    end_x = px + right + 1
    
    view = []
    for y in range(start_y, end_y):
        row = []
        for x in range(start_x, end_x):
            if 0 <= y < len(maze) and 0 <= x < len(maze[0]):
                row.append(maze[y][x])
            else:
                row.append(1)  # append wall for cells outside the maze
        view.append(row)
    
    # Place the player in the relative view
    view[up][left] = "🚶"

    return view

