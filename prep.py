#!/usr/bin/env python
import subprocess, os
import PyQt4
PYUIC="python "+os.path.dirname(PyQt4.__file__)+os.sep+os.sep+"uic"+os.sep+os.sep+"pyuic.py"
PYRCC=os.path.dirname(PyQt4.__file__)+os.sep+os.sep+"bin"+os.sep+os.sep+"pyrcc4"
if os.name=='posix':
   PYUIC='pyuic4'
   PYRCC='pyrcc4'
def _call(cmd):
 print cmd
 subprocess.call(cmd, shell=True)

def _ui2py(name):
 _call(PYUIC+"  qt" + os.sep + os.sep + name+".ui"+" -o  swmm5ea" + os.sep+os.sep+name+".py")


if __name__=="__main__":	
 _call("python service"+os.sep+os.sep+"qrcgen.py  res res")
 #now convert that to python file 
 _call(PYRCC+" -o swmm5ea/res_rc.py res.qrc")
 _ui2py("mainwindow_")
 _ui2py("parameters_dialog_")
 _ui2py("swmmedit_dialog_")
 _ui2py("about_dialog_")
 
 # forget files listed in .hgignore
 _call('hg forget "set:hgignore() and not ignored()" ')



