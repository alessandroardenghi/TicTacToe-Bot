from esbot_class import Bot
from tictactoe_class import TicTacToe
import numpy as np

class Game:

    def __init__(self, player0: str, player1: str):

        self.player0 = player0
        self.player1 = player1
        self.current_player = None
        self.current_state = None
        self.winner = None

        if not isinstance(player0, str):
            raise ValueError('player1 must be a string: name of the player or "Bot"')
        if not isinstance(player1, str):
            raise ValueError('player2 must be a string: name of the player or "Bot"')
        
        if player0 == 'Bot':
            self.player1 = Bot()
        
        if player1 == 'Bot':
            self.player2 = Bot()
        
        print(f'\nPlayer 1: {self.player0} will play as X')
        print(f'\nPlayer 2: {self.player1} will play as O')

    
    def PlayGame(self, grid_size: int = 3):

        self.SetUpGame(grid_size)
        
        self.current_state = TicTacToe(grid_size)
        self.current_player = self.player1

        while self.current_state.check_status() == 0:

            print(self.current_state.grid)
            
            pass


    

        
        