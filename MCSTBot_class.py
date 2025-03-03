from utils import *
import os
import numpy as np
import math
import random

import config

class MCTSNode:
    def __init__(self, state, valid_moves, player, parent=None):
        """
        Each node represents a state in the game.
        - state: instance of TicTacToeState.
        - parent: parent node (None for root).
        - move: the move that led to this state.
        """
        self.state = state
        self.valid_moves = valid_moves
        self.player = player # player that have to move next

        self.parent = parent
        self.children = []

        self.N = 0
        self.V = 0
        self.ucb = math.inf

    def update_board(self, move):
        """Update the board with the given move."""

        if (self.state[0] | self.state[1]) & (1 << move) != 0:
            #raise ValueError('Invalid move')
            print('Invalid move')
            return

        new_moves = self.valid_moves.copy()
        new_moves.remove(move)
        if self.player == 0:
            return (self.state[0] | (1 << move), self.state[1]), new_moves
        else:
            return (self.state[0], self.state[1] | (1 << move)), new_moves
        
    

class MCTSBot:

    def __init__(self, size, winning_configurations, player, verbose=0):
        self.name = 'MCTSBot'
        self.winning_configurations = winning_configurations
        self.size = size
        self.player = player

        self.root = None # starting configuration on which we start building the tree
        
        self.verbose = verbose

    def __str__(self):
        return self.name
    
    
    def next_move(self, current_state, valid_moves):
        
        self.root = MCTSNode(current_state, valid_moves, self.player)

        if is_move_forced(self.root.state, self.winning_configurations, self.size) is not None:
            if self.verbose >= 1:
                print('THE NEXT MOVE IS FORCED')
            return is_move_forced(self.root.state, self.winning_configurations, self.size)

        for move in self.root.valid_moves:
            
            new_state, new_valid_moves = self.root.update_board(move)
            new_node = MCTSNode(new_state, new_valid_moves, 1 - self.root.player, self.root)
            self.root.children.append(new_node)

        v_scores = self._build_strategy()
        
        return self._select_best_move(v_scores)

    def _select_best_move(self, scores):
        return self.root.valid_moves[np.array(scores).argmax()]

    def _build_strategy(self):
        
        #while resources_left():
        for iteration in range(len(self.root.valid_moves)*config.N_ITERATIONS_PER_MOVE):
            if self.verbose >= 2:
                print()
                print(f'CURRENT UCB: {[compute_ucb(leaf) for leaf in self.root.children]}')
                print('SELECTING')

            leaf = self._select()
            
            if self.verbose >= 2:
                #print(f'SELECTED NODE: {display_board(leaf.state, self.size)}\n')
                print(f'SELECTED NODE:')
                display_board(leaf.state, self.size)
                print('EXPANDING')
            
            leaf = self._expand(leaf)

            if self.verbose >= 2:
                print(f'EXPANSION DONE\n')
                print(f'SIMULATING')

            result = self._simulate(leaf.state, leaf.valid_moves, leaf.player)

            if self.verbose >= 2:
                print(f'SIMULATION OVER. RESULT: {result}\n')
                print(f'BACKPROPAGATING\n')

            self._backpropagate(leaf, result)

        if self.verbose >= 1:
            print(f'Results of Strategy:\n')
            for i, move in enumerate(self.root.valid_moves):
                leaf = self.root.children[i]
                print(f'Move: {move}:\n')
                print(f'\tUCB Score: {compute_ucb(leaf)}')
                print(f'\tAverage Value: {leaf.V/leaf.N}')
                print(f'\t# of Times Visited: {leaf.N}')

        return [[leaf.V/leaf.N for leaf in self.root.children]]
    
    def _select(self):
        """
        Select the best leaf node to expand.
        """

        leaf = self.root

        while leaf.children != []:
            
            best_child = np.array([compute_ucb(child) for child in leaf.children]).argmax()

            leaf = leaf.children[best_child]
        
        return leaf

    def _expand(self, leaf):
        """
        Expand the leaf node by adding all possible children.
        """

        if leaf.N == 0 or leaf.valid_moves == [] or is_win(leaf.state, self.winning_configurations):
            
            if self.verbose >= 2:
                print('LEAF NOT VISITED OR LEAF IS TERMINAL STAGE. NOT EXPANDING')

            return leaf
        
        if self.verbose >= 2:
            print(f'LEAF: {display_board(leaf.state, self.size)}')
            print(f'LEFT MOVES: {leaf.valid_moves}')

        if is_move_forced(leaf.state, self.winning_configurations, self.size) is not None:
            move = is_move_forced(leaf.state, self.winning_configurations, self.size)
            new_state, new_valid_moves = leaf.update_board(move)
            new_node = MCTSNode(new_state, new_valid_moves, 1 - leaf.player, leaf)
            leaf.children.append(new_node)
        else:
            for move in leaf.valid_moves:
                
                new_state, new_valid_moves = leaf.update_board(move)
                new_node = MCTSNode(new_state, new_valid_moves, 1 - leaf.player, leaf)

                leaf.children.append(new_node)

        return leaf.children[0]


    def _simulate(self, board, valid_moves, player):
        """ Rollout a game from the given node """

        if self.verbose >= 2:
            print()
            print(f'board in simulation:')
            display_board(board, self.size)
            print(f'valid moves {valid_moves}')

        if is_win(board, self.winning_configurations) == (self.player + 1):
            if self.verbose >= 2:
                print('WIN FOR PLAYER')
            return config.WIN_SCORE
        elif is_win(board, self.winning_configurations) == 2 and self.player == 0:
            if self.verbose >= 2:
                print('LOSS FOR PLAYER')
            return config.LOSE_SCORE
        
        elif is_win(board, self.winning_configurations) == 1 and self.player == 1:
            if self.verbose >= 2:
                print('LOSS FOR PLAYER')
            return config.LOSE_SCORE
        
        elif is_full(board, self.size):
            if self.verbose >= 2:
                print('TIE')
            return config.TIE_SCORE
        
        else:
            
            if is_move_forced(board, self.winning_configurations, self.size) is not None:
                move = is_move_forced(board, self.winning_configurations, self.size)
                if self.verbose >= 2:
                    print(f'MOVE FORCED: {move}')
            else:
                move = random.choice(valid_moves)
            next_player_board = board[player] | (1 << move)
            if player == 0:
                next_board = (next_player_board, board[1])
            else:
                next_board = (board[0], next_player_board)
            remaining_valid_moves = valid_moves.copy()
            remaining_valid_moves.remove(move)


            return self._simulate(next_board, remaining_valid_moves, 1 - player)


    def _backpropagate(self, node, result):
        """ Update the node statistics """

        node.N += 1
        if self.player != node.player:
            node.V += result
        else:
            node.V -= result
        
        if node.parent is not None:
            self._backpropagate(node.parent, result)

    def print_tree(self, node, indent=0):
        print(" " * indent + str(node.status))
        # Recursively print each child, increasing the indentation.
        for child in node.children:
            self.print_tree(child, indent + 4)


# c = MCTSBot(4, create_win_grids(4), 0, n_iterations= config.N_ITERATIONS, verbose=0)
# print(c.next_move((1,2), [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]))