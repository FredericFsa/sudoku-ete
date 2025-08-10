from flask import render_template, request, session, jsonify
from app import app
from app.sudoku import generate_sudoku, solve_sudoku, check_solution, to_symbol
import copy
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import atexit

# ✅ IMPORT DU MODULE D'IMPRESSION
from app.print_styles import print_empty_sudoku, print_solved_sudoku

# ✅ ThreadPoolExecutor pour exécuter le solveur sans bloquer Flask
executor = ThreadPoolExecutor(max_workers=2)

@app.route("/")
def index():
    user_agent = request.headers.get("User-Agent", "").lower()
    is_mobile = any(device in user_agent for device in ["iphone", "android", "ipad", "mobile"])
    template = "index_mobile.html" if is_mobile else "index_desktop.html"
    return render_template(template)

@app.route("/start", methods=["POST"])
def start_game():
    difficulty = request.form.get("difficulty", "easy")
    try:
        size = int(request.form.get("size", 9))
    except ValueError:
        size = 9

    if size not in [4, 9, 16, 25]:
        size = 9  # Sécurité

    # ✅ CORRECTION : Limiter les difficultés pour le 25x25 ET 16x16
    if size == 25 and difficulty not in ["easy", "medium"]:
        difficulty = "medium"  # Forcer au maximum "moyen" pour 25x25
    elif size == 16 and difficulty not in ["easy", "medium", "hard"]:
        difficulty = "hard"    # Forcer au maximum "difficile" pour 16x16

    grid = generate_sudoku(difficulty, size)
    session["original_grid"] = copy.deepcopy(grid)
    session["difficulty"] = difficulty  # ✅ NOUVEAU : Stocker la difficulté
    session["size"] = size  # ✅ NOUVEAU : Stocker la taille

    user_agent = request.headers.get("User-Agent", "").lower()
    is_mobile = any(device in user_agent for device in ["iphone", "android", "ipad", "mobile"])
    template = "game_mobile.html" if is_mobile else "game_desktop.html"

    return render_template(template, grid=grid, difficulty=difficulty, size=size, to_symbol=to_symbol)

@app.route("/check", methods=["POST"])
def check():
    data = request.json
    user_grid = data.get("grid", [])
    original_grid = session.get("original_grid", [])

    if not user_grid or not original_grid:
        return jsonify({"result": "error", "message": "Données manquantes"}), 400

    is_correct = check_solution(user_grid, original_grid)
    return jsonify({"result": "ok", "correct": is_correct})

@app.route("/solution", methods=["GET"])
def solution():
    original = session.get("original_grid", [])
    if not original:
        return jsonify({"error": "Grille non trouvée"}), 400

    solved = copy.deepcopy(original)

    # 🔁 Résolution en tâche de fond avec timeout adaptatif
    size = len(solved)
    timeout = 10 if size <= 9 else (60 if size <= 16 else 120)  # Timeout adaptatif
    
    future = executor.submit(solve_sudoku, solved)

    try:
        success = future.result(timeout=timeout)
        if not success:
            return jsonify({"error": "Grille non résoluble"}), 400
    except TimeoutError:
        return jsonify({"error": f"⏱️ Résolution trop longue (>{timeout}s)"}), 504

    return jsonify({"solution": solved})

# ===== NOUVELLES ROUTES POUR LE MODULE D'IMPRESSION =====

@app.route("/print-css/<int:size>/<difficulty>")
def get_print_css_route(size, difficulty):
    """Retourne le CSS d'impression dynamique pour une taille/difficulté"""
    css = generate_print_css(size, difficulty)
    return css, 200, {'Content-Type': 'text/css'}

@app.route("/print-solution", methods=["POST"])
def print_solution():
    """Génère le HTML d'impression pour une solution"""
    data = request.json
    grid = data.get("grid", [])
    size = data.get("size", 9)
    difficulty = data.get("difficulty", "medium")
    
    if not grid:
        return jsonify({"error": "Grille manquante"}), 400
    
    html = generate_solution_html(grid, size, difficulty)
    return html, 200, {'Content-Type': 'text/html'}

@app.route("/print-empty")
def print_empty_grid():
    """Retourne une page prête pour imprimer la grille vide"""
    # Récupérer les données depuis la session
    original_grid = session.get("original_grid", [])
    difficulty = session.get("difficulty", "medium")
    size = session.get("size", 9)
    
    if not original_grid:
        return "Erreur: Aucune grille en cours", 400
    
    # Générer le CSS d'impression
    css = generate_print_css(size, difficulty)
    
    # Générer le HTML de la grille
    block_size = int(size ** 0.5)
    table_html = ""
    
    for r in range(size):
        table_html += "<tr>"
        for c in range(size):
            val = original_grid[r][c]
            
            # Classes pour bordures de blocs
            classes = []
            if r % block_size == 0:
                classes.append('top-block')
            if c % block_size == 0:
                classes.append('left-block') 
            if r == size - 1:
                classes.append('bottom-block')
            if c == size - 1:
                classes.append('right-block')
            
            class_attr = f'class="{" ".join(classes)}"' if classes else ""
            
            if val == 0:
                table_html += f'<td {class_attr}><input type="text" maxlength="1"></td>'
            else:
                symbol = str(val) if val <= 9 else chr(55 + val)
                table_html += f'<td {class_attr}><span class="fixed">{symbol}</span></td>'
        
        table_html += "</tr>"
    
    # HTML complet avec CSS intégré
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Grille Sudoku {size}x{size} - {difficulty.capitalize()}</title>
      <style>{css}</style>
    </head>
    <body>
      <div class="game-frame">
        <div class="sudoku-wrapper">
          <table>
            {table_html}
          </table>
        </div>
      </div>
      <script>
        window.onload = function() {{ 
          window.print(); 
          window.onafterprint = function() {{
            window.close();
          }};
        }};
      </script>
    </body>
    </html>
    """
    
    return html

@app.route("/print-config/<int:size>")
def get_print_config_route(size):
    """API pour récupérer la configuration d'impression d'une taille"""
    config = get_print_config(size)
    return jsonify(config)

@app.route("/print-test/<int:size>/<difficulty>")
def print_test(size, difficulty):
    """Route de test pour vérifier le rendu d'impression"""
    css = generate_print_css(size, difficulty)
    config = get_print_config(size)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <title>Test impression {size}x{size}</title>
      <style>{css}</style>
    </head>
    <body>
      <h2>Test d'impression Sudoku {size}x{size} - {difficulty}</h2>
      <div class="game-frame">
        <div class="sudoku-wrapper">
          <table>
            <tr><td>Test</td><td class="top-block">Cell</td></tr>
            <tr><td class="left-block">Test</td><td>Cell</td></tr>
          </table>
        </div>
      </div>
      <h3>Configuration:</h3>
      <pre>{config}</pre>
    </body>
    </html>
    """
    return html

# ✅ Fermeture propre du ThreadPoolExecutor à l'arrêt du serveur
@atexit.register
def shutdown_executor():
    executor.shutdown(wait=False)
    
@app.route("/perfect-print-empty")
def perfect_print_empty():
    grid = session.get("original_grid", [])
    size = session.get("size", 9)  
    difficulty = session.get("difficulty", "medium")
    
    html = print_empty_sudoku(grid, size, difficulty)
    return html

@app.route("/perfect-print-solution", methods=["POST"])  
def perfect_print_solution():
    data = request.json
    html = print_solved_sudoku(data["grid"], data["size"], data["difficulty"])
    return html
    


@app.route("/pretty")
def pretty():
    return render_template("sudoku_grids_centered_print_random_fill_fixed.html")
