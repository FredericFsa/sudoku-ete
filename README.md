# ☀️ Sudoku SaaS – Été 2025

Une application web en Python/Flask pour jouer au Sudoku sur toutes les tailles de grille :  
**4x4**, **9x9**, **16x16**, jusqu'à **25x25**, avec des fonctionnalités modernes, propres et imprimables !

---

## 🚀 Fonctionnalités

✅ Choix de la taille de grille :  
- 4×4 (Débutant)  
- 9×9 (Classique)  
- 16×16 (Expert)  
- 25×25 (Maître)

✅ Choix du niveau :  
- Facile à Extrême (modifie le nombre de cases cachées)

✅ Interface responsive, design été avec fond dégradé

✅ Affichage dynamique :
- **Cadre noir épais**
- **Blocs moyens (2x2, 3x3...) en traits moyens**
- **Cases fines en gris clair**

✅ Impression professionnelle :
- Boutons masqués à l’impression
- Style conservé pour la grille ET la solution

✅ Affichage symbolique :
- Nombres > 9 affichés sous forme de lettres (10 → A, 11 → B, ..., 35 → Z)

✅ Solveur évolué :
- 🔁 Algorithme classique + optimisé (MRV, backtracking, pruning)
- 🤖 Choix automatique de la méthode selon la taille
- ⏱️ Résolution en **thread séparé avec timeout (600s)**
- 🌐 Compatible avec **Render**, même pour les grandes grilles

---

## 🧪 Lancer en local

### 🔧 Prérequis

- Python 3.10+ recommandé
- `pip install -r requirements.txt`

### ▶️ Lancer

```bash
python run.py
```

Ouvre [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## ⚙️ Structure du projet

```
.
├── app/
│   ├── __init__.py       # App Flask
│   ├── routes.py         # Routes principales
│   ├── sudoku.py         # Générateur, solveur, vérification
│   ├── templates/
│   │   ├── index.html    # Page d’accueil
│   │   └── game.html     # Grille de jeu
├── run.py                # Lanceur local avec arrêt propre
├── requirements.txt
├── README.md
```

---

## ☁️ Déploiement sur Render

1. Ajouter un `build` command :
   ```
   pip install -r requirements.txt
   ```

2. Start command :
   ```
   python run.py
   ```

3. Ajouter un fichier `render.yaml` si besoin (optionnel)

4. Définir la variable d’environnement :
   ```
   FLASK_ENV=production
   ```

---

## 🛑 Arrêt propre

Appuyez sur `Ctrl+C` → les threads sont fermés proprement avec message.

---

## © Licence

MIT –  
© 2025 Frédéric SALERNO. Tous droits réservés.