import os, shutil, sys, tempfile
from PyQt4 import QtCore, QtGui
import guiqwt
#guiqwt
import guiqwt.plot


import mainwindow
import swmmeaproject
from guiqwt.builder import make
import slotdiff
import re, fnmatch
from glob import glob
from itertools import product
#from guiqwt import QwtPlot

from metadata import *


class EmittingStream(QtCore.QObject):

    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))
    def flush(self):
        pass # to avoid error on sys.stdout/err.flush()


class swmmeacontroller():

    def hasParam(self,param):
        return (self.project and self.project.parameters and hasattr(self.project.parameters,param))
    
    def __init__(self, argv=sys.argv, project=None):

        self.app = QtGui.QApplication(sys.argv)
        self.ui = mainwindow.MainWindow(self)
        self.ui.setWindowIcon(QtGui.QIcon(':/res/res/DNA.ico'))
        self.project=None
        self.run_status=RUN_STATUS_TOBEINITED
        param="zoom_state"
        if self.hasParam(param):
           self.zoom_state=project.parameters.zoom_state
        else:
            self.zoom_state=False
        
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
        
    def showHelp(self):
        loc=os.path.abspath(
            os.path.join(os.path.dirname(__file__),"..","doc","_build","html","index.html"))
        sys.stdout.write("opening help..")
        if (not QtGui.QDesktopServices.openUrl(QtCore.QUrl("file:///"+loc))):
            print "Failed to open help!"
            
        print("... done.")
        
        
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
        self.logfile=tempfile.gettempdir()+ os.sep+os.path.basename(sys.argv[0])+".log"
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
        if not self.project.parameters.multiObjective:
            for i in range(self.project.parameters.pop_size):
                self.resultslist[1].append([])        
        #QObject.connect(self.testThread, SIGNAL("testFinished(PyQt_PyObject)"), self.testFinishedFromThread)
        self.run_status=RUN_STATUS_INITED
        self.ups()
        return True
    
    def zoomState(self, zoom):
        if(self.project and self.project.parameters):
            self.project.parameters.zoomextent=zoom
            print "set zoom to extent", zoom, " and zooming."
            self.zoom_the_plot()
                
        
    def plot_next(self, data):

        pl=self.ui.curve.get_plot()
        pl.del_all_items()        

        c=[]
        if self.project.parameters.multiObjective:
            k=[]
            l=[]
            for i,j in sorted(data[1],key=lambda p: p[0]):
                k.append(i)
                l.append(j)
            self.resultslist[0].append(k)
            self.resultslist[1].append(l)
            
            for i in max(5,range(len(self.resultslist[0]))):
                st=self.styles(i, gen=len(self.resultslist[0]))
                c.append(make.curve(self.resultslist[0][-i-1],self.resultslist[1][-i-1],**st))
                #c.append(make.curve(d[0],d[1],**st))
            [self._plot(i) for i in reversed(c)]
            
            self._plot(make.legend("TR", restrict_items=c[:7]))         
        else:
            self.resultslist[0].append(data[0])
            for i in range(len(data[1])): 
                self.resultslist[1][i].append(data[1][i])  
                if i==len(data[1])-1:
                    st=self.styles(-1)
                else:
                    st=self.styles(i)
                
                c.append(make.curve(self.resultslist[0], self.resultslist[1][i],  **st))
            [self._plot(i) for i in reversed(c)]
            
            lt=len(self.resultslist[1])
            if  lt > 4:
                its=c[:4]
                its.append(c[-1])
            else:
                its=c[:lt+1]
            self._plot(make.legend("TR", restrict_items=its))         
        self.zoom_the_plot(data)
        pl.replot()

    def zoom_the_plot(self, data=None):
        pl=self.ui.curve.get_plot()
        if self.project.parameters.multiObjective:
            xmin=xmax=ymin=ymax=1
            s1=sorted(self.resultslist[0][-1])
            s2=sorted(self.resultslist[1][-1])
            xmin=s1[0]
            xmax=s1[-1]
            ymin=s2[0]
            ymax=s2[-1]
        else:
            validforzoom=3
            if (not hasattr(self, "resultslist")) or len(self.resultslist[0])<1:
                return 
            if not data:
                data=[self.resultslist[0][-1],self.resultslist[1][-1]]
            if data[0] > 4:
                mid=int(len(self.resultslist[0])/2)
            else:
                mid=0
            # but, if the user has indicated zoomextent..
            if self.hasParam("zoomextent") and self.project.parameters.zoomextent:
                mid=0
                validforzoom=None
                        

            
            xmin=self.resultslist[0][mid]
            k=map( lambda x: x[mid:], self.resultslist[1][:validforzoom])
            fl=[item for sublist in k for item in sublist]
     
            xmax=len(self.resultslist[0])
            ymin=min(fl)
            ymax=max(fl)
            diff=(ymax-ymin)
            ymin=ymin-.2*diff
            ymax=ymax+.2*diff
            
            
        #print "setting limits: ", xmin,xmax,ymin,ymax
        pl.set_plot_limits(xmin,xmax,ymin,ymax)

    def styles(self,i, gen=None):
        
        """
        returns all the styles for item i. Pass -1 to get the styles for the last (least fit) member.  Pass gen when handling MOO
        title=u"",
                      color=None, linestyle=None, linewidth=None,
                      marker=None, markersize=None, markerfacecolor=None,
                      markeredgecolor=None, shade=None, fitted=None,
                      curvestyle=None, curvetype=None, baseline=None,
                      xaxis="bottom", yaxis="left"        

                      """
        style=dict()
        col=["r","b", "g", "c", "m", "k"]
        syb=["Ellipse", "Rect", "Diamond", "Triangle", "DTriangle", "UTriangle", "LTriangle", "RTriangle", "Cross", "XCross", "HLine", "VLine", "Star1", "Star2", "Hexagon"]
        #markersize=10
        style["curvestyle"]="NoCurve"
        if self.project.parameters.multiObjective:
            style["title"]="Gen-"+str(gen-i)
            if i<6:
                style["color"]=col[i]
                style["marker"]=syb[i]
                style["markerfacecolor"]=col[i]  
                if i==0:
                    style["title"]="Latest"
                    style["curvestyle"]="Lines"
            else:
                col="G"
                style["color"]=col
                style["marker"]="Triangle"
                style["markerfacecolor"]=col
                style["title"]="Past"
                
            
            
                
        else:
            style["title"]="I-"+str(i)
            if i == -1: 
                style["title"]="Worst"  
            elif i==0:
                style["title"]="Best"
            if i< 4:
                style["color"]=col[i]
                if i > 0: 
                    style["curvestyle"]="NoCurve"
                else:
                    style["curvestyle"]="Lines"
                style["marker"]=syb[i]
                style["markerfacecolor"]=col[i]
            else:
                col="G"
                style["color"]=col
                style["curvestyle"]="NoCurve"
                style["marker"]='Triangle'
                style["markerfacecolor"]=col
            
        return style
    
    def _plot(self,*items):
        #self.ui.curve.get_itemlist_panel().show()
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
        self.get_slotted_data()
        self.ups()
        
    def get_slotted_data(self):
        sf=self.project.swmmfilename+"_"
        sf_with_path=self.project.dirname+os.sep+sf
        if(self.project.parameters.swmmouttype[0]==SWMMREULTSTYPE_STAGE):
            multiple=self.project.parameters.stages
        else:
            multiple=False
        if os.path.exists(sf_with_path):
            sd=slotdiff.slotDiff(self.project.dirname+os.sep+self.project.swmmfilename,sf_with_path,multiple)
            if(sd.testDiff()):
                print sf, " looks like derived from ", self.project.swmmfilename, ". Reusing it!"
                self.inp_diff_passed=True
            else:
                self.inp_diff_passed=False
                reply = QtGui.QMessageBox.information(self.ui, 'Caution ',
""" There is a file named %s in directory 
%s. 
However, it does not look to me as it derived from %s (your current swmm file.)
You can do two things: 
1. Reply 'Cancel', go to the directory %s, delete the file %s and try this operation again.
2. Reply 'OK', I will show the file %s. Then you can decide to go ahead or cancel. """ 
                                                   % (sf, self.project.dirname, self.project.swmmfilename, self.project.dirname,
                                                      sf, sf, ),
                                                   QtGui.QMessageBox.Ok|QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)
                if reply==QtGui.QMessageBox.Cancel:
                    return False
            self.project.slotted_swmmfilename=sf
        self.ups()
        return self.project.getSlottedData()
            
            
            
        
    def saveSlottedSwmmfile(self,text):
        sf=self.project.swmmfilename+"_"
        fname=self.project.dirname+os.sep+sf
        if  os.path.exists(fname) and not self.inp_diff_passed :
            reply = QtGui.QMessageBox.warning(self.ui, 'Overwrite ',
                                   "Do you want to overwrite the existing file "+ sf + " in " + self.project.dirname + " project directory?\n (If 'No' all the edits will be lost!)", QtGui.QMessageBox.Yes | 
                                   QtGui.QMessageBox.No, QtGui.QMessageBox.No)
            if not  reply == QtGui.QMessageBox.Yes:
                return False
        self.project.write_slotted_swmm_file(fname, text)
        print 'swmmfile with slots :'+sf+".", "File : "+sf+ " saved."         
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
        tx,ty,tp=[None]*3
        z=False
        if self.hasParam("swmmouttype"):
                if self.project.parameters.multiObjective:
                    tx,ty,tp=MOOTITLES
                else:
                        ty=PLOTYTITLE[self.project.parameters.swmmouttype[0]]
                        tx,tt=SOOTITLES
        if self.hasParam("zoomextent"):
            z=self.project.parameters.zoomextent
        self.ui.updateStatus(d,s,f,self.run_status,ty,tx,tp,z)
    
if __name__ == "__main__":
    import sys
    sc=swmmeacontroller()
    sys.exit(sc.show())
        
