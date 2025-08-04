
from flask import render_template, request, session, jsonify
from app import app
from app.sudoku import generate_sudoku, solve_sudoku, check_solution
import copy

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/play", methods=["POST"])
def play():
    difficulty = request.form.get("difficulty", "easy")
    size = int(request.form.get("size", 9))
    grid = generate_sudoku(difficulty, size)
    session["original_grid"] = [row[:] for row in grid]
    return render_template("game.html", grid=grid, difficulty=difficulty)

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
    solved = copy.deepcopy(original)
    solve_sudoku(solved)
    return jsonify({"solution": solved})
