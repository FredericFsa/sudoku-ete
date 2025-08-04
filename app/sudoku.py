import random
import copy

def generate_sudoku(difficulty="easy", size=9):
    if size not in [4, 9, 16, 25]:
        size = 9

    base = int(size ** 0.5)
    if base * base != size:
        raise ValueError("La taille doit être un carré parfait (ex: 4, 9, 16, 25)")

    def pattern(r, c): return (base * (r % base) + r // base + c) % size
    def shuffle(s): return random.sample(s, len(s))

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
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
        board[p // size][p % size] = 0

    return board

# ✅ Méthode 1 — classique backtracking (rapide pour 4x4 ou 9x9 faciles)
def solve_sudoku_classic(board):
    size = len(board)
    block = int(size ** 0.5)

    def is_valid(n, row, col):
        for i in range(size):
            if board[row][i] == n or board[i][col] == n:
                return False
        r0, c0 = row - row % block, col - col % block
        for r in range(r0, r0 + block):
            for c in range(c0, c0 + block):
                if board[r][c] == n:
                    return False
        return True

    for row in range(size):
        for col in range(size):
            if board[row][col] == 0:
                for n in range(1, size + 1):
                    if is_valid(n, row, col):
                        board[row][col] = n
                        if solve_sudoku_classic(board):
                            return True
                        board[row][col] = 0
                return False
    return True

# ✅ Méthode 2 — MRV + forward checking (optimisé grandes grilles)
def solve_sudoku_advanced(board):
    size = len(board)
    block_size = int(size ** 0.5)

    rows = [set() for _ in range(size)]
    cols = [set() for _ in range(size)]
    blocks = [[set() for _ in range(block_size)] for _ in range(block_size)]
    empty_cells = []

    for r in range(size):
        for c in range(size):
            val = board[r][c]
            if val != 0:
                rows[r].add(val)
                cols[c].add(val)
                blocks[r // block_size][c // block_size].add(val)
            else:
                empty_cells.append((r, c))

    def sort_by_constraints():
        def count_used(cell):
            r, c = cell
            return len(rows[r] | cols[c] | blocks[r // block_size][c // block_size])
        empty_cells.sort(key=count_used)

    def backtrack(index):
        if index == len(empty_cells):
            return True

        r, c = empty_cells[index]
        used = rows[r] | cols[c] | blocks[r // block_size][c // block_size]
        for num in range(1, size + 1):
            if num not in used:
                board[r][c] = num
                rows[r].add(num)
                cols[c].add(num)
                blocks[r // block_size][c // block_size].add(num)

                if backtrack(index + 1):
                    return True

                board[r][c] = 0
                rows[r].remove(num)
                cols[c].remove(num)
                blocks[r // block_size][c // block_size].remove(num)
        return False

    sort_by_constraints()
    return backtrack(0)

# ✅ Sélection automatique selon la taille
def solve_sudoku(board):
    size = len(board)
    if size <= 9:
        return solve_sudoku_classic(board)
    else:
        return solve_sudoku_advanced(board)

def check_solution(user_grid, original_grid):
    solved_grid = copy.deepcopy(original_grid)
    return solve_sudoku(solved_grid) and user_grid == solved_grid

def to_symbol(n):
    return str(n) if n <= 9 else chr(ord('A') + n - 10)
