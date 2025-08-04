
import random
import copy

def generate_sudoku(difficulty="easy", size=9):
    if size not in [4, 9, 16]:
        size = 9
    base = int(size ** 0.5)

    def pattern(r, c): return (base*(r % base)+r//base+c) % size
    def shuffle(s): return random.sample(s, len(s))
    rBase = range(base)
    rows = [g*base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g*base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, size + 1))

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    squares = size * size
    empties = {
        "easy": int(squares * 0.4),
        "medium": int(squares * 0.5),
        "hard": int(squares * 0.6),
        "expert": int(squares * 0.65),
        "extreme": int(squares * 0.7)
    }.get(difficulty, int(squares * 0.5))

    for p in random.sample(range(squares), empties):
        board[p//size][p % size] = 0

    return board

def solve_sudoku(board):
    size = len(board)
    def is_valid(num, row, col):
        block_size = int(size ** 0.5)
        for i in range(size):
            if board[row][i] == num or board[i][col] == num:
                return False
        start_row, start_col = block_size * (row // block_size), block_size * (col // block_size)
        for i in range(start_row, start_row + block_size):
            for j in range(start_col, start_col + block_size):
                if board[i][j] == num:
                    return False
        return True

    for row in range(size):
        for col in range(size):
            if board[row][col] == 0:
                for num in range(1, size + 1):
                    if is_valid(num, row, col):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def check_solution(user_grid, original_grid):
    solved_grid = copy.deepcopy(original_grid)
    solve_sudoku(solved_grid)
    return user_grid == solved_grid
