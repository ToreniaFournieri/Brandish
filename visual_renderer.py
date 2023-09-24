import blessed


def generate_visual_2D_view(term, grid, x, y):
    # Get grid dimensions
    rows = len(grid)
    cols = len(grid[0])

    # Define constants
    E = '・'  # Empty cell
    Wall = '＃' #
    W = {'＃', "＋"}  # Wall like object

    # For the colors, you can use the following approach:
    wall_style = term.black_on_white
    #empty_style = term.black_on_black

    # Process each cell in the grid
    for i in range(rows):
        for j in range(cols):
            top = grid[i-1][j] if i > 0 else Wall
            bottom = grid[i+1][j] if i < rows-1 else Wall
            left = grid[i][j-1] if j > 0 else Wall
            right = grid[i][j+1] if j < cols-1 else Wall

            if grid[i][j] in Wall:                            
                # Determine the Unicode character based on surrounding walls
                # 4 Walls
                # ?W?
                # WWW
                # ?W?
                if top in W and left in W and right in W and bottom in W:
                    print(term.move(x + i, y + j*2) + wall_style('╋ '))  

                # 3 Walls
                # ?W?
                # WWW
                # ?E?
                elif top in W and left in W and right in W and bottom not in W:
                    print(term.move(x + i, y + j*2) + wall_style('┻ ')) 
                # ?W?
                # EWW
                # ?W?
                elif top in W and right in W and bottom in W and left not in W:
                    print(term.move(x + i, y + j*2) + wall_style('┣ '))  
                # ?E?
                # WWW
                # ?W?
                elif top not in W and right in W and bottom in W and left in W:
                    print(term.move(x + i, y + j*2) + wall_style('┳ '))  

                # ?W?
                # WWE
                # ?W?
                elif top in W and right not in W and bottom in W and left in W:
                    print(term.move(x + i, y + j*2) + wall_style('┫ '))  

                # 2 walls
                # ?E?
                # WWW
                # ?E?
                elif top not in W and right in W and bottom not in W and left in W:
                    print(term.move(x + i, y + j*2) + wall_style('━ '))  

                # ?W?
                # EWE
                # ?W?
                elif top in W and right not in W and bottom in W and left not in W:
                    print(term.move(x + i, y + j*2) + wall_style('┃ '))  

                # ?E?
                # WWE
                # ?W?
                elif top not in W and left in W and bottom in W and right not in W:
                    print(term.move(x + i, y + j*2) + wall_style('┓ '))  
                # ?E?
                # EWW
                # ?W?
                elif top not in W and right in W and bottom in W and left not in W:
                    print(term.move(x + i, y + j*2) + wall_style('┏ '))  
                # ?W?
                # WWE
                # ?E?
                elif top in W and left in W and bottom not in W and right not in W:
                    print(term.move(x + i, y + j*2) + wall_style('┛ '))  
                # ?W?
                # EWW
                # ?E?
                elif top in W and right in W and bottom not in W and left not in W:
                    print(term.move(x + i, y + j*2) + wall_style('┗ '))  

                # 1 wall
                # ?W?
                # EWE
                # ?E?
                elif top in W and right not in W and bottom not in W and left not in W:
                    print(term.move(x + i, y + j*2) + wall_style('╹ '))  
                    
                # ?E?
                # EWE
                # ?W?
                elif top not in W and right not in W and bottom in W and left not in W:
                    print(term.move(x + i, y + j*2) + wall_style('╻ '))  

                # ?E?
                # EWW
                # ?E?
                elif top not in W and right in W and bottom not in W and left not in W:
                    print(term.move(x + i, y + j*2) + wall_style('╺ '))  

                # ?E?
                # WWE
                # ?E?
                elif top not in W and right not in W and bottom not in W and left in W:
                    print(term.move(x + i, y + j*2) + wall_style('╸ '))  


                # No wall
                # ?E?
                # EWE
                # ?E?
                elif top not in W and right not in W and bottom not in W and left not in W:
                    print(term.move(x + i, y + j*2) + wall_style('■ '))  

            elif grid[i][j] == E:
                print(term.move(x + i, y + j*2) + term.normal + '・')
            else:
                print(term.move(x + i, y + j*2) + term.normal + grid[i][j])

'''
            if grid[i][j] in Wall:
                print(term.move(x + i, y + j*2) + wall_style('┻'))
            elif grid[i][j] == E:
                print(term.move(x + i, y + j*2) + '・')
            else:
                print(term.move(x + i, y + j*2) + grid[i][j])


'''