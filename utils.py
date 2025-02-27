import numpy as np
import os 
import time

def create_win_grids(size=3):
    winning_masks = []
    
    # Win over rows
    for row in range(size):
        mask = 0
        for col in range(size):
            mask += 1 << (row * size + col)
        winning_masks.append(mask) 
      
    # Win over columns  
    for col in range(size):
        mask = 0
        for row in range(size):
            mask += 1 << (row * size + col)
        winning_masks.append(mask) 
    
    # Win over main diag
    mask = 0
    for row in range(size):
        mask += 1 << (row * size + row)
    winning_masks.append(mask)
    # Win over anti diag
    mask = 0
    for row in range(size):
        mask += 1 << (row * size + (size - row - 1))
    winning_masks.append(mask)
    
    return winning_masks

def is_win(grid, winning_configurations):

        player0, player1 = grid
        for config in winning_configurations:
            if (player0 & config) == config:
                return 1
            if (player1 & config) == config:
                return 1
        return 0

def is_full(grid, size):
    conf0, conf1 = grid
    if (conf0 | conf1) == (1 << (size * size)) - 1:
        return 1
    return 0


def play_move(grid, player, move):
    if (grid[0] | grid[1]) & (1 << move) != 0:
        print('MOVE NOT ALLOWED')
        return None
    if player == 0:
        return (grid[0] | (1 << move), grid[1])
    else:
        return (grid[0], grid[1] | (1 << move))


def clear_screen():
    """Clears the console screen to refresh the display."""
    os.system('cls' if os.name == 'nt' else 'clear')

