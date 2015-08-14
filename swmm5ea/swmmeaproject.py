import tempfile
import datetime
import swmm_ea_temp_data
import os
from  distutils.dir_util import copy_tree
import sys
import StringIO
import guiqwt
#import swmm5.swmm5 as sw
from swmm5.swmm5tools import SWMM5Simulation
import swmm_ea_controller
from PyQt4 import QtCore





fi=os.path.dirname(os.path.abspath(__file__))
cdir=os.path.abspath(os.path.join(fi,"..","customcode"))
cdir2=os.path.abspath(os.path.join(fi,"..","swmm5ea","customcode"))
if os.path.exists(cdir) or os.path.exists(cdir2):
    if os.path.exists(os.path.join(cdir,"swmm5ec_custom.py")):
        sys.path.append(cdir)
        exec('import %s as swmm5ec' % "swmm5ec_custom")
    elif os.path.exists(os.path.join(cdir2,"swmm5ec_custom.py")):
        cdir=cdir2
        sys.path.append(cdir)
        exec('import %s as swmm5ec' % "swmm5ec_custom")
    else:
        import swmm5ec
else:
    import swmm5ec



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

    def __init__(self, dirname=None, swmmfilename=None):
        self.setSwmmfile(None)
        self.ids={}
        #self.times=None
        self.NPeriods=None
        if dirname:
            self.dirname=dirname
            self.load(dirname,swmmfilename)
        else:
            self.dirname=tempfile.mkdtemp(prefix="swmm-ea-project", suffix="dir")
            if swmmfilename:
                self.setSwmmfile(swmmfilename)
            else:
                self.setSwmmfile("swmm.inp")
            data=swmm_ea_temp_data.data()
            paramfile=data.paramfile
            self.string_to_param(paramfile)
            self.swmm_data=data.swmmfile
            self.setSwmmfile(data.swmmfilename)
            self.save()   
        self.slotted_swmmfilename=None


    def pause_optimization(self,state):
        self.swmm5ec.pause(state)

    def stop_optimization(self):
        self.swmm5ec.stop()
        

    def run_optimization(self):
        self.swmm5ec.start()
    
    def get_ids(self):
        if not self.ids:
            self.get_swmm_ids_times()
        return self.ids
        
    def setSwmmfile(self, swmmfile=None):
        self.swmmfilename=swmmfile
        self.ids={} # reset the ids now next time the swmm file has to be run and ides extracted. 
    
         
    def get_swmm_ids_times(self):
        # first run swmm
        sp=self.dirname+os.sep+self.swmmfilename
        #binfile=sp[:-3]+"bin"
        #rptfile=sp[:-3]+"rpt"  
        print "Attempting to run swmm ..."    
        t=ThreadRun(SWMM5Simulation,sp)  
        t.start()
        t.join()
        st=t.ret
        #if(ret>0):
        #    print ret, "Error!" #sw.ENgeterror(e,25) 
        #    return None
    
        print "Success"
        print ("Running swmm version %s" % st.SWMM5_Version() )
        #f = swmmout.open(binfile)
        
        #types=['subcatchments', 'nodes', 'links', 'system']
        #ids={}
        #times=[]
        #for i in [1,2,3,4]:
        #    ids[types[i]]=map( lambda x: x[0], v[0][1:])
        #    times=map( lambda x: x[0],v)
        self.ids['subcatchments']=st.Subcatch()
        self.ids['nodes']= st.Node()
        self.ids['links']=st.Link()
        self.ids['system']=st.Sys()
        self.NPeriods=st.SWMM_Nperiods
        self.StartDate=st.SWMM_StartDate
        self.ReportStep=st.SWMM_ReportStep
        
    def readCalibFile(self):
        try: 
            with open(self.parameters.calfile,'r') as f:
                lines = f.read().splitlines()   
            lines=[s.strip() for s in lines if not s.strip()[0]==';']
            if not lines[0]==self.parameters.calid[1]:
                print "Problem: The id specified on calibration file, ", lines[0], " is different from ", self.parameters.calid[1]
                raise
            if not lines[1]==self.parameters.caltype[2]:
                print "Problem: The variable type specified in file , ", lines[1], " is different from ", self.parameters.caltype[2]
                raise 
            id_=lines[0]
            type_=lines[1]
            lines=map(lambda x: float(x), lines[2:])
            if not len(lines)== self.NPeriods:
                print "problem: the length of data in the file, ", len(lines), " is different from expected: ", self.NPeriods
                raise
            
            
        except: 
            print "Problem reading calibration file: ", self.parameters.calfile
            return None
        # now write a calibration file for swmm
        
        times=[]
        for i in range(self.NPeriods):
            delta = datetime.timedelta(days=self.StartDate, seconds=i*self.ReportStep)
            times.append(datetime.datetime(1899, 12, 30) + delta,)
        
        datf=self.parameters.calfile+".DAT"
        try:
            l=[times,lines]
            data=map(list,zip(*l))

            with open(datf,'w') as f:
                f.write("; Written by "+os.path.basename(__file__)+"\n")
                f.write(";"+self.parameters.caltype[2]+"\n")
                f.write(self.parameters.calid[1]+"\n")

                for time,value in data:
                    f.write(time.strftime('\t%m/%d/%Y\t%H:%M') + "\t" + str(value) + "\n")
            # now write a small ini file to be used as a template for all resulting inp files (Best_of_gen_xyz.inp)
            inif=self.parameters.projectdirectory+os.sep+"TEMPLATE.INI"
            with open(inif,'w') as f:
                f.write("[Calibration]\nFile%i=%s\n" %(swmm_ea_controller.SWMMCALIBRATIONFILE[self.parameters.caltype[0]], datf))
            self.parameters.calINITEMPLATE=inif
        except:
            print "Problem writing calibration file for swmm: ", datf
            return None            
                
        return lines    
            
            

    def initialize_optimization(self):
        print "Initializing the optimization ..."
        print "*****************************************************************"
        print "List of parameters:"
        print self.parameters
        print "*****************************************************************"
        print "(Advanced message) Using swmm5ec : %s" % swmm5ec.__file__
        print "*****************************************************************"
        parameters=self.parameters
        parameters.bestlist=[]
        for i in range(parameters.pop_size+1):
            parameters.bestlist.append([])          
        parameters.datadirectory = "." 
        parameters.resultsdirectory= "output"        
        parameters.projectdirectory=self.dirname
        parameters.templatefile=self.slotted_swmmfilename
        if parameters.swmmouttype[0]==swmm_ea_controller.SWMMREULTSTYPE_CALIB:
            parameters.calibdata=self.readCalibFile()
            parameters.swmmResultCodes=[parameters.caltype[1][0], parameters.calid[0],parameters.caltype[1][1]]
            if not parameters.calibdata: 
                return False
        self.swmm5ec=swmm5ec.SwmmEA()
        self.swmm5ec.setParams(parameters)
        self.swmm5ec.initialize()
        return True


    def write_slotted_swmm_file(self, full_fname, text):
        f=open(full_fname,'w')
        f.write(text)
        f.close()      
        self.slotted_swmmfilename=os.path.basename(str(QtCore.QDir.toNativeSeparators(full_fname)))

    def setswmmfile(self,swmmfilename):
    # Sets the swmm file swmmfilename that is in the project directory as the current one and Loads it. 
        self.setSwmmfile(swmmfilename)
        try:
            self.read_in_swmm_file()
            return True
        except: 
            print "swmm file: %s can not be found!" % (self.swmmfilename)
            self.setSwmmfile(None)
            return False

    def getSlottedData(self):
        sf=self.dirname+os.sep+(self.slotted_swmmfilename or "")
        slot=True
        if not (self.slotted_swmmfilename and os.path.exists(sf)):
            # then we read the original swmm file
            slot=False
            sf=self.dirname+os.sep+self.swmmfilename
        f=open(sf)
        t=f.read()
        f.close()
        if (not slot) and self.parameters.swmmouttype[0]==swmm_ea_controller.SWMMREULTSTYPE_STAGE: # we've read original swmm file and this analysis is multiple
            return reduce(lambda x,y: x+y, (swmm_ea_controller.SWMMSTAGESEPERATOR % (i) + t for i in range(self.parameters.stages)))
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
            print "Problem opening and loading : ", pfilename
            raise()
        
        f.close() 
        if not swmmfilename:
            # now check in parameters. 
            if hasattr(self.parameters,"swmmfilename"):
                print "Reading in swmmfilename from params.yaml as %s. " % (self.parameters.swmmfilename)
                self.setswmmfile(self.parameters.swmmfilename)
            else:
                import glob
                try:
                    self.setSwmmfile(os.path.basename(glob.glob(dirname+os.sep+'*.inp')[0]))
                except:
                    try:
                        self.setSwmmfile(os.path.basename(glob.glob(dirname+os.sep+'*.INP')[0]))
                    except:
                        print "problem: no swmm files in the directory."
                        return self.LOAD_NOSWMMFILE
        else:
            self.setSwmmfile(swmmfilename)
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
        """As a policy we ignore entries !!python/object: and read as dictionary"""
        st=string.replace("!!python/object:","#!!python/object:")
        f=StringIO.StringIO(st)
        self.parameters=parameters_class_()
        # now add the parameter to ensure compatibility with old version
        self.parameters.swmmouttype=[swmm_ea_controller.SWMMREULTSTYPE_FLOOD, swmm_ea_controller.SWMMCHOICES[swmm_ea_controller.SWMMREULTSTYPE_FLOOD]]# default
        self.parameters.stage_size=1
        self.parameters.discount_rate=1.0
        self.parameters.stages=1
        self.parameters.multiObjective=False
        try:
            import yaml
            dataMap = yaml.load(f)  
            f.close()
            ##if the yaml file has the header !!python/object:swmmeaproject.parameters_class_
            ## yaml.load will load the object directly. 
            ## if not loads a dictionary
            #if(dataMap.__class__.__name__==self.parameters.__class__.__name__):
                #self.parameters=dataMap
            #else:
                #for key in dataMap :
                    #setattr(self.parameters, key, dataMap[key])
                    
            for key in dataMap :
                setattr(self.parameters, key, dataMap[key])             
        except: 
            print "Problem reading parameters ",  sys.exc_info()
            return None
        return True        



    def cleanup_and_make_to_dict(self,params):
        """ 1. removes the temporary parameters in params object.
            2. convert it to a dictionary. 
            """
        from  copy  import deepcopy
        p=deepcopy(params)
        for item in [ "calINITEMPLATE", "calibdata", "bestlist", "linestring",  "projectdirectory",  "resultsdirectory", "templatefile", "datadirectory" ]: 
            try: 
                delattr(p,item)
            except: 
                pass
        return p.__dict__

    def save(self):

        print "Saving to directory : " + self.dirname
        if(self.swmmfilename):
            f=open(self.dirname+os.sep+self.swmmfilename,'w')
            f.write(self.swmm_data)
            f.close()
            print self.swmmfilename + " saved."
        f=open(self.dirname+os.sep+self.paramfilename,'w')
        import yaml
        f.write("#Written programmetically!\n")
        print "Adding name of swmmfile, %s to parameters" % (self.swmmfilename)
        self.parameters.swmmfilename=self.swmmfilename
        d=yaml.dump(self.cleanup_and_make_to_dict(self.parameters),f)
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
            import threading

import threading           
class ThreadRun(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self.ret=self._target(*self._args)

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