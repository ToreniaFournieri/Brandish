import random
# Define constants
E = '.'  # Empty cell
W = '#'  # Wall cell

# Test the function
test_grid = [
    [E, E, E, W, E, E, E, E],
    [E, W, W, W, W, W, W, E],
    [E, W, E, W, E, W, E, E],
    [E, W, W, W, E, W, E, W],
    [E, E, E, E, E, W, E, E],
    [E, E, W, E, E, E, E, E],
    [E, E, E, W, W, E, W, W],
    [E, E, E, E, E, E, W, E]
]

def generate_random_grid(rows, cols, wall_probability=0.4):
    """Generate a random grid with given dimensions and wall probability."""
    return [[W if random.random() < wall_probability else E for _ in range(cols)] for _ in range(rows)]



def generate_visual_2D_view(grid):
    # Get grid dimensions
    rows = len(grid)
    cols = len(grid[0])
    
    # Create an output grid initialized with empty cells
    output = [[E for _ in range(cols)] for _ in range(rows)]
    
        
    # Process each cell in the grid
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == W:
                top = grid[i-1][j] if i > 0 else W
                bottom = grid[i+1][j] if i < rows-1 else W
                top_left = grid[i-1][j-1] if i > 0 and j > 0 else W
                left = grid[i][j-1] if j > 0 else W
                top_right = grid[i-1][j+1]  if i > 0 and j < cols-1 else W
                right = grid[i][j+1] if j < cols-1 else W
                                
                # Determine the Unicode character based on surrounding walls
                # 4 Walls
                # ?W?
                # WWW
                # ?W?
                if top == W and left == W and right == W and bottom == W:
                    output[i][j] = '╋'  # All sides are walls

                # 3 Walls
                # ?W?
                # WWW
                # ?E?
                elif top == W and left == W and right == W and bottom == E:
                    output[i][j] = '╇'
                # ?WW
                # WWE
                # ?W?
                elif top == W and left == W and bottom == W and right == E and top_right == W:
                    output[i][j] = '╉'
                # ?WE
                # WWE
                # ?W?
                elif top == W and left == W and bottom == W and right == E and top_right == E:
                    output[i][j] = '┨'
                # WW?
                # EWW
                # ?W?
                elif top == W and right == W and bottom == W and left == E and top_left == W:
                    output[i][j] = '╊'
                # EW?
                # EWW
                # ?W?
                elif top == W and right == W and bottom == W and left == E and top_left == E:
                    output[i][j] = '┣'
                    
                # ?WW
                # WWE
                # ?W?
                elif top == W and right == W and bottom == W and left == E and top_left == W:
                    output[i][j] = '┠'
                # ?E?
                # WWW
                # ?W?
                elif top == E and right == W and bottom == W and left == W:
                    output[i][j] = '┳'

                # 2 walls
                # ?E?
                # WWW
                # ?E?
                elif top == E and right == W and bottom == E and left == W:
                    output[i][j] = '┯'

                # EWE
                # EWE
                # ?W?
                elif top == W and right == E and bottom == W and left == E and top_right == E and top_left == E:
                    output[i][j] = '┃'
                # WWE
                # EWE
                # ?W?
                elif top == W and right == E and bottom == W and left == E and top_right == E and top_left == W:
                    output[i][j] = '┨'
                # EWW
                # EWE
                # ?W?
                elif top == W and right == E and bottom == W and left == E and top_right == W and top_left == E:
                    output[i][j] = '┠'
                # WWW
                # EWE
                # ?W?
                elif top == W and right == E and bottom == W and left == E and top_right == W and top_left == W:
                    output[i][j] = '╂'

                # ?EW
                # WWE
                # ?W?
                elif top == E and left == W and bottom == W and right == E and top_right == W:
                    output[i][j] = '┱'
                # ?EE
                # WWE
                # ?W?
                elif top == E and left == W and bottom == W and right == E and top_right == E:
                    output[i][j] = '┓'
                # WE?
                # EWW
                # ?W?
                elif top == E and right == W and bottom == W and left == E and top_left == W:
                    output[i][j] = '┲'
                # EE?
                # EWW
                # ?W?
                elif top == E and right == W and bottom == W and left == E and top_left == E:
                    output[i][j] = '┏'

                # ?WW
                # WWE
                # ?E?
                elif top == W and left == W and bottom == E and right == E and top_right == W:
                    output[i][j] = '╃'
                # ?WE
                # WWE
                # ?E?
                elif top == W and left == W and bottom == E and right == E and top_right == E:
                    output[i][j] = '┩'
                # WW?
                # EWW
                # ?E?
                elif top == W and right == W and bottom == E and left == E and top_left == W:
                    output[i][j] = '╄'
                # EW?
                # EWW
                # ?E?
                elif top == W and right == W and bottom == E and left == E and top_left == E:
                    output[i][j] = '┡'

                # 1 wall
                # EWE
                # EWE
                # ?E?
                elif top == W and right == E and bottom == E and left == E and top_right == E and top_left == E:
                    output[i][j] = '╿'
                # WWE
                # EWE
                # ?E?
                elif top == W and right == E and bottom == E and left == E and top_right == E and top_left == W:
                    output[i][j] = '┦'
                # EWW
                # EWE
                # ?E?
                elif top == W and right == E and bottom == E and left == E and top_right == W and top_left == E:
                    output[i][j] = '┞'
                # WWW
                # EWE
                # ?E?
                elif top == W and right == E and bottom == E and left == E and top_right == W and top_left == W:
                    output[i][j] = '╇'

                    
                # ?E?
                # EWE
                # ?W?
                elif top == E and right == E and bottom == W and left == E:
                    output[i][j] = '╻'
                # ?EW
                # WWE
                # ?E?
                elif top == E and left == W and bottom == E and right == E and top_right == W:
                    output[i][j] = '┭'
                # ?EE
                # WWE
                # ?E?
                elif top == E and left == W and bottom == E and right == E and top_right == E:
                    output[i][j] = '┑'
                # WE?
                # EWW
                # ?E?
                elif top == E and right == W and bottom == E and left == E and top_left == W:
                    output[i][j] = '┮'
                # EE?
                # EWW
                # ?E?
                elif top == E and right == W and bottom == E and left == E and top_left == E:
                    output[i][j] = '┍'

                # No wall
                # EEE
                # EWE
                # ?E?
                elif top == E and right == E and bottom == E and left == E and top_right == E and top_left == E:
                    output[i][j] = '╻'
                # WEE
                # EWE
                # ?E?
                elif top == E and right == E and bottom == E and left == E and top_right == E and top_left == W:
                    output[i][j] = '┐'
                # EEW
                # EWE
                # ?E?
                elif top == E and right == E and bottom == E and left == E and top_right == W and top_left == E:
                    output[i][j] = '┌'
                # WEW
                # EWE
                # ?E?
                elif top == E and right == E and bottom == E and left == E and top_right == W and top_left == W:
                    output[i][j] = '┬'


                else:
                    output[i][j] = '?'

            elif grid[i][j] == E:
                top = grid[i-1][j] if i > 0 else W
                bottom = grid[i+1][j] if i < rows-1 else W
                top_left = grid[i-1][j-1] if i > 0 and j > 0 else W
                left = grid[i][j-1] if j > 0 else W
                top_right = grid[i-1][j+1]  if i > 0 and j < cols-1 else W
                right = grid[i][j+1] if j < cols-1 else W

                # if Empty
                # ?W?
                # WEW
                if top == W and right == W and left == W:
                    output[i][j] = '┴'

                # no wall
                # ?E?
                # ?E?
                elif top == E :
                    output[i][j] = '.'

                # WWW
                # ?E?
                elif top == W and right == E and left == E and top_right == W and top_left == W:
                    output[i][j] = '┴'
                # WW?
                # EEW
                elif top == W and right == W and left == E and top_left == W:
                    output[i][j] = '┴'
                # ?WW
                # WEE
                elif top == W and right == E and left == W and top_right == W:
                    output[i][j] = '┴'


                # WWE
                # EEE
                elif top == W and right == E and left == E and top_right == E and top_left == W:
                    output[i][j] = '┘'

                # ?WE
                # WEE
                elif top == W and right == E and left == W and top_right == E:
                    output[i][j] = '┘'


                # EWW
                # EEE
                elif top == W and right == E and left == E and top_right == W and top_left == E:
                    output[i][j] = '└'
                    
                # EW?
                # EEW
                elif top == W and right == W and left == E and top_left == E:
                    output[i][j] = '└'


                # EWE
                # EEE
                elif top == W and right == E and left == E and top_right == E and top_left == E:
                    output[i][j] = '╵'
                    
                else:
                    output[i][j] = '?'
                    




    return output

# Test the function with the previous grid
output_heavy = generate_visual_2D_view(test_grid)
for row in output_heavy:
    print(''.join(row))

# Generate a 10x10 random grid
test_grid_10x10 = generate_random_grid(10, 10)
output2 = generate_visual_2D_view(test_grid_10x10)
for row in test_grid_10x10:
    print(''.join(row))

for row in output2:
    print(''.join(row))
