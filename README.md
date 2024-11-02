# 3DVisCompanion
Simple GUI to upload, rename and delete 3D models, used with 3DVis. Can also rename and delete scenes, and change options in the 3DVis application.

## Install Instructions

1. Install python 3.11.x on your computer, and make sure python.exe is added to PATH. The app has only been tested on 3.11.9, because the bpy module might break on later versions. Python 3.11 can be downloaded from https://www.python.org/downloads/. 
2. Unzip the 3DVisCompanion.zip file.
3. Open a command prompt or powershell window in the `src` folder of the unzipped folder.
4. Make sure python 3.11.x is the active python version by running the `python --version` command.
5. Install the pip modules in requirements.txt by running `pip install -r requirements.txt`.
6. Change the `BASE_PATH` variable in `config.json` to the path where you want the models and scenes to be saved. The default path is configured for the CAVE2 at UniSC.
7. Run `main.py`. Alternatively, create a shortcut by right clicking on the `main.py` file and selecting `Create Shortcut`. This shortcut can
then be moved to the desktop for easier access.