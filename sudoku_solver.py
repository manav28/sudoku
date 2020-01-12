from math import sqrt
import itertools

def find_empty_box(board):
    for i in range(len(board[0])):
        for j in range(len(board)):
            if board[i][j] == 0:
                return (i, j)
    return None

def is_valid(board, num, pos):
    row, col = pos

    for j in range(len(board[0])):
        if board[row][j] == num and col != j:
            return False
    
    for i in range(len(board)):
        if board[i][col] == num and row != i:
            return False
    
    region_size = int(sqrt(len(board)))
    grid_x = row // region_size
    grid_y = col // region_size

    for i, j in itertools.product(range(region_size), repeat=2):
        cell_x = (grid_x * region_size) + i
        cell_y = (grid_y * region_size) + j
        if board[cell_x][cell_y] == num and (cell_x, cell_y) != pos:
            return False
    
    return True

def solve(board):
    find = find_empty_box(board)
    if not find:
        return True
    else:
        row, col = find
    
    for num in range(1, len(board) + 1):
        if is_valid(board, num, (row, col)):
            board[row][col] = num
            
            if solve(board):
                return True
            
            board[row][col] = 0

    return False