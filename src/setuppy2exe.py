from distutils.core import setup
import py2exe

from distutils.filelist import findall
import os
import numpy #, matplotlib
import pygtk

origIsSystemDLL = py2exe.build_exe.isSystemDLL
def isSystemDLL(pathname):
        if os.path.basename(pathname).lower() in ("msvcp90.dll", "libxml2-2.dll", "mfc90.dll"):
                return 0
        return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL



#matplotlibdatadir = matplotlib.get_data_path()
#matplotlibdata = findall(matplotlibdatadir)
#matplotlibdata_files = []
#for f in matplotlibdata:
#    dirname = os.path.join('matplotlibdata', f[len(matplotlibdatadir)+1:])
#    matplotlibdata_files.append((os.path.split(dirname)[0], [f]))
#
packages=['numpy','pytz', 'pygtk' ]
includes=['gio', 'pangocairo', 'atk', 'pygtk']
excludes=[]
setup(
    console=['swmm5ec.py'],
    options={
             'py2exe': {"compressed": 2, 
                          "optimize": 2,
                        'packages' : packages,
			'includes': includes,
                        'excludes': excludes
                       }
            },
    #data_files=matplotlib.get_py2exe_datafiles(),
)