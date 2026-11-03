import os
import sys
import subprocess

def main():
    print("========================================================")
    print(" 🌦️ Starting Poonamallee Weather Station Server")
    print(" 📍 Listening on: http://0.0.0.0:8000")
    print(" 🌐 Local Dashboard: http://localhost:8000")
    print("========================================================")

    # Use virtual environment python if present
    base_dir = os.path.dirname(os.path.abspath(__file__))
    venv_python = os.path.join(base_dir, '.venv', 'Scripts', 'python.exe')
    py_exec = venv_python if os.path.exists(venv_python) else sys.executable

    manage_py = os.path.join(base_dir, 'manage.py')
    
    try:
        subprocess.run([py_exec, manage_py, 'runserver', '0.0.0.0:8000'])
    except KeyboardInterrupt:
        print("\n[INFO] Weather server stopped.")

if __name__ == '__main__':
    main()
