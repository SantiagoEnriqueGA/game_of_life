# ---------------------------------------------------------------------------
# SEGA97
# Simulation of Conway's Game of Life in pygame
# ---------------------------------------------------------------------------
# V2: Updated to user Nunpy array operations
# V3: Updated to only draw the cells that have changed since the last frame
#     Dropped coloring of cells about to die.
#     Added option to wrap cells or not based on input
# V4: Function decomposition, broke down the main function into smaller functions 
#       for initialization, event handling, and game loop execution
#     Implemented Pause and Resume functionality 
#     main_menu() function
# ---------------------------------------------------------------------------

import pygame
import numpy as np

# Constants
COLORS = {
    'pause': (255, 0, 0),
    'alive': (255, 255, 215),
    'background': (10, 10, 40),
    'grid': (30, 30, 60),
    'text': (255, 255, 255)
}
pygame.init()
FONT = pygame.font.SysFont("monospace", 16)
PAUSE_TEXT = pygame.font.SysFont('monospace', 32).render('Paused, press R to resume', True, pygame.color.Color(COLORS['pause']))

def init_game_state(dimx, dimy, pattern=None, glider_count=None):
    cells = np.zeros((dimy, dimx))
    if glider_count == 1:
        # Initialize with Gosper's glider gun
        pattern = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
                            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]])
    elif glider_count == 2:
        # Initialize with two Gosper's glider guns
        pattern = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1],
                            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,1,1,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,1],
                            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0]])
    
    if (glider_count == 1 or glider_count == 2):
        # Position the pattern in the game grid
        pos = (3,3) # Position where the pattern starts
        cells[pos[0]:pos[0]+pattern.shape[0], pos[1]:pos[1]+pattern.shape[1]] = pattern
    
    else:
        cells[:pattern.shape[0], :pattern.shape[1]] = pattern
    

    return cells

def update_game_state(cur, sz, wrap):
    # Pad the current array if wrap is False
    if not wrap:
        cur = np.pad(cur, pad_width=1, mode='constant')
    
    # Create a new array for the next generation
    nxt = np.zeros_like(cur)

    # Use Numpy array operations for neighbor counting and updating
    neighbor_count = (
        np.roll(cur, (-1, -1), axis=(0, 1)) + 
        np.roll(cur, (-1, 0), axis=(0, 1)) + 
        np.roll(cur, (-1, 1), axis=(0, 1)) + 
        np.roll(cur, (0, -1), axis=(0, 1)) + 
        np.roll(cur, (0, 1), axis=(0, 1)) + 
        np.roll(cur, (1, -1), axis=(0, 1)) + 
        np.roll(cur, (1, 0), axis=(0, 1)) + 
        np.roll(cur, (1, 1), axis=(0, 1))
    )

    # Apply Conway's Game of Life rules using Numpy broadcasting
    nxt[(cur == 1) & ((neighbor_count < 2) | (neighbor_count > 3))] = 0
    nxt[(cur == 1) & ((neighbor_count == 2) | (neighbor_count == 3))] = 1
    nxt[(cur == 0) & (neighbor_count == 3)] = 1

    changed_indices = []
    # Iterate through each index and value in the next generation array (nxt)
    for idx, val in np.ndenumerate(nxt):
        # If the cell in the current generation array (cur) is different
        if cur[idx] != val:
            # Add its position (scaled by cell size) to changed_indices
            changed_indices.append((idx[1] * sz, idx[0] * sz))
            # Update the current generation array (cur) with the new value from the next generation
            cur[idx] = val


    # Return the next generation array and changed indices
    if not wrap:
        nxt = nxt[1:-1, 1:-1]
        changed_indices = [(x - 1, y - 1) for x, y in changed_indices]

    return nxt, changed_indices


def draw_cells(surface, cur, sz, changed_indices):
    surface.fill(COLORS['background'])
    for pos in changed_indices:
        # Check if the indices are within bounds of the cur array
        if pos[1] // sz < cur.shape[0] and pos[0] // sz < cur.shape[1]:
            color = COLORS['alive'] if cur[pos[1] // sz, pos[0] // sz] == 1 else COLORS['background']
            pygame.draw.rect(surface, color, pygame.Rect(pos[0], pos[1], sz, sz))


def render_generation_info(surface, gen):
    gentext = FONT.render(f"Generation: {gen}", 1, COLORS['text'])
    surface.blit(gentext, (0, surface.get_height() - 16))

def handle_events():
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            return False, 'stopped'
        elif event.type == pygame.KEYDOWN and keys[pygame.K_p]:
            return True, 'paused'
    return True, 'running'

def handle_pause():
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            return False, 'stopped'
        elif event.type == pygame.KEYDOWN and keys[pygame.K_r]:
            return 'running'
    return 'paused'

def game_loop(dimx, dimy, cellsize, wrap, glider_count=None, pattern=None):
    surface = pygame.display.set_mode((dimx * cellsize, dimy * cellsize))
    pygame.display.set_caption("Py Game of Life")

    cells = init_game_state(dimx, dimy, pattern, glider_count)
    changed_indices = []
    gen = 0
    clock = pygame.time.Clock()
    running = True
    state = 'running'

    while running:
        running, state = handle_events()
        if state == 'running':
            cells, changed_indices = update_game_state(cells, cellsize, wrap)  # Update cells and get changed indices
            draw_cells(surface, cells, cellsize, changed_indices)
            render_generation_info(surface, gen)
            # clock.tick(1)  # Limit frame rate to 1 FPS
            pygame.display.update()
            gen += 1

        while state == 'paused':
            # surface.fill(COLORS['background'])  # Clear the screen
            text_rect = PAUSE_TEXT.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
            surface.blit(PAUSE_TEXT, text_rect)
            state = handle_pause()
            pygame.display.flip()

def main_menu():
    wrap_input = input("Do you want to wrap the cells? (Yes, No): ").lower()
    wrap = wrap_input == 'yes'

    glider_input = input("Run a Gosper's Glider Gun, creating gliders? (Yes, No): ").lower()
    if glider_input == 'yes':
        glider_count = int(input("1 or 2 Gliders? (1, 2): "))
        game_loop(120, 90, 8, wrap, glider_count)
    elif glider_input == 'no':
        n = int(input("Enter world width: "))
        m = int(input("Enter world height: "))
        s = int(input("Enter cell size: "))
        c = float(input("Determine chance of each cell starting with life (0:1): "))
        pattern = np.random.choice([0, 1], size=(n, m), p=[1 - c, c])
        game_loop(n, m, s, wrap, None, pattern)
    else:
        print("Invalid input.")


def main():
    pygame.init()
    pygame.display.set_caption("Conway's Game of Life")

    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(COLORS['background'])
        # Draw main menu elements
        title_text = FONT.render("Conway's Game of Life", True, COLORS['text'])
        screen.blit(title_text, (300, 200))

        start_button = pygame.Rect(300, 300, 200, 50)
        pygame.draw.rect(screen, COLORS['alive'], start_button)
        start_text = FONT.render("START GAME!", True, 'red')  # Updated text to "BEGIN"
        screen.blit(start_text, (350, 315))

        # Check if the start button is clicked
        mouse_pos = pygame.mouse.get_pos()
        if start_button.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                main_menu()

        pygame.display.flip()
        # clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()