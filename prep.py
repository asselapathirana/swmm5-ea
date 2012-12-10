#!/usr/bin/env python
import subprocess, os
import PyQt4
PYUIC="python "+os.path.dirname(PyQt4.__file__)+os.sep+os.sep+"uic"+os.sep+os.sep+"pyuic.py"
PYRCC=os.path.dirname(PyQt4.__file__)+os.sep+os.sep+"bin"+os.sep+os.sep+"pyrcc4"

def _call(cmd):
 print cmd
 subprocess.call(cmd, shell=True)

def _ui2py(name):
 _call(PYUIC+"  qt" + os.sep + os.sep + name+".ui"+" -o  src" + os.sep+os.sep+name+".py")

_call("python service"+os.sep+os.sep+"qrcgen.py  res res")
#now convert that to python file 
_call(PYRCC+" -o src/res_rc.py res.qrc")
_ui2py("mainwindow_")
_ui2py("parameters_dialog_")
_ui2py("swmmedit_dialog_")
_ui2py("about_dialog_")

#_call(PYUIC+" -o src/res_rc.py res.qrc")
#_call (PYUIC+" "+nativepath(qt/mainwindow_.ui) -o src/mainwindow_.py")
#_call (PYUIC+"  qt/parameters_dialog_.ui -o src/parameters_dialog_.py")
#_call (PYUIC+"  qt/swmmedit_dialog_.ui -o src/swmmedit_dialog_.py")
#_call (PYUIC+"  qt/about_dialog_.ui -o src/about_dialog_.py")


