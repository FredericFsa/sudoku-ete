from app import app
from app.routes import executor  # On importe le ThreadPool global
import atexit

def shutdown_executor():
    print("🧵 Fermeture des threads en cours...")
    executor.shutdown(wait=False)
    print("✅ Fermeture propre terminée.")

# Appelé automatiquement à la fermeture (Ctrl+C, fermeture fenêtre, etc.)
atexit.register(shutdown_executor)

if __name__ == "__main__":
    try:
        print("🚀 Lancement du serveur Flask sur http://127.0.0.1:5000")
        app.run(debug=True, use_reloader=False, threaded=True)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt manuel détecté (Ctrl+C)")
