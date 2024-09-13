:: Stop script from outputting to the console
@echo off

:: Run script from the output folder so that the resulting glb file ends up there
mkdir "\\CAVE-HEADNODE\data\3dvis\models"
cd "\\CAVE-HEADNODE\data\3dvis\models"
::mkdir "..\models"
::cd "..\models"

:: -b is for background mode, -P means "run python script [script]", -- seperates the args for blender from the args for python, %1 is the arg
:: intended for 2gltf2.py (which is the argument passed into this script)
"..\Blender 4.2\blender.exe" --log-level -1 -b -P "..\2gltf2_3DVis\2gltf2.py" -- %1