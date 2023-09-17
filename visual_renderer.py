
def generate_visual_2D_view(grid):
    # Get grid dimensions
    rows = len(grid)
    cols = len(grid[0])

    # Define constants
    E = '.'  # Empty cell
    W = '#'  # Wall cell

    output = [list(row) for row in grid]
    # Create an output grid initialized with empty cells
    #output = [[E for _ in range(cols)] for _ in range(rows)]

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
                elif top == W and left == W and right == W and bottom != W:
                    output[i][j] = '┻'
                # ?W?
                # EWW
                # ?W?
                elif top == W and right == W and bottom == W and left != W:
                    output[i][j] = '┣'
                # ?E?
                # WWW
                # ?W?
                elif top != W and right == W and bottom == W and left == W:
                    output[i][j] = '┳'

                # ?W?
                # WWE
                # ?W?
                elif top == W and right != W and bottom == W and left == W:
                    output[i][j] = '┫'

                # 2 walls
                # ?E?
                # WWW
                # ?E?
                elif top != W and right == W and bottom != W and left == W:
                    output[i][j] = '━'

                # ?W?
                # EWE
                # ?W?
                elif top == W and right != W and bottom == W and left != W:
                    output[i][j] = '┃'

                # ?E?
                # WWE
                # ?W?
                elif top != W and left == W and bottom == W and right != W:
                    output[i][j] = '┓'
                # ?E?
                # EWW
                # ?W?
                elif top != W and right == W and bottom == W and left != W:
                    output[i][j] = '┏'
                # EE?
                # EWW
                # ?W?
                elif top != W and right == W and bottom == W and left != W:
                    output[i][j] = '┏'

                # ?W?
                # WWE
                # ?E?
                elif top == W and left == W and bottom != W and right != W:
                    output[i][j] = '┛'
                # ?W?
                # EWW
                # ?E?
                elif top == W and right == W and bottom != W and left != W:
                    output[i][j] = '┗'

                # 1 wall
                # ?W?
                # EWE
                # ?E?
                elif top == W and right != W and bottom != W and left != W:
                    output[i][j] = '╹'
                    
                # ?E?
                # EWE
                # ?W?
                elif top != W and right != W and bottom == W and left != W:
                    output[i][j] = '╻'

                # ?E?
                # EWW
                # ?E?
                elif top != W and right == W and bottom != W and left != W:
                    output[i][j] = '╺'

                # ?E?
                # WWE
                # ?E?
                elif top != W and right != W and bottom != W and left == W:
                    output[i][j] = '╸'



                # No wall
                # ?E?
                # EWE
                # ?E?
                elif top != W and right != W and bottom != W and left != W:
                    output[i][j] = '▪'

                else:
                    output[i][j] = '?'



    return output

