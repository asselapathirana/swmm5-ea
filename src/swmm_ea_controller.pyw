from PyQt4 import QtCore, QtGui
import guiqwt.plot
import os, shutil, sys

import mainwindow
import swmmeaproject

class EmittingStream(QtCore.QObject):

    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


class swmmeacontroller():
    def __init__(self, project=None):
        self.app = QtGui.QApplication(sys.argv)
        self.ui = mainwindow.MainWindow(self)
        self.project=None
        # now redirect all print statements to the 
        sys.stdout = EmittingStream(textWritten=self.ui.normalOutputWritten)
        sys.stderr = EmittingStream(textWritten=self.ui.normalErrorWritten)        
        self.ups()

    def initialize_optimization(self):
        self.project.initialize_optimization()
 
    def pause_optimization(self):
        self.project.pause_optimization()
        
    def stop_optimization(self):
        self.project.stop_optimization()
        
    def run_optimization(self):
        self.project.run_optimization()
    
    
    def show(self):
        self.ui.show()
        self.app.exec_()
        
    def NewProject(self):
        self.project=swmmeaproject.Project()
        self.project.load()
        self.ups()
    def LoadProject(self, yamlfile):       
        self.project=swmmeaproject.Project(dirname=os.path.dirname(yamlfile))
        self.ups()
        
    def get_slotted_data(self):
        sf=self.project.swmmfilename+"_"
        if os.path.exists(self.project.dirname+os.sep+sf):
            reply = QtGui.QMessageBox.information(self.ui, 'Caution ',
                                               "There is a file named: "+ sf + " in " + self.project.dirname + 
                                               " project directory?. This file will be opend."+
                                               " In the next window carefully look whether this is the file you expect."+
                                               "If it is not, manually delete the file "+sf+" and try this action again.",  
                                               QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
            self.project.slotted_swmmfilename=sf
        self.ups()
        return self.project.getSlottedData()
            
            
            
        
    def saveSlottedSwmmfile(self,text):
        sf=self.project.swmmfilename+"_"
        fname=self.project.dirname+os.sep+sf
        if  os.path.exists(fname):
            reply = QtGui.QMessageBox.warning(self.ui, 'Overwrite ',
                                   "Do you want to overwrite the existing file "+ sf + " in " + self.project.dirname + " project directory?\n (If 'No' all the edits will be lost!)", QtGui.QMessageBox.Yes | 
                                   QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if not  reply == QtGui.QMessageBox.Yes:
                return False
        self.project.write_slotted_swmm_file(fname, text)
        reply = QtGui.QMessageBox.information(self.ui, 'swmmfile with slots :'+sf+".", "File : "+sf+ " saved.", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)         
        self.ups()
        return True


        
    def LoadSwmmFile(self,swmmfile):
        dr=self.project.dirname
        base=os.path.basename(swmmfile)  
        newname=dr+os.sep+base
        if not self._samefile(swmmfile,newname):
            if  os.path.exists(newname):
                reply = QtGui.QMessageBox.warning(self.ui, 'Overwrite ',
                       "Do you want to overwrite the existing file "+ base + " in " + dr + " project directory?", QtGui.QMessageBox.Yes | 
                       QtGui.QMessageBox.No, QtGui.QMessageBox.No)
                if not  reply == QtGui.QMessageBox.Yes:
                    return
            shutil.copyfile(swmmfile,newname)
        if(self.project.setswmmfile(base)):
            reply = QtGui.QMessageBox.information(self.ui, 'swmmfile :'+base,
                                   base +" set as the swmm file of project "+dr+".", QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok) 
        self.ups()
            
    def _samefile(self,src, dst):
        # copied form shutil
        # Macintosh, Unix.
        if hasattr(os.path, 'samefile'):
            try:
                return os.path.samefile(src, dst)
            except OSError:
                return False
    
        # All other platforms: check for same pathname.
        return (os.path.normcase(os.path.abspath(src)) ==
                os.path.normcase(os.path.abspath(dst)))        
        
    def getparams(self):
        self.ups()
        return self.project.parameters
    def setparams(self,params):
        self.project.parameters.setvalues(params)
        self.ups()
    def saveproject(self, path=None):
        if path : 
            self.project=self.project.copy(path)
        self.project.save()
        self.ups()

    def ups(self):
        d,s,f=None,None,None
        if self.project:
            d,s,f=self.project.dirname, self.project.swmmfilename, self.project.slotted_swmmfilename
        
        self.ui.updateStatus(d,s,f)
    
if __name__ == "__main__":
    import sys
    sc=swmmeacontroller()
    sys.exit(sc.show())
        