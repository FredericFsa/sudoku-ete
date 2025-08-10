/**
 * SUDOKU GAME - JavaScript Principal
 * © 2025 Frédéric SALERNO. Tous droits réservés.
 */

// ===== VARIABLES GLOBALES =====
const gridSize = window.GRID_SIZE;
const difficulty = window.DIFFICULTY;

// ===== INITIALISATION =====
document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
    addKeyboardNavigation();
});

// ===== GESTIONNAIRES D'ÉVÉNEMENTS =====
function initializeEventListeners() {
    // Boutons principaux
    document.getElementById('btn-check').addEventListener('click', checkSolution);
    document.getElementById('btn-complete').addEventListener('click', checkIfComplete);
    document.getElementById('btn-solution').addEventListener('click', showSolution);
    document.getElementById('btn-clear').addEventListener('click', clearGrid);
    document.getElementById('btn-print-empty').addEventListener('click', printEmptyGrid);
    document.getElementById('btn-print-solution').addEventListener('click', printSolution);
    document.getElementById('btn-print-page').addEventListener('click', printCurrentPage);
    
    // Validation des entrées dans les cases
    document.querySelectorAll('input').forEach(input => {
        input.addEventListener('input', validateInput);
        input.addEventListener('keydown', handleKeyNavigation);
    });
}

// ===== FONCTIONS PRINCIPALES =====

/**
 * Vérifie si la solution actuelle est correcte
 */
async function checkSolution() {
    try {
        const grid = extractGrid();
        
        // Vérifier d'abord si la grille est complète
        let hasEmptyCells = false;
        for (const row of grid) {
            for (const val of row) {
                if (val === 0) {
                    hasEmptyCells = true;
                    break;
                }
            }
            if (hasEmptyCells) break;
        }
        
        if (hasEmptyCells) {
            showMessage("⚠️ Complétez d'abord toute la grille !", 'warning');
            return;
        }
        
        // Essayer de vérifier avec le serveur
        try {
            const response = await fetch('/check', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({grid})
            });
            
            if (response.ok) {
                const result = await response.json();
                showMessage(
                    result.correct ? "✅ La grille est correcte !" : "❌ La grille contient des erreurs !",
                    result.correct ? 'success' : 'error'
                );
                return;
            }
        } catch (fetchError) {
            console.warn('Serveur non disponible, vérification locale');
        }
        
        // Vérification locale basique si le serveur n'est pas disponible
        const isValid = validateGridLocally(grid);
        showMessage(
            isValid ? "✅ La grille semble correcte ! (vérification locale)" : "❌ La grille contient des erreurs !",
            isValid ? 'success' : 'error'
        );
        
    } catch (error) {
        console.error('Erreur lors de la vérification:', error);
        showMessage("❌ Erreur lors de la vérification de la solution", 'error');
    }
}

/**
 * Validation locale basique d'une grille Sudoku
 */
function validateGridLocally(grid) {
    const size = grid.length;
    const blockSize = Math.sqrt(size);
    
    // Vérifier les lignes
    for (let r = 0; r < size; r++) {
        const seen = new Set();
        for (let c = 0; c < size; c++) {
            const val = grid[r][c];
            if (val < 1 || val > size || seen.has(val)) {
                return false;
            }
            seen.add(val);
        }
    }
    
    // Vérifier les colonnes
    for (let c = 0; c < size; c++) {
        const seen = new Set();
        for (let r = 0; r < size; r++) {
            const val = grid[r][c];
            if (seen.has(val)) {
                return false;
            }
            seen.add(val);
        }
    }
    
    // Vérifier les blocs
    for (let blockRow = 0; blockRow < blockSize; blockRow++) {
        for (let blockCol = 0; blockCol < blockSize; blockCol++) {
            const seen = new Set();
            for (let r = blockRow * blockSize; r < (blockRow + 1) * blockSize; r++) {
                for (let c = blockCol * blockSize; c < (blockCol + 1) * blockSize; c++) {
                    const val = grid[r][c];
                    if (seen.has(val)) {
                        return false;
                    }
                    seen.add(val);
                }
            }
        }
    }
    
    return true;
}

/**
 * Vérifie si la grille est complètement remplie
 */
function checkIfComplete() {
    const grid = extractGrid();
    
    for (const row of grid) {
        for (const val of row) {
            if (val === 0) {
                showMessage("⚠️ Il manque encore des chiffres !", 'warning');
                return;
            }
        }
    }
    
    showMessage("✅ La grille est entièrement remplie !", 'success');
}

/**
 * Affiche la solution complète
 */
async function showSolution() {
    const loading = document.getElementById("loading");
    loading.style.display = "block";

    try {
        let solved;
        
        // Essayer de récupérer la solution du serveur
        try {
            const response = await fetch('/solution');
            if (response.ok) {
                const result = await response.json();
                solved = result.solution;
                showMessage("🧠 Solution récupérée du serveur !", 'success');
            } else {
                throw new Error('Serveur non disponible');
            }
        } catch (fetchError) {
            // Si le serveur ne répond pas, générer une solution simple pour demo
            console.warn('Impossible de récupérer la solution du serveur');
            showMessage("⚠️ Serveur indisponible - Mode démonstration", 'warning');
            
            // Générer une grille "solution" basique pour la démonstration
            solved = generateDemoSolution();
        }
        
        fillGridWithSolution(solved);
        
    } catch (error) {
        console.error('Erreur lors de la récupération de la solution:', error);
        showMessage("❌ Erreur lors de la récupération de la solution !", 'error');
    } finally {
        loading.style.display = "none";
    }
}

/**
 * Génère une solution de démonstration quand le serveur n'est pas disponible
 */
function generateDemoSolution() {
    const grid = extractGrid();
    
    // Pour la démo, on remplit simplement les cases vides avec des valeurs séquentielles
    let counter = 1;
    for (let r = 0; r < gridSize; r++) {
        for (let c = 0; c < gridSize; c++) {
            if (grid[r][c] === 0) {
                grid[r][c] = ((counter - 1) % gridSize) + 1;
                counter++;
            }
        }
    }
    
    return grid;
}

/**
 * Efface toutes les réponses de l'utilisateur
 */
function clearGrid() {
    if (confirm("Êtes-vous sûr de vouloir effacer toutes vos réponses ?")) {
        document.querySelectorAll("input").forEach(input => {
            input.value = "";
        });
        showMessage("🧹 Grille effacée !", 'info');
    }
}

// “Imprimer” -> on envoie la grille d'ORIGINE (les givens)
function printEmptyGrid() {
  try {
    const originalGrid = extractOriginalGrid(); // déjà dans ton app
    renderInIframeAndPrint(originalGrid, true);
  } catch (e) {
    console.error(e);
    alert("Impossible d'imprimer la grille d'origine.");
  }
}

async function printSolution() {
  try {
    let solved = null;
    // 1) serveur
    try {
      const r = await fetch('/solution', { cache: 'no-store' });
      if (r.ok) { const d = await r.json(); solved = d.solution || d.grid || d.solved; }
    } catch (_) {}
    // 2) fallback si besoin : grille courante
    if (!solved) { console.warn('Solution serveur indisponible — fallback grille courante'); solved = extractGrid(); }
    renderInIframeAndPrint(solved, true);
  } catch (e) {
    console.error(e);
    alert("Impossible d'imprimer la solution.");
  }
}


// ===== FONCTIONS UTILITAIRES =====

/**
 * Extrait la grille actuelle (avec les réponses de l'utilisateur)
 */
function extractGrid() {
    const rows = document.querySelectorAll("#sudoku-table tr");
    const grid = [];
    
    for (let r = 0; r < rows.length; r++) {
        const cells = rows[r].querySelectorAll("td");
        const row = [];
        
        for (let c = 0; c < cells.length; c++) {
            const input = cells[c].querySelector("input");
            let val;
            
            if (input) {
                // Case modifiable
                const raw = input.value.trim().toUpperCase();
                if (!raw) {
                    val = 0;
                } else if (/[A-Z]/.test(raw)) {
                    val = raw.charCodeAt(0) - 55;
                } else {
                    val = parseInt(raw, 10);
                }
            } else {
                // Case fixe
                const content = cells[c].textContent.trim().toUpperCase();
                if (/[A-Z]/.test(content)) {
                    val = content.charCodeAt(0) - 55;
                } else {
                    val = parseInt(content, 10);
                }
            }
            
            row.push(isNaN(val) ? 0 : val);
        }
        grid.push(row);
    }
    
    return grid;
}

/**
 * Extrait la grille originale (uniquement les cases pré-remplies)
 */
function extractOriginalGrid() {
    const rows = document.querySelectorAll("#sudoku-table tr");
    const grid = [];
    
    for (let r = 0; r < rows.length; r++) {
        const cells = rows[r].querySelectorAll("td");
        const row = [];
        
        for (let c = 0; c < cells.length; c++) {
            const input = cells[c].querySelector("input");
            let val = 0;
            
            if (!input) {
                // Case fixe uniquement
                const content = cells[c].textContent.trim().toUpperCase();
                if (/[A-Z]/.test(content)) {
                    val = content.charCodeAt(0) - 55;
                } else {
                    val = parseInt(content, 10);
                }
            }
            
            row.push(isNaN(val) ? 0 : val);
        }
        grid.push(row);
    }
    
    return grid;
}

/**
 * Remplit la grille avec la solution
 */
function fillGridWithSolution(solved) {
    const rows = document.querySelectorAll("#sudoku-table tr");
    
    for (let r = 0; r < rows.length; r++) {
        const cells = rows[r].querySelectorAll("td");
        for (let c = 0; c < cells.length; c++) {
            const input = cells[c].querySelector("input");
            if (input) {
                input.value = toSymbol(solved[r][c]);
            }
        }
    }
}

/**
 * Convertit un nombre en symbole (1-9, A-Z)
 */
function toSymbol(n) {
    if (n <= 9) {
        return n.toString();
    } else {
        return String.fromCharCode(55 + n);
    }
}

/**
 * Convertit un symbole en nombre
 */
function fromSymbol(symbol) {
    const s = symbol.toString().toUpperCase();
    if (/[0-9]/.test(s)) {
        return parseInt(s, 10);
    } else if (/[A-Z]/.test(s)) {
        return s.charCodeAt(0) - 55;
    }
    return 0;
}

/**
 * Valide l'entrée dans une case
 */
function validateInput(event) {
    const input = event.target;
    const value = input.value.toUpperCase();
    
    // Supprime les caractères invalides
    const validChars = gridSize <= 9 ? '1-9' : gridSize <= 16 ? '1-9A-G' : '1-9A-Z';
    const regex = new RegExp(`[^${validChars}]`, 'g');
    const cleanValue = value.replace(regex, '');
    
    // Limite à 1 caractère
    input.value = cleanValue.slice(0, 1);
    
    // Validation de la valeur
    if (input.value) {
        const num = fromSymbol(input.value);
        if (num < 1 || num > gridSize) {
            input.value = '';
            showMessage(`⚠️ Valeur invalide ! Utilisez 1-${gridSize <= 9 ? gridSize : gridSize <= 16 ? '9,A-G' : '9,A-Z'}`, 'warning');
        }
    }
}

/**
 * Gestion de la navigation au clavier
 */
function handleKeyNavigation(event) {
    const input = event.target;
    const td = input.closest('td');
    const tr = td.closest('tr');
    const table = tr.closest('table');
    
    let targetCell = null;
    
    switch(event.key) {
        case 'ArrowUp':
            event.preventDefault();
            const prevRow = tr.previousElementSibling;
            if (prevRow) {
                const colIndex = Array.from(tr.children).indexOf(td);
                targetCell = prevRow.children[colIndex];
            }
            break;
            
        case 'ArrowDown':
            event.preventDefault();
            const nextRow = tr.nextElementSibling;
            if (nextRow) {
                const colIndex = Array.from(tr.children).indexOf(td);
                targetCell = nextRow.children[colIndex];
            }
            break;
            
        case 'ArrowLeft':
            event.preventDefault();
            targetCell = td.previousElementSibling;
            break;
            
        case 'ArrowRight':
        case 'Tab':
            if (event.key === 'Tab') event.preventDefault();
            targetCell = td.nextElementSibling;
            if (!targetCell) {
                const nextRow = tr.nextElementSibling;
                if (nextRow) {
                    targetCell = nextRow.children[0];
                }
            }
            break;
            
        case 'Enter':
            event.preventDefault();
            const nextRow2 = tr.nextElementSibling;
            if (nextRow2) {
                const colIndex = Array.from(tr.children).indexOf(td);
                targetCell = nextRow2.children[colIndex];
            }
            break;
    }
    
    if (targetCell) {
        const targetInput = targetCell.querySelector('input');
        if (targetInput) {
            targetInput.focus();
            targetInput.select();
        }
    }
}

/**
 * Ajoute la navigation clavier globale
 */
function addKeyboardNavigation() {
    document.addEventListener('keydown', function(event) {
        // Raccourcis clavier globaux
        if (event.ctrlKey || event.metaKey) {
            switch(event.key.toLowerCase()) {
                case 's':
                    event.preventDefault();
                    showSolution();
                    break;
                case 'r':
                    event.preventDefault();
                    clearGrid();
                    break;
                case 'p':
                    event.preventDefault();
                    printEmptyGrid();
                    break;
            }
        }
    });
}

/**
 * Affiche un message à l'utilisateur
 */
function showMessage(message, type = 'info') {
    // Crée ou récupère le conteneur de messages
    let messageContainer = document.getElementById('message-container');
    if (!messageContainer) {
        messageContainer = document.createElement('div');
        messageContainer.id = 'message-container';
        messageContainer.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            max-width: 350px;
        `;
        document.body.appendChild(messageContainer);
    }
    
    // Crée le message
    const messageDiv = document.createElement('div');
    messageDiv.style.cssText = `
        padding: 12px 16px;
        margin-bottom: 10px;
        border-radius: 6px;
        color: white;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        transform: translateX(100%);
        transition: transform 0.3s ease;
        cursor: pointer;
    `;
    
    // Couleurs selon le type
    switch(type) {
        case 'success':
            messageDiv.style.backgroundColor = '#28a745';
            break;
        case 'error':
            messageDiv.style.backgroundColor = '#dc3545';
            break;
        case 'warning':
            messageDiv.style.backgroundColor = '#ffc107';
            messageDiv.style.color = '#212529';
            break;
        default:
            messageDiv.style.backgroundColor = '#17a2b8';
    }
    
    messageDiv.textContent = message;
    messageContainer.appendChild(messageDiv);
    
    // Animation d'apparition
    setTimeout(() => {
        messageDiv.style.transform = 'translateX(0)';
    }, 10);
    
    // Suppression automatique
    setTimeout(() => {
        messageDiv.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (messageContainer.contains(messageDiv)) {
                messageContainer.removeChild(messageDiv);
            }
        }, 300);
    }, 3000);
    
    // Suppression au clic
    messageDiv.addEventListener('click', () => {
        messageDiv.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (messageContainer.contains(messageDiv)) {
                messageContainer.removeChild(messageDiv);
            }
        }, 300);
    });
}

// === Intégration “jolie” : ouvrir la page et lui pousser la grille ===
const PRETTY_URL = "/sudoku_grids_centered_print_random_fill_fixed.html";

function openPrettyAndRender(data, autoPrint = true) {
  const w = window.open(PRETTY_URL, "_blank", "noopener,noreferrer");
  function push() {
    if (!w || w.closed) return;
    if (w.prettyGrid) {
      if (Array.isArray(data)) w.prettyGrid.render(data);
      else w.prettyGrid.renderFromBracketed(data);
      if (autoPrint) w.prettyGrid.print();
    } else {
      setTimeout(push, 50);
    }
  }
  push();
}

// ===== FONCTIONS D'IMPRESSION =====

/**
 * Alternative à l'impression par iframe - utilise window.print() directement
 */
function printCurrentPage() {
    try {
        // Masquer les boutons temporairement
        const controlFrame = document.querySelector('.control-frame');
        const loading = document.getElementById('loading');
        
        controlFrame.style.display = 'none';
        loading.style.display = 'none';
        
        // Imprimer
        window.print();
        
        // Remettre les boutons
        setTimeout(() => {
            controlFrame.style.display = 'flex';
        }, 1000);
        
        showMessage("🖨️ Impression lancée !", 'success');
        
    } catch (error) {
        console.error('Erreur lors de l\'impression:', error);
        showMessage("❌ Erreur lors de l'impression", 'error');
    }
}

/**
 * Génère le HTML pour l'impression de la grille vide
 */
function generateEmptyGridHTML(grid, size) {
    const blockSize = Math.sqrt(size);
    const styles = getPrintStyles(size);
    
    const tableHTML = grid.map((row, r) => `
        <tr>
            ${row.map((val, c) => {
                const classes = [
                    (r % blockSize === 0 ? 'top-block' : ''),
                    (c % blockSize === 0 ? 'left-block' : ''),
                    (r === size - 1 ? 'bottom-block' : ''),
                    (c === size - 1 ? 'right-block' : '')
                ].filter(cls => cls).join(' ');
                
                let content = '';
                if (val !== 0) {
                    content = toSymbol(val);
                }
                
                return `<td class="${classes}">${content}</td>`;
            }).join('')}
        </tr>
    `).join('');

    return generatePrintHTML(
        `🧩 Sudoku ${size}x${size} - Grille à compléter`,
        tableHTML,
        styles
    );
}

/**
 * Génère le HTML pour l'impression de la solution
 */
function generateSolutionHTML(solved, size) {
    const blockSize = Math.sqrt(size);
    const styles = getPrintStyles(size);
    
    const tableHTML = solved.map((row, r) => `
        <tr>
            ${row.map((val, c) => {
                const classes = [
                    (r % blockSize === 0 ? 'top-block' : ''),
                    (c % blockSize === 0 ? 'left-block' : ''),
                    (r === size - 1 ? 'bottom-block' : ''),
                    (c === size - 1 ? 'right-block' : '')
                ].filter(cls => cls).join(' ');
                
                const symbol = toSymbol(val);
                return `<td class="${classes}">${symbol}</td>`;
            }).join('')}
        </tr>
    `).join('');

    return generatePrintHTML(
        `🧩 Sudoku ${size}x${size} - Solution`,
        tableHTML,
        styles
    );
}

/**
 * Génère les styles CSS pour l'impression selon la taille
 */
function getPrintStyles(size) {
    if (size >= 25) {
        return `
            td {
                width: 5mm; height: 5mm; font-size: 6pt; line-height: 5mm;
                border: 0.1mm solid #999; text-align: center; vertical-align: middle;
                padding: 0; background: white; font-weight: bold; color: #000;
            }
            .top-block { border-top: 0.8mm solid #000 !important; }
            .left-block { border-left: 0.8mm solid #000 !important; }
            .bottom-block { border-bottom: 0.8mm solid #000 !important; }
            .right-block { border-right: 0.8mm solid #000 !important; }
        `;
    } else if (size >= 16) {
        return `
            td {
                width: 8mm; height: 8mm; font-size: 10pt; line-height: 8mm;
                border: 0.3mm solid #999; text-align: center; vertical-align: middle;
                padding: 0; background: white; font-weight: bold; color: #000;
            }
            .top-block { border-top: 1.2mm solid #000 !important; }
            .left-block { border-left: 1.2mm solid #000 !important; }
            .bottom-block { border-bottom: 1.2mm solid #000 !important; }
            .right-block { border-right: 1.2mm solid #000 !important; }
        `;
    } else {
        return `
            td {
                width: 12mm; height: 12mm; font-size: 14pt; line-height: 12mm;
                border: 0.5mm solid #999; text-align: center; vertical-align: middle;
                padding: 0; background: white; font-weight: bold; color: #000;
            }
            .top-block { border-top: 1.5mm solid #000 !important; }
            .left-block { border-left: 1.5mm solid #000 !important; }
            .bottom-block { border-bottom: 1.5mm solid #000 !important; }
            .right-block { border-right: 1.5mm solid #000 !important; }
        `;
    }
}

/**
 * Génère le HTML complet pour l'impression
 */
function generatePrintHTML(title, tableHTML, styles) {
    return `
        <!DOCTYPE html>
        <html>
        <head>
            <title>${title}</title>
            <style>
                * { 
                    -webkit-print-color-adjust: exact !important; 
                    print-color-adjust: exact !important; 
                }
                @page { 
                    size: A4; 
                    margin: 15mm; 
                }
                body { 
                    font-family: Arial, sans-serif; 
                    text-align: center; 
                    margin: 0; 
                    padding: 0; 
                    background: white; 
                }
                h2 { 
                    font-size: 16pt; 
                    margin: 0 0 10mm 0; 
                    font-weight: bold; 
                    color: #000; 
                }
                .sudoku-wrapper { 
                    display: table; 
                    margin: 0 auto; 
                    border: 3px solid #000; 
                    padding: 0; 
                    background: white; 
                }
                table { 
                    border-collapse: collapse; 
                    border-spacing: 0; 
                    margin: 0; 
                    background: white; 
                }
                ${styles}
                footer { 
                    margin-top: 10mm; 
                    color: #666; 
                    font-size: 10pt; 
                }
            </style>
        </head>
        <body>
            <h2>${title}</h2>
            <div class="sudoku-wrapper">
                <table>${tableHTML}</table>
            </div>
            <footer>© 2025 Frédéric SALERNO. Tous droits réservés.</footer>
            <script>
                window.onload = function() {
                    window.print();
                };
            </script>
        </body>
        </html>
    `;
}

// ===== MESSAGES D'INFORMATION =====
console.log(`🧩 Sudoku Game ${gridSize}x${gridSize} - Niveau ${difficulty}`);
console.log('📋 Raccourcis clavier disponibles:');
console.log('   • Ctrl+S : Afficher la solution');
console.log('   • Ctrl+R : Effacer la grille');
console.log('   • Ctrl+P : Imprimer');
console.log('   • Flèches : Navigation dans la grille');
console.log('   • Tab/Entrée : Case suivante');
console.log('© 2025 Frédéric SALERNO. Tous droits réservés.');

// === Impression via IFRAME cachée (pas de pop-up) ===========================
const PRETTY_IFRAME_ID = "pretty-frame";

function renderInIframeAndPrint(data, autoPrint = true) {
  const f = document.getElementById(PRETTY_IFRAME_ID);
  if (!f) { console.error("Iframe 'pretty-frame' introuvable"); return; }

  function push() {
    const w = f.contentWindow;
    if (!w || w.closed) return;

    if (w.prettyGrid) {
      if (Array.isArray(data)) w.prettyGrid.render(data);
      else w.prettyGrid.renderFromBracketed(data);
      if (autoPrint) { try { w.focus(); } catch(_) {} w.prettyGrid.print(); }
    } else {
      setTimeout(push, 40); // attendre que la page jolie soit prête
    }
  }
  push();
}
