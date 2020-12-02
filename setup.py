## This file will only be used for get a stable version usable for Windows users.
## Don't try to make a build for others OS with this file.
## You can use this file for testing the build of your ressource before pushing your modification into the main branches.
## It is a "non-official" build

from cx_Freeze import setup, Executable

setup(
    name = "Burokamerad - Pixel",
    version = "0.1",
    description = "Build tester for Windows OS - x64"
    executables = [Executable("your_file.py", base="Win32GUI", targetName="Pixel.exe")]
)