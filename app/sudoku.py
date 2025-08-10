import random
import copy
from typing import List, Set, Tuple, Optional
import time
import logging

# ✅ Configuration du logging pour sortie propre
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

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

    # ✅ CORRECTION : Ratios de difficulté adaptés selon la taille
    squares = size * size
    
    if size >= 25:
        # ✅ Pour 25x25 : SEULEMENT Facile et Moyen
        empties = {
            "easy": int(squares * 0.35),      # 35% - Facile
            "medium": int(squares * 0.42),    # 42% - Moyen
            # Plus de niveaux difficiles pour 25x25
        }.get(difficulty, int(squares * 0.35))  # Par défaut : facile
    elif size >= 16:
        # ✅ Pour 16x16 : SEULEMENT Facile, Moyen, Difficile
        empties = {
            "easy": int(squares * 0.38),      # 38% - Facile
            "medium": int(squares * 0.45),    # 45% - Moyen  
            "hard": int(squares * 0.50),      # 50% - Difficile
            # Plus de niveaux expert/extreme pour 16x16
        }.get(difficulty, int(squares * 0.38))  # Par défaut : facile
    else:
        # Pour 4x4 et 9x9 : ratios originaux
        empties = {
            "easy": int(squares * 0.4),
            "medium": int(squares * 0.5),
            "hard": int(squares * 0.6),
            "expert": int(squares * 0.65),
            "extreme": int(squares * 0.7)
        }.get(difficulty, int(squares * 0.5))

    # ✅ Génération intelligente pour éviter les grilles impossibles
    max_attempts = 50
    for attempt in range(max_attempts):
        # Créer une copie pour tester
        test_board = copy.deepcopy(board)
        
        # Retirer les cases de façon plus intelligente pour grandes grilles
        if size >= 16:
            # Pour grandes grilles : retrait par bloc pour maintenir la solvabilité
            cells_to_remove = []
            
            # Répartir équitablement dans chaque bloc
            cells_per_block = empties // (base * base)
            remaining = empties % (base * base)
            
            for block_r in range(base):
                for block_c in range(base):
                    block_cells = []
                    for r in range(block_r * base, (block_r + 1) * base):
                        for c in range(block_c * base, (block_c + 1) * base):
                            block_cells.append(r * size + c)
                    
                    # Ajouter les cellules de ce bloc
                    to_remove = cells_per_block + (1 if remaining > 0 else 0)
                    if remaining > 0:
                        remaining -= 1
                    
                    cells_to_remove.extend(random.sample(block_cells, min(to_remove, len(block_cells))))
            
            # Retirer les cases sélectionnées
            for p in cells_to_remove:
                test_board[p // size][p % size] = 0
        else:
            # Pour petites grilles : méthode originale
            for p in random.sample(range(squares), empties):
                test_board[p // size][p % size] = 0
        
        # ✅ Vérifier que la grille est solvable
        verification_board = copy.deepcopy(test_board)
        if solve_sudoku_verification(verification_board):
            logger.info(f"✅ Grille {size}x{size} {difficulty} générée (tentative {attempt + 1})")
            return test_board
        else:
            logger.info(f"❌ Grille impossible, nouvelle tentative ({attempt + 1}/{max_attempts})")
    
    # Si aucune grille valide trouvée, générer une grille plus facile
    logger.warning(f"⚠️ Génération difficile en mode {difficulty}, passage en mode facile")
    fallback_empties = int(squares * (0.35 if size >= 25 else 0.4))
    for p in random.sample(range(squares), fallback_empties):
        board[p // size][p % size] = 0
    
    return board

def solve_sudoku_verification(board):
    """Version rapide du solveur juste pour vérifier la solvabilité"""
    size = len(board)
    
    if size <= 9:
        return solve_sudoku_classic_fast_check(board)
    else:
        # Pour les grandes grilles, utiliser un timeout plus court
        solver = UltraSudokuSolver(board)
        return solver.solve_with_timeout(15)  # 15 secondes max pour vérification

class UltraSudokuSolver:
    """Solveur Sudoku ultra-optimisé spécial 25x25"""
    
    def __init__(self, board: List[List[int]]):
        self.size = len(board)
        self.block_size = int(self.size ** 0.5)
        self.board = board  # ✅ RÉFÉRENCE DIRECTE
        
        # ✅ Structures de données ultra-optimisées
        self.row_candidates = [set(range(1, self.size + 1)) for _ in range(self.size)]
        self.col_candidates = [set(range(1, self.size + 1)) for _ in range(self.size)]
        self.block_candidates = [[set(range(1, self.size + 1)) for _ in range(self.block_size)] 
                                for _ in range(self.block_size)]
        
        # Cache des cellules vides triées par difficulté
        self.empty_cells = []
        self.cell_candidates_cache = {}
        
        self._initialize_fast()
    
    def _initialize_fast(self):
        """Initialisation ultra-rapide avec précalcul"""
        # Phase 1: Retirer les nombres déjà placés des candidats
        for r in range(self.size):
            for c in range(self.size):
                val = self.board[r][c]
                if val != 0:
                    self.row_candidates[r].discard(val)
                    self.col_candidates[c].discard(val)
                    self.block_candidates[r // self.block_size][c // self.block_size].discard(val)
                else:
                    self.empty_cells.append((r, c))
        
        # Phase 2: Calculer et mettre en cache les candidats de chaque cellule vide
        for r, c in self.empty_cells:
            candidates = (self.row_candidates[r] & 
                         self.col_candidates[c] & 
                         self.block_candidates[r // self.block_size][c // self.block_size])
            self.cell_candidates_cache[(r, c)] = candidates
    
    def _update_constraints(self, r: int, c: int, num: int, remove: bool = True):
        """Met à jour les contraintes de façon ultra-efficace"""
        if remove:
            self.row_candidates[r].discard(num)
            self.col_candidates[c].discard(num)
            self.block_candidates[r // self.block_size][c // self.block_size].discard(num)
        else:
            self.row_candidates[r].add(num)
            self.col_candidates[c].add(num)
            self.block_candidates[r // self.block_size][c // self.block_size].add(num)
    
    def _get_candidates(self, r: int, c: int) -> Set[int]:
        """Récupération ultra-rapide des candidats"""
        return (self.row_candidates[r] & 
                self.col_candidates[c] & 
                self.block_candidates[r // self.block_size][c // self.block_size])
    
    def _solve_logical_techniques(self) -> bool:
        """Application des techniques logiques avancées"""
        progress = True
        iterations = 0
        max_iterations = self.size * 2  # Éviter les boucles infinies
        
        while progress and iterations < max_iterations:
            progress = False
            iterations += 1
            
            # Naked Singles (cellules avec un seul candidat)
            for r, c in self.empty_cells[:]:  # Copie pour modification sécurisée
                if self.board[r][c] == 0:
                    candidates = self._get_candidates(r, c)
                    if len(candidates) == 1:
                        num = next(iter(candidates))
                        self.board[r][c] = num
                        self.empty_cells.remove((r, c))
                        self._update_constraints(r, c, num)
                        progress = True
                    elif len(candidates) == 0:
                        return False  # Contradiction détectée
            
            # Hidden Singles (nombres qui ne peuvent aller qu'à une place)
            # Par ligne
            for r in range(self.size):
                for num in list(self.row_candidates[r]):
                    possible_cols = [c for c in range(self.size) 
                                   if self.board[r][c] == 0 and num in self._get_candidates(r, c)]
                    if len(possible_cols) == 1:
                        c = possible_cols[0]
                        self.board[r][c] = num
                        if (r, c) in self.empty_cells:
                            self.empty_cells.remove((r, c))
                        self._update_constraints(r, c, num)
                        progress = True
            
            # Par colonne
            for c in range(self.size):
                for num in list(self.col_candidates[c]):
                    possible_rows = [r for r in range(self.size) 
                                   if self.board[r][c] == 0 and num in self._get_candidates(r, c)]
                    if len(possible_rows) == 1:
                        r = possible_rows[0]
                        self.board[r][c] = num
                        if (r, c) in self.empty_cells:
                            self.empty_cells.remove((r, c))
                        self._update_constraints(r, c, num)
                        progress = True
            
            # Par bloc
            for block_r in range(self.block_size):
                for block_c in range(self.block_size):
                    for num in list(self.block_candidates[block_r][block_c]):
                        possible_positions = []
                        for r in range(block_r * self.block_size, (block_r + 1) * self.block_size):
                            for c in range(block_c * self.block_size, (block_c + 1) * self.block_size):
                                if self.board[r][c] == 0 and num in self._get_candidates(r, c):
                                    possible_positions.append((r, c))
                        
                        if len(possible_positions) == 1:
                            r, c = possible_positions[0]
                            self.board[r][c] = num
                            if (r, c) in self.empty_cells:
                                self.empty_cells.remove((r, c))
                            self._update_constraints(r, c, num)
                            progress = True
        
        return True
    
    def _backtrack_ultra_fast(self) -> bool:
        """Backtracking ultra-optimisé avec heuristiques avancées"""
        if not self.empty_cells:
            return True
        
        # MRV + Degree Heuristic : choisir la cellule la plus contrainte
        def cell_priority(pos):
            r, c = pos
            candidates = self._get_candidates(r, c)
            if not candidates:
                return (0, 0)  # Contradiction - priorité maximale
            # Moins de candidats = priorité plus haute, plus de contraintes voisines = priorité plus haute
            neighbor_constraints = len([1 for nr in range(self.size) if self.board[nr][c] == 0]) + \
                                 len([1 for nc in range(self.size) if self.board[r][nc] == 0])
            return (len(candidates), -neighbor_constraints)
        
        self.empty_cells.sort(key=cell_priority)
        r, c = self.empty_cells[0]
        
        candidates = self._get_candidates(r, c)
        if not candidates:
            return False  # Pas de solution possible
        
        # Sauvegarder l'état pour backtrack
        old_empty_cells = self.empty_cells[:]
        old_row_candidates = [s.copy() for s in self.row_candidates]
        old_col_candidates = [s.copy() for s in self.col_candidates]
        old_block_candidates = [[s.copy() for s in row] for row in self.block_candidates]
        
        for num in candidates:
            # Tenter ce nombre
            self.board[r][c] = num
            self.empty_cells.remove((r, c))
            self._update_constraints(r, c, num)
            
            # Appliquer les techniques logiques
            if self._solve_logical_techniques():
                if self._backtrack_ultra_fast():
                    return True
            
            # Backtrack complet
            self.board[r][c] = 0
            self.empty_cells = old_empty_cells[:]
            self.row_candidates = [s.copy() for s in old_row_candidates]
            self.col_candidates = [s.copy() for s in old_col_candidates]
            self.block_candidates = [[s.copy() for s in row] for row in old_block_candidates]
        
        return False
    
    def solve_with_timeout(self, timeout_seconds=15):
        """Version avec timeout pour la vérification"""
        start_time = time.time()
        
        # Phase 1: Techniques logiques avec timeout
        if not self._solve_logical_techniques():
            return False
        
        # Phase 2: Backtracking rapide avec timeout
        return self._backtrack_with_timeout(start_time, timeout_seconds)
    
    def _backtrack_with_timeout(self, start_time, timeout_seconds):
        """Backtracking avec timeout"""
        if time.time() - start_time > timeout_seconds:
            return False  # Timeout atteint
            
        if not self.empty_cells:
            return True
        
        # MRV simplifié pour plus de vitesse
        r, c = min(self.empty_cells, key=lambda pos: len(self._get_candidates(pos[0], pos[1])))
        candidates = self._get_candidates(r, c)
        
        if not candidates:
            return False
        
        self.empty_cells.remove((r, c))
        
        for num in list(candidates)[:3]:  # ✅ Limiter à 3 candidats max pour vitesse
            self.board[r][c] = num
            self._update_constraints(r, c, num)
            
            if self._backtrack_with_timeout(start_time, timeout_seconds):
                return True
            
            # Backtrack rapide
            self.board[r][c] = 0
            self._update_constraints(r, c, num, remove=False)
        
        self.empty_cells.append((r, c))
        return False
    
    def solve(self) -> bool:
        """Résolution complète ultra-optimisée"""
        start_time = time.time()
        
        # Phase 1: Techniques logiques pures
        if not self._solve_logical_techniques():
            logger.info("❌ Contradiction détectée - pas de solution")
            return False
        
        # Phase 2: Backtracking si nécessaire
        result = self._backtrack_ultra_fast()
        
        end_time = time.time()
        logger.info(f"🚀 Résolution {self.size}x{self.size} en {end_time - start_time:.2f}s")
        return result

def solve_sudoku_classic_fast_check(board):
    """Vérification rapide pour petites grilles (version allégée)"""
    size = len(board)
    block = int(size ** 0.5)
    empty_cells = [(r, c) for r in range(size) for c in range(size) if board[r][c] == 0]
    
    def is_valid(r, c, num):
        # Vérification ligne
        if num in board[r]:
            return False
        # Vérification colonne
        if num in [board[i][c] for i in range(size)]:
            return False
        # Vérification bloc
        br, bc = r // block * block, c // block * block
        for i in range(br, br + block):
            for j in range(bc, bc + block):
                if board[i][j] == num:
                    return False
        return True
    
    def solve_fast():
        if not empty_cells:
            return True
        
        r, c = empty_cells.pop(0)
        for num in range(1, size + 1):
            if is_valid(r, c, num):
                board[r][c] = num
                if solve_fast():
                    return True
                board[r][c] = 0
        
        empty_cells.insert(0, (r, c))
        return False
    
    return solve_fast()

def solve_sudoku_classic_optimized(board):
    """Version classique ultra-optimisée pour petites grilles"""
    size = len(board)
    block = int(size ** 0.5)
    
    # Précalcul des contraintes pour vitesse maximale
    row_sets = [set() for _ in range(size)]
    col_sets = [set() for _ in range(size)]
    block_sets = [[set() for _ in range(block)] for _ in range(block)]
    
    empty_cells = []
    
    # Initialisation
    for r in range(size):
        for c in range(size):
            val = board[r][c]
            if val != 0:
                row_sets[r].add(val)
                col_sets[c].add(val)
                block_sets[r // block][c // block].add(val)
            else:
                empty_cells.append((r, c))
    
    def get_candidates(r, c):
        used = row_sets[r] | col_sets[c] | block_sets[r // block][c // block]
        return [n for n in range(1, size + 1) if n not in used]
    
    def solve():
        if not empty_cells:
            return True
        
        # MRV : trouver la cellule avec le moins de candidats
        best_cell = min(empty_cells, key=lambda pos: len(get_candidates(pos[0], pos[1])))
        r, c = best_cell
        candidates = get_candidates(r, c)
        
        if not candidates:
            return False
        
        empty_cells.remove((r, c))
        
        for num in candidates:
            board[r][c] = num
            row_sets[r].add(num)
            col_sets[c].add(num)
            block_sets[r // block][c // block].add(num)
            
            if solve():
                return True
            
            # Backtrack
            board[r][c] = 0
            row_sets[r].remove(num)
            col_sets[c].remove(num)
            block_sets[r // block][c // block].remove(num)
        
        empty_cells.append((r, c))
        return False
    
    start_time = time.time()
    result = solve()
    end_time = time.time()
    logger.info(f"🚀 Résolution {size}x{size} en {end_time - start_time:.2f}s")
    return result

# ✅ Interface principale - PLUS DE MULTIPROCESSING
def solve_sudoku(board):
    """Solveur principal avec sélection automatique intelligente"""
    size = len(board)
    empty_count = sum(row.count(0) for row in board)
    
    # Log minimal et propre
    logger.info(f"🧩 Résolution {size}x{size} ({empty_count} cases)")
    
    # Sélection du solveur selon la taille
    if size <= 9:
        # Petites grilles : algorithme classique optimisé
        return solve_sudoku_classic_optimized(board)
    else:
        # Grandes grilles : solveur ultra-avancé
        solver = UltraSudokuSolver(board)
        return solver.solve()

def check_solution(user_grid, original_grid):
    solved_grid = copy.deepcopy(original_grid)
    return solve_sudoku(solved_grid) and user_grid == solved_grid

def to_symbol(n):
    return str(n) if n <= 9 else chr(ord('A') + n - 10)