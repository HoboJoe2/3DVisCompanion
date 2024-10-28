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
import send2trash

# Global variables
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, 'config.json'))
ICON_FILE_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, 'icon.ico'))

with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
    loaded_json = json.load(f)
    BASE_PATH = loaded_json["base_path"]

MODEL_FOLDER_PATH = os.path.join(BASE_PATH + "\\models")
SCENE_FOLDER_PATH = os.path.join(BASE_PATH + "\\scenes")
OPTIONS_FILE_PATH = os.path.join(BASE_PATH + "\\options.json")
SUPPORTED_EXTENSIONS = ['.gltf', '.glb', '.abc', '.blend', '.dae', '.fbx', '.obj', '.ply', '.stl', '.usd', '.usda', '.usdc', '.usdz']
ERROR_FILE_PATH = os.path.join(MODEL_FOLDER_PATH, "last_error.txt")
BLUE = colorama.Fore.BLUE
RED = colorama.Fore.RED
colorama.init(autoreset=True)


# Class definitions
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3DVisCompanion")
        self.setWindowIcon(QIcon(ICON_FILE_PATH))
        self.browser = QWebEngineView()
        self.browser.setPage(QWebEnginePage(self.browser))
        self.browser.setUrl(QUrl('http://127.0.0.1:5000'))
        self.setCentralWidget(self.browser)
        self.showMaximized()
        self.browser.loadFinished.connect(self.on_load_finished) # Connect loadFinished signal to the method that will inject JavaScript
        return

    def on_load_finished(self): # Inject custom JavaScript to hide the scrollbar after the page has finished loading
        page = self.browser.page()
        if page:
            page.runJavaScript("""
                var style = document.createElement('style');
                style.innerHTML = '::-webkit-scrollbar { display: none; } body { overflow: hidden; }';
                document.head.appendChild(style);
            """)
        return


# These 2 lines have to be outside the main logic for the function decorators
app = flask.Flask(__name__)
socketio = flask_socketio.SocketIO(app, async_mode='threading')


# Function definitions
def getJSONFilesFromDirectories(models_path, scenes_path, options_path):
    json_dict = { # This will be returned, and eventually sent to the frontend javascript
        "last_error": False, # Sets the last_error back to false if it was set to true
        "models": [],
        "scenes": [],
        "options": {}
    } 

    for dirpath, dirnames, filenames in os.walk(models_path): # Look through all files in the models directory, recursively
        for filename in filenames:
            if filename.lower().endswith(".json"):
                json_object = {}
                json_file_path = os.path.join(dirpath, filename)
                try:
                    with open(json_file_path, 'r', encoding="utf-8") as json_file:
                        json_object[json_file_path] = json.load(json_file)
                    json_dict["models"].append(json_object) # Add model to the list of models in json_dict
                except json.decoder.JSONDecodeError as e:
                    print(RED + f"--- ERROR WITH {json_file_path}: {e}. JSON FILE MUST BE MANUALLY FIXED! ---\n\n")

    for dirpath, dirnames, filenames in os.walk(scenes_path): # Look through all files in the scenes directory, recursively
        for filename in filenames:
            if filename.lower().endswith(".json"):
                json_object = {}
                json_file_path = os.path.join(dirpath, filename)
                try:
                    with open(json_file_path, 'r', encoding="utf-8") as json_file:
                        json_object[json_file_path] = json.load(json_file)
                    json_dict["scenes"].append(json_object) # Add scene to the list of scenes in json_dict
                except json.decoder.JSONDecodeError as e:
                    print(RED + f"--- ERROR WITH {json_file_path}: {e}. JSON FILE MUST BE MANUALLY FIXED! ---\n\n")

    try:
        with open(options_path, "r", encoding="utf-8") as f:
            options = json.load(f)
            json_dict["options"] = options # Update options in json_dict 
    except json.decoder.JSONDecodeError as e:
        print(RED + f"--- ERROR WITH {json_file_path}: {e}. JSON FILE MUST BE MANUALLY FIXED! ---\n\n")

    if os.path.exists(ERROR_FILE_PATH):
        with open(ERROR_FILE_PATH, "r", encoding="utf-8") as f:
            json_dict["last_error"] = f.read() # If an error file exists that means the last model conversion failed, so add the message to the json_dict
        os.remove(ERROR_FILE_PATH) # Remove the error file, since it has been noticed

    return json_dict

def updateAndDeleteJSONFiles(recieved_json_data):
    generated_json_data = getJSONFilesFromDirectories(MODEL_FOLDER_PATH, SCENE_FOLDER_PATH, OPTIONS_FILE_PATH) # Generated from files on filesystem
    generated_json_paths = []
    recieved_json_paths = []
    object_types_to_check = ["models", "scenes"]

    for object_type in object_types_to_check: # Will be 'models' and 'scenes'
        for generated_json_item in generated_json_data[object_type]: # Will have structure {"[file_path]": {[json data about model/scene]}}
            for path in generated_json_item.keys():
                generated_json_paths.append(path)
        for recieved_json_item in recieved_json_data[object_type]: # recieved_json_data is recieved from frontend, will have same structure as generated
            for path, json_data in recieved_json_item.items():
                recieved_json_paths.append(path)

                if os.path.exists(path): 
                    with open(path, 'w', encoding="utf-8") as json_file:
                        json.dump(json_data, json_file, indent=4) # Update the json data with what is recieved from frontend

    for model in generated_json_data["models"]: # Delete model if path in list of files on filesystem is not in list of files recieved from frontend
        for path in model.keys():
            if path not in recieved_json_paths:        
                send2trash.send2trash(os.path.dirname(path))
    
    for scene in generated_json_data["scenes"]: # Scenes delete the path, models delete the parent folder
        for path in scene.keys():
            if path not in recieved_json_paths:
                send2trash.send2trash(path)

    with open(OPTIONS_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(recieved_json_data["options"], f, indent=4) # Update the options with what is recieved from frontend
    return

def convertFile(file_path):
    file_name, extension = os.path.splitext(file_path)
    if (extension.lower() not in SUPPORTED_EXTENSIONS) or (file_name == ""):
        print(RED + f"--- ERROR: {file_path} IS NOT A SUPPORTED FILE TYPE/FILE NAME ---\n\n")
        return

    print(BLUE + f"--- BEGINNING IMPORT OF {file_path} ---\n\n")

    try:
        result = subprocess.run(["Blender\\blender.exe", "-b", "-P", "2gltf2.py", "--", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE) # convert the file
        print(BLUE + "--- OUTPUT FROM BLENDER CONVERSION (stdout stream) ---\n\n", result.stdout.decode())
        print(BLUE + "--- OUTPUT FROM BLENDER CONVERSION (stderr stream) ---\n\n", result.stderr.decode())
    except subprocess.CalledProcessError as e:
        print(RED + f"--- ERROR OCURRED DURING BLENDER CONVERSION: {e} ---\n\n")

    print(BLUE + f"--- FINISHED IMPORT OF {file_path} ---\n\n")
    return

def convertAllFilesInDir(dir_path):
    matched_files = []
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            for ext in SUPPORTED_EXTENSIONS:
                if filename.lower().endswith(ext):
                    matched_files.append(os.path.join(dirpath, filename)) # Add model to list of matched files
                    break  # Stop checking other extensions once it confirms that the extention is valid

    for file in matched_files:
        convertFile(file)
    return

def run_flask_app():
    socketio.run(app, port=5000)
    return

@socketio.on('connect') # Happens each time the client connects, which happens when the app is started and also after each model import
def handle_socket_connect():
    json_dict = getJSONFilesFromDirectories(MODEL_FOLDER_PATH, SCENE_FOLDER_PATH, OPTIONS_FILE_PATH)
    socketio.emit('json_transfer_to_js', json_dict) # Send a dictionary to the frontend to populate the table based on what is in the json files
    return

@socketio.on('json_transfer_to_python') # Happens when data is recieved from the frontend, which happens whenever the user presses any of the buttons such as save options, update model name etc.
def handle_socket_event(data):
    updateAndDeleteJSONFiles(data) # Update and delete json files based on what the frontend says they should be
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


# Main program
if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs(MODEL_FOLDER_PATH, exist_ok=True)
    os.makedirs(SCENE_FOLDER_PATH, exist_ok=True)
    if os.path.exists(ERROR_FILE_PATH): 
        os.remove(ERROR_FILE_PATH) # Each time the program is started, the error file is removed

    if not os.path.exists(OPTIONS_FILE_PATH):
        data = {
            "cameraSensitivity": 0.5,
            "movementSpeed": 0.5,
            "positionSpeed": 0.5,
            "rotationSpeed": 0.5,
            "scaleSpeed": 0.5,
            "wandSmoothing": 20,
            "graphicsQuality": 5,
            "invertCameraControlsXAxis": False,
            "invertCameraControlsYAxis": False,
            "hideControls": False
        }
        with open(OPTIONS_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    # Configure logging
    log = logging.getLogger('werkzeug') # Werkzeug logger is used by flask
    log.setLevel(logging.ERROR) # Stop flask from logging each button click

    # Start Flask app in a separate thread
    threading.Thread(target=run_flask_app, daemon=True).start()

    # Start PyQt application
    Qapp = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(Qapp.exec())
