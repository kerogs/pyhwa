# why does it work when running the exe from the command line but not with a double-click?
import subprocess
import sys

python_interpreter = sys.executable
fichier_a_executer = "app.py" 

try:
    subprocess.run([python_interpreter, fichier_a_executer], check=True)
except KeyboardInterrupt:
    print("Le serveur a été arrêté manuellement.")
except Exception as e:
    print(f"Une erreur s'est produite : {e}")
