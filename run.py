from app import app
from app.routes import executor
import atexit
import logging
import os

# ✅ Configuration pour logs propres
def setup_clean_logging():
    """Configure un logging minimal et propre"""
    # Désactiver les logs Werkzeug (Flask) en production
    if not app.debug:
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
    
    # Logger personnalisé pour l'application
    app_logger = logging.getLogger('sudoku')
    app_logger.setLevel(logging.INFO)
    
    # Handler avec format propre
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(message)s'))
    app_logger.addHandler(handler)

def shutdown_executor():
    print("🛑 Arrêt du serveur Sudoku")
    executor.shutdown(wait=False)

# Configuration au démarrage
setup_clean_logging()
atexit.register(shutdown_executor)

if __name__ == "__main__":
    try:
        print("🌞 Sudoku d'Été démarré sur http://127.0.0.1:5000")
        print("   Appuyez sur Ctrl+C pour arrêter")
        print("-" * 50)
        
        # ✅ Suppression complète des logs HTTP
        import sys
        import logging
        from werkzeug.serving import WSGIRequestHandler
        
        # Rediriger les logs Werkzeug vers /dev/null (Windows compatible)
        class SilentRequestHandler(WSGIRequestHandler):
            def log_request(self, *args, **kwargs):
                pass  # Ne rien afficher
        
        # Configurer Flask pour mode silencieux
        logging.getLogger('werkzeug').setLevel(logging.ERROR)
        
        app.run(
            host="0.0.0.0", 
            port=5000, 
            debug=False,
            use_reloader=False,
            threaded=True,
            request_handler=SilentRequestHandler  # ✅ Handler silencieux
        )
    except KeyboardInterrupt:
        print("\n🌅 Au revoir !")
    except Exception as e:
        print(f"❌ Erreur: {e}")