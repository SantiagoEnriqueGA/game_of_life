# Conway's Game of Life with Pygame and Numpy

This repository contains Python code for Conway's Game of Life implemented using Pygame for graphics and Numpy for array operations. The game simulates cellular automata where cells evolve based on simple rules.

## Files

- `gameOfLife_v1.py` to `gameOfLife_v5.py`: Different versions of the Game of Life implementation, with version 5 being the latest.
- `glider.csv` and `gliders.csv`: CSV files storing starting configurations for one and two Gosper's glider guns, respectively.

## Version History

- **V1**: Initial implementation.
- **V2**: Updated to use Numpy array operations.
- **V3**: Optimized drawing by only updating changed cells.
- **V4**: Refactored code into functions, added Pause and Resume functionality.
- **V5**: Improved user interaction by moving inputs into the Pygame window, added restart feature, and implemented clock speed control.

## Running the Game

To run the game, execute the appropriate version file (`gameOfLife_v5.py` for the latest version) using Python. Ensure you have Pygame and Numpy installed.

Example:
```
python gameOfLife_v5.py
```

## Game Controls

- **Up Arrow**: Increase game speed.
- **Down Arrow**: Decrease game speed.
- **P**: Pause the game.
- **S**: Return to the start menu while paused.
- **R**: Resume the game when paused.
- **Escape**: Quit the game.

## Screens

The game includes several screens for user interaction:

1. **Start Menu**: Allows starting the game and selecting initial settings.
2. **Wrap Menu**: Choose whether cells should wrap around the edges.
3. **Glider Menu**: Decide if Gosper's glider gun should be used, and if so, how many.
4. **Size Menu**: Select the size of the game world, cell size, and initial cell probability.

## Screenshots

![image](https://github.com/SantiagoEnriqueGA/gameOfLife/assets/50879742/c4f814f8-37d1-46ca-9d7d-70d1b52092a5)
![image](https://github.com/SantiagoEnriqueGA/gameOfLife/assets/50879742/f1ac1cf0-baf6-4df0-aeb3-673d5bf62ef1)
![image](https://github.com/SantiagoEnriqueGA/gameOfLife/assets/50879742/6cd879a5-dd13-4208-92b6-18ad84251a85)
![image](https://github.com/SantiagoEnriqueGA/gameOfLife/assets/50879742/76eff2ca-8648-4d42-9500-d9d1376f8198)


