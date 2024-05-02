# ---------------------------------------------------------------------------
# SEGA97
# Simulation of Conway's Game of Life in pygame
# ---------------------------------------------------------------------------
# V2: Updated to user Nunpy array operations
# V3: Updated to only draw the cells that have changed since the last frame
#     Dropped coloring of cells about to die.
#     Added option to wrap cells or not based on input
# ---------------------------------------------------------------------------
# Possible speedups:
# TODO: Rather than iterating over every cell in the grid every frame, only update cells that are near living cells
# TODO: Parallelize computations?


import pygame
import numpy as np

# Initialize pygame font for displaying generation information
pygame.font.init()

# Define colors for the cells and background
col_about_to_die = (255, 0, 0) #red
col_alive = (255, 255, 215)
col_background = (10, 10, 40)
col_grid = (30, 30, 60)

# Initialize a font for displaying generation information
myfont = pygame.font.SysFont("monospace", 16)

# Function to update the game state and draw cells
def update(surface, cur, sz, gen, changed_indices, wrap):
    # Pad the current array if wrap is False
    if not wrap:
        cur = np.pad(cur, pad_width=1, mode='constant')

    # Create a new array for the next generation
    nxt = np.zeros_like(cur)   

    # Use Numpy array operations for neighbor counting and updating
    neighbor_count = (
        np.roll(cur, (-1, -1),  axis=(0, 1)) + 
        np.roll(cur, (-1, 0),   axis=(0, 1)) +
        np.roll(cur, (-1, 1),   axis=(0, 1)) + 
        np.roll(cur, (0, -1),   axis=(0, 1)) +
        np.roll(cur, (0, 1),    axis=(0, 1)) + 
        np.roll(cur, (1, -1),   axis=(0, 1)) +
        np.roll(cur, (1, 0),    axis=(0, 1)) + 
        np.roll(cur, (1, 1),    axis=(0, 1))
    )
    
    # Apply Conway's Game of Life rules using Numpy broadcasting
    nxt[(cur == 1) & ((neighbor_count < 2) | (neighbor_count > 3))] = 0
    nxt[(cur == 1) & ((neighbor_count == 2) | (neighbor_count == 3))] = 1
    nxt[(cur == 0) & (neighbor_count == 3)] = 1

    # Clear the list of changed indices from the previous generation
    changed_indices.clear()

    # Iterate through each index and value in the next generation array (nxt)
    for idx, val in np.ndenumerate(nxt):
        # If the cell in the current generation array (cur) is different
        if cur[idx] != val:
            # Add its position (scaled by cell size) to changed_indices
            changed_indices.append((idx[1] * sz, idx[0] * sz))
            # Update the current generation array (cur) with the new value from the next generation
            cur[idx] = val

    # Fill the surface with the background color
    surface.fill(col_background)

    # Draw alive and dead cells with their respective color
    for pos in changed_indices:
        if cur[pos[1] // sz, pos[0] // sz] == 1:
            pygame.draw.rect(surface, col_alive, pygame.Rect(pos[0], pos[1], sz, sz))
        else:
            pygame.draw.rect(surface, col_background, pygame.Rect(pos[0], pos[1], sz, sz))

    # Render and display generation information
    gentext = myfont.render("Generation: {0}".format(gen), 1, (255, 255, 255))
    surface.blit(gentext, (0, cur.shape[0] * sz - 16))
    
    # Return new array and current array
    if not wrap:
        nxt = nxt[1:-1, 1:-1]
        cur = cur[1:-1, 1:-1]
        
    # Return new array
    return nxt


# Initialize the game grid with a given x and y size and an optional pattern
def init(dimx, dimy, pattern):
    cells = np.zeros((dimy, dimx))
    cells[:pattern.shape[0], :pattern.shape[1]] = pattern
    return cells


# Initialize the game grid with gliders pattern
def init_gliders(dimx, dimy, glider_count):
    cells = np.zeros((dimy, dimx))
    pattern = []

    # Define patterns for one or two Gosper's glider guns
    if glider_count == '1':
        # A single Gosper's glider gun creating gliders   
        pattern = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
                            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
    elif glider_count == '2':
        # Two Gosper's glider gun creating gliders   
        pattern = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1],
                            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,1,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,1],
                            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0]])

    # Position the pattern in the game grid
    pos = (3,3) # Position where the pattern starts
    cells[pos[0]:pos[0]+pattern.shape[0], pos[1]:pos[1]+pattern.shape[1]] = pattern
    return cells

# Main function to run the game
def main(dimx, dimy, cellsize, wrap, glider_count=None, pattern=None):
    # Initialize game state
    pygame.init()
    surface = pygame.display.set_mode((dimx * cellsize, dimy * cellsize))
    pygame.display.set_caption("Py Game of Life")

    cells = None
    changed_indices = []

    # Initialize based on user input
    if glider_count == '1' or glider_count == '2':
        cells = init_gliders(dimx, dimy, glider_count)
    else:
        cells = init(dimx, dimy, pattern)
    
    gen = 0
    clock = pygame.time.Clock()
    running = True

    # Game loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        cells = update(surface, cells, cellsize, gen, changed_indices, wrap)
        pygame.display.update()
        gen += 1
        # clock.tick(1)  # Limit frame rate to 1 FPS

# Get user input to determine the game setup
wrap = input("Do you want to wrap the cells? (Yes, No): ").lower()
if(wrap == 'yes'): wrap = True 
else: wrap = False

gliders = input("Run a Gosper's Glider Gun, creating gliders? (Yes, No): ").lower()
if gliders == 'yes':
    glider_count = input("1 or 2 Gliders? (1, 2): ")
    if glider_count == '1' or glider_count == '2':
        main(120, 90, 8, wrap, glider_count, None)
    else:
        print("Invalid input for glider count.")

elif gliders == 'no':
    n = int(input("Enter world width: "))
    m = int(input("Enter world height: "))
    s = int(input("Enter cell size: "))
    c = float(input("Determine chance of each cell starting with a life (0:1): "))
    pattern = np.random.choice([0, 1], size=(n, m), p=[1 - c, c])
    main(n, m, s, wrap, None, pattern)
else:
    print("Invalid input.")

