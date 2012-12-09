import sys
from cx_Freeze import setup, Executable

build_exe_options = {}

base = None
if sys.platform == "win32":
   base = "Win32GUI"

setup(  name = "gui.py",
        version = "0.1",
        description = "SWMM 5 EA Drive",
        options = {"build_exe": build_exe_options},
        executables = [Executable("gui.pyw", base=base)])
