from PyQt4 import QtCore, QtGui
import guiqwt.plot

import mainwindow_
import swmmedit_dialog
import swmm_ea_controller
import parameters_dialog
import sys
import about_dialog

class MainWindow(QtGui.QMainWindow,
mainwindow_.Ui_SWMM5EA):
    def __init__(self, controller=None):
        super(QtGui.QMainWindow, self).__init__() # because of multiple inheritance, here we call the __init__ of  QtGui.QMainWindow
        #first

        self.setupUi(self) # extremely important for on_<object>_<trigger> type (auto-connnect) to work. 
        self.curve = guiqwt.plot.CurveWidget(self.curve_window,"Convergence Plot","Generation Number", "Cost","","")#QtGui.QWidget(self.dockWidgetContents)
        self.curve.plot.set_antialiasing(True)
        self.addguiqwtToolbar_and_context_menu()
        self.gridLayout_2.addWidget(self.curve, 0, 0, 1, 1)   
        self.controller=controller
        if not controller: self.controller=swmm_ea_controller.swmmeacontroller()
        self.status1=QtGui.QLabel()
        self.statusBar().addWidget(self.status1,10)
        self.status2=QtGui.QLabel()
        self.statusBar().addWidget(self.status2,5)        
        self.status3=QtGui.QLabel()
        self.statusBar().addWidget(self.status3,5)  

        
    def addguiqwtToolbar_and_context_menu(self):
        toolbar=self.addToolBar("Graph Tools")
        self.curve.add_toolbar(toolbar, "default")
        self.curve.register_all_curve_tools()        



    def updateStatus(self,project=None, swmmfile=None, slottedfile=None, run_status=0, ytitle="Cost", xtitle=None, plottitle=None,zoomextent=False):
        self.curve.plot.set_titles(plottitle,xtitle,ytitle)
        #print run_status
        self.status1.setText("Project:"+(project or ""))
        #print "here", self
        self.status2.setText("Swmm file:"+(swmmfile or ""))
        self.status3.setText("Sloted sf:"+(slottedfile or ""))
        # 0 - project loaded
        # 1 - swmm loaded
        # 2 - slot loaded
        #self.action_NewProject.setEnabled(False)
        #self.action_OpenProject.setEnabled(False) 
        self.actionSave_As.setEnabled(False)
        self.action_EditProject.setEnabled(False)
        self.action_SaveProject.setEnabled(False)        
        self.action_Load_SWMM_File.setEnabled(False)
        self.action_Insert_Slots.setEnabled(False)
        self.actionRun_Optimization.setEnabled(False)
        self.actionPause_Optimization.setEnabled(False)
        self.actionStop_Optimization.setEnabled(False)     
        self.actionInitialize_model.setEnabled(False)
        
        # just set the state
        self.action_Zoom_Extent.setChecked(zoomextent)
        if project:
            # 0
            self.actionSave_As.setEnabled(True)
            self.action_EditProject.setEnabled(True)
            self.action_SaveProject.setEnabled(True)        
            self.action_Load_SWMM_File.setEnabled(True)
        if swmmfile:
            # 1
            self.action_Insert_Slots.setEnabled(True)
        if slottedfile:
            # 2
            self.actionInitialize_model.setEnabled(True)
            
            if run_status==swmm_ea_controller.RUN_STATUS_TOBEINITED:
                self.actionPause_Optimization.setEnabled(False)
                self.actionStop_Optimization.setEnabled(False)
                self.actionInitialize_model.setEnabled(True) 
                self.actionRun_Optimization.setEnabled(False)                
                pass
            if run_status==swmm_ea_controller.RUN_STATUS_INITED:
                self.actionPause_Optimization.setEnabled(False)
                self.actionStop_Optimization.setEnabled(False)
                self.actionInitialize_model.setEnabled(False) 
                self.actionRun_Optimization.setEnabled(True)                
                pass
            
            if run_status==swmm_ea_controller.RUN_STATUS_RUNNING:
                self.actionPause_Optimization.setEnabled(True)
                self.actionPause_Optimization.setChecked(False)
                self.actionStop_Optimization.setEnabled(True)
                self.actionInitialize_model.setEnabled(False) 
                self.actionRun_Optimization.setEnabled(False)                
                pass            
            if run_status==swmm_ea_controller.RUN_STATUS_PAUSED:
                self.actionPause_Optimization.setEnabled(True)
                self.actionStop_Optimization.setEnabled(False)
                self.actionInitialize_model.setEnabled(False) 
                self.actionRun_Optimization.setEnabled(False)                
                pass            
            



    #Exit
    @QtCore.pyqtSignature("")
    def on_actionExit_triggered(self,checed=None):
        self.close()
        
    #action_Zoom_Extent
    @QtCore.pyqtSignature("bool")    
    def on_action_Zoom_Extent_toggled(self, checked=False):
        self.controller.zoomState(checked)
        
    #actionInitialize_model
    @QtCore.pyqtSignature("")
    def on_actionInitialize_model_triggered(self,checed=None):
        self.controller.initialize_optimization()


    #actionRun_Optimization
    @QtCore.pyqtSignature("")
    def on_actionRun_Optimization_triggered(self,checed=None):
        self.controller.run_optimization()

    #actionPause_Optimization
    @QtCore.pyqtSignature("bool")
    def on_actionPause_Optimization_toggled (self,checked):
        self.controller.pause_optimization(checked)

    #actionStop_Optimization
    @QtCore.pyqtSignature("")
    def on_actionStop_Optimization_triggered(self,checed=None):
        self.controller.stop_optimization()


    #action_Insert_Slots
    @QtCore.pyqtSignature("")
    def on_action_Insert_Slots_triggered(self,checed=None):
        if(self.controller.project.swmmfilename):
            tx=self.controller.get_slotted_data()
            if not tx:
                return 
            ids=self.controller.project.get_ids()
            if not ids:
                print "Problem retriving ids of objects. Check SWMM file."
                return
            self.slot_dialog_ui = swmmedit_dialog.Ui_swmmedit_dialog(self.controller, ids, text=tx)
            self.slot_dialog_ui.show()
            if QtGui.QDialog.Accepted==self.slot_dialog_ui.exec_():
                self.controller.saveSlottedSwmmfile(self.slot_dialog_ui.text)
                self.controller.project.parameters.calfile=self.slot_dialog_ui.calfile_
                self.controller.project.parameters.caltype=self.slot_dialog_ui.caltype_
                self.controller.project.parameters.calid=self.slot_dialog_ui.calid_
                self.controller.saveproject()
                

    #action_Load_SWMM_File
    @QtCore.pyqtSignature("")
    def on_action_Load_SWMM_File_triggered(self,checed=None):
        dr=self.controller.settings.value("lastswmmfile").toString()
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                                                     "Open a SWMM input file to copy to project", dr ,
                                                     "*.inp")
        if(fileName):
            self.controller.LoadSwmmFile(str(self.qt_fix_path(fileName))) 
            self.controller.settings.setValue("lastswmmfile",fileName)

    def qt_fix_path(self,path):
        return QtCore.QDir.toNativeSeparators(path)
    
    #action_EditProject
    @QtCore.pyqtSignature("")
    def on_action_EditProject_triggered(self,checed=None):
        self.parametersdialog = parameters_dialog.Ui_parameters_dialog()
        self.parametersdialog.setDataMap(self.controller.getparams())
        self.parametersdialog.show()
        if QtGui.QDialog.Accepted==self.parametersdialog.exec_():
            self.controller.setparams(self.parametersdialog.getDataMap())



    #actionSave_As
    @QtCore.pyqtSignature("")
    def on_actionSave_As_triggered(self,checed=None):

        fl=QtGui.QFileDialog.getSaveFileName(self, "New Project Direcoty", options = QtGui.QFileDialog.ShowDirsOnly, filter="Directory")
        if str:
            if(self.controller.saveproject(str(self.qt_fix_path(fl)) )):
                self.controller.settings.setValue("lastprojectloc",fl)            
        return 
        #dlg=QtGui.QFileDialog(self,caption="New directory");
        #dlg.setFileMode(QtGui.QFileDialog.AnyFile)
        #dlg.setOption(QtGui.QFileDialog.ShowDirsOnly)
        #dlg.setOption(QtGui.QFileDialog.DontUseNativeDialog)
        #dlg.setNameFilter("Directory name")
        #dlg.setLabelText(QtGui.QFileDialog.FileName,"Directory")
        #dlg.setLabelText(QtGui.QFileDialog.Accept,"Create")
        #dlg.setLabelText(QtGui.QFileDialog.Reject,"Cancel")
        #dlg.setLabelText(QtGui.QFileDialog.FileType,"")
        #dlg.setLabelText(QtGui.QFileDialog.LookIn,"Project Directory")
        
        ##dlg.selectFile(self.controller.settings.value("lastprojectloc").toString())
        ##newdir=QtGui.QFileDialog.getSaveFileName(self,
        ##                                         "Save project as", ".", "*")
        #if dlg.exec_():
            #if(self.controller.saveproject(str(self.qt_fix_path(dlg.selectedFiles()[0])) )):
                #self.controller.settings.setValue("lastprojectloc",dlg.selectedFiles()[0])


    #action_SaveProject
    @QtCore.pyqtSignature("")
    def on_action_SaveProject_triggered(self,checed=None):
        self.controller.saveproject()


    #action_NewProject
    @QtCore.pyqtSignature("")
    def on_action_NewProject_triggered(self,checed=None):
        self.controller.NewProject()

    #action_OpenProject
    @QtCore.pyqtSignature("")
    def on_action_OpenProject_triggered(self,checed=None):
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                                                     "Open project", self.controller.settings.value("lastprojectloc").toString(), "param.yaml")   
        if(fileName):
            self.controller.LoadProject(str(self.qt_fix_path(fileName))) 
            self.controller.settings.setValue("lastprojectloc",fileName)
        

    #actionHelp_About
    @QtCore.pyqtSignature("")
    def on_actionHelp_About_triggered(self,checed=None):
        self.about_dialog_window = QtGui.QDialog()
        self.about_dialog_ui = about_dialog.Ui_Dialog()
        self.about_dialog_ui.setupUi(self.about_dialog_window)
        self.about_dialog_window.exec_()    


    #actionHelp_Users_Guide
    @QtCore.pyqtSignature("")
    def on_actionHelp_Users_Guide_triggered(self,checed=None):
        #reply = QtGui.QMessageBox.information(self, "Help","Please refer to http://assela.pathirana.net for help using this application.",  
        #                                      QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
        self.controller.showHelp()


    def normalOutputWritten(self, text):
        """Append text to the QTextEdit."""
        #http://stackoverflow.com/questions/8356336/how-to-capture-output-of-pythons-interpreter-and-show-in-a-text-widget
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()  
        self.tabWidget.setCurrentWidget(self.textEdit_tab)


    def normalErrorWritten(self, text):
        """Append text to the QTextEdit."""
        #http://stackoverflow.com/questions/8356336/how-to-capture-output-of-pythons-interpreter-and-show-in-a-text-widget
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        cursor = self.textEdit_2.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit_2.setTextCursor(cursor)
        self.textEdit_2.ensureCursorVisible()   
        self.tabWidget.setCurrentWidget(self.textEdit_2_tab)


    def closeEvent(self, event):
    
        quit_msg = "Are you sure you want to exit the SWMM5-EA?"
        reply = QtGui.QMessageBox.question(self, 'Message', 
                         quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
    
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

# Do NOT start this application here. It should be started from swmm_ea_controller.py
#if __name__ == "__main__":
    #import sys
    #app = QtGui.QApplication(sys.argv)
    #ui = MainWindow()
    #ui.show()
    #ex=app.exec_()
    #sys.exit(ex)
    