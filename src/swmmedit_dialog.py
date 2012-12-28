from PyQt4 import QtCore, QtGui
import guiqwt.plot

import swmmedit_dialog_
import swmm_ea_controller

class _PushButton(QtGui.QPushButton):
     def __init__(self, label=None, textlocation=None):
          super(QtGui.QPushButton, self).__init__(label)
          self.textlocation=textlocation


class Ui_swmmedit_dialog(QtGui.QDialog,swmmedit_dialog_.Ui_Dialog):


     def __init__(self, controller, ids=None, text=None):
          super(QtGui.QDialog, self).__init__() # because of multiple inheritance, here we call the __init__ of  QtGui.QDialog
                    #first        
          self.ids=ids
          self.setupUi(self)
          self.caltype.addItems(swmm_ea_controller.SWMMCALIBRATIONTYPES)
          font = QtGui.QFont()
          font.setFamily('Courier')
          font.setPointSize(12)
          self.editor.setFont(font)   
          self.editor.setLineWrapMode(QtGui.QTextEdit.NoWrap)
          if(text):
               self.editor.insertPlainText(text)
          self.highlighter=highlighter(self.editor)
          #self.highlighter2=highlighter(self.slotdisplay)
          self.text=text
          self.gototop(True)
          self.on_update_clicked()
          self.controller=controller
          try:
               c=self.controller.project.parameters.swmmouttype[0]==swmm_ea_controller.SWMMREULTSTYPE_CALIB
          except:
               c=False
          self.calbutton.setEnabled(c)
          self.caltype.setEnabled(c)
          self.calfile.setEnabled(c)
          self.calids.setEnabled(c)


          try: 
               self.calfile.setText(self.controller.project.parameters.calfile)
          except:
               pass
          try:
               self.caltype.setCurrentIndex(self.controller.project.parameters.caltype[0])
          except:
               pass
          try: 
               self.calids.setCurrentIndex(self.controller.project.parameters.calid[0])
          except: 
               pass
     def qt_fix_path(self,path):
          return QtCore.QDir.toNativeSeparators(path)     

     #action_caltype
     @QtCore.pyqtSignature("int")
     def on_caltype_currentIndexChanged(self,index):
          self.calids.clear()
          if(self.ids):
               self.calids.addItems(self.ids[swmm_ea_controller.SWMMCALIBRATIONTYPES2[index]])


     #action_calbutton
     @QtCore.pyqtSignature("")
     def on_calbutton_clicked(self):
          dr=self.controller.settings.value("lastcalfile").toString()
          fileName = QtGui.QFileDialog.getOpenFileName(self,
                                                       "Open a calibration data file", dr ,
                                                       "*.cal")
          if(fileName):

               self.controller.settings.setValue("lastcalfile",fileName) 
               self.calfile.setText(fileName)


     def on_editor_selectionChanged(self):
          txt=self.editor.textCursor().selectedText()
          try:
               float(txt)
               self.addvar.setEnabled(True)
          except:
               self.addvar.setEnabled(False)
     @QtCore.pyqtSignature("")
     def on_addvar_clicked(self):
          cursor=self.editor.textCursor()
          cursor.removeSelectedText()
          cursor.movePosition(QtGui.QTextCursor.NextWord, QtGui.QTextCursor.KeepAnchor)
          cursor.insertText(" @!v%(val)s!@ "% {"val": str(self.nextvar.text()) }) 
          self.nextvar.setText(str(int(str(self.nextvar.text()))+1))
          self.on_update_clicked()

     @QtCore.pyqtSignature("")          
     def on_update_clicked(self):
          if not self.text : return 
          self.slots=[]
          doc=self.editor.document()
          regex=QtCore.QRegExp(u"@!.*!@")
          regex.setMinimal(True)
          c = self.gototop()
          while True:
               c=doc.find(regex,c)
               if c.isNull(): break
               self.slots.append(_PushButton(c.selectedText(),c))
               #print c.selectedText()
          self.updateslots()
          
     def findText(self,cursor, text):
          self.gototop(True)
          regex = QtCore.QRegExp(QtCore.QRegExp.escape(text))
          index = regex.indexIn(self.editor.toPlainText(), 0)
          if (index<0): 
               print "Problem locating! (Try manually)"
               return
          self.editor.setTextCursor(cursor)
          cursor.setPosition(index)
          self.editor.ensureCursorVisible()          
          cursor.movePosition(QtGui.QTextCursor.Right, QtGui.QTextCursor.KeepAnchor, len(text)) 
          self.editor.ensureCursorVisible() 
          #print index, len(text)
          
     def gototop(self,updatewindow=False):
          c=self.editor.textCursor()
          c.setPosition(QtGui.QTextCursor.Start) # start on top\
          if(updatewindow): self.editor.setTextCursor(c)
          return c

     def accept(self):
          self.text=self.editor.toPlainText()#temperarily  store here. 
          f=str(self.qt_fix_path(self.calfile.text()))
          self.calfile_=f # temporarily store here. 
          i=self.caltype.currentIndex()
          self.caltype_=[i,swmm_ea_controller.SWMMVARTYPES[i],str(self.caltype.itemText(i))] #temperarily 
          j=self.calids.currentIndex()
          self.calid_=[j,str(self.calids.itemText(j))]
          QtGui.QDialog.accept(self)

     def clearLayout(self, layout):
         for i in reversed(range(layout.count())):
             item = layout.itemAt(i)
     
             if isinstance(item, QtGui.QWidgetItem):
                 #print "widget" + str(item)
                 item.widget().close()
             elif isinstance(item, QtGui.QSpacerItem):
                  pass
             else:
                  self.clearLayout(item.layout())
             layout.removeItem(item)          

     def updateslots(self):
          self.clearLayout(self.slotdisplay)
          
          for line in self.slots:         
               self.slotdisplay.addWidget(line)
               line.clicked.connect(self.onVarButtonClicked)
          self.spacer=QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
          self.slotdisplay.addItem(self.spacer)
          
          
     def onVarButtonClicked(self):
          self.findText(self.sender().textlocation, self.sender().text() )

class HighlightingRule():
     def __init__(self, pattern, fmt):
          self.pattern = pattern
          self.fmt = fmt

class highlighter(QtGui.QSyntaxHighlighter ):     
     def __init__( self, parent):
          QtGui.QSyntaxHighlighter.__init__( self, parent )
          self.parent = parent
          self.highlightingRules = []   
          reservedClasses = QtGui.QTextCharFormat()
          reservedClasses.setForeground( QtCore.Qt.darkRed )
          #reservedClasses.setBackground( QtCore.Qt.green)
          reservedClasses.setFontWeight( QtGui.QFont.Bold)
          regex=QtCore.QRegExp(QtCore.QString(u"@!.*!@"))
          regex.setMinimal(True)
          self.rule = HighlightingRule( regex, reservedClasses )
          self.highlightingRules.append( self.rule )

     def highlightBlock( self, text ):
          for rule in self.highlightingRules:
               expression = QtCore.QRegExp( self.rule.pattern )
               index=0
               while index >= 0:
                    index = expression.indexIn( text, index)
                    length = expression.matchedLength()
                    self.setFormat( index, length, self.rule.fmt )
                    index = text.indexOf( expression, index + length )
          self.setCurrentBlockState( 0 ) 


if __name__ == "__main__":
     import sys
     app = QtGui.QApplication(sys.argv)
     swmmfile="""
    [TITLE]

    [OPTIONS]
    FLOW_UNITS           LPS
    INFILTRATION         CURVE_NUMBER
    FLOW_ROUTING         DYNWAVE
    START_DATE           10/28/2011
    START_TIME           00:00:00
    REPORT_START_DATE    10/28/2011
    REPORT_START_TIME    00:00:00
    END_DATE             10/28/2011
    END_TIME             06:00:00
    SWEEP_START          01/01
    SWEEP_END            12/31
    DRY_DAYS             0
    REPORT_STEP          00:01:00
    WET_STEP             00:01:00
    DRY_STEP             00:01:00
    ROUTING_STEP         0:00:01 
    ALLOW_PONDING        NO
    INERTIAL_DAMPING     PARTIAL
    VARIABLE_STEP        0.75
    LENGTHENING_STEP     0
    MIN_SURFAREA         0
    NORMAL_FLOW_LIMITED  SLOPE
    SKIP_STEADY_STATE    NO
    FORCE_MAIN_EQUATION  H-W
    LINK_OFFSETS         DEPTH
    MIN_SLOPE            0

    [EVAPORATION]
    ;;Type       Parameters
    ;;---------- ----------
    CONSTANT     0.0
    DRY_ONLY     NO

    [RAINGAGES]
    ;;               Rain      Time   Snow   Data      
    ;;Name           Type      Intrvl Catch  Source    
    ;;-------------- --------- ------ ------ ----------
    Gage1            VOLUME    0:03   1.0    TIMESERIES ABM10yrs2hrs    

    [SUBCATCHMENTS]
    ;;                                                 Total    Pcnt.             Pcnt.    Curb     Snow    
    ;;Name           Raingage         Outlet           Area     Imperv   Width    Slope    Length   Pack    
    ;;-------------- ---------------- ---------------- -------- -------- -------- -------- -------- --------
    A2               Gage1            J4               96.9     40.80    1000     4.13     0                        
    A1               Gage1            J1               33.8     29.24    1000     4.13     0                        
    A3               Gage1            J3               50.7     32.17    1000     4.13     0                        
    A4               Gage1            J10              30.0     25.17    1000     4.13     0                        
    A5               Gage1            J9               25.5     10.00    1000     4.13     0                        
    E1               Gage1            J8               34.9     0        1000     1.86     0                        

    [SUBAREAS]
    ;;Subcatchment   N-Imperv   N-Perv     S-Imperv   S-Perv     PctZero    RouteTo    PctRouted 
    ;;-------------- ---------- ---------- ---------- ---------- ---------- ---------- ----------
    A2               0.01       0.1        0.05       0.05       25         OUTLET    
    A1               0.01       0.1        0.05       0.05       25         OUTLET    
    A3               0.01       0.1        0.05       0.05       25         OUTLET    
    A4               0.01       0.1        0.05       0.05       25         OUTLET    
    A5               0.01       0.1        0.05       0.05       25         OUTLET    
    E1               0.01       0.1        0.05       0.05       25         OUTLET    

    [INFILTRATION]
    ;;Subcatchment   CurveNum   HydCon     DryTime   
    ;;-------------- ---------- ---------- ----------
    A2               90         0.5        7         
    A1               90         0.5        7         
    A3               90         0.5        7         
    A4               90         0.5        7         
    A5               90         0.5        7         
    E1               70         0.5        7         

    [JUNCTIONS]
    ;;               Invert     Max.       Init.      Surcharge  Ponded    
    ;;Name           Elev.      Depth      Depth      Depth      Area      
    ;;-------------- ---------- ---------- ---------- ---------- ----------
    J2               45.633     1.8        0          0          0         
    J5               47.381     1.8        0          0          0         
    J6               41.909     1.8        0          0          0         
    J8               23.459     3          0          0          0         
    J9               37.689     2          0          0          0         
    J10              32.424     2          0          0          0         

    [OUTFALLS]
    ;;               Invert     Outfall    Stage/Table      Tide
    ;;Name           Elev.      Type       Time Series      Gate
    ;;-------------- ---------- ---------- ---------------- ----
    J12              15.649     FREE                        NO

    [STORAGE]
    ;;               Invert   Max.     Init.    Storage    Curve                      Ponded   Evap.   
    ;;Name           Elev.    Depth    Depth    Curve      Params                     Area     Frac.    Infiltration Parameters
    ;;-------------- -------- -------- -------- ---------- -------- -------- -------- -------- -------- -----------------------
    J11              27.159   1.8      0        FUNCTIONAL 6857.35055782 0        0        0        0       
    J3               36.437   1.8      0        FUNCTIONAL 33503.0726772 0        0        0        0       
    J4               52.853   1.8      0        FUNCTIONAL 8708.42058662 0        0        0        0       
    J1               55       1.8      0        FUNCTIONAL 30661.9663269 0        0        0        0       
    J7               29.589   1.8      0        FUNCTIONAL 1586.55686276 0        0        0        0       

    [CONDUITS]
    ;;               Inlet            Outlet                      Manning    Inlet      Outlet     Init.      Max.      
    ;;Name           Node             Node             Length     N          Offset     Offset     Flow       Flow      
    ;;-------------- ---------------- ---------------- ---------- ---------- ---------- ---------- ---------- ----------
    T4-1             J9               J10              117        0.02       0          0          0          0         
    T4-2             J10              J11              117        0.02       0          0          0          0         
    T4-3             J11              J8               60         0.02       1.5        0          0          0         
    T1-1             J1               J2               242        0.02       1          0          0          0         
    T1-2             J2               J3               400        0.02       0          0          0          0         
    T2-1             J4               J5               288        0.02       1          0          0          0         
    T2-2             J5               J6               288        0.02       0          0          0          0         
    T2-3             J6               J3               288        0.02       0          0          0          0         
    T3-1             J3               J7               428        0.02       1          0          0          0         
    T3-2             J7               J8               342        0.02       1.0        0          0          0         
    T5               J8               J12              235        0.01       0          0          0          0         

    [XSECTIONS]
    ;;Link           Shape        Geom1            Geom2      Geom3      Geom4      Barrels   
    ;;-------------- ------------ ---------------- ---------- ---------- ---------- ----------
    T4-1             CIRCULAR     2                0          0          0          1                    
    T4-2             CIRCULAR     2                0          0          0          1                    
    T4-3             CIRCULAR     2                0          0          0          1                    
    T1-1             CIRCULAR     1.2              0          0          0          1                    
    T1-2             CIRCULAR     1.2              0          0          0          1                    
    T2-1             CIRCULAR     2                0          0          0          1                    
    T2-2             CIRCULAR     2                0          0          0          1                    
    T2-3             CIRCULAR     2                0          0          0          1                    
    T3-1             CIRCULAR     1.5              0          0          0          3                    
    T3-2             CIRCULAR     1.5              0          0          0          2                    
    T5               RECT_OPEN    .4               3          0          0          1                    

    [LOSSES]
    ;;Link           Inlet      Outlet     Average    Flap Gate 
    ;;-------------- ---------- ---------- ---------- ----------

    [TIMESERIES]
    ;;Name           Date       Time       Value     
    ;;-------------- ---------- ---------- ----------
    ;2hr
    2hrRainfall                 0:00       0.00      
    2hrRainfall                 0:01       0.12      
    2hrRainfall                 0:02       0.12      
    2hrRainfall                 0:03       0.12      
    2hrRainfall                 0:04       0.12      
    2hrRainfall                 0:05       0.12      
    2hrRainfall                 0:06       0.13      
    2hrRainfall                 0:07       0.13      
    2hrRainfall                 0:08       0.13      
    2hrRainfall                 0:09       0.14      
    2hrRainfall                 0:10       0.13      
    2hrRainfall                 0:11       0.14      
    2hrRainfall                 0:12       0.15      
    2hrRainfall                 0:13       0.15      
    2hrRainfall                 0:14       0.14      
    2hrRainfall                 0:15       0.16      
    2hrRainfall                 0:16       0.16      
    2hrRainfall                 0:17       0.16      
    2hrRainfall                 0:18       0.17      
    2hrRainfall                 0:19       0.17      
    2hrRainfall                 0:20       0.17      
    2hrRainfall                 0:21       0.17      
    2hrRainfall                 0:22       0.18      
    2hrRainfall                 0:23       0.19      
    2hrRainfall                 0:24       0.19      
    2hrRainfall                 0:25       0.2       
    2hrRainfall                 0:26       0.2       
    2hrRainfall                 0:27       0.2       
    2hrRainfall                 0:28       0.21      
    2hrRainfall                 0:29       0.22      
    2hrRainfall                 0:30       0.23      
    2hrRainfall                 0:31       0.23      
    2hrRainfall                 0:32       0.24      
    2hrRainfall                 0:33       0.25      
    2hrRainfall                 0:34       0.26      
    2hrRainfall                 0:35       0.27      
    2hrRainfall                 0:36       0.28      
    2hrRainfall                 0:37       0.29      
    2hrRainfall                 0:38       0.3       
    2hrRainfall                 0:39       0.31      
    2hrRainfall                 0:40       0.33      
    2hrRainfall                 0:41       0.35      
    2hrRainfall                 0:42       0.37      
    2hrRainfall                 0:43       0.39      
    2hrRainfall                 0:44       0.41      
    2hrRainfall                 0:45       0.43      
    2hrRainfall                 0:46       0.46      
    2hrRainfall                 0:47       0.5       
    2hrRainfall                 0:48       0.53      
    2hrRainfall                 0:49       0.57      
    2hrRainfall                 0:50       0.62      
    2hrRainfall                 0:51       0.67      
    2hrRainfall                 0:52       0.74      
    2hrRainfall                 0:53       0.81      
    2hrRainfall                 0:54       0.91      
    2hrRainfall                 0:55       1.02      
    2hrRainfall                 0:56       1.17      
    2hrRainfall                 0:57       1.34      
    2hrRainfall                 0:58       1.58      
    2hrRainfall                 0:59       1.89      
    2hrRainfall                 1:00       2.34      
    2hrRainfall                 1:01       2.1       
    2hrRainfall                 1:02       1.73      
    2hrRainfall                 1:03       1.45      
    2hrRainfall                 1:04       1.24      
    2hrRainfall                 1:05       1.08      
    2hrRainfall                 1:06       0.96      
    2hrRainfall                 1:07       0.86      
    2hrRainfall                 1:08       0.78      
    2hrRainfall                 1:09       0.7       
    2hrRainfall                 1:10       0.65      
    2hrRainfall                 1:11       0.59      
    2hrRainfall                 1:12       0.55      
    2hrRainfall                 1:13       0.51      
    2hrRainfall                 1:14       0.48      
    2hrRainfall                 1:15       0.45      
    2hrRainfall                 1:16       0.43      
    2hrRainfall                 1:17       0.39      
    2hrRainfall                 1:18       0.38      
    2hrRainfall                 1:19       0.36      
    2hrRainfall                 1:20       0.34      
    2hrRainfall                 1:21       0.33      
    2hrRainfall                 1:22       0.32      
    2hrRainfall                 1:23       0.3       
    2hrRainfall                 1:24       0.29      
    2hrRainfall                 1:25       0.27      
    2hrRainfall                 1:26       0.26      
    2hrRainfall                 1:27       0.26      
    2hrRainfall                 1:28       0.24      
    2hrRainfall                 1:29       0.24      
    2hrRainfall                 1:30       0.23      
    2hrRainfall                 1:31       0.22      
    2hrRainfall                 1:32       0.22      
    2hrRainfall                 1:33       0.21      
    2hrRainfall                 1:34       0.2       
    2hrRainfall                 1:35       0.2       
    2hrRainfall                 1:36       0.19      
    2hrRainfall                 1:37       0.18      
    2hrRainfall                 1:38       0.18      
    2hrRainfall                 1:39       0.18      
    2hrRainfall                 1:40       0.17      
    2hrRainfall                 1:41       0.17      
    2hrRainfall                 1:42       0.16      
    2hrRainfall                 1:43       0.16      
    2hrRainfall                 1:44       0.15      
    2hrRainfall                 1:45       0.15      
    2hrRainfall                 1:46       0.15      
    2hrRainfall                 1:47       0.15      
    2hrRainfall                 1:48       0.14      
    2hrRainfall                 1:49       0.14      
    2hrRainfall                 1:50       0.14      
    2hrRainfall                 1:51       0.14      
    2hrRainfall                 1:52       0.13      
    2hrRainfall                 1:53       0.13      
    2hrRainfall                 1:54       0.13      
    2hrRainfall                 1:55       0.13      
    2hrRainfall                 1:56       0.13      
    2hrRainfall                 1:57       0.12      
    2hrRainfall                 1:58       0.12      
    2hrRainfall                 1:59       0.12      
    2hrRainfall                 2:00       0.11      

    ;Rainfall Data
    ABM10yrs2hrs                0:00       0         
    ABM10yrs2hrs                0:03       0.36      
    ABM10yrs2hrs                0:06       0.38      
    ABM10yrs2hrs                0:09       0.40      
    ABM10yrs2hrs                0:12       0.42      
    ABM10yrs2hrs                0:15       0.45      
    ABM10yrs2hrs                0:18       0.48      
    ABM10yrs2hrs                0:21       0.52      
    ABM10yrs2hrs                0:24       0.56      
    ABM10yrs2hrs                0:27       0.61      
    ABM10yrs2hrs                0:30       0.67      
    ABM10yrs2hrs                0:33       0.74      
    ABM10yrs2hrs                0:36       0.82      
    ABM10yrs2hrs                0:39       0.93      
    ABM10yrs2hrs                0:42       1.08      
    ABM10yrs2hrs                0:45       1.27      
    ABM10yrs2hrs                0:48       1.54      
    ABM10yrs2hrs                0:51       1.94      
    ABM10yrs2hrs                0:54       2.58      
    ABM10yrs2hrs                0:57       3.75      
    ABM10yrs2hrs                1:00       6.33      
    ABM10yrs2hrs                1:03       4.75      
    ABM10yrs2hrs                1:06       3.07      
    ABM10yrs2hrs                1:09       2.22      
    ABM10yrs2hrs                1:12       1.71      
    ABM10yrs2hrs                1:15       1.39      
    ABM10yrs2hrs                1:18       1.16      
    ABM10yrs2hrs                1:21       1.00      
    ABM10yrs2hrs                1:24       0.88      
    ABM10yrs2hrs                1:27       0.78      
    ABM10yrs2hrs                1:30       0.70      
    ABM10yrs2hrs                1:33       0.64      
    ABM10yrs2hrs                1:36       0.58      
    ABM10yrs2hrs                1:39       0.54      
    ABM10yrs2hrs                1:42       0.50      
    ABM10yrs2hrs                1:45       0.47      
    ABM10yrs2hrs                1:48       0.44      
    ABM10yrs2hrs                1:51       0.41      
    ABM10yrs2hrs                1:54       0.39      
    ABM10yrs2hrs                1:57       0.37      
    ABM10yrs2hrs                2:00       0.35      

    [REPORT]
    INPUT      NO
    CONTROLS   NO
    SUBCATCHMENTS ALL
    NODES ALL
    LINKS ALL

    [TAGS]

    [MAP]
    DIMENSIONS 0.000 0.000 10000.000 10000.000
    Units      None

    [COORDINATES]
    ;;Node           X-Coord            Y-Coord           
    ;;-------------- ------------------ ------------------
    J2               5415.068           1893.131          
    J5               6566.084           1307.978          
    J6               6360.316           1809.538          
    J8               5138.567           3802.918          
    J9               4418.378           2889.821          
    J10              4424.808           3153.462          
    J12              5312.184           5063.248          
    J11              4752.751           3571.429          
    J3               5595.115           2336.819          
    J4               6823.294           1140.791          
    J1               4778.472           1417.292          
    J7               5325.044           3102.020          

    [VERTICES]
    ;;Link           X-Coord            Y-Coord           
    ;;-------------- ------------------ ------------------
    T4-2             4739.891           3397.812          
    T4-3             5035.683           3571.429          
    T4-3             5042.113           3706.464          
    T3-2             5337.905           3732.185          

    [Polygons]
    ;;Subcatchment   X-Coord            Y-Coord           
    ;;-------------- ------------------ ------------------
    A2               9137.862           940.587           
    A2               9302.164           1556.721          
    A2               8390.285           2526.106          
    A2               7379.825           2567.182          
    A2               7429.116           1400.634          
    A1               4086.563           458.062           
    A1               4160.500           975.615           
    A1               4669.837           950.970           
    A1               5548.856           1452.093          
    A1               5581.716           310.190           
    A1               4867.000           195.178           
    A3               6297.935           2800.132          
    A3               6946.737           3271.194          
    A3               7907.907           3139.752          
    A3               7940.767           3410.852          
    A3               7293.018           3745.043          
    A3               6971.382           4602.045          
    A3               6585.271           4429.527          
    A3               6420.969           3714.811          
    A3               5955.091           2959.011          
    A4               3550.123           3206.322          
    A4               3342.244           2942.475          
    A4               2918.491           3086.392          
    A4               2478.747           3030.424          
    A4               3070.403           4013.851          
    A4               3686.044           3917.907          
    A5               4226.039           1863.728          
    A5               3682.356           1607.877          
    A5               3442.496           1815.756          
    A5               3554.430           1975.662          
    A5               3466.482           2207.527          
    A5               3826.272           2647.271          
    A5               4337.974           2719.229          
    A5               4689.769           2567.318          
    E1               4365.046           4144.795          
    E1               4518.867           4808.151          
    E1               4586.164           5202.318          
    E1               4481.613           5204.819          
    E1               3818.829           4472.268          
    E1               3722.900           4062.388          

    [SYMBOLS]
    ;;Gage           X-Coord            Y-Coord           
    ;;-------------- ------------------ ------------------
    Gage1            9936.709           6075.949          


    """
     ui = Ui_swmmedit_dialog(text=swmmfile)
     ui.show()
     app.exec_()
     print ui.text
