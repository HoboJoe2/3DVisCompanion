from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEnginePage
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QIcon
import flask
import flask_socketio
import os
import filedialpy
import subprocess
import threading
import colorama
import logging
import sys
import json
import shutil

# Global variables
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, 'icon.png'))
MODEL_FOLDER_PATH = "C:\\Users\\joedi\\Documents\\_ICT342\\3DVisUploader\\src\\models" # "\\CAVE-HEADNODE\data\3dvis\models" "C:\\Users\\joedi\\OneDrive - University of the Sunshine Coast\\_ICT342 (IT Project)\\3DVisUploader\\src\\models" "C:\\Users\\vez17\\Desktop\\models"
BLUE = colorama.Fore.BLUE
RED = colorama.Fore.RED
colorama.init(autoreset=True)

# Class definitions
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3DVisUploader")
        self.setWindowIcon(QIcon(ICON_PATH))
        self.browser = QWebEngineView()
        self.browser.setPage(QWebEnginePage(self.browser))
        self.browser.setUrl(QUrl('http://127.0.0.1:5000'))  # URL of your Flask app
        self.setCentralWidget(self.browser)
        self.showMaximized()

        # Connect loadFinished signal to the method that will inject JavaScript
        self.browser.loadFinished.connect(self.on_load_finished)

    def on_load_finished(self):
        # Inject custom JavaScript to hide the scrollbar after the page has finished loading
        self.browser.page().runJavaScript("""
            var style = document.createElement('style');
            style.innerHTML = '::-webkit-scrollbar { display: none; } body { overflow: hidden; }';
            document.head.appendChild(style);
        """)

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

def updateAndDeleteJSONFiles(json_dict):
    for json_file_path in getJSONFilesFromDirectory(MODEL_FOLDER_PATH):
        if json_file_path not in json_dict.keys():
            shutil.rmtree(os.path.dirname(json_file_path))
    for json_file_path, json_data in json_dict.items():
        with open(json_file_path, 'w') as json_file:
            json.dump(json_data, json_file)
    return

def convertFile(file_path):
    print(BLUE + f"--- BEGINNING IMPORT OF {file_path} ---\n\n")

    try:
        #result = subprocess.run(f"""powershell -File convert.ps1 -modelPath "{file_path}""", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = subprocess.run(f""""Blender 4.2\\blender.exe" -b -P 2gltf2.py -- -modelPath "{file_path}""""", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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

def createModelPath(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app)

@socketio.on('connect')
def handle_socket_connect():
    json_files = getJSONFilesFromDirectory(MODEL_FOLDER_PATH)
    model_data = createJSONDictFromFilePathList(json_files)
    socketio.emit('json_transfer_to_js', model_data) # Send a dictionary to the frontend to populate the table on connection
    return

@socketio.on('json_transfer_to_python')
def handle_socket_event(data):
    updateAndDeleteJSONFiles(data) # Update and delete json files when data is received from frontend (when user changes a name or deletes a model)
    return

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/import_file', methods=['POST'])
def import_file():
    path = filedialpy.openFile() # Get single file path
    os.chdir(SCRIPT_DIR) # Necessary since opening the file dialogue changes the working directory 
    convertFile(path)
    return flask.redirect(flask.url_for('index'))  # Redirect back to the homepage

@app.route('/import_directory', methods=['POST'])
def import_directory():
    dir = filedialpy.openDir() # Get directory path
    os.chdir(SCRIPT_DIR) # Necessary since opening the file dialogue changes the working directory 
    convertAllFilesInDir(dir)
    return flask.redirect(flask.url_for('index'))  # Redirect back to the homepage

def run_flask_app():
    socketio.run(app, port=5000)
    return

if __name__ == '__main__':
    createModelPath(MODEL_FOLDER_PATH)
    log = logging.getLogger('werkzeug') # Werkzeug logger is used by flask
    log.setLevel(logging.ERROR) # Stop flask from logging each button click

    # Start Flask app in a separate thread
    threading.Thread(target=run_flask_app, daemon=True).start()

    # Start PyQt application
    Qapp = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(Qapp.exec())
