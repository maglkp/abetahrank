import time
import copy

import sys

E = '_'
X = 'X'
O = 'O'
WIN_X = 'W'
WIN_O = 'O'
LOSE = 'L'
DRAW = 'D'
SYMBOL = {True: X, False: O}
empty_board = [[E, E, E], [E, E, E], [E, E, E]]
XS_ROW = [X, X, X]
OS_ROW = [O, O, O]
NOT_FOUND = -1
BOARD_SIZE = 3
node_cnt = 0


# def is_won_by(board, player_is_x):
#     symbol = SYMBOL[player_is_x]
#     # horizontal row
#     winning_row = [symbol, symbol, symbol]
#     if board[0] == winning_row or board[1] == winning_row or board[2] == winning_row:
#         return True
#     # vertical row
#     if board[0][0] == board[1][0] == board[2][0] == symbol:
#         return True
#     if board[0][1] == board[1][1] == board[2][1] == symbol:
#         return True
#     if board[0][2] == board[1][2] == board[2][2] == symbol:
#         return True
#     # cross rows
#     if board[0][0] == board[1][1] == board[2][2] == symbol:
#         return True
#     if board[2][0] == board[1][1] == board[0][2] == symbol:
#         return True
#     return False


def get_empty_spaces(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == E:
                yield (i, j)


# returns all legal moves as the next board states
def get_legal_moves(board, player_is_x):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == E:
                move = copy.deepcopy(board)
                move[i][j] = SYMBOL[player_is_x]
                yield move


def full_board(board):
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == E:
                return False
    return True


def visit_dfs(board, player_is_x, results):
    global node_cnt
    node_cnt += 1

    # full board
    if full_board(board):
        return [DRAW]

    # current player's winning move
    win_move = get_winning_move(board, player_is_x)
    if win_move != NOT_FOUND:
        return results + [WIN_X if player_is_x else WIN_O]

    # next_board = copy.deepcopy(board)
    # next_board[opp_win_move_coord[0]][opp_win_move_coord[1]] = SYMBOL[player_is_x]
    # return visit(next_board, not player_is_x)
    # if last move by the opposing player resulted in a win
    # if is_won_by(board, not player_is_x):
    #    return [LOSE] if player_is_x else [WIN]

    states = []
    for next_board in get_legal_moves(board, player_is_x):
        states += visit_dfs(next_board, not player_is_x, results)
    return states


# returns coordinates of a winning move in a given row (horizontal, vertical or cross)
# for a player or NOT_FOUND if none exists
def get_winning_move_in_row(board, p1, p2, p3, player_is_x):
    symbol = SYMBOL[player_is_x]
    row = [board[p1[0]][p1[1]], board[p2[0]][p2[1]], board[p3[0]][p3[1]]]
    # there are 2 symbols belonging to active player in this row
    two_symbols_in_row = sum(list(map(lambda e: e == symbol, row))) == 2
    # and 1 empty space
    one_empty_place = sum(list(map(lambda e: e == E, row))) == 1
    # return the index of winning move
    if two_symbols_in_row and one_empty_place:
        return [p1, p2, p3][row.index(E)]
    return NOT_FOUND


# returns coordinates of a winning move for a player or NOT_FOUND if none exists
def get_winning_move(board, player_is_x):
    winning_moves_or_not_founds = [get_winning_move_in_row(board, (0, 0), (0, 1), (0, 2), player_is_x),
                                   get_winning_move_in_row(board, (1, 0), (1, 1), (1, 2), player_is_x),
                                   get_winning_move_in_row(board, (2, 0), (2, 1), (2, 2), player_is_x),
                                   get_winning_move_in_row(board, (0, 0), (1, 0), (2, 0), player_is_x),
                                   get_winning_move_in_row(board, (0, 1), (1, 1), (2, 1), player_is_x),
                                   get_winning_move_in_row(board, (0, 2), (1, 2), (2, 2), player_is_x),
                                   get_winning_move_in_row(board, (0, 0), (1, 1), (2, 2), player_is_x),
                                   get_winning_move_in_row(board, (0, 2), (1, 1), (2, 0), player_is_x)]
    winning_moves = list(filter(lambda e: e != NOT_FOUND, winning_moves_or_not_founds))
    if len(winning_moves) > 0:
        return winning_moves[0]
    return NOT_FOUND


def print_grid(grid):
    for line in grid:
        for cell in line:
            sys.stdout.write(cell)
        sys.stdout.write("\n")
    sys.stdout.write("\n")


def test():
    start = time.time()

    board = [[O, X, E], [E, E, E], [E, E, E]]
    results = visit_dfs(board, True, [])

    x_win_ratio = sum(list(map(lambda e: e == WIN_X, results))) / len(results)
    o_win_ratio = sum(list(map(lambda e: e == WIN_O, results))) / len(results)
    draw_ratio = sum(list(map(lambda e: e == DRAW, results))) / len(results)

    end = time.time()
    print(end - start)

    # visit(empty_board, True)
    # print(len(results))

    # full: 549946
    # 48437


def board_is_empty(board):
    # oh yeah, that's quick and dirty baby...
    empty_row = [E, E, E]
    if board[0] == empty_row and board[1] == empty_row and board[2] == empty_row:
        return True
    return False


def get_win_lose_draw_ratio(board, player_is_x):
    results = visit_dfs(board, player_is_x, [])
    x_win_ratio = sum(list(map(lambda e: e == WIN_X, results))) / len(results)
    o_win_ratio = sum(list(map(lambda e: e == WIN_O, results))) / len(results)
    draw_ratio = sum(list(map(lambda e: e == DRAW, results))) / len(results)
    return x_win_ratio, o_win_ratio, draw_ratio


def next_move(board, player_is_x):
    # choose a corner move if board is empty
    if board_is_empty(board):
        return 0, 0

    symbol = SYMBOL[player_is_x]
    best_solution = (NOT_FOUND, NOT_FOUND)

    for empty_space in get_empty_spaces(board):

        win_move = get_winning_move(board, player_is_x)
        if win_move != NOT_FOUND:
            return win_move

        new_board = copy.deepcopy(board)
        # place the active player's symbol in every empty place and run the game for the opposing player
        new_board[empty_space[0]][empty_space[1]] = symbol
        ratio = get_win_lose_draw_ratio(new_board, not player_is_x)
        win_rate_for_active_player = ratio[0] if player_is_x else ratio[1]

        print("move: ")
        print(empty_space)
        print(ratio)
        print("")

        if best_solution[0] == NOT_FOUND or best_solution[0] < win_rate_for_active_player:
            best_solution = (win_rate_for_active_player, empty_space)

    return best_solution[1]


if __name__ == "__main__":
    player_is_x = input().strip() == X
    board = [[j for j in input().strip()] for i in range(BOARD_SIZE)]
    # print_grid(board)
    move = next_move(board, player_is_x)
    print(str(move[0]) + " " + str(move[1]))

    # lost game:
    # https://www.hackerrank.com/challenges/tic-tac-toe/submissions/game/30869577/all/page/1
