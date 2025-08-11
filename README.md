![Render Live](https://img.shields.io/badge/Render-Live-brightgreen?logo=render&style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.11-blue?logo=python&style=for-the-badge)
![Flask](https://img.shields.io/badge/Flask-3.1.1-lightgrey?logo=flask&style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
[![GitHub stars](https://img.shields.io/github/stars/FredericFsa/sudoku-ete?style=for-the-badge)](https://github.com/FredericFsa/sudoku-ete/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/FredericFsa/sudoku-ete?style=for-the-badge)](https://github.com/FredericFsa/sudoku-ete/issues)


# 🧩 Sudoku Été

**Sudoku Été** est une application web interactive permettant de jouer à des grilles de Sudoku de différentes tailles (4×4, 9×9, 16×16 et 25×25), avec plusieurs niveaux de difficulté.  
Le jeu est accessible depuis tous les appareils (PC, tablette, mobile) et intègre des fonctionnalités avancées comme la vérification, l'affichage de la solution, l'effacement rapide et l'impression optimisée.

---

## 🌐 Démo en ligne
Application disponible ici : **https://sudoku-ete.onrender.com/**

---

## ✨ Fonctionnalités

- 🎯 **Choix de la taille et de la difficulté** dès l'accueil (restrictions adaptées pour 16×16 et 25×25).
- 📱 **Interface responsive** optimisée pour desktop et mobile (titres/boutons fixes, zone de jeu scrollable).
- ✅ **Vérification** de la grille (côté serveur), avec **fallback local**.
- 🔍 **Contrôle rapide** si la grille est entièrement remplie.
- 🧠 **Affichage de la solution** sur demande (résolution en tâche de fond, timeout adaptatif).
- 🧹 **Effacement rapide** de toutes les entrées.
- 🖨 **Mode impression** : grille vide ou solution, avec styles HTML/CSS dédiés.
- 🎨 **Design estival** avec fond en dégradé doux.

---

## 📂 Structure du projet (suggestion)

```
app/
├── __init__.py                      # Initialisation Flask (clé secrète à mettre en variable d'env)
├── routes.py                        # Routes web & API (start, check, solution, print...)
├── sudoku.py                        # Génération & résolution (solveur optimisé pour 9×9/16×16/25×25)
├── print_styles.py                  # Pages HTML/CSS d'impression (grille/solution)
├── run.py                           # Point d'entrée (logs propres, arrêt propre)
│
├── templates/
│   ├── index_desktop.html           # Accueil desktop
│   ├── index_mobile.html            # Accueil mobile
│   ├── game_desktop.html            # Jeu desktop (frame commandes + frame grille)
│   ├── game_mobile.html             # Jeu mobile (grille CSS Grid)
│   └── sudoku_grids_centered_print_random_fill_fixed.html  # Impression “jolie” via prettyGrid
│
├── static/
│   └── sudoku_game_js.js            # Logique front-end (navigation, vérifs, impression)
│
├── requirements.txt                 # Dépendances Python
└── render.yaml                      # Configuration Render.com
```

> ℹ️ Selon ton repo actuel, les fichiers peuvent être à la racine. La structure ci‑dessus correspond à l’organisation recommandée.

---

## ⚙️ Installation locale

### 1) Cloner le dépôt
```bash
git clone https://github.com/<ton-utilisateur>/<ton-repo>.git
cd <ton-repo>
```

### 2) Environnement virtuel
```bash
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3) Dépendances
```bash
pip install -r requirements.txt
```

### 4) Variables d’environnement (recommandé)
```bash
# à adapter à ton shell
export FLASK_ENV=production
export SECRET_KEY="change-me"
```

### 5) Lancer en dev
```bash
python run.py
```
Application disponible sur **http://127.0.0.1:5000**.

### 6) Lancer en prod (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

---

## 🚀 Déploiement sur Render

Le projet inclut `render.yaml`. Pour déployer :  
1. Crée un service **Web Service** sur [Render](https://render.com/).  
2. Connecte ton dépôt GitHub.  
3. Render installe les dépendances via `requirements.txt` et lance la commande définie (ex. `gunicorn run:app`).  
4. Configure les variables **SECRET_KEY** et **FLASK_ENV** dans l’onglet *Environment*.  

👉 Démonstration déployée : **https://sudoku-ete.onrender.com/**

---

## 🧪 Endpoints principaux

- `GET /` – accueil (détection mobile/desktop).  
- `POST /start` – génère une grille selon taille/difficulté.  
- `POST /check` – vérifie une grille soumise.  
- `GET /solution` – calcule/renvoie la solution (timeout adaptatif).  
- `GET /perfect-print-empty` – page d’impression de la **grille**.  
- `POST /perfect-print-solution` – page d’impression de la **solution**.  

---

## 🔐 Sécurité & bonnes pratiques

- **SECRET_KEY** : ne pas laisser en dur dans `__init__.py`; utiliser une variable d’environnement.  
- **Validation** : revalider serveur toutes les entrées (taille, contenu de grille).  
- **CSRF** : si tu ajoutes des formulaires POST supplémentaires, penser à activer une protection CSRF (Flask‑WTF).

---

## 🖼 Captures d’écran (optionnel)

Place des images dans `docs/` puis référence-les :  
```markdown
![Accueil](docs/sudoku_home.png)
![Partie](docs/sudoku_game.png)
```

---

## 📄 Licence

© 2025 Frédéric SALERNO. Tous droits réservés.
