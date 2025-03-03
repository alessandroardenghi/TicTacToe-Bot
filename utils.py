import numpy as np
import os 
import time
import math
from tqdm import tqdm
import config


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
                return 2
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


def compute_ucb(leaf):
    if leaf.parent is None:
        print('CANNOT COMPUTE UCB FOR THE ROOT')
        return None
    if leaf.N == 0:
        return math.inf
    return leaf.V/leaf.N + 2* math.sqrt((2 * math.log(leaf.parent.N)) /leaf.N)

def display_board(grid, size):

    bin0 = np.array(list(bin(grid[0])[2:].zfill(size**2)[::-1]), dtype=int)
    bin1 = np.array(list(bin(grid[1])[2:].zfill(size**2)[::-1]), dtype=int)

    board_grid = (bin0 - bin1).reshape(size, size)  

    for i, row in enumerate(board_grid):

        row_display = " | ".join('X' if cell == 1 else 'O' if cell == -1 else ' ' for cell in row)
        
        print(" " + row_display + " ")

        if i < len(board_grid) - 1:
            print("---+" * (size - 1) + "---")
            
            
def is_move_forced(grid, winning_configurations, size):
    conf1, conf2 = grid
    for configuration in winning_configurations:
        if bin(configuration & conf1).count('1') == (size - 1) and bin(configuration & conf2).count('1') == 0:
            #print(configuration & ~conf1)
            return int(math.log2(configuration & ~conf1))
        if bin(configuration & conf2).count('1') == (size - 1) and bin(configuration & conf1).count('1') == 0:
            #print(configuration & ~conf2)
            return int(math.log2(configuration & ~conf2))
    return None



def multiple_games(game, num_games, bot1, bot2):

    player0 = bot1
    player1 = bot2
    
    results = {0: 0, 1: 0, 2: 0}

    for _ in tqdm(range(num_games), desc="Playing Games", unit="game"):
        output = game.automatic_games(player0, player1)
        results[output] += 1

    print(f'\nBot {player0} is playing as first player, Bot {player1} is playing as second player')
    print(f'Percentage of wins for {player0}: {results[1]/num_games:.2%}')
    print(f'Percentage of wins for {player1}: {results[2]/num_games:.2%}')
    print(f'Percentage of draws: {results[0]/num_games:.2%}')

    return {player0.name: results[1]/num_games, player1.name: results[2]/num_games, 'draws': results[0]/num_games}

def evaluate_bot(game_size, num_games, game_class, bot, bechmark_bot):

    game = game_class(game_size)

    bot_test_first = bot(game_size, game.winning_configurations, 0, n_iterations=config.N_ITERATIONS)
    bot_test_second = bot(game_size, game.winning_configurations, 1, n_iterations=config.N_ITERATIONS)
    bot_benchmark = bechmark_bot(game_size, game.winning_configurations)

    print(f'Ouput for the bot {bot_test_first} playing as first player and the bot {bot_benchmark} playing as second player')
    result1 = multiple_games(game, num_games, bot_test_first, bot_benchmark)

    print(f'\nOuput for the bot {bot_test_second} playing as second player and the bot {bot_benchmark} playing as first player')
    result2 = multiple_games(game, num_games, bot_benchmark, bot_test_second)

    full_results = {key : (result1[key]*num_games)+(result2[key]*num_games) for key in result1.keys()}

    return full_results

