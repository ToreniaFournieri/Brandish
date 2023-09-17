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
                left = grid[i][j-1] if j > 0 else W
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
                    output[i][j] = '┻'
                # ?W?
                # EWW
                # ?W?
                elif top == W and right == W and bottom == W and left == E:
                    output[i][j] = '┣'
                # ?E?
                # WWW
                # ?W?
                elif top == E and right == W and bottom == W and left == W:
                    output[i][j] = '┳'

                # ?W?
                # WWE
                # ?W?
                elif top == W and right == E and bottom == W and left == W:
                    output[i][j] = '┫'

                # 2 walls
                # ?E?
                # WWW
                # ?E?
                elif top == E and right == W and bottom == E and left == W:
                    output[i][j] = '━'

                # ?W?
                # EWE
                # ?W?
                elif top == W and right == E and bottom == W and left == E:
                    output[i][j] = '┃'

                # ?E?
                # WWE
                # ?W?
                elif top == E and left == W and bottom == W and right == E:
                    output[i][j] = '┓'
                # ?E?
                # EWW
                # ?W?
                elif top == E and right == W and bottom == W and left == E:
                    output[i][j] = '┏'
                # EE?
                # EWW
                # ?W?
                elif top == E and right == W and bottom == W and left == E:
                    output[i][j] = '┏'

                # ?W?
                # WWE
                # ?E?
                elif top == W and left == W and bottom == E and right == E:
                    output[i][j] = '┛'
                # ?W?
                # EWW
                # ?E?
                elif top == W and right == W and bottom == E and left == E:
                    output[i][j] = '┗'

                # 1 wall
                # EWE
                # EWE
                # ?E?
                elif top == W and right == E and bottom == E and left == E:
                    output[i][j] = '╹'
                    
                # ?E?
                # EWE
                # ?W?
                elif top == E and right == E and bottom == W and left == E:
                    output[i][j] = '╻'

                # ?E?
                # EWW
                # ?E?
                elif top == E and right == W and bottom == E and left == E:
                    output[i][j] = '╺'

                # ?E?
                # WWE
                # ?E?
                elif top == E and right == E and bottom == E and left == W:
                    output[i][j] = '╸'



                # No wall
                # ?E?
                # EWE
                # ?E?
                elif top == E and right == E and bottom == E and left == E:
                    output[i][j] = '▪'

                else:
                    output[i][j] = '?'




    return output


'''
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
'''
