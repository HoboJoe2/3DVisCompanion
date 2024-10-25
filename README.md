# 3DVisCompanion
Simple UI to upload, rename and delete 3D models, used with 3DVis. Can also rename and delete scenes.

## Build Instructions

1. Install the pip modules in requirements.txt with `pip install -r requirements.txt` on Python 3.11.x. This has only been tested on 3.11.9, bpy will break on 3.12.x (I think).
2. Change the `MODEL_FOLDER_PATH` and `SCENE_FOLDER_PATH` variables in main.py and 2gltf2.py to your desired paths.
3. Run `python main.py`.