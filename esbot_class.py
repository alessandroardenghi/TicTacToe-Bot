from utils import *
import os

class ESBot:

    def __init__(self, size, winning_configurations):
        self.name = 'ESBot'
        self.strategy = self.compute_optimal_strategy((0,0), 0,  winning_configurations, seen_by_moves = None, size = size)
        self.current_grid = None


    def compute_optimal_strategy(self, grid, player, winning_configurations, seen_by_moves, size = 3):
        
        if seen_by_moves is None:
            seen_by_moves = {i: dict() for i in range(size * size + 1)}
            
        conf1, conf2 = grid   
        n_moves = bin(conf1 | conf2).count('1')
        
        if grid in seen_by_moves[n_moves]:
            return seen_by_moves
        
        seen_by_moves[n_moves][grid] = (None, None)
        
        if is_win(grid, winning_configurations):
            seen_by_moves[n_moves][grid] = (None, -1)
            return seen_by_moves
        
        if is_full(grid, size):
            seen_by_moves[n_moves][grid] = (None, 0)
            return seen_by_moves
        
        current_best_score = -1
        current_best_move = None
        for move in range(size ** 2):
            if (conf1 | conf2) & (1 << move) != 0:
                continue
            new_grid = play_move(grid, player, move)
            
            if new_grid is None:
                continue
            seen_by_moves = self.compute_optimal_strategy(new_grid, 1 - player , winning_configurations, seen_by_moves, size)
            
            move_score = - seen_by_moves[n_moves + 1][new_grid][1]
            if move_score > current_best_score:
                current_best_score = move_score
                current_best_move = move
        seen_by_moves[n_moves][grid] = (current_best_move, current_best_score)

        return seen_by_moves
        

    def next_move(self, current_state):
        """
        This method should return the next move of the bot using the precomputed tree.
        The current_state parameter is the current state of the game.
        """
        self.current_grid = tuple(current_state)

        return self.strategy[bin(self.current_grid[0] | self.current_grid[1]).count('1')][self.current_grid][0]

    def __str__(self):
        return self.name

class MCTSBot:
    pass


# bot = ESBot(3, create_win_grids(3))
# print(bot.strategy[2])