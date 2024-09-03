import os
import subprocess

# Replace 'path_to_your_batch_file.bat' with the path to your batch file
batch_file = "convert.bat"

# Run the batch file
try:
    result = subprocess.run(batch_file, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("Output:\n", result.stdout)
    print("Errors:\n", result.stderr)
except subprocess.CalledProcessError as e:
    print(f"Error occurred: {e}")