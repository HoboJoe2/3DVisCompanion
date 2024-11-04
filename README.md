# 3DVisCompanion
Simple GUI to upload, rename and delete 3D models, used with 3DVis. Can also rename and delete scenes, and change options in the 3DVis application.

## Install Instructions

1. Download the latest release from the releases section in GitHub
2. Install python 3.11.9 on your computer (later versions won't work), and make sure python.exe is added to PATH. Python 3.11.9 can be downloaded from https://www.python.org/downloads/release/python-3119/. 
3. Unzip the 3DVisCompanion.zip file.
4. Open a command prompt or powershell window in the `src` folder of the unzipped folder.
5. Make sure python 3.11.x is the active python version by running the `python --version` command.
6. Install the pip modules in requirements.txt by running `pip install -r requirements.txt`.
7. Change the `BASE_PATH` variable in `config.json` to the path where you want the models and scenes to be saved. The default path is configured for the CAVE2 at UniSC.
8. Run `main.py`. Alternatively, create a shortcut by right clicking on the `main.py` file and selecting `Create Shortcut`. This shortcut can
then be moved to the desktop for easier access.