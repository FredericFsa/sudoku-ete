# Impression “jolie” des grilles Sudoku (via iframe `/pretty`)

Ce module ajoute une impression **propre, centrée, une seule page** pour vos grilles **4×4 / 9×9 / 16×16 / 25×25**, avec **titre** en haut et **copyright** en bas.  
L’intégration se fait via une **page d’impression minimaliste** (`pretty_print_lite.html`) chargée dans une **iframe cachée** et pilotée depuis votre page de jeu.

---

## 1) Prérequis

- Python / Flask (ou équivalent Jinja).
- Vos routes habituelles, dont (optionnel) `/solution` renvoyant la solution sous forme de matrice.
- Vos fonctions côté front (si existantes) :
  - `extractOriginalGrid()` → matrice des “givens” (0 pour vide, 1..9, 10=A, …35=Z)
  - `extractGrid()` → matrice de la grille affichée

---

## 2) Fichiers utiles

```
app/
├─ templates/
│  ├─ game_desktop.html             # votre écran de jeu
│  └─ pretty_print_lite.html        # page d’impression minimaliste (voir §4)
└─ static/
   └─ js/ …                        # vos scripts existants
```

**`pretty_print_lite.html`** expose l’API (côté iframe) :

```js
window.prettyGrid = {
  render(grid),            // matrice [[...],[...]]
  renderFromBracketed(txt),// texte "[005][043]...\n[...]"
  setHeader(meta),         // { title, size, difficulty, date, copyright }
  print()                  // lance l’impression
};
```

---

## 3) Route Flask

Dans `app/routes.py` :

```python
from flask import render_template

@app.route("/pretty")
def pretty():
    return render_template("pretty_print_lite.html")
```

---

## 4) Page d’impression “Lite” (à créer)

Créez `app/templates/pretty_print_lite.html` avec le contenu fourni séparément (ou copiez-le depuis ce repo si présent).  
Cette page ne contient **aucun contrôle UI**, uniquement **header + grille + footer** et le CSS **print**.

---

## 5) Intégration front (sans pop-up)

Dans `app/templates/game_desktop.html`, juste avant `</body>` :

```html
<!-- 1) IFRAME cachée vers /pretty -->
<iframe id="pretty-frame" src="/pretty"
        style="position:absolute;left:-9999px;top:-9999px;width:0;height:0;border:0;"></iframe>

<!-- 2) Pont d’impression : envoie les données + méta à l’iframe, lance print() -->
<script>
(function(){
  const frame = document.getElementById('pretty-frame');

  function pushToPretty(data, meta, autoPrint=true){
    function go(){
      const w = frame?.contentWindow;
      if (w && w.prettyGrid){
        // 1) grille
        if (Array.isArray(data)) w.prettyGrid.render(data);
        else w.prettyGrid.renderFromBracketed(data);
        // 2) en-tête
        if (meta) w.prettyGrid.setHeader(meta);
        // 3) impression
        if (autoPrint){ try{ w.focus(); }catch(_){} w.prettyGrid.print(); }
      } else {
        setTimeout(go, 40); // attend que /pretty soit prêt
      }
    }
    go();
  }

  // Bouton “Imprimer” -> givens (grille d’origine)
  document.addEventListener('click', async (ev) => {
    const btn = ev.target.closest('#btn-print-empty,[onclick*="perfectPrintEmpty"],[onclick*="printEmptyGrid"]');
    if (!btn) return;
    ev.preventDefault(); ev.stopImmediatePropagation();

    const grid = (typeof window.extractOriginalGrid==='function')
      ? window.extractOriginalGrid()
      : (typeof window.extractGrid==='function' ? window.extractGrid() : []);

    const n = Array.isArray(grid) ? grid.length : 9;
    const meta = {
      title: `Sudoku ${n}×${n}`,
      size:  `${n}×${n}`,
      difficulty: (window.DIFFICULTY||'').toString(),
      date: new Date().toLocaleDateString('fr-BE'),
      copyright: '© 2025 MonApp'
    };
    pushToPretty(grid, meta, true);
    return false;
  }, true);

  // Bouton “Imprimer Solution”
  document.addEventListener('click', async (ev) => {
    const btn = ev.target.closest('#btn-print-solution,[onclick*="printSolution"]');
    if (!btn) return;
    ev.preventDefault(); ev.stopImmediatePropagation();

    let solved = null;
    try{
      const r = await fetch('/solution', { cache: 'no-store' });
      if (r.ok){ const d = await r.json(); solved = d.solution || d.grid || d.solved; }
    }catch(_){}
    if (!solved && typeof window.extractGrid==='function') solved = window.extractGrid();

    const n = Array.isArray(solved) ? solved.length : 9;
    const meta = {
      title: `Sudoku ${n}×${n} — Solution`,
      size:  `${n}×${n}`,
      difficulty: (window.DIFFICULTY||'').toString(),
      date: new Date().toLocaleDateString('fr-BE'),
      copyright: '© 2025 MonApp'
    };
    pushToPretty(solved, meta, true);
    return false;
  }, true);
})();
</script>
```

> **Important :** on n’utilise plus `window.open()` ⇒ **aucun pop-up**.  
> L’impression part depuis **l’iframe**.

---

## 6) Formats de données acceptés

- **Matrice** `number[][]`  
  - `0` = vide  
  - `1..9` = chiffres  
  - `10..35` = `A..Z` (pour 16×16, 25×25)
- **Texte bracketé** :
  ```
  [005][043][000]
  [400][208][056]
  [002][507][304]
  ...
  ```

---

## 7) Personnalisation rapide

- **Titre/détails**: envoyez `meta` à `setHeader` (voir §5).
- **Copyright**: changez la valeur `© 2025 MonApp`.
- **Marge papier**: dans `pretty_print_lite.html`, règle `@page { margin: 10mm; }`.
- **Taille des cases (print)**: ajustez `table.sudoku td { width:24px; height:24px; font-size:14px; }`
  - *Mode compact 25×25 (option)* :
    ```css
    @media print {
      /* décommentez si n > 16 (à détecter côté app si besoin) */
      /* table.sudoku td { width:22px; height:22px; font-size:13px; } */
    }
    ```

---

## 8) Dépannage

- **/pretty en 404**  
  → Vérifiez la route Flask et que `pretty_print_lite.html` est bien dans `app/templates/`.

- **Rien ne s’imprime / modal de pop-up**  
  → Un ancien code `window.open` traîne. L’interception de clics (voir §5) doit empêcher tout pop-up.  
  → Vérifiez que l’iframe existe : dans la console, `!!document.getElementById('pretty-frame').contentWindow` doit renvoyer `true`.

- **Deux pages à l’impression**  
  → La page Lite inclut un CSS print qui **neutralise** les hauteurs plein écran et **centre**.  
  → Si un navigateur ajoute une page blanche, baissez **très légèrement** l’échelle :
    ```css
    .canvas { transform: scale(0.985); }
    ```

- **Lettres manquantes sur 16×16 / 25×25**  
  → Les valeurs `10..35` sont rendues comme `A..Z`. Assurez-vous d’envoyer **des nombres**, pas des lettres, côté matrice (la page se charge de l’affichage).

---

## 9) Licence

Au choix. Si vous n’avez pas encore de licence, ajoutez un `LICENSE` (MIT par exemple).

---

## 10) Résumé

- `/pretty` charge **`pretty_print_lite.html`** (ultra léger).  
- **Iframe cachée** dans `game_desktop.html`.  
- Les boutons **Imprimer** / **Solution** envoient la **grille + méta** vers l’iframe, qui **rend** et **imprime**.  
- **Zéro pop-up**, **1 seule page**, **centré** et **propre**.
