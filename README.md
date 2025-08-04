
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

## 🚀 Démo en ligne (Render)

> 🔗 https://sudoku-ete.onrender.com *(exemple)*

---

## 📦 Installation locale

### 1. Cloner ou dézipper ce projet

```bash
git clone https://github.com/votre-utilisateur/sudoku-ete.git
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

Puis ouvrir [http://localhost:5000](http://localhost:5000)

---

## 🌐 Déploiement sur Render (gratuit)

1. Créer un compte sur [https://render.com](https://render.com)
2. Lier ton dépôt GitHub
3. Cliquer sur **“New Web Service”**
4. Saisir les infos suivantes :

- **Start command**: `gunicorn run:app`
- **Build command**: `pip install -r requirements.txt`

5. Lancer le déploiement

---

## 📁 Structure

```
sudoku_saas/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── sudoku.py
│   └── templates/
│       ├── index.html
│       └── game.html
├── requirements.txt
├── run.py
├── Procfile
├── render.yaml
└── README.md
```

---

## 📦 Dépendances

- Python 3.8+
- Flask
- Gunicorn

---

## 👤 Auteur

**Frédéric SALERNO**  
© 2025 Tous droits réservés.

---

## 🧠 À venir (TODO)

- ⏱️ Ajouter un chrono ou des scores
- 🧠 Générateur plus intelligent
- 👤 Système de comptes & leaderboard
- 📱 Version mobile ou PWA

---

## 🔒 Licence

Ce projet est publié sous licence **MIT** (à adapter si besoin).
