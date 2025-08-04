from flask import render_template, request, session, jsonify
from app import app
from app.sudoku import generate_sudoku, solve_sudoku, check_solution, to_symbol
import copy
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import atexit




# ✅ ThreadPoolExecutor pour exécuter le solveur sans bloquer Flask
executor = ThreadPoolExecutor(max_workers=2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/play", methods=["POST"])
def play():
    difficulty = request.form.get("difficulty", "easy")
    try:
        size = int(request.form.get("size", 9))
    except ValueError:
        size = 9
    if size not in [4, 9, 16, 25]:
        size = 9  # Sécurité

    grid = generate_sudoku(difficulty, size)
    session["original_grid"] = copy.deepcopy(grid)
    return render_template("game.html", grid=grid, difficulty=difficulty, to_symbol=to_symbol)

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

    # 🔁 Résolution en tâche de fond
    future = executor.submit(solve_sudoku, solved)

    try:
        success = future.result(timeout=600)  # Timeout max en secondes
        if not success:
            return jsonify({"error": "Grille non résoluble"}), 400
    except TimeoutError:
        return jsonify({"error": "⏱️ Résolution trop longue"}), 504

    return jsonify({"solution": solved})

# Fermeture propre du ThreadPoolExecutor à l’arrêt du serveur
@atexit.register
def shutdown_executor():
    print("⏹️ Fermeture propre des threads...")
    executor.shutdown(wait=False)