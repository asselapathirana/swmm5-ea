from distutils.core import setup
import py2exe, matplotlib

from distutils.filelist import findall
import os
import pygtk

origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
        if os.path.basename(pathname).lower() in ("msvcp90.dll", "libxml2-2.dll", "mfc90.dll"):
                return 0
        return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL



matplotlibdatadir = matplotlib.get_data_path()
matplotlibdata = findall(matplotlibdatadir)
matplotlibdata_files = []
for f in matplotlibdata:
    dirname = os.path.join('matplotlibdata', f[len(matplotlibdatadir)+1:])
    matplotlibdata_files.append((os.path.split(dirname)[0], [f]))


setup(
    windows=['gui.pyw'],
    options={
             'py2exe': {
                        'packages' : ['easygui' ],
			'includes': [],
                       }
            },
    data_files=matplotlib.get_py2exe_datafiles(),
)