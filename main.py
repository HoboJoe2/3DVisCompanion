import os
import subprocess

def convert_file(file_path):
    batch_file = ["convert.bat", file_path]

    # Run the batch file (copied from chatgpt, not sure what some of this means)
    try:
        result = subprocess.run(batch_file, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Output:\n", result.stdout)
        print("Errors:\n", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

convert_file("assets\\birds\\source\\bird.fbx")