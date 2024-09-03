import os
import shutil
import time
import dearpygui.dearpygui as dpg
import subprocess

def convertFile(file_path):
    batch_file = ["convert.bat", file_path]

    if file_path.lower().endswith(".glb") or file_path.lower().endswith(".gltf"):
        shutil.copy(file_path, "output")
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

def runGUI():
    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=600, height=300)
    
    def callback(sender, app_data, user_data):
        print("Sender: ", sender)
        print("App Data: ", app_data)
    
    def uploadFileCallback(sender, app_data):
        print(f"sender is: {sender}")
        print(f"app_data is: {app_data}")
        dpg.show_item("file_dialog_id")
   

    def uploadFolderCallback(sender, app_data):
        print(f"sender is: {sender}")
        print(f"app_data is: {app_data}")

    with dpg.file_dialog(directory_selector=False, show=False, callback=callback, id="file_dialog_id", width=700 ,height=400):
        dpg.add_file_extension(".*")

    with dpg.window(label="Example Window"):
        dpg.add_text("Hello, world")
        dpg.add_button(label="Save")
        dpg.add_input_text(label="string", default_value="Quick brown fox")
        dpg.add_slider_float(label="float", default_value=0.273, max_value=1)
        dpg.add_button(label="Upload File", callback=uploadFileCallback)
        dpg.add_button(label="Upload Folder", callback=uploadFolderCallback)

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

runGUI()