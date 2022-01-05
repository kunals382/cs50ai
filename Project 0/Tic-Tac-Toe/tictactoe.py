"""
Tic Tac Toe Player
"""

import math
import sys
import copy

X = "X"
O = "O"
EMPTY = None


def is_full(board):
    """
    Returns True if the board is full else returns False
    """
    for i in range(3):
        if(None in board[i]):
            return False
    return True


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    for row in range(len(board)):
        for column in range(len(board[0])):
            if(board[row][column] is X):
                x_count += 1
            if(board[row][column] is O):
                o_count += 1
    if(abs(x_count-o_count) > 1):
        sys.exit("Invalid Board")
    if(x_count > o_count):
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible = set()

    for row in range(len(board)):
        for column in range(len(board[0])):
            if(board[row][column] is None):
                possible.add((row,column))

    return possible


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if(action is None):
        return board
    board2 = copy.deepcopy(board)
    board2[action[0]][action[1]] = player(board)
    return board2


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in range(len(board)):
        for column in range(len(board[0])):
            if(row == column or (row + column) == 2): #X or O can always be found on the X dianol of the board if there is a winner  
                if(board[row][column] is X or board[row][column] is O):
                    winning_side = board[row][column]

                    # Three in a row

                    for i in range(3):
                        if(board[i][0] == board[i][1] == board[i][2] == winning_side):
                            return winning_side
                        if(board[0][i] == board[1][i] == board[2][i] == winning_side):
                            return winning_side

                    # Diagnols

                    if(board[0][0] == board[1][1] == board[2][2] == winning_side):
                        return winning_side
                    if(board[0][2] == board[1][1] == board[2][0] == winning_side):
                        return winning_side

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if(is_full(board) or winner(board) is not None):
        return True
    return False 


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if(win is not None):
        if(win is X):
            return 1
        if(win is O):
            return -1
    return 0




def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if(terminal(board)):
        return None
    playing_side = player(board)
    
    if(playing_side is X):
        value, optimal_move = max_value(board,beta=math.inf)
        return optimal_move
    else:
        value, optimal_move = min_value(board,alpha=-math.inf)
        return optimal_move




def min_value(board, alpha):
    if(terminal(board)):
        return(utility(board)), None

    v = math.inf
    ac = None
    beta = math.inf
    for action in actions(board):
        v1, _ = max_value(result(board, action), beta)
        if(v1 < v): 
            ac = action

        if(alpha >= v1):
            v = min(v, v1)
            beta = min(beta, v)
            break

        if(v1 < v):
            ac = action
        v = min(v, v1)
        beta = min(beta, v)


        if v == -1:
            return v,action

    return v, ac


def max_value(board, beta):
    if(terminal(board)):
        return(utility(board)), None
    v = -math.inf
    ac = None
    alpha = -math.inf
    for action in actions(board):
        v1, _ = min_value(result(board,action), alpha)
        if(v1 > v): 
            ac = action

        if(v1 >= beta):
            v = max(v,v1)
            alpha = max(alpha,v)
            break

        v = max(v,v1)
        alpha = max(alpha,v)

        if v == 1:
            return v,action
    return v, ac 



