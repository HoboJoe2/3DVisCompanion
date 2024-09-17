import PyQt6.QtWidgets
import PyQt6.QtWebEngineWidgets
import PyQt6.QtCore
from flask import Flask, redirect, url_for, render_template
import PyQt6
import os
import filedialpy
import subprocess
import threading
import webbrowser
import colorama
import logging
import time
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BLUE = colorama.Fore.BLUE
RED = colorama.Fore.RED
colorama.init(autoreset=True)

class MainWindow(PyQt6.QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.browser = PyQt6.QtWebEngineWidgets.QWebEngineView()
        self.browser.setUrl(PyQt6.QtCore.QUrl('http://127.0.0.1:5000'))  # URL of your Flask app
        self.setCentralWidget(self.browser)
        self.show()

def convertFile(file_path):    
    print(BLUE + f"--- BEGINNING IMPORT OF {file_path} ---\n\n")
    os.chdir(SCRIPT_DIR)

    try:
        result = subprocess.run(f"""powershell -File convert.ps1 -modelPath "{file_path}""", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(BLUE + "--- STANDARD OUTPUT FROM POWERSHELL FILE ---\n\n", result.stdout.decode())
        print(BLUE + "--- STANDARD ERROR OUTPUT FROM POWERSHELL FILE ---\n\n", result.stderr.decode())
    except subprocess.CalledProcessError as e:
        print(RED + f"--- ERROR OCURRED DURING POWERSHELL EXECUTION: {e} ---\n\n")

    print(BLUE + f"\n--- FINISHED IMPORT OF {file_path} ---\n\n")
    return

def convertAllFilesInDir(dir_path):
    matched_files = []
    extensions = ['.gltf', '.glb', '.abc', '.blend', '.dae', '.fbx', '.glb', '.gltf', '.obj', '.ply', '.stl', '.usd', '.usda', '.usdc', '.wrl', '.x3d']
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            for ext in extensions:
                if filename.lower().endswith(ext):
                    matched_files.append(os.path.join(dirpath, filename))
                    break  # Stop checking other extensions once a match is found

    for file in matched_files:
        convertFile(file)
    return

def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")
    return

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/import_file', methods=['POST'])
def import_file():
    path = filedialpy.openFile()
    convertFile(path)  # Call the first function when Button 1 is pressed
    return redirect(url_for('index'))  # Redirect back to the homepage

@app.route('/import_directory', methods=['POST'])
def import_directory():
    dir = filedialpy.openDir()
    convertAllFilesInDir(dir)  # Call the second function when Button 2 is pressed
    return redirect(url_for('index'))  # Redirect back to the homepage

def run_flask_app():
    app.run(port=5000)

if __name__ == '__main__':
    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    time.sleep(1)

    # Start PyQt application
    Qapp = PyQt6.QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(Qapp.exec())
