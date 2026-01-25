import os
import PyInstaller.__main__
import customtkinter
import platform

# Get the location of customtkinter to add it to the build
ctk_path = os.path.dirname(customtkinter.__file__)

# Determine separator based on OS (though we are targeting macOS here)
# Windows uses ';', macOS/Linux uses ':'
separator = ';' if platform.system() == 'Windows' else ':'

# Define PyInstaller arguments
args = [
    'YouGotIt.py',                  # Script to build
    '--name=YouGotIt',              # Name of the executable/app
    '--noconfirm',                  # Replace existing spec/dist files
    '--onedir',                     # Create a directory-based bundle (required for proper macOS .app bundles)
    '--windowed',                   # Create a windowed app (macOS .app)
    '--clean',                      # Clean cache
    f'--add-data={ctk_path}{separator}customtkinter', # Include customtkinter assets
]

print("Starting build for macOS...")
print(f"Including customtkinter from: {ctk_path}")
PyInstaller.__main__.run(args)
print("Build complete. Check the 'dist' folder for YouGotIt.app")
