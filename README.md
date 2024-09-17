# 3DVisUploader
Simple UI to upload 3D models to 3DVis.
Also automatically converts models to GLTF format.

## Build Instructions

1. Install the pip modules in requirements.txt with `pip install -r requirements.txt` on Python 3.11.x. This has only been tested on 3.11.9, bpy will break on 3.12.x (I think). I recommend using a python virtual environment.
2. Copy blender from your program files into the src folder (blender's folder name should be `Blender 4.2`)
3. Change the $outputFolder variable in convert.ps1 to where you want the model to end up
4. Run `pyinstaller main.spec` from in the src folder (with the virtual environment active if you made one)