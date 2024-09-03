# 3DVisUploader

Simple UI to upload 3D models to 3DVis.
Also automatically converts models to GLTF format.


chatgpt explanation of batch file for future reference:
Let's break down this batch script line by line:

1. ECHO OFF
Explanation: This command turns off the display of commands in the command prompt. When ECHO OFF is used, the commands themselves won't be shown on the screen, only the output will be displayed.
2. IF "%1"=="" GOTO USAGE
Explanation: This line checks if the first argument passed to the script (%1) is empty (""). If no argument is provided, the script will jump to the :USAGE label.
3. "C:/Program Files/Blender Foundation/Blender 3.5/blender.exe" -b -P 2gltf2.py -- %1
Explanation: This line runs Blender (located at the specified path) in background mode (-b), and executes a Python script named 2gltf2.py. The -- indicates the end of Blender command-line options, and %1 passes the first argument provided to the batch script to the Python script. Essentially, this line converts the file specified by the argument into glTF 2.0 format using Blender.
4. GOTO END
Explanation: After executing the command in the previous line, this line directs the script to skip the :USAGE section and go directly to the :END label.
5. :USAGE
Explanation: This is a label used to define a section of the script. Labels are used as markers within the script that you can jump to using the GOTO command.
6. ECHO To glTF 2.0 converter.
Explanation: This line displays the text "To glTF 2.0 converter." in the command prompt. It's part of the usage instructions shown to the user if no argument is provided.
7. ECHO Supported file formats: .abc .blend .dae .fbx. .obj .ply .stl .usd .wrl .x3d
Explanation: This line displays the supported file formats that can be converted to glTF 2.0 using this script.
8. ECHO.
Explanation: This command outputs a blank line to the command prompt. It's used to add spacing between lines for better readability.
9. ECHO 2gltf2.bat [filename]
Explanation: This line shows the correct usage of the batch script, indicating that the user should run it with a filename as an argument.
10. :END
Explanation: This is another label that marks the end of the script. When the script reaches this label, it stops executing.
Summary:
The script is a batch file to convert various 3D file formats to glTF 2.0 using Blender. If no file is provided as an argument, it shows usage instructions. If a file is provided, it runs Blender with a Python script to perform the conversion.