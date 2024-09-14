import os
from flask import Flask, redirect, url_for, render_template
import filedialpy
import subprocess
import threading
import webbrowser

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def convertFile(file_path):
    print(f"--- BEGINNING IMPORT OF {file_path} ---")
    os.chdir(SCRIPT_DIR)

    # Run the batch file (copied from chatgpt, not sure what some of this means.)
    try:
        result = subprocess.run(f"powershell -File convert.ps1 -arg1 {file_path}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("--- STANDARD OUTPUT FROM POWERSHELL FILE ---\n", result.stdout.decode())
        print("--- STANDARD ERROR OUTPUT FROM BATCH FILE ---\n", result.stderr.decode())
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during powershell file execution: {e}")
    return

def convertAllFilesInDir(dir_path):
    matched_files = []
    extensions = ['.abc', '.blend', '.dae', '.fbx', '.glb', '.gltf', '.obj', '.ply', '.stl', '.usd', '.usda', '.usdc', '.wrl', '.x3d']
    for dirpath, dirnames, filenames in os.walk(dir_path):
        for filename in filenames:
            for ext in extensions:
                if filename.lower().endswith(ext):
                    matched_files.append(os.path.join(dirpath, filename))
                    break  # Stop checking other extensions once a match is found
    print("Found the following files:", matched_files)
    for file in matched_files:
        convertFile(file)
    return

def open_browser():
    webbrowser.open("http://127.0.0.1:5000/")
    return

app = Flask(__name__)

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

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run(debug=False)
