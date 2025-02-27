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


def clear_screen():
    """Clears the console screen to refresh the display."""
    os.system('cls' if os.name == 'nt' else 'clear')