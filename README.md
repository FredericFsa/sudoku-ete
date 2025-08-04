
# ☀️ Sudoku d'Été - Web App (Flask)

Un jeu **Sudoku en ligne**, conçu avec ❤️ pour jouer n'importe où — y compris sur la plage 🏖️.  
Choisissez la **taille de la grille** (4x4, 9x9, 16x16), la **difficulté**, jouez dans votre navigateur, imprimez, vérifiez, recommencez !

---

## 🎮 Fonctionnalités

- 🧩 **3 tailles de grilles** disponibles : 4x4, 9x9, 16x16
- 🎚️ **5 niveaux de difficulté** : Facile → Très compliqué
- 🎨 **Thème été** doux et responsive
- ✅ Vérification automatique de la grille remplie
- 🔍 Vérification si la grille est complète
- 🖨️ Impression de la **grille de jeu**
- 🧠 Impression **silencieuse** de la solution complète
- 🧹 Bouton pour réinitialiser les entrées
- 🔄 Bouton “Nouvelle partie”
- ✍️ Footer personnalisé : `© 2025 Frédéric SALERNO. Tous droits réservés.`

---

## 🚀 Installation locale

### 1. Cloner ou dézipper ce projet

```bash
git clone https://github.com/votre-repo/sudoku-ete.git
cd sudoku-ete
```

### 2. Créer un environnement Python

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Lancer le serveur local

```bash
python run.py
```

Puis ouvrir [http://localhost:5000](http://localhost:5000) dans votre navigateur 🧠

---

## 📁 Structure

```
sudoku_saas/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── sudoku.py
│   ├── templates/
│   │   ├── index.html
│   │   └── game.html
├── requirements.txt
├── run.py
└── README.md
```

---

## 📦 Dépendances

- Python 3.8+
- Flask

---

## 👤 Auteur

**Frédéric SALERNO**  
© 2025 Tous droits réservés.

---

## 🧠 Idées futures (TODO)

- ⏱️ Ajouter un chrono ou des scores
- 🌐 Déployer en ligne (Render, Railway, Vercel…)
- 🧠 Générateur plus intelligent avec techniques avancées
- 👤 Système de comptes & leaderboard

---

## 🔒 Licence

Ce projet est publié sous licence **MIT**, à personnaliser si nécessaire.
