import os
import shutil
from flask import Flask, redirect, url_for, render_template
import filedialpy
import subprocess

def convertFile(file_path):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    batch_file = ["convert.bat", file_path]

    if file_path.lower().endswith(".glb") or file_path.lower().endswith(".gltf"):
        shutil.copy(file_path, "..\\output")
    else:
        # Run the batch file (copied from chatgpt, not sure what some of this means)
        try:
            result = subprocess.run(batch_file, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print("Output:\n", result.stdout)
            print("Errors:\n", result.stderr)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
    return

def convertAllFilesInDir(dir_path):
    matched_files = []
    extensions = ['.abc', '.blend', '.dae', '.fbx', '.glb', '.gltf', '.obj', '.ply', '.stl', '.usd', '.usda', '.usdc', '.wrl', '.x3d']
    for dirpath, dirnames, filenames in os.walk(dir_path):
        print(f"{dirpath}, {dirnames}, {filenames}")
        for filename in filenames:
            for ext in extensions:
                if filename.lower().endswith(ext):
                    matched_files.append(os.path.join(dirpath, filename))
                    break  # Stop checking other extensions once a match is found
    print(matched_files)
    for file in matched_files:
        convertFile(file)
    return


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/button_one', methods=['POST'])
def button_one():
    path = filedialpy.openFile()
    print("path is ", path)
    convertFile(path)  # Call the first function when Button 1 is pressed
    return redirect(url_for('index'))  # Redirect back to the homepage

@app.route('/button_two', methods=['POST'])
def button_two():
    dir = filedialpy.openDir()
    convertAllFilesInDir(dir)  # Call the second function when Button 2 is pressed
    return redirect(url_for('index'))  # Redirect back to the homepage

if __name__ == '__main__':
    app.run(debug=True)