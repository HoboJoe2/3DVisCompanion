# 3DVisCompanion
Simple GUI to upload, rename and delete 3D models, used with 3DVis. Can also rename and delete scenes, and change options in the 3DVis application.

## Build Instructions

1. Install python 3.11.x on your computer. The app has only been tested on 3.11.9, because the bpy module might break on later versions. Python 3.11 can be downloaded from https://www.python.org/downloads/.
2. Install the pip modules in requirements.txt by running `pip install -r requirements.txt` in a command prompt or powershell window in the `src` folder. 
3. Change the `BASE_PATH` variable in `main.py` and `2gltf2.py` to the path where you want the models and scenes to be saved. This can be achieved by right clicking on the files and selecting 'Open With...', then choosing a text editor of your choice. The default paths are configured for the CAVE2 at UniSC.
4. Run `main.py`. Alternatively, create a shortcut by right clicking on the `main.py` file and selecting `Create Shortcut`. This shortcut can
then be moved to the desktop for easier access.