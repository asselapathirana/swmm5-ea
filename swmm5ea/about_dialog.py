import about_dialog_
from PyQt4 import QtCore, QtGui
import swmm_ea_controller 
class Ui_Dialog(about_dialog_.Ui_Dialog):
    def __init__(self):
        self.body="""<?xml version="1.0" encoding="iso-8859-1"?>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
              "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
          <meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
          <title>New</title>
          <meta name="generator" content="Amaya, see http://www.w3.org/Amaya/" />
        </head>
        
        <body>
        <h1 align=\"center\">%s</h1>
        <p align=\"center\"><img src=":/res/res/logo2.gif" /> </p>
        <p align=\"center\">Evolutionary
        methods for Optimization of Urban Drainage Networks: A product for Learning.</p>
        
        <p align=\"center\">Version: %s</p>
        
        <p align=\"center\">Written by
        Assela Pathirana (2012)<br/>Released under
        the The GNU General Public License version 3.0 license text is available at
        http://www.gnu.org/licenses/gpl.html (Source Code available)</p>
        
        <p align=\"center\">contact:
        assela@pathirana.net/ a.pathirana@unesco-ihe.org</p>
        <p align=\"center\"> <img src=":/res/res/logo.gif" /> </p>
        </body>
        </html>""" % (swmm_ea_controller.NAME, swmm_ea_controller.VERSION)    
    
    def retranslateUi(self, Dialog):
         Dialog.setWindowTitle(QtGui.QApplication.translate("About %s" % (swmm_ea_controller.NAME), "About %s" % (swmm_ea_controller.NAME), None, QtGui.QApplication.UnicodeUTF8))
         self.textBrowser.setHtml(QtGui.QApplication.translate("About %s" % (swmm_ea_controller.NAME), self.body, None, QtGui.QApplication.UnicodeUTF8))    
         
