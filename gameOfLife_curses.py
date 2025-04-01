import curses
import numpy as np
import time

# Globals and constants
GAME_VARS = {
    'start': None,         # Start flag
    'wrap': None,          # Wrap cells flag
    's_size': None,        # World size
    'c_prob': None         # Probability of cell being alive initially
}

CELL_HISTORY = []  # cell history

def reset_GAME_VARS():
    GAME_VARS['start'] = None
    GAME_VARS['wrap'] = None
    GAME_VARS['s_size'] = None
    GAME_VARS['c_prob'] = None

def init_game_state(dimx, dimy, pattern=None):
    cells = np.zeros((dimy, dimx))
    cells[:pattern.shape[0], :pattern.shape[1]] = pattern
    return cells

def update_game_state(cur, wrap):
    # If not wrapping, pad the array with zeros
    working = cur if wrap else np.pad(cur, pad_width=1, mode='constant')
    nxt = np.zeros_like(working)
    neighbor_count = (
        np.roll(working, (-1, -1), axis=(0, 1)) +
        np.roll(working, (-1, 0), axis=(0, 1)) +
        np.roll(working, (-1, 1), axis=(0, 1)) +
        np.roll(working, (0, -1), axis=(0, 1)) +
        np.roll(working, (0, 1), axis=(0, 1)) +
        np.roll(working, (1, -1), axis=(0, 1)) +
        np.roll(working, (1, 0), axis=(0, 1)) +
        np.roll(working, (1, 1), axis=(0, 1))
    )

    nxt[(working == 1) & ((neighbor_count < 2) | (neighbor_count > 3))] = 0
    nxt[(working == 1) & ((neighbor_count == 2) | (neighbor_count == 3))] = 1
    nxt[(working == 0) & (neighbor_count == 3)] = 1

    changed_indices = []
    # When updating, record indices where state changed.
    for idx, val in np.ndenumerate(nxt):
        if working[idx] != val:
            # Use (row,col) indices (each cell is one character)
            changed_indices.append((idx[0], idx[1]))
            working[idx] = val

    if not wrap:
        nxt = nxt[1:-1, 1:-1]
        changed_indices = [(y-1, x-1) for y, x in changed_indices]
    # Update the provided array so that cur now reflects nxt.
    cur[:] = nxt[:]
    return cur, changed_indices

def draw_cells(stdscr, cur, changed_indices):
    # For each cell changed, draw an "O" if alive or a space if dead.
    max_y, max_x = stdscr.getmaxyx()
    for y, x in changed_indices:
        if y < cur.shape[0] and x < cur.shape[1]:
            char = "O" if cur[y, x] == 1 else " "
            try:
                stdscr.addch(y, x, char)
            except curses.error:
                pass  # skip positions off-screen

def render_game_info(stdscr, gen, speed):
    max_y, max_x = stdscr.getmaxyx()
    info = f"Generation: {gen}  Speed: {speed} (Use UP/DOWN to adjust, 'p' to pause, 'q' to quit)"
    try:
        stdscr.addstr(max_y-1, 0, info[:max_x-1])
    except curses.error:
        pass

def handle_events(stdscr, clock_speed):
    stdscr.nodelay(True)
    key = stdscr.getch()
    if key == ord('q'):
        return False, 'stopped', clock_speed
    elif key == ord('p'):
        return True, 'paused', clock_speed
    elif key == curses.KEY_DOWN:
        if clock_speed > 1: clock_speed -= 1
        return True, 'running', clock_speed
    elif key == curses.KEY_UP:
        return True, 'running', clock_speed + 1
    return True, 'running', clock_speed

def handle_pause(stdscr):
    # Display pause prompt and wait until resumed or quit
    stdscr.nodelay(False)
    max_y, max_x = stdscr.getmaxyx()
    prompt = "Paused - press (r) to resume, (s) to restart, (q) to quit."
    stdscr.addstr(max_y//2, max_x//2 - len(prompt)//2, prompt)
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            return False, 'stopped'
        elif key == ord('r'):
            return True, 'running'
        elif key == ord('s'):
            return True, 'restart'
        time.sleep(0.1)

def save_cell_history(current_cells):
    CELL_HISTORY.append(np.copy(current_cells))

def game_loop(stdscr, dimx, dimy, wrap, pattern=None):
    # Initialize game state and configure screen
    cells = init_game_state(dimx, dimy, pattern)
    stdscr.clear()
    stdscr.nodelay(True)
    gen = 0
    state = 'running'
    clock_speed = 10  # generations per second

    while True:
        cont, state, clock_speed = handle_events(stdscr, clock_speed)
        if not cont or state == 'stopped':
            break

        if state == 'running':
            cells, changed_indices = update_game_state(cells, wrap)
            save_cell_history(cells)
            draw_cells(stdscr, cells, changed_indices)
            render_game_info(stdscr, gen, clock_speed)
            stdscr.refresh()
            gen += 1
            time.sleep(1/clock_speed)
        elif state == 'paused':
            cont, new_state = handle_pause(stdscr)
            if not cont or new_state == 'stopped':
                break
            if new_state == 'restart':
                reset_GAME_VARS()
                main_curses(stdscr)
                return
            # Clear prompt before resuming
            stdscr.clear()
    # End of game loop
    stdscr.nodelay(False)

def start_menu(stdscr):
    stdscr.clear()
    msg = "Conway's Game of Life. Press (s) to Start, (q) to Quit."
    max_y, max_x = stdscr.getmaxyx()
    stdscr.addstr(max_y//2, max_x//2 - len(msg)//2, msg)
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('s'):
            GAME_VARS['start'] = True
            return
        elif key == ord('q'):
            exit()

def wrap_menu(stdscr):
    stdscr.clear()
    msg = "Wrap cells? (y) Yes / (n) No"
    max_y, max_x = stdscr.getmaxyx()
    stdscr.addstr(max_y//2, max_x//2 - len(msg)//2, msg)
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('y'):
            GAME_VARS['wrap'] = True
            return
        elif key == ord('n'):
            GAME_VARS['wrap'] = False
            return

def game_size_menu(stdscr):
    stdscr.clear()
    msg = "Select World Size: (1) 100, (2) 250, (3) 500"
    max_y, max_x = stdscr.getmaxyx()
    stdscr.addstr(max_y//2, max_x//2 - len(msg)//2, msg)
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('1'):
            GAME_VARS['s_size'] = 100
            return
        elif key == ord('2'):
            GAME_VARS['s_size'] = 250
            return
        elif key == ord('3'):
            GAME_VARS['s_size'] = 500
            return

def cell_prob_menu(stdscr):
    stdscr.clear()
    msg = "Select initial live cell probability: (1) 0.1, (2) 0.25, (3) 0.5"
    max_y, max_x = stdscr.getmaxyx()
    stdscr.addstr(max_y//2, max_x//2 - len(msg)//2, msg)
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('1'):
            GAME_VARS['c_prob'] = 0.1
            return
        elif key == ord('2'):
            GAME_VARS['c_prob'] = 0.25
            return
        elif key == ord('3'):
            GAME_VARS['c_prob'] = 0.5
            return

def game_logic(stdscr):
    # Run menus in sequence if values are not set
    if GAME_VARS['start'] is None:
        start_menu(stdscr)
    if GAME_VARS['wrap'] is None:
        wrap_menu(stdscr)
    if GAME_VARS['s_size'] is None:
        game_size_menu(stdscr)
    if GAME_VARS['c_prob'] is None:
        cell_prob_menu(stdscr)
    
    # For terminal drawing, we ignore c_size and treat each cell as one character.
    n = GAME_VARS['s_size']
    m = GAME_VARS['s_size']
    probability = GAME_VARS['c_prob']
    # Create a random board.
    pattern = np.random.choice([0, 1], size=(n, m), p=[1 - probability, probability])
    game_loop(stdscr, m, n, GAME_VARS['wrap'], pattern=pattern)

def main_curses(stdscr):
    curses.curs_set(0)
    reset_GAME_VARS()
    stdscr.clear()
    game_logic(stdscr)
    stdscr.addstr(0, 0, "Press any key to exit.")
    stdscr.nodelay(False)
    stdscr.getch()

if __name__ == '__main__':
    # windows-curses must be installed in your environment
    curses.wrapper(main_curses)
