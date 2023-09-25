
# Raw map as a single string
raw_map = """
 --------------------------
 |>......^^^^^^^^^^^^^^^^.|
 |.......----------------.|
 -------.------         |.|
  |...........|         |.|
  |.0.0.0.0.0.|         |.|
 --------.----|         |.|
 |...0.0..0.0.|         |.|
 |...0........|         |.|
 -----.--------   ------|.|
  |..0.0.0...|  --|.....|.|
  |.....0....|  |.+.....|.|
  |.0.0...0.--  |-|.....|.|
 -------.----   |.+.....+.|
 |..0.....|     |-|.....|--
 |........|     |.+.....|
 |...------     --|.....|
 -----            -------  
"""

# Split the raw map into lines
lines = raw_map.strip().split('\n')

# Format each line and print the result
nethack_map = lines

# Provided character-to-emoji mapping
emoji_map = {
    ' ': '＃',
    '-': '＃',
    '|': '＃',
    '0': '🪨',
    '^': '🕳',
    '?': '💰',
    '.': '・',
    '>': '🔼',
    '<': '🔽',
    '+': '🚪'
}

# Convert the map
converted_map = []

for row in nethack_map:
    new_row = ""
    for char in row:
        if char in emoji_map:
            new_row += emoji_map[char]
        else:
            new_row += char
    converted_map.append(new_row)

formatted_map = []

for row in converted_map:
    formatted_map.append(f'    "{row}",')

print("Sokoban1 = [")
for row in formatted_map:
    print(row)
print("]")
