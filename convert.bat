:: Run script from the output folder so that the resulting glb file ends up there
cd output

:: -b is for background mode, -P means "run python script [script]", -- seperates the args for blender from the args for python, %1 is the arg
:: intended for 2gltf2.py (which is the argument passed into this script)
"..\Blender 4.2\blender.exe" -b -P "..\2gltf2\2gltf2.py" -- "..\%1"