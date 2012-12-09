import sys
from cx_Freeze import setup, Executable

from disthelpers_old import (remove_build_dist, get_default_excludes,
                         get_default_dll_excludes, create_vs2008_data_files,
                         add_modules)

# Removing old build/dist folders
remove_build_dist()

# Including/excluding DLLs and Python modules
EXCLUDES = get_default_excludes()
INCLUDES = []
DLL_EXCLUDES = get_default_dll_excludes()
DATA_FILES = create_vs2008_data_files()

# Configuring/including Python modules
add_modules(('PyQt4', 'guidata', 'guiqwt'), DATA_FILES, INCLUDES, EXCLUDES)

from cx_Freeze import setup, Executable
 
exe = Executable(
    script="swmm5ec.pyw",
    base="Win32GUI",
    )
 
setup(
    name = "wxSampleApp",
    version = "0.1",
    description = "An example wxPython script",
    executables = [exe]
    )