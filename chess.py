#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import copy
import sys

#TODO more play testing, and comments

def input_process(string): 
    return string.strip().lower()

def print_board(board):
    row_id = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    pieces = ['Q', 'B', 'N', 'R', 'P']
    print("Top Dead:\t\t0\t1\t2\t3\t4\t5\t6\t7\t\tBottom Dead:")
    for row in range(len(board.rows)):
        if row in range(5):
            top_dead = "{0}: {1}".format(pieces[row], board.top_dead[row])
            bottom_dead = "{0}: {1}".format(pieces[row], board.bottom_dead[row])
        else:
            top_dead = ' ' * 4
            bottom_dead = ''
        col_A = '\t\t{0}\t{1}'.format(row_id[row], board.rows[row][0])
        col_B = '\t{0}'.format(board.rows[row][1])
        col_C = '\t{0}'.format(board.rows[row][2])
        col_D = '\t{0}'.format(board.rows[row][3])
        col_E = '\t{0}'.format(board.rows[row][4])
        col_F = '\t{0}'.format(board.rows[row][5])
        col_G = '\t{0}'.format(board.rows[row][6])
        col_H = '\t{0}'.format(board.rows[row][7] + '\t\t')
        print('\n\n' + top_dead + col_A + col_B + col_C + col_D + col_E + col_F + col_G + col_H + bottom_dead)
    print('\n\n')    

def move_piece(board, piece, move_to):
    row_index = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    p_row = row_index[piece[0]]
    p_column = int(piece[-1])
    m_row = row_index[move_to[0]]
    m_column = int(move_to[-1])
    
    piece_to_move = board.rows[p_row][p_column]
    dead_piece = board.rows[m_row][m_column]

    board.rows[m_row][m_column] = piece_to_move
    board.rows[p_row][p_column] = 'x'

    if dead_piece[0] == 'b':
        if dead_piece[-1] == 'Q':
            board.bottom_dead[0] += 1
        elif dead_piece[-1] == 'B':
            board.bottom_dead[1] += 1
        elif dead_piece[-1] == 'N':
            board.bottom_dead[2] += 1
        elif dead_piece[-1] == 'R':
            board.bottom_dead[3] += 1
        elif dead_piece[-1] == 'P':
            board.bottom_dead[4] += 1
    else:
        if dead_piece[-1] == 'Q':
            board.top_dead[0] += 1
        elif dead_piece[-1] == 'B':
            board.top_dead[1] += 1
        elif dead_piece[-1] == 'N':
            board.top_dead[2] += 1
        elif dead_piece[-1] == 'R':
            board.top_dead[3] += 1
        elif dead_piece[-1] == 'P':
            board.top_dead[4] += 1

def is_valid_move(board, piece, move_to):
    row_index = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    columns = [0,1,2,3,4,5,6,7]
    try:
        if type(piece[0]) == int and type(move_to[0]) == int:
            p_row = columns[piece[0]]
            p_column = columns[piece[-1]]
            m_row = columns[move_to[0]]
            m_column = columns[move_to[-1]]
        else:
            p_row = row_index[piece[0]]
            p_column = columns[int(piece[-1])]
            m_row = row_index[move_to[0]]
            m_column = columns[int(move_to[-1])]
    except:
        return False
    if board.rows[m_row][m_column][0] == board.rows[p_row][p_column][0]:
            return False
    piece_type = board.rows[p_row][p_column][-1]
    if piece_type == 'R':
        if p_row == m_row:
            if p_column < m_column:
                for i in range(p_column + 1, m_column):
                    if board.rows[p_row][i] != 'x':
                        return False
            else:
                for i in range(m_column + 1, p_column):
                    if board.rows[p_row][p_column - i] != 'x':
                        return False
        elif p_column == m_column:
            if p_row < m_row:
                for i in range(p_row + 1, m_row):
                    if board.rows[i][p_column] != 'x':
                        return False
            else:
                for i in range(m_row + 1, p_row):
                    if board.rows[p_row - i][p_column] != 'x':
                        return False
        else:
            return False
    elif piece_type == 'N':
        if p_row + 2 == m_row or p_row - 2 == m_row:
            if p_column + 1 != m_column and p_column - 1 != m_column:
                return False
        elif p_column + 2 == m_column or p_column - 2 == m_column:
            if p_row + 1 != m_row and p_row - 1 != m_row:
                return False
        else:
            return False
    elif piece_type == 'B':
        if abs((p_row - m_row) / (p_column - m_column)) != 1:
            return False
        if m_row > p_row:
            if m_column < p_column: 
                for i in range(1, p_column - m_column):
                    if board.rows[p_row + i][p_column - i] != 'x':
                        return False
            elif m_column > p_column:
                for i in range(1, m_column - p_column):
                    if board.rows[p_row + i][p_column + i] != 'x':
                        return False
        elif m_row < p_row:
            if m_column > p_column:
                for i in range(1, m_column - p_column):
                    if board.rows[p_row - i][p_column + i] != 'x':
                        return False
            elif m_column < p_column:
                for i in range(1, p_column - m_column):
                    if board.rows[p_row - i][p_column - i] != 'x':
                        return False
    elif piece_type == 'P':
        if board.rows[p_row][p_column][0] == 'b':
            if p_row == 6:
                if m_column == p_column:
                    if m_row + 2 == p_row or m_row + 1 == p_row:
                        for i in range(m_row, p_row):
                            if board.rows[i][p_column] != 'x':
                                return False
                    else: 
                        return False
                elif m_column + 1 == p_column or m_column - 1 == p_column:
                    if m_row + 1 != p_row or board.rows[m_row][m_column] == 'x':
                        return False
                else:
                    return False
            elif p_row < 6:
                if m_column == p_column:
                    if m_row + 1 != p_row or board.rows[m_row][m_column] != 'x':
                        return False
                elif m_column + 1 == p_column or m_column - 1 == p_column:
                    if m_row + 1 != p_row or board.rows[m_row][m_column] == 'x':
                        return False
                else:
                    return False
            else:
                return False
        elif board.rows[p_row][p_column][0] == 't':
            if p_row == 1:
                if m_column == p_column:
                    if m_row - 1 == p_row or m_row - 2 == p_row:
                        for i in range(p_row + 1, m_row + 1):
                            if board.rows[i][p_column] != 'x':
                                return False
                    else:
                        return False
                elif m_column + 1 == p_column or m_column - 1 == p_column:
                    if m_row - 1 != p_row or board.rows[m_row][m_column] == 'x':
                        return False
                else:
                    return False
            elif p_row > 1:
                if m_column == p_column:
                    if m_row - 1 != p_row or board.rows[m_row][m_column] != 'x':
                        return False
                elif m_column + 1 == p_column or m_column - 1 == p_column:
                    if m_row - 1 != p_row or board.rows[m_row][m_column] == 'x':
                        return False
                else:
                    return False
    elif piece_type == 'K':
        if abs(m_row - p_row) > 1 or abs(m_column - p_column) > 1:
            return False
    elif piece_type == 'Q':
        if m_column == p_column:
            if m_row > p_row:
                for i in range(p_row + 1, m_row):
                    if board.rows[i][p_column] != 'x':
                        return False
            elif p_row > m_row:
                for i in range(m_row + 1, p_row):
                    if board.rows[i][p_column] != 'x':
                        return False
        elif m_row == p_row:
            if m_column > p_column:
                for i in range(p_column + 1, m_column):
                    if board.rows[p_row][i] != 'x':
                        return False
            elif p_column > m_column:
                for i in range(m_column + 1, p_column):
                    if board.rows[p_row][i] != 'x':
                        return False
        else:
            if abs((m_row - p_row) // (m_column - p_column)) != 1:
                return False
            if m_row > p_row:
                if m_column < p_column: 
                    for i in range(1, p_column - m_column):
                        if board.rows[p_row + i][p_column - i] != 'x':
                            return False
                elif m_column > p_column:
                    for i in range(1, m_column - p_column):
                        if board.rows[p_row + i][p_column + i] != 'x':
                            return False
            elif m_row < p_row:
                if m_column > p_column:
                    for i in range(1, m_column - p_column):
                        if board.rows[p_row - i][p_column - i] != 'x':
                            return False
                elif m_column < p_column:
                    for i in range(1, p_column - m_column):
                        if board.rows[p_row - i][p_column - i] != 'x':
                            return False
    return True
                    
def is_valid_piece(board, turn, piece):
    row_index = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}
    columns = [0,1,2,3,4,5,6,7]
    try:
        p_row = row_index[piece[0]]
        p_column = columns[int(piece[-1])]
        if turn:
            if board.rows[p_row][p_column][0] != 'b':
                return False
        else:
            if board.rows[p_row][p_column][0] != 't':
                return False
        return True
    except:
        print("INVALID CHOICE!")
        return False  

def exchange_piece(board, bottom_turn):
    if bottom_turn:
        for column in range(len(board.rows[0])):
            if board.rows[0][column] == 'bP':
                print("You have a pawn that you could upgrade.\nIf you would like to upgrade it enter the suffix of the piece you want ot exchange it for or if you don't want to exchange it enter 'no'. ")
                exchange = input_process(input(">>> "))
                if exchange == 'no':
                    break
                elif exchange.upper() in ['B', 'N', 'R', 'Q']:
                    board.rows[0][column] = 'b' + exchange.upper()
                    return True
    else:
        for column in range(len(board.rows[7])):
            if board.rows[7][column] == 'tP':
                print("You have a pawn that you could upgrade.\nIf you would like to upgrade it enter the suffix of the piece you want ot exchange it for or if you don't want to exchange it enter 'no'. ")
                exchange = input_process(input(">>> "))
                if exchange == 'no':
                    break
                elif exchange.upper() in ['B', 'N', 'R', 'Q']:
                    board.rows[7][column] = 't' + exchange.upper()
                    return True
    return False

def king_position(board, bottom_turn):
    if bottom_turn:
        player = 'b'
    else:
        player = 't'
    king_row = 0
    king_column = 0
    for row in range(len(board.rows)):
        for column in range(len(board.rows[0])):
            if board.rows[row][column] == player + 'K':
                king_row = row
                king_column = column
                return king_row, king_column

def player_in_check(board, bottom_turn, king_row, king_column):
    if bottom_turn:
        player = 'b'
    else:
        player = 't'
    # horizontal checks
    for i in range(1, king_column + 1):
        if board.rows[king_row][king_column - i] != 'x':
            if board.rows[king_row][king_column - i][0] == player:
                break
            elif board.rows[king_row][king_column - i][-1] in ['Q', 'R']:
                return king_row, king_column - i
            elif board.rows[king_row][king_column - i][-1] == 'K' and i == 1:
                return king_row, king_column - i
    for i in range(king_column + 1, 8):
        if board.rows[king_row][i] != 'x':
            if board.rows[king_row][i][0] == player:
                break
            elif board.rows[king_row][i][-1] in ['Q', 'R']:
                return king_row, i
            elif board.rows[king_row][i][-1] == 'K' and king_column + 1 == i:
                return king_row, i
    # vertical checks
    for i in range(1, king_row + 1):
        if board.rows[king_row - i][king_column] != 'x':
            if board.rows[king_row - i][king_column][0] == player:
                break
            elif board.rows[king_row - i][king_column][-1] in ['Q', 'R']:
                return king_row - i, king_column
            elif board.rows[king_row - i][king_column][-1] == 'K' and i == 1:
                return king_row - i, king_column
    for i in range(king_row + 1, 8):
        if board.rows[i][king_column] != 'x':
            if board.rows[i][king_column][0] == player:
                break
            elif board.rows[i][king_column][-1] in ['Q', 'R']:
                return i, king_column
            elif board.rows[i][king_column][-1] == 'K' and king_row + 1 == i:
                return i, king_column
    # diagonal checks
    for i in range(1, king_row + 1):
        if king_column - i in range(king_column):
            if board.rows[king_row - i][king_column - i] != 'x':
                if board.rows[king_row - i][king_column - i][0] == player:
                    break
                elif board.rows[king_row - i][king_column - i][-1] in ['Q', 'B']:
                    return king_row - i, king_column - i
                elif board.rows[king_row - i][king_column - i][-1] == 'K' and i == 1:
                    return king_row - i, king_column - i
                elif board.rows[king_row - i][king_column - i][-1] == 'P' and i == 1:
                    if player == 'b':
                        return king_row - i, king_column - i
        else:
            break
    for i in range(1, king_row + 1):
        if king_column + i in range(king_column + 1, 8):
            if board.rows[king_row - i][king_column + i] != 'x':
                if board.rows[king_row - i][king_column + i][0] == player:
                    break
                elif board.rows[king_row - i][king_column + i][-1] in ['Q', 'B']:
                    return king_row - i, king_column + i
                elif board.rows[king_row - i][king_column + i][-1] == 'K' and i == 1:
                    return king_row - i, king_column + i
                elif board.rows[king_row - i][king_column + i][-1] == 'P' and i == 1:
                    if player == 'b':
                        return king_row - i, king_column + i
        else:
            break
    for i in range(1, 8 - king_row):
        if king_column - i in range(king_column):
            if board.rows[king_row + i][king_column - i] != 'x':
                if board.rows[king_row + i][king_column - i][0] == player:
                    break
                elif board.rows[king_row + i][king_column - i][-1] in ['Q', 'B']:
                    return king_row + i, king_column - i
                elif board.rows[king_row + i][king_column - i][-1] == 'K' and i == 1:
                    return king_row + i, king_column - i
                elif board.rows[king_row + i][king_column - i][-1] == 'P' and i == 1:
                    if player == 't':
                        return king_row + i, king_column - i
        else:
            break
    for i in range(1, 8 - king_row):
        if king_column + i in range(king_column + 1, 8):
            if board.rows[king_row + i][king_column + i] != 'x':
                if board.rows[king_row + i][king_column + i][0] == player:
                    break
                elif board.rows[king_row + i][king_column + i][-1] in ['Q', 'B']:
                    return king_row + i, king_column + i
                elif board.rows[king_row + i][king_column + i][-1] == 'K' and i == 1:
                    return king_row + i, king_column + i
                elif board.rows[king_row + i][king_column + i][-1] == 'P' and i == 1:
                    if player == 't':
                        return king_row + i, king_column + i
        else:
            break
    # knight checks
    if (king_row - 2) in range(0, 8) and (king_column - 1) in range(0, 8):
        if board.rows[king_row - 2][king_column - 1][-1] == 'N' and board.rows[king_row - 2][king_column - 1][0] != player:
            return king_row - 2, king_column - 1
    if (king_row - 2) in range(0, 8) and (king_column + 1) in range(0, 8):
        if board.rows[king_row - 2][king_column + 1][-1] == 'N' and board.rows[king_row - 2][king_column + 1][0] != player:
            return king_row - 2, king_column + 1
    if (king_row + 2) in range(0, 8) and (king_column - 1) in range(0, 8):
        if board.rows[king_row + 2][king_column - 1][-1] == 'N' and board.rows[king_row + 2][king_column - 1][0] != player:
            return king_row + 2, king_column -1
    if (king_row + 2) in range(0, 8) and (king_column + 1) in range(0, 8):
        if board.rows[king_row + 2][king_column + 1][-1] == 'N' and board.rows[king_row + 2][king_column + 1][0] != player:
            return king_row + 2, king_column + 1
    if (king_row + 1) in range(0, 8) and (king_column - 2) in range(0, 8):
        if board.rows[king_row + 1][king_column - 2][-1] == 'N' and board.rows[king_row + 1][king_column - 2][0] != player:
            return king_row + 1, king_column - 2
    if (king_row - 1) in range(0, 8) and (king_column - 2) in range(0, 8):
        if board.rows[king_row - 1][king_column - 2][-1] == 'N' and board.rows[king_row - 1][king_column - 2][0] != player:
            return king_row - 1, king_column - 2
    if (king_row - 1) in range(0, 8) and (king_column + 2) in range(0, 8):
        if board.rows[king_row - 1][king_column + 2][-1] == 'N' and board.rows[king_row - 1][king_column + 2][0] != player:
            return king_row - 1, king_column + 2
    if (king_row + 1) in range(0, 8) and (king_column + 2) in range(0, 8):
        if board.rows[king_row + 1][king_column + 2][-1] == 'N' and board.rows[king_row + 1][king_column + 2][0]!= player:
            return king_row + 1, king_column + 2
    return False

def player_in_checkmate(board, bottom_turn, king_row, king_column):
    if bottom_turn:
        player = 'b'
    else:
        player = 't'
    class test_board:
        rows = copy.deepcopy(board.rows)
    test_board.rows[king_row][king_column] = 'x'
    # checks to see if king can move out of check
    try:
        if is_valid_move(board,[king_row, king_column], [king_row, king_column + 1]):
            if player_in_check(test_board, bottom_turn, king_row, king_column + 1) == False: 
                return False
    except: pass
    try:
        if is_valid_move(board, [king_row, king_column], [king_row, king_column - 1]):
            if player_in_check(test_board, bottom_turn, king_row, king_column - 1) == False:
                return False
    except: pass
    try:
        if is_valid_move(board, [king_row, king_column], [king_row - 1, king_column]):
            if player_in_check(test_board, bottom_turn, king_row - 1, king_column) == False:
                return False
    except: pass
    try:
        if is_valid_move(board, [king_row, king_column], [king_row + 1, king_column]):
            if player_in_check(test_board, bottom_turn, king_row + 1, king_column) == False:
                return False
    except: pass
    try:
        if is_valid_move(board, [king_row, king_column], [king_row - 1, king_column - 1]):
            if player_in_check(test_board, bottom_turn, king_row - 1, king_column - 1) == False:
                return False
    except: pass
    try:
        if is_valid_move(board, [king_row, king_column], [king_row - 1, king_column + 1]):
            if player_in_check(test_board, bottom_turn, king_row - 1, king_column + 1) == False:
                return False
    except: pass
    try:
        if is_valid_move(board, [king_row, king_column], [king_row + 1, king_column + 1]):
            if player_in_check(test_board, bottom_turn, king_row + 1, king_column + 1) == False:
                return False
    except: pass
    try:
        if is_valid_move(board, [king_row, king_column], [king_row + 1, king_column - 1]):
            if player_in_check(test_board, bottom_turn, king_row + 1, king_column - 1) == False:
                return False
    except: pass
    # checks to see if more than one piece is threating the king 
    test_board.rows = copy.deepcopy(board.rows)
    # removes first threating piece found 
    piece_row, piece_column = player_in_check(board, bottom_turn, king_row, king_column)
    test_board.rows[piece_row][piece_column] = 'x' 
    if player_in_check(test_board, bottom_turn, king_row, king_column) != False:
        return True
    else:
        threat_points = []
        # charts all points in between threating piece and king
        # since kings and pawns only can take pieces next to them and knights can jump over other pieces 
        # the only pieces that need to have to points in between them and the king are queens, bishops, and rooks
        piece_type = board.rows[piece_row][piece_column][-1]
        if piece_type == 'R':
            if piece_column == king_column:
                if piece_row < king_row:
                    for i in range(piece_row, king_row):
                        threat_points.append([i, piece_column])
                elif king_row < piece_row:
                    for i in range(king_row + 1, piece_row + 1):
                        threat_points.append([i, piece_column])
            elif piece_row == king_row:
                if piece_column < king_column:
                    for i in range(piece_column, king_column):
                        threat_points.append([king_row, i])
                elif king_column < piece_column:
                    for i in range(king_column + 1, piece_column + 1):
                        threat_points.append([king_row, i])
        elif piece_type == 'B':
            if piece_row < king_row:
                if piece_column < king_column:
                    for i in range(1, abs(king_row - piece_row)):
                        threat_points.append([piece_row + i, piece_column + i])
                elif king_column < piece_column:
                    for i in range(1, abs(king_row - piece_row)):
                        threat_points.append([piece_row + i, piece_column - i])
            elif king_row < piece_row:
                if piece_column < king_column:
                    for i in range(1, abs(king_row - piece_row)):
                        threat_points.append([piece_row - i, piece_column + i])
                elif king_column < piece_column:
                    for i in range(1, abs(king_row - piece_row)):
                        threat_points.append([piece_row - i, piece_column - i])
        elif piece_type == 'Q':
            if abs((piece_row - king_row) // (piece_column - king_column)) == 1:
                if piece_row < king_row:
                    if piece_column < king_column:
                        for i in range(1, abs(king_row - piece_row)):
                            threat_points.append([piece_row + i, piece_column + i])
                    elif king_column < piece_column:
                        for i in range(1, abs(king_row - piece_row)):
                            threat_points.append([piece_row + i, piece_column - i])
                elif king_row < piece_row:
                    if piece_column < king_column:
                        for i in range(1, abs(king_row - piece_row)):
                            threat_points.append([piece_row - i, piece_column + i])
                    elif king_column < piece_column:
                        for i in range(1, abs(king_row - piece_row)):
                            threat_points.append([piece_row - i, piece_column - i])
            else:
                if piece_column == king_column:
                    if piece_row < king_row:
                        for i in range(piece_row, king_row):
                            threat_points.append([i, piece_column])
                    elif king_row < piece_row:
                        for i in range(king_row + 1, piece_row + 1):
                            threat_points.append([i, piece_column])
                elif piece_row == king_row:
                    if piece_column < king_column:
                        for i in range(piece_column, king_column):
                            threat_points.append([king_row, i])
                    elif king_column < piece_column:
                        for i in range(king_column + 1, piece_column + 1):
                            threat_points.append([king_row, i])
        else:
            threat_points.append([piece_row, piece_column])
        # finds all pieces belonging to player that is in check
        player_pieces = []
        for row in range(len(board.rows)):
            for column in range(len(board.rows[row])):
                if board.rows[row][column][0] == player and board.rows[row][column][-1] != 'K':
                    player_pieces.append([row, column])
        # checks to see if any player controlled pieces could make a move to remove the king from check
        for piece in player_pieces:
            for point in threat_points:
                if is_valid_move(board, piece, point):
                    return False
        return True

def castle_king(board, bottom_turn, king_row, king_column):
    if bottom_turn:
        if king_row == 7 and king_column == 4:
            if board.rows[7][5] == 'x' and board.rows[7][6] == 'x':
                if board.rows[7][7] == 'bR':
                    u_input = input_process(input("You can castle your king, do you want to? (yes/no) : "))
                    if u_input == 'yes':
                        move_piece(board, ['h', 7], ['h', 5])
                        board.rows[7][4] = 'x' 
                        board.rows[7][6] = 'bK'
                        return True
    else:
        if king_row == 0 and king_column == 4:
            if board.rows[0][5] == 'x' and board.rows[0][6] == 'x':
                if board.rows[0][7] == 'tR':
                    u_input = input_process(input("You can castle your king, do you want to? (yes/no) : "))
                    if u_input == 'yes':
                        move_piece(board, ['a', 7], ['a', 5])
                        board.rows[0][4] = 'x'
                        board.rows[0][6] = 'tK'
                        return True
    return False

def main():
    first_run = True
    bottom_turn = True
    in_checkmate = False
    in_check = False
    conceded = False
    
    """ 
    top = t
    bottom = b
    king = K
    queen = Q 
    bishop = B 
    knight = N
    rook = R
    pawn = P """
    # rows board is set to on game start
    default_rows = [ ['tR', 'x', 'x', 'x', 'x', 'tR', 'tK', 'x'],
                     ['tP', 'tP', 'x', 'x', 'tP', 'tP', 'tB', 'tP'],
                     ['x', 'x', 'tN', 'tP', 'x', 'tN', 'tP', 'x'],
                     ['tQ', 'x', 'x', 'x', 'x', 'x', 'x', 'x'],
                     ['x', 'x', 'bP', 'bN', 'bP', 'x', 'x', 'x'],
                     ['x', 'bP', 'bN', 'x', 'x', 'bP', 'x', 'x'],
                     ['bP', 'bB', 'x', 'x', 'x', 'x', 'bP', 'bP'],
                     ['bR', 'x', 'x', 'bQ', 'x', 'bR', 'bK', 'x'] ]

    sys.stdout.write("\x1b[8;40;120t")
    print("WELCOME!\n")
    time.sleep(1)
    
    while True:
        # board
        class Game_Board:
            """This class represents the board for the current game, everything references this. Rows 
            is the current board represented using a list holding 8 nested lists, each nested list contains
             8 items, positions on the board. The two lists for the dead pieces simply hold an integer representing 
            how many of each respective piece for the sides are dead. The pieces are in the order: Q B N R P"""
            rows = default_rows
            top_dead = [0, 0, 0, 0, 0]
            bottom_dead = [0, 0, 0, 0, 0]

        while True:
            menu = input_process(input("Enter 'play' to play a game or 'quit' to exit the game. "))
            if menu == 'quit' or menu == 'play':
                break
        if menu == 'quit':
            break

        while True:
            if first_run:
                print("\nSuffix key:\nking = K\nqueen = Q\nbishop = B\nknight = N\nrook = R\npawn = P")
                print("The bottom player's pieces have a lowercase b as a prefix\n")
                print("The top player's pieces have a lowercase t as a prefix\n")
                print("To play pick a piece on the board with a lettered row and a numbered column such as (A0)\n")
                time.sleep(3)
                u_input = input("When you are done reading hit enter.")
                first_run = False

            print('\n\n\n')
            print_board(Game_Board)

            king_row, king_column = king_position(Game_Board, bottom_turn)

            castled = castle_king(Game_Board, bottom_turn, king_row, king_column)
            if castled:
                print_board(Game_Board)
                bottom_turn = not bottom_turn
                continue

            piece_exchanged = exchange_piece(Game_Board, bottom_turn)
            if piece_exchanged:
                print_board(Game_Board)

            if player_in_check(Game_Board, bottom_turn, king_row, king_column) != False:
                if player_in_checkmate(Game_Board, bottom_turn, king_row, king_column):
                    in_checkmate = True
                    break
                else:
                    print("You are in check!")

            valid_piece = False
            while not valid_piece:
                print("If you want to concede enter 'concede'\n")
                if bottom_turn:
                    piece = input_process(input("Bottom Player >>> "))
                else:
                    piece = input_process(input("Top Player >>> "))
                if piece == 'quit' or 'concede':
                    break
                valid_piece = is_valid_piece(Game_Board, bottom_turn, piece)
            if piece == 'quit':
                break
            if piece == 'concede':
                conceded = True

            valid_move = False
            while not valid_move:
                print("\nIf you want to move a different piece enter 'CP'\n")
                move_to = input_process(input("Where do you want to move this piece? >>> "))
                if move_to == 'quit':
                    break
                if move_to == 'cp':
                    valid_piece = False
                    while not valid_piece:
                        if bottom_turn:
                            piece = input_process(input("select a new piece >>> "))
                        else:
                            piece = input_process(input("select a new piece >>> "))
                        if piece == 'quit':
                            break
                        valid_piece = is_valid_piece(Game_Board, bottom_turn, piece)
                        if piece == 'quit':
                            break
                elif is_valid_move(Game_Board, piece, move_to):
                    class test_board:
                        rows = copy.deepcopy(Game_Board.rows)
                        bottom_dead = copy.deepcopy(Game_Board.bottom_dead)
                        top_dead = copy.deepcopy(Game_Board.top_dead)
                    move_piece(test_board, piece, move_to)
                    test_king_row, test_king_column = king_position(test_board, bottom_turn)
                    if player_in_check(test_board, bottom_turn, test_king_row, test_king_column) == False:
                        valid_move = True 
                elif not valid_move:
                    print("\nThat is not a valid move!\n")
            if move_to == "quit":
                break  
            elif valid_move:
                move_piece(Game_Board, piece, move_to) 

            bottom_turn = not bottom_turn

        if in_checkmate:
            if bottom_turn:
                print("The top player has won! Congrats.")
            else:
                print("The bottom player has won! Congrats.")

        if conceded:
            if bottom_turn:
                print("The bottom player has conceded the game.")
            else:
                print("The top player has conceded the game.")

if __name__ == "__main__":
    main()