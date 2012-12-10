# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\\swmmedit_dialog_.ui'
#
# Created: Mon Dec 10 19:54:00 2012
#      by: PyQt4 UI code generator 4.8.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(967, 638)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(450, 570, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.layoutWidget = QtGui.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(50, 20, 871, 541))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.editor = QtGui.QTextEdit(self.layoutWidget)
        self.editor.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.editor.setObjectName(_fromUtf8("editor"))
        self.horizontalLayout.addWidget(self.editor)
        self.frame = QtGui.QFrame(self.layoutWidget)
        self.frame.setMaximumSize(QtCore.QSize(200, 16777215))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.addvar = QtGui.QPushButton(self.frame)
        self.addvar.setEnabled(False)
        self.addvar.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.addvar.setObjectName(_fromUtf8("addvar"))
        self.gridLayout.addWidget(self.addvar, 0, 0, 1, 1)
        self.nextvar = QtGui.QLineEdit(self.frame)
        self.nextvar.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.nextvar.setReadOnly(False)
        self.nextvar.setObjectName(_fromUtf8("nextvar"))
        self.gridLayout.addWidget(self.nextvar, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.update = QtGui.QPushButton(self.frame)
        self.update.setObjectName(_fromUtf8("update"))
        self.gridLayout_2.addWidget(self.update, 1, 0, 1, 1)
        self.slotdisplay = QtGui.QTextEdit(self.frame)
        self.slotdisplay.setReadOnly(True)
        self.slotdisplay.setObjectName(_fromUtf8("slotdisplay"))
        self.gridLayout_2.addWidget(self.slotdisplay, 2, 0, 1, 1)
        self.horizontalLayout.addWidget(self.frame)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.addvar.setText(QtGui.QApplication.translate("Dialog", "&Add Var:", None, QtGui.QApplication.UnicodeUTF8))
        self.nextvar.setText(QtGui.QApplication.translate("Dialog", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.update.setText(QtGui.QApplication.translate("Dialog", "Update Formulas", None, QtGui.QApplication.UnicodeUTF8))

