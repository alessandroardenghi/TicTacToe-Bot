import numpy as np
from bot_class import ESBot, MCTSBot
from utils import *
import os
from IPython.display import clear_output

#import keyboard

class TicTacToe:
    def __init__(self, grid_size: int):
        self.size = grid_size
        self.grid = [0,0]
        self.valid_plays = [i for i in range(self.size**2)]
        self.winning_configurations = create_win_grids(self.size)

        self.player0 = None
        self.player1 = None
        self.current_player = None
        self.winner = None
    
    def _play(self, player, position):

        if self.player0 is None or self.player1 is None:
            print('Players not set up')
            return -2
        
        if player not in [self.player0,self.player1]:
            print('Player not allowed')
            return 0
        
        if self._check_status() == 1: 
            print('The game is over')
            return 1
        
        if position not in self.valid_plays:
            print('Play not allowed! Try again')
            return -1
        
        if np.sum(bin(self.grid[0]).count('1')) == np.sum(bin(self.grid[1]).count('1')) + 1 and player == self.player0:
            print(f'Player {self.player0} cannot play twice in a row')
            return 0
        
        if np.sum(bin(self.grid[0]).count('1')) == np.sum(bin(self.grid[1]).count('1')) and player == self.player1:
            print(f'Player {self.player1} cannot play twice in a row')
            return 0
        
        if player == self.player0:
            self.grid[0] |= (1 << position)
        else:
            self.grid[1] |= (1 << position)
        
        self.valid_plays.remove(position)
        
        if self._check_status():
            self.winner = player
            return 1
        

    def _check_status(self):
        if is_win(self.grid, self.winning_configurations) == 1 or is_full(self.grid, self.size) == 1:
            return 1
        return 0

    
    def _display_board(self):

        bin0 = np.array(list(bin(self.grid[0])[2:].zfill(self.size**2)[::-1]), dtype=int)
        bin1 = np.array(list(bin(self.grid[1])[2:].zfill(self.size**2)[::-1]), dtype=int)

        board_grid = (bin0 - bin1).reshape(self.size, self.size)  

        for i, row in enumerate(board_grid):

            row_display = " | ".join('X' if cell == 1 else 'O' if cell == -1 else ' ' for cell in row)
            
            print(" " + row_display + " ")

            if i < len(board_grid) - 1:
                print("---+" * (self.size - 1) + "---")


    def _SetUpGame(self, player0, player1):

        if not isinstance(player0, str):
            raise ValueError('player1 must be a string: name of the human player, "ESBot" or "MCTSBot"')
        if not isinstance(player1, str):
            raise ValueError('player2 must be a string: name of the human player, "ESBot" or "MCTSBot"')
        
        if player0 == 'ESBot':
            self.player1 = ESBot(self.size, self.winning_configurations)
        elif player0 == 'MCTSBot':
            self.player1 = MCTSBot('Monte Carlo Tree Search', self.size)
        else:
            self.player0 = player0
        
        if player1 == 'ESBot':
            self.player1 = ESBot(self.size, self.winning_configurations)
        elif player1 == 'MCTSBot':
            self.player1 = MCTSBot('Monte Carlo Tree Search', self.size)
        else:
            self.player1 = player1
        
        self.current_player = self.player0
        print(f'\nPlayer 1: {self.player0} will play as X')
        print(f'\nPlayer 2: {self.player1} will play as O')

    def _reset_game(self):
        self.grid = [0,0]
        self.valid_plays = [i for i in range(self.size**2)]
        self.winner = None
        self.current_player = None

    def PlayGame(self, player0: str, player1: str):
        """Starts an interactive Tic-Tac-Toe game loop."""
        
        self._SetUpGame(player0, player1)
        
        while self._check_status() == 0:
            #clear_output(wait=False)
            # print(f'\nPlayer 1: {self.player0} will play as X')
            # print(f'Player 2: {self.player1} will play as O')
            print("\nCurrent Board:")
            self._display_board() 

            # Get user input for the move
            
            print(self.current_player)
            if not isinstance(self.current_player, ESBot):

                user_input = input(f"{self.current_player}, enter row (0,{self.size-1}) and column (0,{self.size-1}) separated by space (press 'enter' to exit the game)")

                if user_input in "":
                    print("\nGame stopped by user (quit command).")
                    break
                
                try:
                    row, col = map(int, user_input.split())

                    if (row < 0 or row >= self.size) or (col < 0 or col >= self.size):
                        print(f"Invalid input. enter row (0,{self.size-1}) and column (0,{self.size-1}) separated by space (press 'enter' to exit the game)")
                        continue

                    position = row * self.size + col  # convert it into a position
                except ValueError:
                    print(f"Invalid input. enter row (0,{self.size-1}) and column (0,{self.size-1}) separated by space (press 'enter' to exit the game)")
                    continue

            else: # Bot's turn
                
                # TODO: Implement bot's move
                position = self.current_player.next_move(self.grid) 

            
            status = self._play(self.current_player, position)

            if self.winner != None:
                break  # Stop loop if the game has ended

            if status == -1: # Invalid move do not switch player
                continue

            # Switch player
            self.current_player = self.player0 if self.current_player == self.player1 else self.player1

        # Game has ended, show final board and result
        clear_output(wait=True)
        print(f'\nPlayer 1: {self.player0} will play as X')
        print(f'Player 2: {self.player1} will play as O')
        print("\nFinal Board:")
        self._display_board()
        
        if self.winner:
            print(f"Congratulations! {self.current_player} wins! 🎉")
        else:
            print("It's a draw! 🤝")

        # Reset game state
        self._reset_game()
        

                
                
                