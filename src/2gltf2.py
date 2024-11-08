# 
# The MIT License (MIT)
#
# Copyright (c) since 2017 UX3D GmbH
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import bpy
import os
import sys
import datetime
import json

# Global variables
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_PATH = os.path.abspath(os.path.join(SCRIPT_DIR, 'config.json'))

with open(CONFIG_FILE_PATH, "r", encoding="utf-8") as f:
    loaded_json = json.load(f)
    BASE_PATH = loaded_json["base_path"]

MODEL_FOLDER_PATH = os.path.join(BASE_PATH + "\\models")


# Function definitions
def generateUniqueFolderName(model_name):
    return f"""{model_name}_{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")}"""


# Main program
try: # Try except block is necessary to write an error file if conversion fails. The conversion file is read by main.py
    current_argument = sys.argv[-1] # Will be the file path to the model to convert

    root, current_extension = os.path.splitext(current_argument)
    current_basename = os.path.basename(root)

    bpy.ops.wm.read_factory_settings(use_empty=True) # Resets blenders internal scene to an empty environment to help with conversion

    match current_extension:
        case ".gltf" | ".glb":
            bpy.ops.import_scene.gltf(filepath=current_argument)

        case ".abc":
            bpy.ops.wm.alembic_import(filepath=current_argument)

        case ".blend":
            bpy.ops.wm.open_mainfile(filepath=current_argument)

        case ".dae":
            bpy.ops.wm.collada_import(filepath=current_argument)

        case ".fbx":
            bpy.ops.import_scene.fbx(filepath=current_argument, use_anim=True, use_image_search=True)

        case ".obj":
            bpy.ops.wm.obj_import(filepath=current_argument)

        case ".ply":
            bpy.ops.wm.ply_import(filepath=current_argument)

        case ".stl":
            bpy.ops.wm.stl_import(filepath=current_argument)

        case ".usd" | ".usda" | ".usdc" | ".usdz":
            bpy.ops.wm.usd_import(filepath=current_argument)

    model_folder_name = generateUniqueFolderName(f"{current_basename}{current_extension}") # will be a unique name based on the current time
    export_dir = f"{MODEL_FOLDER_PATH}\\{model_folder_name}" 
    os.makedirs(export_dir, exist_ok=True) # Create the model folder

    bpy.ops.export_scene.gltf(filepath=f"{export_dir}\\scene.gltf", export_format="GLTF_SEPARATE", export_texture_dir="textures", export_draco_mesh_compression_enable=False) # Render/export the converted model

    json_metadata = f"""
    {{
        "originalModelName": "{current_basename}",
        "originalExtension": "{current_extension}",
        "modelDisplayName": "{current_basename}",
        "modelCategory": ""
    }}
    """

    with open(f"{export_dir}\\metadata.json", "w", encoding="utf-8") as f:
        f.write(json_metadata) # Write the metadata file in the models folder

except Exception as e:
    with open(os.path.join(MODEL_FOLDER_PATH, "last_error.txt"), "w", encoding="utf-8") as f:
        f.write(str(e))
