import tempfile
import swmm_ea_temp_data
import os
from  distutils.dir_util import copy_tree
import sys
import StringIO
import swmm5ec
import guiqwt
from PyQt4 import QtCore



class parameters_class_(object):
    def __init__(self):
        pass  
    def setvalues(self,attrs):
        for a in attrs:
            setattr(self, a,attrs[a])
    def __str__(self):
        s=""
        for a,b in self.__dict__.iteritems():
            s=s+ a + "\t=>\t"+str(b )+"\n"
        return s


class Project():



    paramfilename="param.yaml"
    LOAD_NOSWMMFILE=2
    LOAD_COMPLETE=1
    outdir="output"
    tmpdir="tmp"


    def pause_optimization(self,state):
        self.swmm5ec.pause(state)

    def stop_optimization(self):
        self.swmm5ec.stop()
        

    def run_optimization(self):
        self.swmm5ec.start()


    def initialize_optimization(self):
        print "Initializing the optimization ..."
        print "*****************************************************************"
        print "List of parameters:"
        print self.parameters
        print "*****************************************************************"
        parameters=self.parameters
        parameters.bestlist=[]
        for i in range(parameters.pop_size+1):
            parameters.bestlist.append([])          
        parameters.datadirectory = "." 
        parameters.resultsdirectory= "output"        
        parameters.projectdirectory=self.dirname
        parameters.templatefile=self.slotted_swmmfilename
        #parameters.gnuplot = "E:\\Urban_drainageI_II\\2012\GA\\inspyred\gnuplot\\pgnuplot.exe" 
        #parameters.gnuplotscript = "plotfile.plt" # search in datadirectory
        parameters.gnuplotdata = "data.dat" # search in datadirectory
        self.swmm5ec=swmm5ec.SwmmEA()
        self.swmm5ec.setParams(parameters)



    def __init__(self, dirname=None, swmmfilename=None):
        self.swmmfilename=None

        if dirname:
            self.dirname=dirname
            self.load(dirname,swmmfilename)
        else:
            self.dirname=tempfile.mkdtemp(prefix="swmm-ea-project", suffix="dir")
            if swmmfilename:
                self.swmmfilename=swmmfilename
            else:
                self.swmmfilename="swmm.inp"
            data=swmm_ea_temp_data.data()
            paramfile=data.paramfile
            self.string_to_param(paramfile)
            self.swmm_data=data.swmmfile
            self.swmmfilename=data.swmmfilename
            self.save()   
        self.slotted_swmmfilename=None

    def write_slotted_swmm_file(self, full_fname, text):
        f=open(full_fname,'w')
        f.write(text)
        f.close()      
        self.slotted_swmmfilename=os.path.basename(str(QtCore.QDir.toNativeSeparators(full_fname)))

    def setswmmfile(self,swmmfilename):
    # Sets the swmm file swmmfilename that is in the project directory as the current one and Loads it. 
        self.swmmfilename=swmmfilename
        try:
            self.read_in_swmm_file()
            return True
        except: 
            self.swmmfilename=None
            return False

    def getSlottedData(self):
        sf=self.dirname+os.sep+(self.slotted_swmmfilename or "")
        if not (self.slotted_swmmfilename and os.path.exists(sf)):
            sf=self.dirname+os.sep+self.swmmfilename
        f=open(sf)
        t=f.read()
        f.close()
        return t

    def load(self, dirname=None, swmmfilename=None):
        if not dirname:
            dirname=self.dirname
        # first check directory
        if not os.path.isdir(dirname):
            return False
        pfilename=dirname+os.sep+self.paramfilename
        if not os.path.exists(pfilename):
            return False
        print "Using parameter file :" , pfilename
        f = open(pfilename)   
        flag=self.string_to_param(f.read())
        if not flag: 
            print "Problem opening and loading : "
        f.close() 
        if not swmmfilename:
            import glob
            try:
                self.swmmfilename=os.path.basename(glob.glob(dirname+os.sep+'*.inp')[0])
            except:
                print "problem: no swmm files in the directory."
                return self.LOAD_NOSWMMFILE
        else:
            self.swmmfilename=swmmfilename
        self.read_in_swmm_file()
        return self.LOAD_COMPLETE

    def read_in_swmm_file(self):
        f = open(self.dirname+os.sep+self.swmmfilename)
        self.swmm_data=f.read()
        f.close()
        sf=self.dirname+os.sep+(self.swmmfilename or "")+"_"
        if os.path.exists(sf):
            self.slotted_swmmfilename=os.path.basename(str(sf))
        else:
            self.slotted_swmmfilename=None


    def string_to_param(self, string ):

        f=StringIO.StringIO(string)
        self.parameters=parameters_class_()
        try:
            import yaml
            dataMap = yaml.load(f)            
            f.close()
            for key in dataMap :
                setattr(self.parameters, key, dataMap[key])
        except: 
            print "Problem reading parameters ",  sys.exc_info()
            return None
        return True        




    def save(self):

        print "Saving to directory : " + self.dirname
        if(self.swmmfilename):
            f=open(self.dirname+os.sep+self.swmmfilename,'w')
            f.write(self.swmm_data)
            f.close()
            print self.swmmfilename + " saved."
        f=open(self.dirname+os.sep+self.paramfilename,'w')
        import yaml
        f.write("#Written programmetically!")
        d=yaml.dump(self.parameters,f)
        f.close()

        print self.paramfilename + " saved."
        f.close
        self.makeemptydirectory(self.dirname+os.sep+self.outdir)
        self.makeemptydirectory(self.dirname+os.sep+self.tmpdir)



    def copy(self,dirname=None):
        if os.path.exists(dirname+os.sep+"param.yaml"):
            print "Please delete %s directory and try again!" % (dirname)
            return None
        try:
            self.save()
            copy_tree(str(QtCore.QDir.toNativeSeparators(self.dirname)),str(QtCore.QDir.toNativeSeparators(dirname)))
            # above copy_tree is from distutils
            return Project(dirname,self.swmmfilename)
        except:
            print "Error in creating new project location: "+ dirname
            return None

    def makeemptydirectory(self, out):
        if not os.path.isdir(out):
            if os.path.exists(out):
                os.remove(out)
            os.mkdir(out)

if __name__ == "__main__":
    pr=Project()
    print pr.dirname
    print pr.paramfilename
    print pr.swmmfilename
    pr.save()
    npr=pr.copy("C:\\Users\\apa.EDUCATION\\Desktop\\tmpswmmea")
    if not npr:
        print "copying failed!"
    else:
        print npr.dirname
        print npr.paramfilename
        print npr.swmmfilename 
        pr2=Project("C:\\Users\\apa.EDUCATION\\Desktop\\tmpswmmea")
        print "hi"