from cx_Freeze import setup, Executable
import os

include_files = [
    ("components", "components")
]

build_options = {
}

setup(
    name="ArchLinuxInstaller",
    version="1.0",
    description="Arch Linux Installer GUI",
    # options={"build_exe": build_options},
    executables=[
        Executable("main.py", target_name="ArchLinuxInstaller.exe", base="Win32GUI")
    ]
)
