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
# V5: Moved all inputs into pygame
# ---------------------------------------------------------------------------

import pygame
import numpy as np

# Constants
COLORS = {
    'pause': (255, 0, 0),
    'alive': (255, 255, 215),
    'background': (10, 10, 40),
    'grid': (30, 30, 60),
    # 'text': (255, 255, 255),
    'text': 'red',
}
GAME_VARS = {
    'start' : None,
    'wrap' : None,
    'glider' : None,
    'glider_count' : None,
    's_size' : None,
    'c_size' : None,
    'c_prob' : None
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


def render_game_info(surface, gen):
    gentext = FONT.render(f"Generation: {gen}", 1, COLORS['text'])
    surface.blit(gentext, (0, surface.get_height() - 16))    

    instructions = FONT.render('Press P to Pause',True, COLORS['text'])
    surface.blit(instructions, (surface.get_width()/2, surface.get_height() - 16))    


def handle_events():
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            quit_game()
        elif event.type == pygame.KEYDOWN and keys[pygame.K_p]:
            return True, 'paused'

    return True, 'running'

def quit_game():
    pygame.quit()
    quit()

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
            render_game_info(surface, gen)
            # clock.tick(1)  # Limit frame rate to 1 FPS
            pygame.display.update()
            gen += 1

        while state == 'paused':
            # surface.fill(COLORS['background'])  # Clear the screen
            text_rect = PAUSE_TEXT.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
            surface.blit(PAUSE_TEXT, text_rect)
            state = handle_pause()
            pygame.display.flip()

def start_menu(screen):
    # Display main menu elements
    screen.fill(COLORS['background'])
    title_text = FONT.render("Conway's Game of Life", True, COLORS['text'])
    screen.blit(title_text, (300, 200))

    start_button = pygame.Rect(300, 300, 200, 50)
    pygame.draw.rect(screen, COLORS['alive'], start_button)
    start_text = FONT.render("START GAME!", True, COLORS['text'])
    screen.blit(start_text, (350, 315))
    
    # Check if the start button is clicked
    mouse_pos = pygame.mouse.get_pos()
    if start_button.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0]:
            GAME_VARS['start'] = True
            return 
    pygame.display.flip()
    return

def wrap_menu(screen):
    # Display main menu elements
    screen.fill(COLORS['background'])
    title_text = FONT.render("Wrap cells?", True, COLORS['text'])
    screen.blit(title_text, (300, 200))

    wrap_button = pygame.Rect(300, 300, 200, 50)
    pygame.draw.rect(screen, COLORS['alive'], wrap_button)
    wrap_text = FONT.render("Wrap Cells.", True, COLORS['text'])
    screen.blit(wrap_text, (320, 315))

    no_wrap_button = pygame.Rect(300, 400, 200, 50)
    pygame.draw.rect(screen, COLORS['alive'], no_wrap_button)
    no_wrap_text = FONT.render("Don't Wrap Cells.", True, COLORS['text'])
    screen.blit(no_wrap_text, (310, 415))

    # Check if the start button is clicked
    mouse_pos = pygame.mouse.get_pos()
    if wrap_button.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0]:
            GAME_VARS['wrap'] = True
            return 
    elif no_wrap_button.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0]:
            GAME_VARS['wrap'] = False
            return 

    pygame.display.flip()
    return 

def ask_glider(screen):
    # Display main menu elements
    screen.fill(COLORS['background'])
    title_text = FONT.render("Run a Gosper's Glider Gun?", True, COLORS['text'])
    screen.blit(title_text, (300, 200))

    yes_button = pygame.Rect(200, 300, 200, 50)
    pygame.draw.rect(screen, COLORS['alive'], yes_button)
    yes_text = FONT.render("YES", True, COLORS['text'])
    screen.blit(yes_text, (320, 315))

    no_button = pygame.Rect(450, 300, 200, 50)
    pygame.draw.rect(screen, COLORS['alive'], no_button)
    no_text = FONT.render("NO", True, COLORS['text'])
    screen.blit(no_text, (510, 315))

    # Check if the start button is clicked
    mouse_pos = pygame.mouse.get_pos()
    if no_button.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0]:
            GAME_VARS['glider'] = False
            GAME_VARS['glider_count'] = False
            return 
    elif yes_button.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0]:
            GAME_VARS['glider'] = True

    if GAME_VARS['glider'] == True:    
        sub_title_text = FONT.render("1 or 2 Glider Guns?", True, COLORS['text'])
        screen.blit(sub_title_text, (325, 375))

        one_button = pygame.Rect(200, 425, 200, 50)
        pygame.draw.rect(screen, COLORS['alive'], one_button)
        one_text = FONT.render("ONE", True, COLORS['text'])
        screen.blit(one_text, (320, 440))

        two_button = pygame.Rect(450, 425, 200, 50)
        pygame.draw.rect(screen, COLORS['alive'], two_button)
        two_text = FONT.render("TWO", True, COLORS['text'])
        screen.blit(two_text, (510, 440))

        if one_button.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                GAME_VARS['glider_count'] = 1
                game_loop(120, 90, 8, GAME_VARS['wrap'], GAME_VARS['glider_count'])
                
        elif two_button.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                GAME_VARS['glider_count'] = 2
                game_loop(120, 90, 8, GAME_VARS['wrap'], GAME_VARS['glider_count'])
        
    pygame.display.flip()
    return 

def ask_gameSize(screen):
    # Display main menu elements
    screen.fill(COLORS['background'])
    title_text = FONT.render("Select World Size:", True, COLORS['text'])
    screen.blit(title_text, (300, 50))

    button_100 = pygame.Rect(50, 100, 200, 50)
    pygame.draw.rect(screen, COLORS['alive'], button_100)
    text_100 = FONT.render("100", True, COLORS['text'])
    screen.blit(text_100, (130, 115))

    button_250 = pygame.Rect(300, 100, 200, 50)
    pygame.draw.rect(screen, COLORS['alive'], button_250)
    text_250 = FONT.render("250", True, COLORS['text'])
    screen.blit(text_250, (380, 115))

    button_500 = pygame.Rect(550, 100, 200, 50)
    pygame.draw.rect(screen, COLORS['alive'], button_500)
    text_500 = FONT.render("500", True, COLORS['text'])
    screen.blit(text_500, (630, 115))

    # Check if the start button is clicked
    mouse_pos = pygame.mouse.get_pos()
    if button_100.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0]:
            GAME_VARS['s_size'] = 100
            return
    elif button_250.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0]:
            GAME_VARS['s_size'] = 250
            return
    elif button_500.collidepoint(mouse_pos):
        if pygame.mouse.get_pressed()[0]:
            GAME_VARS['s_size'] = 500
            return
        
    if GAME_VARS['s_size'] is not None:
        sub_title_text = FONT.render("Select Cell Size:", True, COLORS['text'])
        screen.blit(sub_title_text, (300, 250))

        button_1 = pygame.Rect(50, 285, 200, 50)
        pygame.draw.rect(screen, COLORS['alive'], button_1)
        text_1 = FONT.render("1", True, COLORS['text'])
        screen.blit(text_1, (130, 300))

        button_2 = pygame.Rect(300, 285, 200, 50)
        pygame.draw.rect(screen, COLORS['alive'], button_2)
        text_2 = FONT.render("2", True, COLORS['text'])
        screen.blit(text_2, (380, 300))

        button_5 = pygame.Rect(550, 285, 200, 50)
        pygame.draw.rect(screen, COLORS['alive'], button_5)
        text_5 = FONT.render("5", True, COLORS['text'])
        screen.blit(text_5, (630, 300))

        # Check if the start button is clicked
        if button_1.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                GAME_VARS['c_size'] = 1
                return
        elif button_2.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                GAME_VARS['c_size'] = 2
                return
        elif button_5.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                GAME_VARS['c_size'] = 5
                return

    if GAME_VARS['c_size'] is not None:
        sub_sub_title_text = FONT.render("Select probability of each cell to begin alive:", True, COLORS['text'])
        screen.blit(sub_sub_title_text, (100, 450))

        button_1 = pygame.Rect(50, 485, 200, 50)
        pygame.draw.rect(screen, COLORS['alive'], button_1)
        text_1 = FONT.render("0.1", True, COLORS['text'])
        screen.blit(text_1, (130, 500))

        button_25 = pygame.Rect(300, 485, 200, 50)
        pygame.draw.rect(screen, COLORS['alive'], button_25)
        text_2 = FONT.render("0.25", True, COLORS['text'])
        screen.blit(text_2, (380, 500))

        button_5 = pygame.Rect(550, 485, 200, 50)
        pygame.draw.rect(screen, COLORS['alive'], button_5)
        text_5 = FONT.render("0.5", True, COLORS['text'])
        screen.blit(text_5, (630, 500))

        # Check if the start button is clicked
        if button_1.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                GAME_VARS['c_prob'] = .1
                return
        elif button_25.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                GAME_VARS['c_prob'] = .25
                return
        elif button_5.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                GAME_VARS['c_prob'] = .5
                return
    
    pygame.display.flip()
    return

def game_logic(screen):
    if GAME_VARS['start'] is None:
        start_menu(screen)
        return 
    
    elif GAME_VARS['wrap'] is None:
        wrap_menu(screen)
        return  

    elif GAME_VARS['glider'] is None or GAME_VARS['glider_count'] is None:
        ask_glider(screen)
        return  # User hasn't chosen an option yet
    
    elif GAME_VARS['s_size'] is None or\
         GAME_VARS['c_size'] is None or\
         GAME_VARS['c_prob'] is None:
        ask_gameSize(screen)
        return

    else: 
        n, m = GAME_VARS['s_size'], GAME_VARS['s_size']
        probability = GAME_VARS['c_prob']
        pattern = np.random.choice([0, 1], size=(n, m), p=[1 - probability, probability])
        game_loop(n, m, GAME_VARS['c_size'], GAME_VARS['wrap'], glider_count=None, pattern=pattern)

def main():
    pygame.init()
    pygame.display.set_caption("Conway's Game of Life")

    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                quit_game()
        
        game_logic(screen)  # Always call game logic      
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()