# This is unnecessary, the argument could have been passed straight in instead of as -modelPath, but
# I was trying for a while to make the argument work and chatgpt suggested this so I may as well leave it here
param (
    [Parameter(Position=0)]
    [string]$modelPath
)

# Stop script from outputting to the console
$InformationPreference = "SilentlyContinue"

# Run script from the output folder so that the resulting gltf file ends up there
$outputFolder = "..\models" # "\\CAVE-HEADNODE\data\3dvis\models"
if (!(Test-Path $outputFolder)) {
    New-Item -ItemType Directory -Path $outputFolder
}
Set-Location $outputFolder

# -b is for background mode, -P means "run python script [script]", -- seperates the args for blender from the args for python
& "..\Blender 4.2\blender.exe" -b -P "..\2gltf2_3DVis\2gltf2.py" -- $modelPath