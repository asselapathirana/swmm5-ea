#!/bin/bash
cat ../src/mainwindow_.py|grep "= QtGui.QAction"|sed "s/self.//g; s/= QtGui.QAction(MainWindow)//g"|awk '{print     "\n     #" $1 "\n     @QtCore.pyqtSignature(\"\")\n     def on_" $1 "_triggered(self,checed=None):\n          print \"" $1 "triggered\""    }'
