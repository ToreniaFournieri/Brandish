import curses


def generate_visual_2D_view(stdscr, grid, x, y):
    # Get grid dimensions
    rows = len(grid)
    cols = len(grid[0])

    # Define constants
    E = '・'  # Empty cell
    Wall = '＃' #
    W = {'#', "+"}  # Wall like object

    output = [list(row) for row in grid]


    # Process each cell in the grid
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] in Wall:
                stdscr.addstr(x + i, y + j*2, '＃', curses.color_pair(4) | curses.A_BOLD)
            elif grid[i][j] == E:
                stdscr.addstr(x + i, y + j*2, '・', curses.color_pair(5) | curses.A_BOLD)
            else:
                stdscr.addstr(x + i, y + j*2, grid[i][j])
                

'''
                top = grid[i-1][j] if i > 0 else W
                bottom = grid[i+1][j] if i < rows-1 else W
                left = grid[i][j-1] if j > 0 else W
                right = grid[i][j+1] if j < cols-1 else W
                                
                # Determine the Unicode character based on surrounding walls
                # 4 Walls
                # ?W?
                # WWW
                # ?W?
                if top in W and left in W and right in W and bottom in W:
                    output[i][j] = '╋'  # All sides are walls

                # 3 Walls
                # ?W?
                # WWW
                # ?E?
                elif top in W and left in W and right in W and bottom not in W:
                    output[i][j] = '┻'
                # ?W?
                # EWW
                # ?W?
                elif top in W and right in W and bottom in W and left not in W:
                    output[i][j] = '┣'
                # ?E?
                # WWW
                # ?W?
                elif top not in W and right in W and bottom in W and left in W:
                    output[i][j] = '┳'

                # ?W?
                # WWE
                # ?W?
                elif top in W and right not in W and bottom in W and left in W:
                    output[i][j] = '┫'

                # 2 walls
                # ?E?
                # WWW
                # ?E?
                elif top not in W and right in W and bottom not in W and left in W:
                    output[i][j] = '━'

                # ?W?
                # EWE
                # ?W?
                elif top in W and right not in W and bottom in W and left not in W:
                    output[i][j] = '┃'

                # ?E?
                # WWE
                # ?W?
                elif top not in W and left in W and bottom in W and right not in W:
                    output[i][j] = '┓'
                # ?E?
                # EWW
                # ?W?
                elif top not in W and right in W and bottom in W and left not in W:
                    output[i][j] = '┏'
                # EE?
                # EWW
                # ?W?
                elif top not in W and right in W and bottom in W and left not in W:
                    output[i][j] = '┏'

                # ?W?
                # WWE
                # ?E?
                elif top in W and left in W and bottom not in W and right not in W:
                    output[i][j] = '┛'
                # ?W?
                # EWW
                # ?E?
                elif top in W and right in W and bottom not in W and left not in W:
                    output[i][j] = '┗'

                # 1 wall
                # ?W?
                # EWE
                # ?E?
                elif top in W and right not in W and bottom not in W and left not in W:
                    output[i][j] = '╹'
                    
                # ?E?
                # EWE
                # ?W?
                elif top not in W and right not in W and bottom in W and left not in W:
                    output[i][j] = '╻'

                # ?E?
                # EWW
                # ?E?
                elif top not in W and right in W and bottom not in W and left not in W:
                    output[i][j] = '╺'

                # ?E?
                # WWE
                # ?E?
                elif top not in W and right not in W and bottom not in W and left in W:
                    output[i][j] = '╸'



                # No wall
                # ?E?
                # EWE
                # ?E?
                elif top not in W and right not in W and bottom not in W and left not in W:
                    output[i][j] = '■'
                else:
                    output[i][j] = '？'
'''