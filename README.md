# 🧩 Sudoku SaaS - Par Frédéric Salerno

Sudoku SaaS est une application web responsive permettant de jouer au Sudoku avec différentes tailles de grille (4x4, 9x9, 16x16, 25x25) et niveaux de difficulté. Elle est optimisée pour **mobile et desktop** avec un rendu HTML/CSS dynamique et des interactions en JavaScript.

🔗 **Application en ligne** : [https://sudoku-ete.onrender.com](https://sudoku-ete.onrender.com)

## 🚀 Fonctionnalités principales

- ✅ Génération aléatoire de grilles Sudoku
- 🧠 Vérification de la solution
- 🔍 Détection si la grille est remplie
- 🖨️ Impression de la grille ou de la solution
- 🔄 Nouvelle partie rapide
- 🎯 Adaptation automatique à l'appareil (mobile ou desktop)

## 🛠️ Technologies utilisées

- Python 3 + Flask
- HTML5 + CSS3 (avec Bootstrap 5)
- JavaScript (DOM manipulation, fetch API)
- Jinja2 (template Flask)
- ThreadPoolExecutor (pour le solveur)

## 📁 Structure du projet

```
sudoku_saas/
├── app/
│   ├── __init__.py
│   ├── routes.py          # Logique de routing Flask
│   ├── sudoku.py          # Génération, vérification et résolution des grilles
│   └── templates/
│       ├── index_mobile.html
│       ├── index_desktop.html
│       ├── game_mobile.html
│       └── game_desktop.html
├── static/                # favicon, style perso, etc.
├── run.py                 # Lancement du serveur Flask
├── requirements.txt       # Dépendances Python
└── README.md              # Ce fichier
```

## ⚙️ Installation locale

1. Cloner ce dépôt :

```bash
git clone https://github.com/votre-repo/sudoku_saas.git
cd sudoku_saas
```

2. Créer un environnement virtuel :

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate    # Windows
```

3. Installer les dépendances :

```bash
pip install -r requirements.txt
```

4. Lancer l'application :

```bash
python run.py
```

Accéder à l'application sur : [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 🌐 Déploiement

Cette application est hébergée sur **Render** :  
🔗 [https://sudoku-ete.onrender.com](https://sudoku-ete.onrender.com)

> 💡 Tu peux aussi la déployer sur : Heroku, Railway, Docker, ou via Nginx + Gunicorn.

## 📌 Auteur

© 2025 [Frédéric SALERNO](mailto:fred.salerno.dev@gmail.com)  
Tous droits réservés.
