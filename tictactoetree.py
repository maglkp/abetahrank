import copy

E = '-'
X = 'X'
O = 'O'
WIN = 'W'
LOSE = 'L'
DRAW = 'D'
SYMBOL = {True: X, False: O}
# empty_board = [[E, E, E], [E, E, E], [E, E, E]]
empty_board = [[E, E, E], [E, E, E], [E, E, E]]
XS_ROW = [X, X, X]
OS_ROW = [O, O, O]
NOT_FOUND = -1

times = 0


def is_won_by(board, player_is_x):
    symbol = SYMBOL[player_is_x]
    # horizontal row
    winning_row = [symbol, symbol, symbol]
    if board[0] == winning_row or board[1] == winning_row or board[2] == winning_row:
        return True
    # vertical row
    if board[0][0] == board[1][0] == board[2][0] == symbol:
        return True
    if board[0][1] == board[1][1] == board[2][1] == symbol:
        return True
    if board[0][2] == board[1][2] == board[2][2] == symbol:
        return True
    # cross rows
    if board[0][0] == board[1][1] == board[2][2] == symbol:
        return True
    if board[2][0] == board[1][1] == board[0][2] == symbol:
        return True
    return False


# returns all legal moves as the next board states
def get_legal_moves(board, player_is_x):
    for i in range(3):
        for j in range(3):
            if board[i][j] == E:
                move = copy.deepcopy(board)
                move[i][j] = SYMBOL[player_is_x]
                yield move


def full_board(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == E:
                return False
    return True


def visit(board, player_is_x):
    global times
    times += 1

    # basic tree pruning
    if get_winning_move(board, player_is_x) != NOT_FOUND:
        return [WIN]

    opp_win_move_coord = get_winning_move(board, not player_is_x)
    if opp_win_move_coord != NOT_FOUND:
        next_board = copy.deepcopy(board)
        next_board[opp_win_move_coord[0]][opp_win_move_coord[1]] = SYMBOL[player_is_x]
        return visit(next_board, not player_is_x)

    # if last move by the opposing player resulted in a win
    if is_won_by(board, not player_is_x):
        return [LOSE] if player_is_x else [WIN]
    if full_board(board):
        return [DRAW]

    states = []
    for next_board in get_legal_moves(board, player_is_x):
        states += visit(next_board, not player_is_x)
    return states


# returns coordinates of a winning move for a player or NOT_FOUND if none exists
def get_winning_move(board, player_is_x):
    pass


#def can_win_in_row(cell1, cell2, cell3, player_is_x):
#    symbol = SYMBOL[player_is_x]


visit(empty_board, True)
print(times)

# full: 549946
# 48437