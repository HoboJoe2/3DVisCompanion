import PyQt6.QtWidgets
import PyQt6.QtWebEngineWidgets
from PyQt6.QtWebEngineCore import QWebEnginePage
import PyQt6.QtCore
import PyQt6.QtGui
import PyQt6
from flask import Flask, redirect, url_for, render_template
import flask_socketio
import os
import filedialpy
import subprocess
import threading
import colorama
import logging
import time
import sys
import json

# Global variables
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, 'icon.png'))
MODEL_FOLDER_PATH = "src\\models"
BLUE = colorama.Fore.BLUE
RED = colorama.Fore.RED
colorama.init(autoreset=True)

# Class definitions
class CustomWebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, line, sourceID):
        print(f"JS Console [{level}] from {sourceID}:{line} - {message}") # Override to print console messages

class MainWindow(PyQt6.QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3DVisUploader")
        self.setWindowIcon(PyQt6.QtGui.QIcon(ICON_PATH))
        self.browser = PyQt6.QtWebEngineWidgets.QWebEngineView()
        self.browser.setPage(CustomWebEnginePage(self.browser))
        self.browser.setUrl(PyQt6.QtCore.QUrl('http://127.0.0.1:5000')) # URL of your Flask app
        self.setCentralWidget(self.browser)
        self.showMaximized()

    def handle_console_message(self, level, message, line, sourceID):
        print(f"JS Console [{level}] from {sourceID}:{line} - {message}")

# Function definitions
def getJSONFilesFromDirectory(dir_path):
    matched_files = []
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            if filename.lower().endswith(".json"):
                matched_files.append(os.path.join(dirpath, filename))
    return matched_files

def createJSONDictFromFilePathList(file_path_list):
    json_dict = {}
    for json_path in file_path_list:
        with open(json_path, 'r') as json_file:
            json_dict[json_path] = json.load(json_file)
    return json_dict

def convertFile(file_path):
    os.chdir(SCRIPT_DIR) # Necessary since opening the file dialogue changes the working directory 

    print(BLUE + f"--- BEGINNING IMPORT OF {file_path} ---\n\n")

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

app = Flask(__name__)
socketio = flask_socketio.SocketIO(app)

@socketio.on('connect')
def handle_socket_connect():
    print("Client connected")
    json_files = getJSONFilesFromDirectory(MODEL_FOLDER_PATH)
    model_data = createJSONDictFromFilePathList(json_files)
    socketio.emit('json_transfer_to_js', model_data)
    return

@socketio.on('json_transfer_to_python')
def handle_socket_event(data):
    print(f"Received JSON: {data}")
    return

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/import_file', methods=['POST'])
def import_file():
    path = filedialpy.openFile() # Get single file path
    convertFile(path)
    return redirect(url_for('index'))  # Redirect back to the homepage

@app.route('/import_directory', methods=['POST'])
def import_directory():
    dir = filedialpy.openDir() # Get directory path
    convertAllFilesInDir(dir)
    return redirect(url_for('index'))  # Redirect back to the homepage

def run_flask_app():
    socketio.run(app, port=5000)
    return


if __name__ == '__main__':
    #log = logging.getLogger('werkzeug') # Werkzeug logger is used by flask
    #log.setLevel(logging.ERROR) # Stop flask from logging each button click

    # Start Flask app in a separate thread
    threading.Thread(target=run_flask_app).start()

    # Start PyQt application
    Qapp = PyQt6.QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(Qapp.exec())
