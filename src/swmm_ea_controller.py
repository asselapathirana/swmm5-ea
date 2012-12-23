from PyQt4 import QtCore, QtGui
import guiqwt
guiqwt
import guiqwt.plot
import os, shutil, sys, tempfile

import mainwindow
import swmmeaproject
from guiqwt.builder import make
#from guiqwt import QwtPlot

# program metadata

NAME=u"SWMM5_EA" # do not have spaces !!
VERSION="0.8.0.0"
DESCRIPTION=u"SWMM5-EA"
LICENSE=u"GNU General Public License version 3"
PUBLISHER=u"Assela Pathirana"
URL="http://assela.pathirana.net/SWMM5_EA"
TARGET="swmm5ec.exe"
SETUPNAME=NAME+"-"+VERSION



RUN_STATUS_TOBEINITED=0
RUN_STATUS_INITED=1
RUN_STATUS_RUNNING=2
RUN_STATUS_PAUSED=3

#
SWMMREULTSTYPE_FLOOD=0
SWMMREULTSTYPE_CALIB=1
SWMMCHOICES= [
     'Flood Volume',
     'Calibration var.'
    ] 
SWMMCALIBRATIONTYPES=[# this should match with SWMMVARTYPES
    "Subcatchment Runoff",
    "Subcatchment Groundwater Flow", 
    "Subcatchment Groundwater Elevation", 
    "Subcatchment Snow Pack Depth", 
    "Subcatchment Pollutant Washoff (pollutant 1)", 
    "Node Depth", 
    "Node Lateral Inflow", 
    "Node Flooding", 
    "Node Water Quality (pollutant 1)", 
    "Link Flow", 
    "Link Velocity", 
    "Link Depth"]
SWMMCALIBRATIONTYPES2=[# this should match with above and below
     'subcatchments',
     'subcatchments',
     'subcatchments',
     'subcatchments',
     'subcatchments',
     'nodes',
     'nodes',
     'nodes',
     'nodes',
     'links',
     'links'
     'links'] 
SWMMVARTYPES=[ # refer to swmm5 interfacing guide. This should match with SWMMCALIBRATIONTYPES
    [0,3],[0,4],[0,5],[0,6],
    [1,0],[1,3],[1,5],[1,6],
    [2,0],[2,2],[2,1] 
    ]    


# make sure the indexes match the values above



class EmittingStream(QtCore.QObject):

    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))
    def flush(self):
        pass # to avoid error on sys.stdout/err.flush()


class swmmeacontroller():

        
    
    def __init__(self, argv=sys.argv, project=None):

        self.app = QtGui.QApplication(sys.argv)
        self.ui = mainwindow.MainWindow(self)
        self.ui.setWindowIcon(QtGui.QIcon(':/res/res/DNA.ico'))
        self.project=None
        self.run_status=RUN_STATUS_TOBEINITED
        
        self.start_logging()
        
        self.QSettings_init()
        
        
        if len(argv) > 1: 
            self.LoadProject(argv[1])
            if len(argv) > 2: 
                self.LoadSwmmFile(argv[2])
                if len(argv) > 3: 
                    self.project.slotted_swmmfilename=argv[3]
                    self.initialize_optimization()                   
            
        self.ups()
        
        
    def QSettings_init(self):
        self.app.setOrganizationName("UNESCO-IHE/Assela Pathirana")
        self.app.setOrganizationDomain("pathirana.net")
        self.app.setApplicationName("SWMM5 EC")
        self.settings=QtCore.QSettings()
        
    def start_logging(self):
        import tee_test, logging
        from time import strftime, localtime
        log = logging.getLogger(strftime("%Y%b%d:%H:%M:%S:", localtime()))
        # open our log file
        self.logfile=tempfile.gettempdir()+ os.sep+os.path.basename(__file__)+".log"
        logging.basicConfig(level=logging.INFO,
                        filename=self.logfile,
                        filemode='a')
    
        sys.stdout = tee_test.StreamLogger(EmittingStream(textWritten=self.ui.normalOutputWritten), log, '[stdout] ')   
        sys.stderr = tee_test.StreamLogger(EmittingStream(textWritten=self.ui.normalErrorWritten), log, '>>>>> [stderr] ')    
        
        print 'Starting the logging process..'
        
        # now redirect all print statements to the 
        #sys.stdout = EmittingStream(textWritten=self.ui.normalOutputWritten)
        #sys.stderr = EmittingStream(textWritten=self.ui.normalErrorWritten)
        print "Log file: ", self.logfile   
    def show_message(self,msg):
        self.ui.normalOutputWritten(msg)

    def initialize_optimization(self):
        if(not self.project.initialize_optimization()):
            return False
        QtCore.QObject.connect(self.project.swmm5ec,QtCore.SIGNAL("nextGeneration(PyQt_PyObject)"),self.plot_next)
        QtCore.QObject.connect(self.project.swmm5ec,QtCore.SIGNAL('message(QString)'),self.show_message)        
        self.resultslist=[[],[]]
        for i in range(self.project.parameters.pop_size):
            self.resultslist[1].append([])        
        #QObject.connect(self.testThread, SIGNAL("testFinished(PyQt_PyObject)"), self.testFinishedFromThread)
        self.run_status=RUN_STATUS_INITED
        self.ups()
        return True
        
    def plot_next(self, data):
        #from numpy import linspace, sin
        #x = linspace(-10, 10, 200)  
        #self.ui.curve.get_plot().del_all_items()
        #self._plot(make.curve(x, sin(2*x), color="r"))
        pl=self.ui.curve.get_plot()
        pl.del_all_items()        
        self.resultslist[0].append(data[0])
        c=[]
        for i in range(len(data[1])):
            self.resultslist[1][i].append(data[1][i])
            c.append(make.curve(self.resultslist[0], self.resultslist[1][i],  **self.styles(i)))
            self._plot(c[i])
        
        if data[0] > 4:
            mid=int(len(self.resultslist[0])/2)
        else:
            mid=0
        lt=len(self.resultslist[1])
        if  lt > 3+1:
            lt=3
        self._plot(make.legend("TR", restrict_items=c[:lt+1]))  
        xmin=self.resultslist[0][mid]
        k=map( lambda x: x[mid:], self.resultslist[1][:3])
        fl=[item for sublist in k for item in sublist]
        xmax=len(self.resultslist[0])
        ymin=min(fl)
        ymax=max(fl)
        diff=(ymax-ymin)
        ymin=ymin-.2*diff
        ymax=ymax+.2*diff
        #print "setting limits: ", xmin,xmax,ymin,ymax
        pl.set_plot_limits(xmin,xmax,ymin,ymax)
        
        
        pl.replot()
    def styles(self,i):
        """
        title=u"",
                      color=None, linestyle=None, linewidth=None,
                      marker=None, markersize=None, markerfacecolor=None,
                      markeredgecolor=None, shade=None, fitted=None,
                      curvestyle=None, curvetype=None, baseline=None,
                      xaxis="bottom", yaxis="left"        

                      """
        style=dict()
        col=["r","b", "g", "c", "m", "k"]
        #markersize=10
        style["title"]="I-"+str(i)
        if i< 4:
            style["color"]=col[i]
            style["curvestyle"]="Lines"
            style["marker"]='Rect'
            style["markerfacecolor"]=col[i]
        else:
            col="G"
            style["color"]=col
            style["curvestyle"]="NoCurve"
            style["marker"]='Triangle'
            style["markerfacecolor"]=col
            
        return style
    
    def _plot(self,*items):
        self.ui.curve.get_itemlist_panel().show()
        for item in items:
            self.ui.curve.get_plot().add_item(item)
        #self.ui.curve.set_axis_font("left", QFont("Courier"))
                #self.ui.curve.set_items_readonly(False)          
 
    def pause_optimization(self,state):
        self.project.pause_optimization(state)
        if state:
            self.run_status=RUN_STATUS_PAUSED
        else:
            self.run_status=RUN_STATUS_RUNNING
        self.ups()
        
        
    def stop_optimization(self):
        self.project.stop_optimization()
        self.run_status=RUN_STATUS_TOBEINITED
        self.ups()
        
    def run_optimization(self):
        #if not self.initialized_the_optimization:
        #    self.initialize_optimization()  
        self.project.run_optimization()
        self.run_status=RUN_STATUS_RUNNING        
        self.ups()
    
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
            print "copying file: " + swmmfile + " to "+newname + "."
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
            tmp=self.project.copy(path)
            if tmp:
                self.project= tmp
                self.project.save()
                self.project.load()
                self.ups()    
                return True
            else:
                reply = QtGui.QMessageBox.warning(self.ui, "Save failed","Saving the project to :"+path+" failed.",
                                                  QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)  
                return False
        else:
            self.project.save()


    def ups(self):
        d,s,f=None,None,None
        if self.project:
            d,s,f=self.project.dirname, self.project.swmmfilename, self.project.slotted_swmmfilename
        
        self.ui.updateStatus(d,s,f,self.run_status)
    
if __name__ == "__main__":
    import sys
    sc=swmmeacontroller()
    sys.exit(sc.show())
        