from utils import *
import os
import numpy as np
import math
import random

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
        

    def best_child(self, exploration=1.41):
        """Select the child with the highest UCT (Upper Confidence Bound) value."""
        choices_weights = []
        for child in self.children:
            if child.visits == 0:
                choices_weights.append(float('inf'))
            else:
                exploitation = child.wins / child.visits
                exploration_term = exploration * math.sqrt(math.log(self.visits) / child.visits)
                choices_weights.append(exploitation + exploration_term)
        return self.children[choices_weights.index(max(choices_weights))]
    

class MCTSBot:

    def __init__(self, size, winning_configurations, player, n_iterations = 100, debug=False):
        self.n_iterations = n_iterations
        self.name = 'MCTSBot'
        self.winning_configurations = winning_configurations
        self.size = size
        self.player = player

        self.root = None # starting configuration on which we start building the tree
        
        self.debug = debug

    def __str__(self):
        return self.name
    
    def resources_left(self):
        return True
    
    def next_move(self, current_state, valid_moves):
        
        self.root = MCTSNode(current_state, valid_moves, self.player)

        for move in self.root.valid_moves:
            
            new_state, new_valid_moves = self.root.update_board(move)
            new_node = MCTSNode(new_state, new_valid_moves, 1 - self.root.player, self.root)
            self.root.children.append(new_node)

        v_scores = self._build_strategy()
        
        return self._select_best_move(v_scores)

    def _select_best_move(self, ucb_scores):
        return self.root.valid_moves[np.array(ucb_scores).argmax()]

    def _build_strategy(self):
        
        #while resources_left():
        for iteration in range(self.n_iterations):
            if self.debug:
                print(f'CURRENT UCB: {[compute_ucb(leaf) for leaf in self.root.children]}')
                print('SELECTING')

            leaf = self._select()
            
            if self.debug:
                print(f'SELECTED NODE: {leaf.state}\n')
                print('EXPANDING')
            
            leaf = self._expand(leaf)

            if self.debug:
                print(f'EXPANSION DONE')
                print(f'SIMULATING')

            result = self._simulate(leaf.state, leaf.valid_moves, leaf.player)

            if self.debug:
                print(f'SIMULATION OVER. RESULT: {result}')
                print(f'BACKPROPAGATING')

            self._backpropagate(leaf, result)

        if self.debug:
            print([compute_ucb(child) for child in self.root.children])
            print([leaf.V/leaf.N for leaf in self.root.children])
            print([leaf.N for leaf in self.root.children])

        return [[leaf.V/leaf.N for leaf in self.root.children]]
    
    def _select(self):
        """
        Select the best leaf node to expand.
        """

        leaf = self.root

        while leaf.children != []:
            
            best_child = np.array([compute_ucb(child.parent, child.V , child.N, child.parent.N) for child in leaf.children]).argmax()

            leaf = leaf.children[best_child]
        
        return leaf

    def _expand(self, leaf):
        """
        Expand the leaf node by adding all possible children.
        """

        if leaf.N == 0 or leaf.valid_moves == []:
            
            if self.debug:
                print('LEAF NOT VISITED OR LEAF IS TERMINAL STAGE. NOT EXPANDING')

            return leaf
        
        if self.debug:
            print(f'LEAF: {leaf.state}')
            print(f'LEFT MOVES: {leaf.valid_moves}')

        for move in leaf.valid_moves:
            
            new_state, new_valid_moves = leaf.update_board(move)
            new_node = MCTSNode(new_state, new_valid_moves, 1 - leaf.player, leaf)

            leaf.children.append(new_node)

        return leaf.children[0]


    def _simulate(self, board, valid_moves, player):
        """ Rollout a game from the given node """

        if self.debug:
            print(f'board in simulation: {board}')
            print(f'valid moves {valid_moves}')

        if is_win(board, self.winning_configurations) and player == self.player:
            if self.debug:
                print('LOSS FOR PLAYER')
            return config.LOSE_SCORE
        elif is_win(board, self.winning_configurations) and player != self.player:
            if self.debug:
                print('WIN FOR PLAYER')
            return config.WIN_SCORE
        elif is_full(board, self.size):
            if self.debug:
                print('TIE')
            return config.TIE_SCORE
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
        node.V += result
        
        if node.parent is not None:
            self._backpropagate(node.parent, result)

    def print_tree(self, node, indent=0):
        print(" " * indent + str(node.status))
        # Recursively print each child, increasing the indentation.
        for child in node.children:
            self.print_tree(child, indent + 4)


a = MCTSBot(3, create_win_grids(3), 0, 15000)
print(a.next_move((5, 16), [1, 3, 5, 6, 7, 8]))

