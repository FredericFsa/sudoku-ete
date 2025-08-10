# ===== SYSTÈME D'IMPRESSION HTML REDESSINÉ COMPLÈTEMENT =====
# Fichier: print_system_new.py

def create_sudoku_print_page(grid_data, size, difficulty, is_solution=False):
    """
    Redessine complètement les grilles pour l'impression en HTML pur
    
    Args:
        grid_data (list): Grille 2D avec 0 pour cases vides
        size (int): Taille de la grille
        difficulty (str): Niveau de difficulté
        is_solution (bool): True si c'est une solution
    
    Returns:
        str: Page HTML complète optimisée pour impression
    """
    
    # Configuration par taille - REDESSINÉE
    print_configs = {
        4: {"cell": "15mm", "font": "16pt", "thin": "1mm solid #333", "thick": "3mm solid #000"},
        9: {"cell": "12mm", "font": "14pt", "thin": "0.8mm solid #333", "thick": "2.5mm solid #000"},
        16: {"cell": "8mm", "font": "11pt", "thin": "0.6mm solid #333", "thick": "2mm solid #000"},
        25: {"cell": "6mm", "font": "8pt", "thin": "0.4mm solid #333", "thick": "1.5mm solid #000"}
    }
    
    config = print_configs.get(size, print_configs[9])
    block_size = int(size ** 0.5)
    
    # Génération de la grille HTML - REDESSINÉE
    def generate_grid_html():
        html_rows = []
        
        for row_idx in range(size):
            row_cells = []
            
            for col_idx in range(size):
                cell_value = grid_data[row_idx][col_idx]
                
                # Classes CSS pour bordures de blocs
                css_classes = ["sudoku-cell"]
                
                # Bordures de blocs
                if row_idx % block_size == 0:
                    css_classes.append("border-top-thick")
                if col_idx % block_size == 0:
                    css_classes.append("border-left-thick")
                if row_idx == size - 1:
                    css_classes.append("border-bottom-thick")
                if col_idx == size - 1:
                    css_classes.append("border-right-thick")
                
                # Contenu de la cellule - UNIFIÉ
                if cell_value == 0:
                    # Case vide - même traitement pour grille vide et solution
                    cell_content = ""  # Complètement vide
                else:
                    # Case remplie - conversion en symbole
                    if cell_value <= 9:
                        cell_content = str(cell_value)
                    else:
                        # A=10, B=11, etc.
                        cell_content = chr(ord('A') + cell_value - 10)
                
                # Construction de la cellule
                classes_str = " ".join(css_classes)
                row_cells.append(f'<td class="{classes_str}">{cell_content}</td>')
            
            # Construction de la ligne
            html_rows.append(f'<tr>{"".join(row_cells)}</tr>')
        
        return "\n".join(html_rows)
    
    # Type de grille pour le titre
    grid_type = "Solution du" if is_solution else "Grille de"
    
    # CSS complet redessiné
    css_styles = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>{grid_type} Sudoku {size}x{size}</title>
        <style>
            /* RESET COMPLET */
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
            
            /* PAGE CONFIGURATION */
            @page {{
                size: A4;
                margin: 12mm;
            }}
            
            html, body {{
                width: 100%;
                height: 100%;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: white;
                color: black;
            }}
            
            /* CONTAINER PRINCIPAL */
            .print-container {{
                width: 100%;
                max-width: 190mm;
                margin: 0 auto;
                padding: 5mm;
                text-align: center;
            }}
            
            /* TITRE */
            .sudoku-title {{
                font-size: 18pt;
                font-weight: bold;
                color: #000;
                margin-bottom: 8mm;
                text-align: center;
            }}
            
            /* WRAPPER DE LA GRILLE */
            .sudoku-grid-wrapper {{
                display: inline-block;
                border: 3mm solid #000;
                background: white;
                margin: 0 auto;
            }}
            
            /* TABLE DE LA GRILLE */
            .sudoku-table {{
                border-collapse: collapse;
                border-spacing: 0;
                width: auto;
                height: auto;
                background: white;
            }}
            
            /* CELLULES DE BASE */
            .sudoku-cell {{
                width: {config['cell']};
                height: {config['cell']};
                min-width: {config['cell']};
                min-height: {config['cell']};
                max-width: {config['cell']};
                max-height: {config['cell']};
                
                font-size: {config['font']};
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
                
                text-align: center;
                vertical-align: middle;
                
                border: {config['thin']};
                background: white;
                color: #000;
                
                line-height: {config['cell']};
                padding: 0;
                margin: 0;
            }}
            
            /* BORDURES ÉPAISSES POUR BLOCS */
            .border-top-thick {{
                border-top: {config['thick']} !important;
            }}
            
            .border-left-thick {{
                border-left: {config['thick']} !important;
            }}
            
            .border-bottom-thick {{
                border-bottom: {config['thick']} !important;
            }}
            
            .border-right-thick {{
                border-right: {config['thick']} !important;
            }}
            
            /* FOOTER */
            .sudoku-footer {{
                margin-top: 8mm;
                font-size: 10pt;
                color: #666;
                text-align: center;
            }}
            
            /* STYLES D'IMPRESSION SPÉCIFIQUES */
            @media print {{
                .print-container {{
                    max-width: none;
                    width: 100%;
                }}
                
                /* Forcer les couleurs */
                .sudoku-cell {{
                    -webkit-print-color-adjust: exact !important;
                    print-color-adjust: exact !important;
                    color: #000 !important;
                    background: white !important;
                }}
                
                /* Optimisations par taille */
                {f'''
                .sudoku-cell {{
                    font-size: {config['font']} !important;
                    width: {config['cell']} !important;
                    height: {config['cell']} !important;
                    border: {config['thin']} !important;
                }}
                ''' if size <= 16 else f'''
                .sudoku-cell {{
                    font-size: {config['font']} !important;
                    width: {config['cell']} !important;
                    height: {config['cell']} !important;
                    border: 0.5mm solid #000 !important;
                }}
                .border-top-thick {{ border-top: 2mm solid #000 !important; }}
                .border-left-thick {{ border-left: 2mm solid #000 !important; }}
                .border-bottom-thick {{ border-bottom: 2mm solid #000 !important; }}
                .border-right-thick {{ border-right: 2mm solid #000 !important; }}
                '''}
            }}
        </style>
    </head>
    <body>
        <div class="print-container">
            <!-- TITRE -->
            <div class="sudoku-title">
                🧩 {grid_type} Sudoku {size}×{size} - Niveau {difficulty.capitalize()}
            </div>
            
            <!-- GRILLE -->
            <div class="sudoku-grid-wrapper">
                <table class="sudoku-table">
                    {generate_grid_html()}
                </table>
            </div>
            
            <!-- FOOTER -->
            <div class="sudoku-footer">
                © 2025 Frédéric SALERNO. Tous droits réservés.
            </div>
        </div>
        
        <!-- AUTO-IMPRESSION -->
        <script>
            window.onload = function() {{
                // Petit délai pour s'assurer que tout est chargé
                setTimeout(function() {{
                    window.print();
                    // Fermer après impression
                    window.onafterprint = function() {{
                        window.close();
                    }};
                }}, 100);
            }};
        </script>
    </body>
    </html>
    """
    
    return css_styles

# ===== FONCTIONS D'INTERFACE =====

def print_empty_sudoku(grid_data, size, difficulty):
    """Génère l'impression d'une grille vide"""
    return create_sudoku_print_page(grid_data, size, difficulty, is_solution=False)

def print_solved_sudoku(grid_data, size, difficulty):
    """Génère l'impression d'une solution"""
    return create_sudoku_print_page(grid_data, size, difficulty, is_solution=True)

# ===== ROUTES FLASK SIMPLIFIÉES =====

def setup_print_routes(app):
    """Configure les routes d'impression dans votre app Flask"""


# ===== EXEMPLE D'USAGE =====
if __name__ == "__main__":
    # Test avec grille 4x4
    test_empty = [
        [1, 0, 2, 0],
        [0, 4, 0, 3], 
        [4, 0, 0, 2],
        [0, 2, 4, 0]
    ]
    
    test_solved = [
        [1, 3, 2, 4],
        [2, 4, 1, 3], 
        [4, 1, 3, 2],
        [3, 2, 4, 1]
    ]
    
    print("🧪 Génération grille vide 4x4...")
    html_empty = print_empty_sudoku(test_empty, 4, "easy")
    print(f"✅ {len(html_empty)} caractères générés")
    
    print("🧪 Génération solution 4x4...")
    html_solution = print_solved_sudoku(test_solved, 4, "easy")
    print(f"✅ {len(html_solution)} caractères générés")
    
    # Test avec 25x25
    import random
    test_25x25 = [[random.randint(0, 25) for _ in range(25)] for _ in range(25)]
    
    print("🧪 Génération grille 25x25...")
    html_25 = print_empty_sudoku(test_25x25, 25, "medium")
    print(f"✅ Grille 25x25 générée ({len(html_25)} caractères)")
    
    print("\n🎯 Système d'impression redessiné prêt !")
    print("   • HTML pur, aucune dépendance")
    print("   • Configuration par taille optimisée")
    print("   • Rendu parfaitement identique grilles vides/solutions")
    print("   • CSS print spécialisé par taille")