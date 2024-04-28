# ---------------------------------------------------------------------------
# SEGA97
# Simulation of Conway's Game of Life in pygame
# ---------------------------------------------------------------------------
# Possible speedups:
# TODO: Instead of redrawing the entire grid every frame, only update the cells that have changed since the last frame
# TODO: Rather than iterating over every cell in the grid every frame, only update cells that are near living cells
# TODO: Parallelize computations?


import pygame
import numpy as np
# import win32gui
# import win32con

pygame.font.init()

# Define colors for the cells and background
col_about_to_die = (200, 200, 225)
col_about_to_die = (255, 0, 0) #red
col_alive = (255, 255, 215)
col_background = (10, 10, 40)
col_grid = (30, 30, 60)

# Initialize a font for displaying generation information
myfont = pygame.font.SysFont("monospace", 16)

# Function to update the game state and draw cells
def update(surface, cur, sz, gen):
    nxt = np.zeros_like(cur)
    
    # Use Numpy's efficient array operations for neighbor counting and updating
    neighbor_count = (
        np.roll(cur, (-1, -1), axis=(0, 1)) + np.roll(cur, (-1, 0), axis=(0, 1)) +
        np.roll(cur, (-1, 1), axis=(0, 1)) + np.roll(cur, (0, -1), axis=(0, 1)) +
        np.roll(cur, (0, 1), axis=(0, 1)) + np.roll(cur, (1, -1), axis=(0, 1)) +
        np.roll(cur, (1, 0), axis=(0, 1)) + np.roll(cur, (1, 1), axis=(0, 1))
    )
    
    # Apply Conway's Game of Life rules using Numpy's broadcasting
    nxt[(cur == 1) & ((neighbor_count < 2) | (neighbor_count > 3))] = 0
    nxt[(cur == 1) & ((neighbor_count == 2) | (neighbor_count == 3))] = 1
    nxt[(cur == 0) & (neighbor_count == 3)] = 1

    # Update cell colors directly using Numpy operations
    alive_indices = np.argwhere(cur == 1)
    dead_indices = np.argwhere(cur == 0)
    
    # Convert indices to tuples for set_at function
    alive_indices = [(idx[1] * sz, idx[0] * sz) for idx in alive_indices]
    dead_indices = [(idx[1] * sz, idx[0] * sz) for idx in dead_indices]
    
    surface.fill(col_background)
    for pos in alive_indices:
        pygame.draw.rect(surface, col_alive, pygame.Rect(pos[0], pos[1], sz, sz))
    for pos in dead_indices:
        pygame.draw.rect(surface, col_background, pygame.Rect(pos[0], pos[1], sz, sz))

    # Apply color change for cells about to die
    about_to_die_indices = np.argwhere((cur == 1) & ((neighbor_count < 2) | (neighbor_count > 3)))
    about_to_die_indices = [(idx[1] * sz, idx[0] * sz) for idx in about_to_die_indices]
    for pos in about_to_die_indices:
        pygame.draw.rect(surface, col_about_to_die, pygame.Rect(pos[0], pos[1], sz, sz))
    
    gentext = myfont.render("Generation: {0}".format(gen), 1, (255, 255, 255))
    surface.blit(gentext, (0, cur.shape[0] * sz - 16))
    
    return nxt



# Initialize the game grid with a given x and y size
def init(dimx, dimy, pattern):
    cells = np.zeros((dimy, dimx))
    cells[:pattern.shape[0], :pattern.shape[1]] = pattern
    return cells


# Initialize the game grid with gliders pattern
def init_gliders(dimx, dimy, pattern):
    cells = np.zeros((dimy, dimx))

    # Define patterns for one or two Gosper's glider guns
    if pattern == '1':
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
    elif pattern == '2':
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
    pos = (3,3)
    cells[pos[0]:pos[0]+pattern.shape[0], pos[1]:pos[1]+pattern.shape[1]] = pattern
    return cells

# Main function to run the game
def main(dimx, dimy, cellsize, pattern):
    pygame.init()
    surface = pygame.display.set_mode((dimx * cellsize, dimy * cellsize))
    pygame.display.set_caption("Py Game of Life")

    if pattern == '1':
        cells = init_gliders(dimx, dimy, pattern)
    elif pattern == '2':
        cells = init_gliders(dimx, dimy, pattern)
    else:
        cells = init(dimx, dimy, pattern)
    
    gen = 0
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        cells = update(surface, cells, cellsize, gen)
        pygame.display.update()
        gen += 1
        # clock.tick(10)  # Limit frame rate to 10 FPS

# Get user input to determine the game setup
gliders = input("Run a Gosper's Glider Gun, creating gliders? (Yes, No): ").lower()
if gliders == 'yes':
    glider_count = input("1 or 2 Gliders? (1, 2): ")
    if glider_count == '1' or glider_count == '2':
        main(120, 90, 8, glider_count)
    else:
        print("Invalid input for glider count.")
elif gliders == 'no':
    n = int(input("Enter world width: "))
    m = int(input("Enter world height: "))
    s = int(input("Enter cell size: "))
    c = float(input("Determine chance of each cell starting with a life (0:1): "))
    pattern = np.random.choice([0, 1], size=(n, m), p=[1 - c, c])
    main(n, m, s, pattern)
else:
    print("Invalid input.")

