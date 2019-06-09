# from Game import *
from copy import deepcopy

MAX_DEPTH = 4


class Node:
    def __init__(self, value, piece, move, depth):
        self.value = value
        self.piece = piece
        self.move = move
        self.depth = depth
        self.children = list()

    def add_child(self, child):
        self.children.append(child)


def AI_move(board):
    # piece = board.valid_pieces()[0]
    # print(piece, board.valid_moves(piece))
    # return piece, board.valid_moves(piece)[0]
    current_depth = 0
    root = Node(float('-inf'), None, None, current_depth)
    root = make_tree(board, root)
    value, move, piece = min_max_func(root)
    for n in root.children:
        if n.value == value:
            move = n.move
            piece = n.piece
    # print(value)
    # print(piece)
    # print(move)
    return piece, move


def make_tree(board, root):
    # print(board)
    if board.check_win():
        return root
    # print(0)
    if root.depth == MAX_DEPTH:
        return root
    # print(0)
    valid_pieces = board.valid_pieces()
    # print(valid_pieces)
    # valid_moves = [board.valid_moves(x) for x in valid_pieces]
    # print(valid_moves)
    for p in valid_pieces:
        valid_moves = board.valid_moves(p)
        for m in valid_moves:
            new_board = deepcopy(board)
            # print(p)
            # print(m)
            new_board.move(p, m)
            # print(new_board)
            current_depth = root.depth + 1
            if current_depth == MAX_DEPTH:
                # print(new_board)
                new_node = Node(h(new_board), p, m, current_depth)
                # print(10)
            else:
                if root.value == float('inf'):
                    # print('max node created')
                    new_node = Node(float('-inf'), p, m, current_depth)
                else:
                    new_node = Node(float('inf'), p, m, current_depth)
                    # print('min node created')
            root.add_child(new_node)
            make_tree(new_board, new_node)
    return root


def h(board):
    heuristic = 0
    if board.check_win():
        if board.isAI:
            heuristic = float('inf')
        else:
            heuristic = float('-inf')
        return heuristic
    heuristic += board.AINumber
    heuristic -= board.playerNumber
    for r in board.pieces:
        for p in r:
            if p is None:
                continue
            if p.isKing:
                if p.isAI:
                    heuristic += 3
                else:
                    heuristic -= 3
    for r in board.pieces:
        for p in r:
            if p is not None and p.isAI:
                heuristic += check(p.getNortheast(), board)
                heuristic += check(p.getNorthwest(), board)
                heuristic += check(p.getSoutheast(), board)
                heuristic += check(p.getSouthwest(), board)
    return heuristic


def check(p, board):
    if p is not None:
        piece = board.pieces[p[0]][p[1]]
        if piece is not None:
            if piece.isAI:
                return 1
            else:
                return -1
        else:
            return 0
    else:
        return 0


def min_max_func(root):
    if root.value != float('-inf') and root.value != float('inf'):
        return root.value, root.move, root.piece
    elif root.value == float('-inf'):
        # temp = None
        # temp_value = float('-inf')
        for n in root.children:
            temp = min_max_func(n)
            if temp[0] > root.value:
                root.value = temp[0]
                root.move = temp[1]
                root.piece = temp[2]
    else:
        for n in root.children:
            temp = min_max_func(n)
            if temp[0] < root.value:
                root.value = temp[0]
                # root.move = temp[1]
                # root.piece = temp[2]
    return root.value, root.move, root.piece

# if __name__ == '__main__':
#     game_board = Board.Board(720)
#     AI_move(game_board)
